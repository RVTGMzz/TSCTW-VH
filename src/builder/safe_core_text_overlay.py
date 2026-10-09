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
CTSS = 0x43545353
SELECTOR_KEY = (CTSS, 0xFFFFFFFF, 1, 0)
INSTALLED_SELECTOR_FILES = {
    "N001": "TSData/Res/UserData/Neighborhoods/N001/N001_Neighborhood.package",
    "N002": "TSData/Res/UserData/Neighborhoods/N002/N002_Neighborhood.package",
}
SELECTOR_SOURCES = {
    "N001": ((0, "Shipwrecked and Single"), (1, "Very little is known about this remote tropical paradise.")),
    "N002": ((0, "Wanmami Island"), (1, "Wanmami Island is home to the local, the lost")),
}


def selector_quote_normalize(text):
    """Treat typographic and plain quotes as equivalent, not arbitrary edits."""
    return text.translate(str.maketrans({"’":"'", "‘":"'", "“":'"', "”":'"'}))


def patch_installed_selector(original, island, approved_ui):
    """Patch only known N001/N002 CTSS rows, without touching unrelated resources."""
    if island not in SELECTOR_SOURCES:
        raise ValueError(("Unknown installed neighborhood", island))
    approved = {}
    for ordinal, anchor in SELECTOR_SOURCES[island]:
        candidates = [(en, vi) for en, vi in approved_ui.items()
                      if en == anchor or (ordinal == 1 and en.startswith(anchor))]
        if len(candidates) != 1:
            raise ValueError(("Missing/ambiguous selector translation", island, ordinal))
        approved[ordinal] = candidates[0]
    package = Package(original)
    if package.width != 24:
        return original, 0, 0
    entry = next((e for e in package.entries if e.key == SELECTOR_KEY), None)
    if entry is None:
        return original, 0, 0
    raw = package.raw(entry)
    rows, tail = parse_table(raw)
    changed = 0
    for ordinal, (en, vi) in approved.items():
        if ordinal < len(rows) and rows[ordinal][0] in (1, 2) and selector_quote_normalize(rows[ordinal][1]) == selector_quote_normalize(en):
            rows[ordinal][1] = vi
            changed += 1
    if not changed:
        return original, 0, 0
    encoded = encode_table(raw, rows)
    verified, verified_tail = parse_table(encoded)
    if verified != rows or verified_tail != tail:
        raise AssertionError(("Neighborhood CTSS roundtrip failed", island))
    return package.patch({SELECTOR_KEY: encoded}), changed, 1


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


# Source identities transcribed from the user's Build 66 read-only resource scan.
# These were absent from the historical core English catalog; never use
# substring matching or apply them to a different resource/language.
VISIBLE_TEXT_TARGETS = {
    ("CAS.package", (STR, 0xFFFFFFFF, 141), 51, 2): (
        "Please select your Sim's Turn-Ons and Turn-Off. Click on each of the boxes above and select a trait. \n\nYour Sim will be more romantically attracted to other Sims who have the traits that you've selected as Turn-Ons. Likewise, your Sim will be less attracted to Sims who have the trait you select as a Turn-Off.\n\nThese selections can be changed later by using the ReNuYuSenso Orb Aspiration Reward Object. Get out there and get attracted!",
        "Hãy chọn những đặc điểm khiến Sim của bạn bị thu hút hoặc mất hứng. Nhấn vào từng ô phía trên để chọn một đặc điểm.\n\nSim của bạn sẽ dễ rung động trước những Sim có đặc điểm được chọn trong mục Thu hút. Ngược lại, Sim sẽ ít bị hấp dẫn bởi những đặc điểm trong mục Mất hứng.\n\nBạn có thể thay đổi các lựa chọn này về sau bằng phần thưởng Khát vọng Quả cầu ReNuYuSenso. Giờ thì đi tìm người hợp gu thôi!",
    ),
    ("Live.package", (STR, 0xFFFFFFFF, 145), 80, 2): (
        "Negative side effects may occur if used below Gold Aspiration. Consult your Aspiration Meter before use.",
        "Có thể xảy ra tác dụng phụ nếu dùng khi mức Khát vọng chưa đạt Vàng. Hãy kiểm tra thanh Khát vọng trước khi sử dụng.",
    ),
}
TREE_RELATIVE = "TSData/Res/Catalog/CANHObjects/catcanhobjects.bundle.package"
TREE_TARGETS = {
    (STR, 2143531697, 123): ("Row of Trees", "Hàng cây"),
    (STR, 2142521860, 123): ("Pine Tree", "Cây thông"),
    (STR, 2140068512, 123): ("Pine Tree", "Cây thông"),
    (STR, 2144203450, 123): ("Pine Tree", "Cây thông"),
}


def exact_visible_patch(original, name, tree=False):
    """Match package identity, complete DBPF key, ordinal, language and English."""
    package = Package(original)
    targets = TREE_TARGETS if tree else VISIBLE_TEXT_TARGETS
    replacements = {}
    touched = 0
    for entry in package.entries:
        if tree:
            if entry.key not in targets:
                continue
            en, vi = targets[entry.key]
            wanted = [(0, 1, en, vi)]
        else:
            wanted = [(ordinal, lang, source, target) for
                      (filename, key, ordinal, lang), (source, target) in targets.items()
                      if filename == name and key == entry.key]
        if not wanted:
            continue
        raw = package.raw(entry)
        rows, tail = parse_table(raw)
        changed = False
        for ordinal, lang, en, vi in wanted:
            if ordinal >= len(rows):
                continue
            line = rows[ordinal]
            if line[0] == lang and line[1] == en:
                line[1] = vi
                touched += 1
                changed = True
        if changed:
            encoded = encode_table(raw, rows)
            checked, checked_tail = parse_table(encoded)
            if checked != rows or checked_tail != tail:
                raise AssertionError(("Exact visible row round-trip failed", name, entry.key))
            replacements[entry.key] = encoded
    return (package.patch(replacements), touched, len(replacements)) if replacements else (original, 0, 0)


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
    candidate_paths = [(name,f"TSData/Res/Text/{name}") for name in sorted(CORE_NAMES)]
    # Castaway installations may also have the active UIText resource under
    # TSData/Res/UI; scan both real locations rather than assuming Text only.
    candidate_paths.append(("UIText.package","TSData/Res/UI/UIText.package"))
    for name,path in candidate_paths:
        if path in current:
            raise ValueError(("Core/runtime path collision",path))
        source=game/path
        if not source.is_file():
            continue
        before=source.read_bytes()
        after,rows,resources=core_patch(before,name,locations)
        after,extra_rows,extra_resources=exact_visible_patch(after,name)
        rows+=extra_rows
        resources+=extra_resources
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
    # Catalog decorative trees live outside Res/Text and Objects. Apply only
    # four complete source-verified STR# identities; keep all other resources.
    if TREE_RELATIVE in current:
        raise ValueError(("Catalog/runtime path collision", TREE_RELATIVE))
    tree_path=game/TREE_RELATIVE
    if tree_path.is_file():
        before=tree_path.read_bytes()
        after,rows,resources=exact_visible_patch(before,tree_path.name,tree=True)
        if rows:
            target=bundle/"Payload"/TREE_RELATIVE
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(after)
            additions.append({
                "path":TREE_RELATIVE,"original_sha256":sha_bytes(before),
                "patched_sha256":sha_bytes(after),
                "changed_rows":rows,"changed_resources":resources,
            })
    core_text_file_count = len(additions)
    core_text_row_count = sum(r["changed_rows"] for r in additions)
    # Installed neighborhood templates are separate from Documents save data.
    # Add only CTSS rows that match the exact full audited English strings.
    installed_candidates = [(island, path) for island, path in INSTALLED_SELECTOR_FILES.items()
                            if (game / path).is_file()]
    approved_ui = {}
    if installed_candidates:
        ui_file = Path(catalog_path).parent / "runtime" / "translations" / "ui.json"
        approved_ui = json.loads(ui_file.read_text(encoding="utf-8"))
    selector_files = 0
    selector_rows = 0
    for island, path in installed_candidates:
        if path in current:
            raise ValueError(("Selector/runtime path collision", path))
        source = game / path
        if not source.is_file():
            continue
        before = source.read_bytes()
        after, rows, resources = patch_installed_selector(before, island, approved_ui)
        if not rows:
            continue
        target = bundle / "Payload" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(after)
        additions.append({
            "path": path, "original_sha256": sha_bytes(before),
            "patched_sha256": sha_bytes(after),
            "changed_rows": rows, "changed_resources": resources,
        })
        selector_files += 1
        selector_rows += rows
    manifest["installed_selector_overlay"] = {
        "changed_files": selector_files, "changed_rows": selector_rows,
        "mode": "installed-N001-N002-exact-CTSS-rows-only",
        "documents_saves_modified": False,
        "runtime_read_precedence_verified": False,
    }
    manifest["install_files"]=sorted(manifest["install_files"]+additions,key=lambda r:r["path"])
    manifest["core_text_overlay"]={
        "mode":"approved-English-only-rebase-on-installed-Text",
        "changed_files":core_text_file_count,
        "changed_rows":core_text_row_count,
        "unknown_previous_translations":"left unchanged",
        "note":"Same transaction and original-byte backups as runtime overlay; needs real in-game QA",
    }
    if not manifest["install_files"]:
        manifest["no_applicable_english_rows"]=True
    else:
        manifest["no_applicable_english_rows"]=False
    (bundle/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return manifest
