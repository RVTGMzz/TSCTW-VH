"""Read-only Windows local source locator for user-visible missing Castaway text.

Inspects TEXT resources in user's installed packages and optionally their
current Documents neighborhood files. Does not modify, upload or export raw
game package bytes. Uses exact resource key/row identities for follow-up work.
"""
from __future__ import annotations

import collections
import json
from pathlib import Path
import re
from runtime_dbpf import Package, parse_table, TEXT_TYPES

SEARCH = {
    "island_selector": r"Shipwrecked and Single|Wanmami Island|Very little is known about|Wanmami Island is home",
    "aspiration": r"Elixir of Life|aspiration reward|negative side effects|Perfect for those who like|gold aspiration",
    "attraction": r"Please select your Sim.s Turn|Romantically attracted|turn-offs|ReNuYuSenso",
    "trees": r"^Pine Tree$|^Row of Trees$",
    "stone_couch": r"Conveniently Cozy Rock Couch|Ghế đá đôi Êm Tiện Thể|Ghế đá đôi Êm Một Bên",
    "credit": r"^Credits$|^Main Menu$|^The Sims.? Castaway Stories$",
}
COMP = {k:re.compile(v,re.I) for k,v in SEARCH.items()}


def local_package_candidates(game, documents=None):
    """Conservative finite list of likely GUI/story/catalog source packages."""
    game=Path(game)
    paths=[]
    for directory in ("TSData/Res/Text", "TSData/Res/UI", "TSData/Res/Objects",
                      "TSData/Res/Catalog", "TSData/Res/Catalog/CANHObjects",
                      "TSData/Res/Neighborhood"):
        root=game/directory
        if root.is_dir():
            paths.extend(p for p in root.glob("*.package") if p.is_file())
    for base in (game/"TSData/Res/UserData/Neighborhoods",
                 Path(documents)/"Neighborhoods" if documents else None):
        if base is None or not base.is_dir():
            continue
        for island in ("N001","N002"):
            p=base/island/f"{island}_Neighborhood.package"
            if p.is_file():
                paths.append(p)
    return list(dict.fromkeys(p.resolve() for p in paths))


def scan_package(path, max_per_pattern=30, progress=lambda msg:None):
    """Yield bounded matching text without changing source package bytes."""
    data=Path(path).read_bytes()
    p=Package(data)
    results=[]
    counts=collections.Counter()
    scanned=0
    for e in p.entries:
        if e.key[0] not in TEXT_TYPES:
            continue
        scanned+=1
        try:
            records,_=parse_table(p.raw(e))
        except (ValueError,IndexError,UnicodeError,AssertionError,OverflowError):
            continue
        for index,(language,value,description) in enumerate(records):
            if language not in (1,2):
                continue
            matched=[name for name,regex in COMP.items()
                     if counts[name]<max_per_pattern and regex.search(value)]
            for name in matched:
                counts[name]+=1
                results.append({
                    "group":name,"file":str(path),"key":list(e.key),
                    "row":index,"language":language,
                    "english_or_existing":value[:1100],
                    "metadata_preview":description[:100],
                })
        if scanned%2500==0:
            progress(f"Đã rà {scanned:,} resource chữ trong {Path(path).name}")
    return results


# Selector verification deliberately reports BOTH existing translated and original
# English values: mere keyword matches cannot prove where the game reads text.
SELECTOR_ANCHORS = {
    "story_title": ("Shipwrecked and Single", "Đắm tàu và độc thân"),
    "island_title": ("Wanmami Island", "Đảo Wanmami"),
    "story_description": ("Very little is known about this remote tropical paradise.", "Người ta biết rất ít về thiên đường nhiệt đới xa xôi này."),
    "island_description": ("Wanmami Island is home to the local, the lost", "Đảo Wanmami là mái nhà"),
}


def selector_source_matrix(files, progress=lambda msg:None):
    """Read-only source/status matrix for both selection tiles and descriptions.

    Inspects only small selector owner candidates (Text/UI and N001/N002),
    not broad object animation tables. Returns evidence, never runtime proof.
    """
    hits=[]
    failures=[]
    for path in files:
        p=Path(path)
        normalized=str(p).replace("\\\\","/").lower()
        if not (p.name in ("UIText.package","Neighborhood.package") or
                p.name in ("N001_Neighborhood.package","N002_Neighborhood.package")):
            continue
        try:
            package=Package(p.read_bytes())
            for e in package.entries:
                if e.key[0] not in TEXT_TYPES:
                    continue
                try:
                    rows,_=parse_table(package.raw(e))
                except (ValueError,IndexError,UnicodeError,AssertionError,OverflowError):
                    continue
                for index,(language,value,description) in enumerate(rows):
                    if language not in (1,2):
                        continue
                    for group,(english,vietnamese) in SELECTOR_ANCHORS.items():
                        matching = (value == english or value == vietnamese) if group.endswith("_title") else (english in value or vietnamese in value)
                        if matching:
                            hits.append({
                                "field":group, "file":str(p),
                                "source_area":("installation_neighborhood" if "/tsdata/res/userdata/neighborhoods/" in normalized
                                    else "documents_neighborhood" if "/neighborhoods/" in normalized
                                    else "game_text"),
                                "key":list(e.key),"row":index,"language":language,
                                "state":"vietnamese" if (vietnamese in value) else "english",
                                "text_preview":value[:250],
                                "metadata_preview":description[:120],
                            })
        except (ValueError,IndexError,OSError,AssertionError,UnicodeError) as exc:
            failures.append({"file":str(p),"error":f"{type(exc).__name__}: {exc}"})
    progress(f"Đối chiếu màn chọn chế độ: {len(hits)} dòng nhận diện theo nguồn.")
    return {"matches":hits,"failed":failures,
            "runtime_read_precedence_verified":False,
            "note":"Translated resource existence does not prove the running selector uses that package."}


def discover_documents_roots():
    import os
    home=Path.home()
    roots=[]
    for base in [home/"Documents",home/"OneDrive"/"Documents",
                 Path(os.environ.get("OneDrive",""))/"Documents" if os.environ.get("OneDrive") else None]:
        if base is None:
            continue
        for name in ("The Sims Castaway Stories","The Sims™ Castaway Stories"):
            target=base/"Electronic Arts"/name
            if (target/"Neighborhoods").is_dir():
                roots.append(target)
    return list(dict.fromkeys(p.resolve() for p in roots))


def diagnose(game,progress=lambda m:None):
    """Call in GUI background worker. No file modification or network access."""
    roots=discover_documents_roots()
    files=local_package_candidates(game, roots[0] if roots else None)
    if not files:
        raise FileNotFoundError("Không tìm thấy package để rà. Chọn thư mục game có TSData.")
    output=[]
    failed=[]
    for n,path in enumerate(files,1):
        progress(f"Rà nguồn {n}/{len(files)}: {path.name}")
        try:
            output.extend(scan_package(path,progress=progress))
        except (ValueError,IndexError,OSError,AssertionError,UnicodeError) as exc:
            failed.append({"file":str(path),"error":f"{type(exc).__name__}: {exc}"})
    return {
        "files_scanned":len(files),"hits":output,"files_failed":failed,
        "selector_matrix":selector_source_matrix(files,progress),
        "documents_scanned":bool(roots),
        "evidence_only":True,
        "reminder":"Text resource hit is a candidate; not proof game runtime reads it. No package was changed.",
    }


def concise_for_gui(report,limit=55):
    lines=[
        f"Đã rà {report['files_scanned']} package (chỉ đọc). Tìm được {len(report['hits'])} dòng liên quan.",
        f"Documents được rà: {'có' if report['documents_scanned'] else 'chưa tìm thấy'}; tệp không đọc được: {len(report['files_failed'])}.",
    ]
    matrix=report.get("selector_matrix",{})
    if matrix:
        lines.append(f"Đối chiếu hai chế độ: {len(matrix.get('matches',[]))} bản ghi; chưa xác minh thứ tự game đọc.")
    for row in report["hits"][:limit]:
        lines.append(
            f"[{row['group']}] {Path(row['file']).name} / {row['key']} / dòng {row['row']} / "
            +row["english_or_existing"].replace("\n"," ")[:180]
        )
    if len(report["hits"])>limit:
        lines.append(f"… còn {len(report['hits'])-limit} kết quả. Báo cáo sẽ giữ toàn bộ.")
    return lines
