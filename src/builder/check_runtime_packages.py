"""Exercise actual package writes in a disposable QA output; not a release builder."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
from runtime_dbpf import Package, encode_table, parse_table
from validate_runtime import ROOT, RUNTIME, effective_records, load_maps, load_row_translations, row_identity
from stage_runtime_inputs import select_inventory


def apply(data, records, maps, decisions, exact_translations):
    package = Package(data)
    index = {e.key:e for e in package.entries}
    grouped = collections.defaultdict(list)
    for row in records:
        key = row['category'],row['en']
        identity = row_identity(row)
        if identity not in exact_translations and (key in decisions or row['en'] not in maps.get(row['category'],{})):
            continue
        grouped[tuple(row['key'])].append(row)
    replacements = {}
    changed_rows = 0
    for key,targets in grouped.items():
        original = package.raw(index[key])
        rows,tail = parse_table(original)
        for row in targets:
            lang,value,desc = rows[row['row']]
            if lang != row['language'] or desc != row['description']:
                raise ValueError(('Resource metadata differs from audit',key,row['row']))
            identity = row_identity(row)
            vi = exact_translations[identity]['vi'] if identity in exact_translations else maps[row['category']][row['en']]
            if value == vi:
                continue
            if value != row['en']:
                raise ValueError(('Source row differs from audit; never overwrite blindly',key,row['row']))
            rows[row['row']][1] = vi
            changed_rows += 1
        encoded = encode_table(original,rows)
        if encoded != original:
            decoded,after_tail = parse_table(encoded)
            if decoded != rows or after_tail != tail:
                raise AssertionError('Table round trip/padding failed')
            replacements[key] = encoded
    if not replacements:
        return data, 0, 0
    return package.patch(replacements), changed_rows, len(replacements)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input',type=Path,default=ROOT/'work/input')
    ap.add_argument('--output',type=Path,default=ROOT/'work/runtime_qa')
    ap.add_argument('--include-save-snapshots',action='store_true',help='DEVELOPMENT QA ONLY: verify and patch cloned Documents save snapshots; never ship originals or patched saves')
    args = ap.parse_args()
    if (args.output.resolve() == args.input.resolve() or args.input.resolve() in args.output.resolve().parents
            or args.output.resolve() in args.input.resolve().parents):
        raise ValueError('QA output must be separate from baseline input')
    maps=load_maps()
    exact_translations={(r['package'],tuple(r['key']),r['row']):r for r in load_row_translations()}
    decisions={(r['category'],r['en']) for r in json.loads((RUNTIME/'scope_decisions.json').read_text(encoding='utf-8'))}
    records=collections.defaultdict(list)
    effective,_ = effective_records()
    for r in effective:
        records[r['package']].append(r)
    inventory=json.loads((RUNTIME/'inventory.json').read_text(encoding='utf-8'))
    total_inventory=len(inventory)
    inventory=select_inventory(inventory, args.include_save_snapshots)
    if any(p['errors'] for p in inventory):
        raise ValueError('Unresolved input parse errors')
    report={'purpose':'development package QA, not v0.8 release','in_game_tested':False,
            'included_user_save_snapshots':bool(args.include_save_snapshots),
            'skipped_user_save_snapshots':total_inventory-len(inventory),
            'files':[]}
    for p in inventory:
        path=args.input/p['package']
        before=path.read_bytes()
        if hashlib.sha256(before).hexdigest()!=p['sha256']:
            raise ValueError(('Input hash differs from committed audit',str(path)))
        after,n,resources=apply(before,records[p['package']],maps,decisions,exact_translations)
        repeated,n2,r2=apply(after,records[p['package']],maps,decisions,exact_translations)
        if repeated!=after or n2 or r2:
            raise AssertionError('Idempotence failed')
        if n:
            output=args.output/p['package']
            output.parent.mkdir(parents=True,exist_ok=True)
            output.write_bytes(after)
        item=dict(package=p['package'],sha256_before=p['sha256'],sha256_after=hashlib.sha256(after).hexdigest(),changed_rows=n,changed_resources=resources,idempotence=True,unchanged_resources_preserved=True)
        report['files'].append(item)
        print(p['package'],n,'rows',resources,'resources',flush=True)
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':main()
