"""Reproducible resource/row inventory. Candidate is not a runtime-completion claim."""
from pathlib import Path
import argparse, collections, gzip, hashlib, json, re
from runtime_dbpf import Package, TEXT_TYPES, parse_table

ROOT = Path(__file__).resolve().parents[2]
CAST = re.compile(r'^Cast\s+(Menu|Catalog|UI|Want|Wants|Story|Dialog|Tutorial|Text|Object|Character|Neighborhood)\b',re.I)
INTERNAL = re.compile(r'debug|do not translate|don[\'’]?t\s+translate|not used|unused|placeholder|shouldn.t be in the catalog|variable -',re.I)
TECH = re.compile(r'anim|bone|mesh|model|material|sound|effect|attribute|slot|script|tree prim|data labels|flags|function table',re.I)
LEGACY_TECH = re.compile(r'attribute|relationship|skill table|end table (?:slots )?labels|slots? labels|suit primitive|named trees|behavior editor|skin colors',re.I)

def classify(path, name, typ, value, description):
    if not value.strip() or re.fullmatch(r'[\W\d_]+',value): return 'retain','empty/numeric'
    if INTERNAL.search(description) or re.match(r'^[!?]',value):return 'excluded','explicit developer/internal marker'
    m=CAST.match(description.strip())
    if m:
        if re.fullmatch(r'(?:\$[A-Za-z0-9_:]+[\s.]*)+',value):return 'retain','variable-only'
        return m[1].lower().rstrip('s') if m[1].lower()=='wants' else m[1].lower(), 'Cast localization metadata'
    if description.lstrip().startswith('!Cast'):return 'review','flagged Cast metadata requires human review'
    if TECH.search(name) or 'Behavior.package' in path:return 'excluded','technical resource name/package'
    if typ in (0x43545353,0x54544173) or re.search(r'dialog|action|catalog',name,re.I):return 'review','inherited or untagged potentially visible text'
    return 'excluded','no Cast metadata; outside confirmed scope'

def load_row_overrides():
    rows=[]
    for path in sorted((ROOT/'runtime').glob('row_scope_overrides*.json')):
        data=json.loads(path.read_text())
        if not isinstance(data,list):raise ValueError(('Row override shard must be a JSON list',path.name))
        rows.extend(data)
    return rows

def load_row_review_decisions():
    rows=[]
    for path in sorted((ROOT/'runtime').glob('row_review_decisions*.json')):
        if path.name=='row_review_decisions_applied.json':continue
        data=json.loads(path.read_text())
        if not isinstance(data,list):raise ValueError(('Row review decision shard must be a JSON list',path.name))
        rows.extend(data)
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,default=ROOT/'work/input');ap.add_argument('--output',type=Path,default=ROOT/'runtime');args=ap.parse_args()
    records=[]; inventory=[]; review=[]
    overrides={}; used=set()
    for override in load_row_overrides():
        identity=(override['package'],tuple(override['key']),override['row'])
        if identity in overrides:raise ValueError(('Duplicate row override',identity))
        if override['category'] not in ('menu','catalog','ui','story','tutorial','want','dialog'):
            raise ValueError(('Unsupported override category',identity))
        overrides[identity]=override
    review_decisions={}; used_review_decisions=set()
    for decision in load_row_review_decisions():
        identity=(decision['package'],tuple(decision['key']),decision['row'])
        if identity in review_decisions:raise ValueError(('Duplicate row review decision',identity))
        if identity in overrides:raise ValueError(('Row cannot be both promoted and excluded/retained',identity))
        if decision.get('status') not in ('excluded','retain'):
            raise ValueError(('Unsupported row review decision status',identity,decision.get('status')))
        review_decisions[identity]=decision
    for path in sorted(args.input.rglob('*.package')):
        rel=path.relative_to(args.input).as_posix()
        if '/Text/' in rel and path.name not in ('Wants.package','EPText.package'):continue
        pack=Package(path.read_bytes());counts=collections.Counter();resources=collections.Counter();errors=[];legacy=[];padding=0
        for entry in pack.entries:
            if entry.key[0] not in TEXT_TYPES:continue
            try:
                raw=pack.raw(entry);name=raw[:64].split(b'\0')[0].decode('utf8','surrogateescape')
                if raw[64:66]!=b'\xfd\xff' and LEGACY_TECH.search(name):
                    legacy.append(dict(key=list(entry.key),name=name,format=raw[64:66].hex(),reason='reviewed legacy technical resource; preserved byte-for-byte'));continue
                rows,tail=parse_table(raw)
            except Exception as ex:errors.append({'key':list(entry.key),'error':str(ex)});continue
            padding+=bool(tail);found=set()
            confirmed = {}
            for lang, value, desc in rows:
                if lang in (1, 2):
                    cat, reason = classify(rel, name, entry.key[0], value, desc)
                    if cat not in ('excluded', 'retain', 'review'):
                        confirmed[value] = cat
            for ordinal,(lang,value,desc) in enumerate(rows):
                if lang not in (1,2):continue
                category,reason=classify(rel,name,entry.key[0],value,desc)
                if category in ('excluded', 'review') and value in confirmed and not INTERNAL.search(desc):
                    category, reason = confirmed[value], 'Exact English variant of a Cast-tagged row in the same resource'
                identity=(rel,entry.key,ordinal)
                if identity in review_decisions:
                    decision=review_decisions[identity]
                    if category!='review' or (lang,value,desc)!=(decision['language'],decision['en'],decision['description']):
                        raise ValueError(('Row review decision baseline mismatch',identity))
                    category,reason=decision['status'],decision['reason']
                    used_review_decisions.add(identity)
                elif identity in overrides:
                    override=overrides[identity]
                    if category!='review' or (lang,value,desc)!=(override['language'],override['en'],override['description']):
                        raise ValueError(('Row override baseline mismatch',identity))
                    category,reason=override['category'],override['reason']
                    used.add(identity)
                counts[category]+=1;found.add(category)
                if category in ('excluded','retain'):continue
                record=dict(package=rel,key=list(entry.key),type=TEXT_TYPES[entry.key[0]],name=name,row=ordinal,language=lang,en=value,description=desc,category=category,reason=reason)
                (review if category=='review' else records).append(record)
            resources.update(found)
        inventory.append(dict(package=rel,sha256=hashlib.sha256(pack.data).hexdigest(),bytes=len(pack.data),index_width=pack.width,resources=len(pack.entries),text_row_categories=dict(counts),text_resource_categories=dict(resources),tables_with_preserved_tail=padding,legacy_technical_resources=legacy,errors=errors))
        print(rel,dict(counts), 'parse errors',len(errors),flush=True)
    if used!=set(overrides):raise ValueError(('Unused row overrides',set(overrides)-used))
    if used_review_decisions!=set(review_decisions):raise ValueError(('Unused row review decisions',set(review_decisions)-used_review_decisions))
    args.output.mkdir(parents=True,exist_ok=True)
    for filename,data in [('catalog.json',records),('review_queue.json',review),('inventory.json',inventory)]:
        (args.output/filename).write_text(json.dumps(data,ensure_ascii=True,indent=2)+'\n')
        if filename != 'inventory.json':
            encoded = (json.dumps(data,ensure_ascii=True,separators=(',',':'))+'\n').encode('utf8')
            (args.output/(filename+'.gz')).write_bytes(gzip.compress(encoded,mtime=0))
    applied=[review_decisions[k] for k in sorted(review_decisions,key=lambda x:(x[0],x[1],x[2]))]
    (args.output/'row_review_decisions_applied.json').write_text(json.dumps(applied,ensure_ascii=True,indent=2)+'\n')
    if any(x['errors'] for x in inventory):raise RuntimeError('Some string tables could not be parsed; inspect inventory.json')

if __name__=='__main__':main()
