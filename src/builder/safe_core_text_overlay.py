"""Conservative CORE Text overlay on an already localized v0.7a installation.

Uses the actual original source catalog (file, instance, exact English) and
reviewed translation map. Does not require unmodified original Text packages.
Never rewrites older Vietnamese values, nonmatching resource metadata or
non-Text resources. Returns patch candidates; caller handles transactional
backup/install/restore together with runtime.
"""
from __future__ import annotations
import collections
import hashlib
import json
from pathlib import Path

from runtime_dbpf import Package, TEXT_TYPES, parse_table, encode_table

CORE_NAMES = frozenset({
    "Options.package", "UIText.package", "Live.package",
    "Neighborhood.package", "Build.package", "CAS.package",
    "CAS_Shared.package", "Tutorial.package",
})
STR = 0x53545223


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def approved_core_locations(catalog, translations):
    """Only patch exact English strings approved for that original package/instance."""
    origins = collections.defaultdict(dict)
    for row in catalog:
        name, instance, en = row.get("file"), row.get("id"), row.get("text")
        if name not in CORE_NAMES or not isinstance(instance,int) or en not in translations:
            continue
        # Some original catalogs track multiple rows, description metadata
        # only when provided. Never search/rewrite arbitrary STR instances.
        desc = row.get("description")
        key = (name,int(instance))
        if en in origins[key] and origins[key][en] != translations[en]:
            raise ValueError(("Conflicting vetted core translation",key,en))
        origins[key][en] = translations[en]
    return origins


def core_patch(original, name, locations):
    package=Package(original)
    if package.width != 20:
        raise ValueError(("Unsupported core Text DBPF index width",name,package.width))
    replacements={}
    translated=0
    for entry in package.entries:
        if entry.key[0] != STR or (name,entry.key[2]) not in locations:
            continue
        raw=package.raw(entry)
        try:
            rows,tail=parse_table(raw)
        except (ValueError,IndexError,AssertionError,UnicodeError):
            raise ValueError(("Source catalog points to unreadable core STR#",name,list(entry.key)))
        updates=False
        approved=locations[(name,entry.key[2])]
        for line in rows:
            language,en,description=line
            if language not in (1,2):
                continue
            if en not in approved:
                continue  # Older Vietnamese, localized by another patch, or unknown.
            vi=approved[en]
            if en==vi:
                continue
            line[1]=vi
            translated+=1
            updates=True
        if updates:
            encoded=encode_table(raw,rows)
            again,tail2=parse_table(encoded)
            if again!=rows or tail2!=tail:
                raise AssertionError(("Core Text encode roundtrip failure",name,list(entry.key)))
            replacements[entry.key]=encoded
    if not replacements:
        return original,0,0
    after=package.patch(replacements)
    return after,translated,len(replacements)


def collect_core_overlay(game, bundle, manifest, catalog_path, translations_dir):
    """Append safe core Text changes to an already-built runtime candidate.

    Called on local user-owned files only. No Documents or EA binaries included
    in the EXE. Builder outputs are in a disposable bundle outside game.
    """
    from build_v07 import load_translations
    # build_v07 globals are configured by the frozen GUI before this call.
    translations,_,_=load_translations()
    catalog=json.loads(Path(catalog_path).read_text(encoding="utf-8"))
    locations=approved_core_locations(catalog,translations)
    current={r["path"] for r in manifest["install_files"]}
    additions=[]
    game=Path(game)
    bundle=Path(bundle)
    for name in sorted(CORE_NAMES):
        path=f"TSData/Res/Text/{name}"
        if path in current:
            raise ValueError(("Core/runtime path collision",path))
        source=game/path
        if not source.is_file():
            continue
        before=source.read_bytes()
        after,rows,resources=core_patch(before,name,locations)
        if not rows:
            continue
        target=bundle/"Payload"/path
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(after)
        additions.append({
            "path":path,"original_sha256":sha_bytes(before),
            "patched_sha256":sha_bytes(after),
            "changed_rows":rows,"changed_resources":resources,
        })
    manifest["install_files"]=sorted(manifest["install_files"]+additions,key=lambda r:r["path"])
    manifest["core_text_overlay"]={
        "mode":"approved-English-only-rebase-on-installed-Text",
        "changed_files":len(additions),
        "changed_rows":sum(r["changed_rows"] for r in additions),
        "unknown_previous_translations":"left unchanged",
        "note":"Same transaction and original-byte backups as runtime overlay; needs real in-game QA",
    }
    if not manifest["install_files"]:
        manifest["no_applicable_english_rows"]=True
    else:
        manifest["no_applicable_english_rows"]=False
    (bundle/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return manifest
