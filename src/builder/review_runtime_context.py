"""Attach local resource evidence to unresolved rows; never equates origin with reachability."""
import collections,gzip,hashlib,json,re
from pathlib import Path
from runtime_dbpf import Package
from validate_runtime import read_records,ROOT,RUNTIME

def main():
    inputs=ROOT/'work/input'
    inventory={x['package']:x for x in json.loads((RUNTIME/'inventory.json').read_text())}
    evidence=[]
    groups=collections.defaultdict(list)
    candidates=read_records('catalog')
    cast_groups={(r['package'],r['key'][1]) for r in candidates}
    for row in read_records('review_queue'):
        groups[row['package']].append(row)
    for path,rows in groups.items():
        data=(inputs/path).read_bytes()
        if hashlib.sha256(data).hexdigest()!=inventory[path]['sha256']:
            raise ValueError('Input differs from audited baseline: '+path)
        package=Package(data);objects=collections.defaultdict(set)
        for entry in package.entries:
            if entry.key[0]==0x4f424a44:
                name=package.raw(entry)[:64].split(b'\0')[0].decode('utf8','surrogateescape')
                objects[entry.key[1]].add(name)
        for row in rows:
            desc=row['description'];value=row['en'];names=sorted(objects[row['key'][1]])
            if re.search(r"\b(?:do\s+not|don['’]?t)\s+translate\b|\bdebug(?:ging)?\b|\b(?:unused|not used)\b",desc,re.I):
                decision='exclude';reason='explicit source metadata says internal/debug/do not translate'
            elif re.fullmatch(r'(?:\$[A-Za-z0-9_:]+[\s.]*)+',value):
                decision='retain';reason='variable-only value'
            else:
                decision='review';reason='source ownership does not establish runtime reachability'
            evidence.append(dict(**row,object_names=names,shares_group_with_cast_text=(path,row['key'][1]) in cast_groups,decision=decision,decision_reason=reason))
    encoded=(json.dumps(evidence,ensure_ascii=True,separators=(',',':'))+'\n').encode()
    (RUNTIME/'review_context.json.gz').write_bytes(gzip.compress(encoded,mtime=0))
    summary={
        'purpose':'Evidence for review, not a replacement for classification or reachability tests',
        'source_review_queue_sha256':hashlib.sha256((RUNTIME/'review_queue.json.gz').read_bytes()).hexdigest(),
        'rows':len(evidence),'unique_values':len({r['en'] for r in evidence}),
        'decisions':dict(collections.Counter(r['decision'] for r in evidence)),
        'unresolved_in_groups_with_cast_text':sum(r['decision']=='review' and r['shares_group_with_cast_text'] for r in evidence),
        'unresolved_in_cs_named_objects':sum(r['decision']=='review' and any(n.startswith('CS -') for n in r['object_names']) for r in evidence),
        'warning':'EP/base-game metadata or a CS object name alone never proves a row unused or reachable. The main coverage report still retains the entire inherited queue until per-resource decisions are integrated.'}
    (RUNTIME/'review_context_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
