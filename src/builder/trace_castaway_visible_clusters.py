"""Read-only, Castaway-player-screenshot-driven SOURCE CLUSTER TRACE.

Finds actual DBPF package/key/row, candidate vs inherited status,
neighboring texts in the same resource and previously translated mappings.
The tool never modifies any commercial game package or Documents save.
"""
import collections
import json
import re
from pathlib import Path
from validate_runtime import RUNTIME, ROOT, read_records, load_maps, load_row_translations, load_row_overrides, row_identity

TERMS = {
    "story-selector": [r"Shipwrecked and Single",r"Wanmami Island",
       r"Very little is known about this remote",r"Wanmami Island is home"],
    "neighborhood-people": [r"Valance",r"Linea is a high-flying",
       r"shipwreck survivors, because",r"\bWilson\b",r"\bSpear Point\b"],
    "attraction-panel": [r"Turn-Ons? and Turn-Off",r"select your Sim.s Turn",
       r"ReNuYuSenso",r"romantically attracted to other Sims"],
    "aspiration-rewards": [r"Elixir of Life",r"Negative side effects may occur",
       r"Aspiration Meter",r"Aspiration Reward",r"Perfect for those who like their idle"],
    "decor-tree": [r"^Pine Tree$",r"^Row of Trees$",r"pointy things pencil",
       r"cannot place decoration on an occupied lot"],
    "stone-loveseat": [r"While You.re At It",r"At It.*Loveseat",r"stone.*love",
       r"Em Tiện Thể",r"tough yesterday",r"hard day",
       r"terrible day",r"yesterday was a hard"],
    "credit-possibilities": [r"^Credits$",r"^About$",r"Game Credits",r"Castaway Stories",r"^Main Menu$"],
}
def shorten(s, limit=380):
    s = str(s or "")
    return s if len(s) <= limit else s[:limit] + " …"
def main():
    maps=load_maps()
    core_maps=[]
    for path in sorted((ROOT/"translations").glob("*.json")):
        obj=json.loads(path.read_text(encoding="utf-8"))
        if isinstance(obj,dict):
            core_maps.extend((path.name,k,v) for k,v in obj.items() if isinstance(v,str))
    catalog=read_records("catalog")
    review=read_records("review_queue")
    rows=catalog+review
    neighbors=collections.defaultdict(list)
    for row in rows:
        neighbors[(row["package"], tuple(row["key"]))].append(row)
    exact={row_identity(x):x["vi"] for x in load_row_translations()}
    overrides={row_identity(x):x["category"] for x in load_row_overrides()}
    print("=== CASTAWAY CLUSTER TRACE / SCREENSHOT OWNER AUDIT ===")
    print(json.dumps({"all_rows":len(rows),"categories":{cat:len(x) for cat,x in maps.items()}},ensure_ascii=False))
    for cluster,patterns in TERMS.items():
        rs=[re.compile(x,re.I) for x in patterns]
        found=[]
        for row in rows:
            if any(p.search(row.get("en") or "") or p.search(row.get("description") or "") for p in rs):
                cat=overrides.get(row_identity(row),row["category"])
                vi=exact.get(row_identity(row),maps.get(cat,{}).get(row["en"],None))
                found.append((row,vi,cat))
        found.sort(key=lambda x:(0 if x[0]["category"]!="review" else 1,
                                 0 if "UserData" in x[0]["package"] else 1,
                                 len(x[0].get("en") or "")))
        print("=== CLUSTER",cluster,"FOUND",len(found),"===")
        for row,vi,cat in found[:75]:
            siblings=neighbors[(row["package"],tuple(row["key"]))]
            nearby=[{"row":s["row"],"en":shorten(s.get("en"),140)} for s in siblings
                    if abs(s["row"]-row["row"])<=2 and s["row"]!=row["row"]][:5]
            print(json.dumps({
              "package":row["package"],"key":row["key"],"row":row["row"],
              "language":row["language"],"type":row.get("type"),
              "category":cat,"description":shorten(row.get("description"),700 if cluster=="aspiration-rewards" else 170),
              "en":shorten(row.get("en"),510),
              "approved_vi":shorten(vi,300) if vi else None,
              "nearby":nearby
            },ensure_ascii=False))
        print("OMITTED",max(0,len(found)-75))
        if cluster=="stone-loveseat":
            candidates=[(section,k,v) for section,m in maps.items()
                        for k,v in m.items() if re.search("tiện thể|ghế đá đôi",v,re.I)]
            candidates+= [(p,k,v) for p,k,v in core_maps if re.search("tiện thể|ghế đá đôi",v,re.I)]
            print("PHRASE_MATCHES",json.dumps([{"source":x,"en":shorten(k,450),"vi":shorten(v,240)}
                                          for x,k,v in candidates[:40]],ensure_ascii=False))
    # Compare against the separate ORIGINAL core Text catalog: these rows
    # cannot be fixed by translating runtime/Objects alone.
    from build_v07 import CATALOG_PATH
    try:
        core_catalog=json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        print("=== CORE TEXT CATALOG CLUSTER TRACE ===")
        for cluster,patterns in TERMS.items():
            found=[r for r in core_catalog if isinstance(r.get("text"),str)
                   and any(re.search(p,r["text"],re.I) for p in patterns)]
            print("CORE",cluster,"FOUND",len(found))
            for r in found[:50]:
                print("CORE_ROW",json.dumps({
                    "file":r.get("file"),"id":r.get("id"),
                    "text":shorten(r.get("text"),550),
                    "description":shorten(r.get("description"),130)
                },ensure_ascii=False))
        print("=== END CORE TEXT CATALOG CLUSTER TRACE ===")
    except (FileNotFoundError,ValueError) as exc:
        print("CORE_CATALOG_UNAVAILABLE",type(exc).__name__,str(exc))
    print("=== END CASTAWAY CLUSTER TRACE ===")

if __name__=="__main__":
    main()
