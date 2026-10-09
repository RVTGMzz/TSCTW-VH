"""Opt-in surgical translation of CURRENT Documents N001/N002 neighborhood text.

Never overwrite neighborhood saves as installation templates. Only exact
audited STR#/CTSS resource rows are modified; all other bytes/resources
remain untouched by DBPF writer. User-facing GUI requires explicit consent,
game shutdown, separate verified backups and guarded restore. Source
ownership is known; whether the game's story-selector reads these rows is
still to be verified in Windows gameplay.
"""
from __future__ import annotations
import collections
import hashlib
import json
import os
from pathlib import Path
import shutil
import uuid

from check_runtime_packages import apply
from validate_runtime import effective_records, load_maps, load_row_translations, row_identity

SAVE_ALIASES = {
    "N001":"TSData/Res/UserData/Neighborhoods/N001/N001_Neighborhood.package",
    "N002":"TSData/Res/UserData/Neighborhoods/N002/N002_Neighborhood.package",
}


def hash_bytes(data):
    return hashlib.sha256(data).hexdigest()


def guarded_source_paths(save_root):
    save_root=Path(save_root).resolve()
    if not (save_root/"Neighborhoods").is_dir():
        raise FileNotFoundError("Không tìm thấy Neighborhoods trong thư mục save đã chọn.")
    sources={}
    for island in ("N001","N002"):
        source=save_root/"Neighborhoods"/island/f"{island}_Neighborhood.package"
        if not source.is_file() or source.is_symlink():
            raise FileNotFoundError(f"Thiếu file save của đảo {island}: {source}")
        sources[island]=source
    return sources


def build_saved_neighborhood_updates(save_root):
    """Read bytes only; prepare exact-row candidates without touching saves."""
    sources=guarded_source_paths(save_root)
    effective,_=effective_records()
    groups=collections.defaultdict(list)
    for row in effective:
        if row["package"] in SAVE_ALIASES.values() and row["category"] in ("ui","character","neighborhood"):
            groups[row["package"]].append(row)
    maps=load_maps()
    exact={row_identity(r):r for r in load_row_translations()}
    updates=[]
    for island,source in sources.items():
        before=source.read_bytes()
        patched,n,res=apply(before,groups[SAVE_ALIASES[island]],maps,set(),exact,
                            preserve_unrecognized=True)
        if n:
            updates.append({
                "island":island,"source":source,"original":before,
                "patched":patched,"rows":n,"resources":res,
                "before_hash":hash_bytes(before),"after_hash":hash_bytes(patched),
            })
    return updates


def selector_translation_status(save_root):
    """Read-only inspection of both mode titles/descriptions in current N001/N002."""
    from diagnose_visible_strings import selector_source_matrix
    sources=guarded_source_paths(save_root)
    report=selector_source_matrix(list(sources.values()))
    fields=("story_title","island_title","story_description","island_description")
    matches=report["matches"]
    return {
        "fields":{field:{
            "english":sum(r["field"]==field and r["state"]=="english" for r in matches),
            "vietnamese":sum(r["field"]==field and r["state"]=="vietnamese" for r in matches)
        } for field in fields},
        "source_files":[str(p) for p in sources.values()],
        "runtime_read_precedence_verified":False,
        "files_failed":report["failed"],
    }


def inside(path,parent):
    path,parent=Path(path).resolve(),Path(parent).resolve()
    return path==parent or parent in path.parents


def apply_saved_neighborhood_updates(save_root,backup_dir):
    """Atomic file replacement with full-byte verified rollback on failure."""
    save_root=Path(save_root).resolve()
    backup_dir=Path(backup_dir).resolve()
    if inside(backup_dir,save_root) or inside(save_root,backup_dir):
        raise ValueError("Thư mục sao lưu phải nằm ngoài thư mục save Documents")
    if backup_dir.exists():
        raise FileExistsError("Đã có thư mục backup, không ghi đè")
    updates=build_saved_neighborhood_updates(save_root)
    selector_before=selector_translation_status(save_root)
    if not updates:
        return {"state":"NO_NEW_ROWS","saved_files":0,"changed_rows":0,
                "selector_status":selector_translation_status(save_root),
                "selector_before":selector_before}
    # Recheck ALL sources before creating anything.
    for item in updates:
        if hash_bytes(item["source"].read_bytes())!=item["before_hash"]:
            raise ValueError(("Save changed while building translations",str(item["source"])))
    changed=[]
    try:
        for item in updates:
            dest=backup_dir/"Neighborhoods"/item["island"]/item["source"].name
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(item["source"],dest)
            if hash_bytes(dest.read_bytes())!=item["before_hash"]:
                raise AssertionError("Save backup did not verify")
        manifest={
            "schema":"TSCTW-SAVE-LOC-TEXT-1",
            "save_root":str(save_root),
            "files":[{
                "island":u["island"],
                "path":str(u["source"].relative_to(save_root)),
                "original_sha256":u["before_hash"],
                "patched_sha256":u["after_hash"],
                "changed_rows":u["rows"],
                "changed_resources":u["resources"],
            } for u in updates],
            "gameplay_verified":False,
            "note":"Separate Documents save backup: do not publish or overwrite user progress.",
        }
        (backup_dir/"restore_manifest.json").write_text(
            json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        for item in updates:
            dst=item["source"]
            temp=dst.with_name(dst.name+"."+uuid.uuid4().hex+".tmp")
            try:
                temp.write_bytes(item["patched"])
                if hash_bytes(temp.read_bytes())!=item["after_hash"]:
                    raise AssertionError("Written temporary save mismatch")
                if hash_bytes(dst.read_bytes())!=item["before_hash"]:
                    raise ValueError("Save changed before write; abort")
                os.replace(temp,dst)
                changed.append(item)
            finally:
                temp.unlink(missing_ok=True)
        for item in updates:
            if hash_bytes(item["source"].read_bytes())!=item["after_hash"]:
                raise AssertionError("Post-patch Documents save checksum failed")
        return {"state":"PATCHED_FOR_TEST","saved_files":len(updates),
                "changed_rows":sum(x["rows"] for x in updates),
                "backup":str(backup_dir),
                "selector_status":selector_translation_status(save_root),
                "selector_before":selector_before}
    except Exception:
        # Roll back all written files, even if a post-write check failed.
        for item in reversed(changed):
            dst=item["source"]
            back=backup_dir/"Neighborhoods"/item["island"]/dst.name
            tmp=dst.with_name(dst.name+"."+uuid.uuid4().hex+".rollbacktmp")
            try:
                shutil.copy2(back,tmp)
                os.replace(tmp,dst)
            finally:
                tmp.unlink(missing_ok=True)
        raise


def restore_saved_neighborhoods(save_root,backup_dir):
    save_root=Path(save_root).resolve()
    backup_dir=Path(backup_dir).resolve()
    manifest=json.loads((backup_dir/"restore_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema")!="TSCTW-SAVE-LOC-TEXT-1" or manifest.get("save_root")!=str(save_root):
        raise ValueError("Backup không thuộc thư mục save này")
    records=[]
    for row in manifest["files"]:
        relative=Path(row["path"])
        island=row["island"]
        if island not in SAVE_ALIASES or relative.parts != ("Neighborhoods",island,f"{island}_Neighborhood.package"):
            raise ValueError("Unsafe save restoration path")
        saved=backup_dir/relative
        active=save_root/relative
        if not saved.is_file() or saved.is_symlink() or not active.is_file() or active.is_symlink():
            raise FileNotFoundError("Missing or linked save/backup")
        if hash_bytes(saved.read_bytes())!=row["original_sha256"]:
            raise ValueError("Backup checksum differs; refusing restoration")
        current=hash_bytes(active.read_bytes())
        if current not in (row["original_sha256"],row["patched_sha256"]):
            raise ValueError("Save changed since patch, refusing to erase game progress")
        records.append((row,active,saved,current))
    count=0
    for row,active,saved,current in records:
        if current==row["original_sha256"]:
            continue
        tmp=active.with_name(active.name+"."+uuid.uuid4().hex+".restoretmp")
        try:
            shutil.copy2(saved,tmp)
            if hash_bytes(tmp.read_bytes())!=row["original_sha256"]:
                raise AssertionError("Save restoration checksum failed")
            os.replace(tmp,active)
            count+=1
        finally:
            tmp.unlink(missing_ok=True)
    return {"state":"RESTORED_PREVIOUS_SAVE_STATE","restored_files":count,
            "backup_retained":str(backup_dir)}
