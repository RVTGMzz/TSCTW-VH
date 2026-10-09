"""Hash-guarded LOCAL Castaway v0.8 TEST install/restore, never touches Documents saves.

Default is DRY RUN. --apply additionally requires --game-closed.
Backups live outside the game and are never silently overwritten.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import uuid


def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as fd:
        for block in iter(lambda:fd.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()


# Only two installed neighborhood templates can be part of a verified
# game installation transaction. Documents save files stay untouched.
INSTALLED_NEIGHBORHOOD_ALLOWLIST = frozenset({
    "TSData/Res/UserData/Neighborhoods/N001/N001_Neighborhood.package",
    "TSData/Res/UserData/Neighborhoods/N002/N002_Neighborhood.package",
})


def validate_path(rel):
    if not isinstance(rel,str) or not rel.startswith("TSData/Res/") or not rel.endswith(".package"):
        raise ValueError(f"Unsafe payload path: {rel!r}")
    pure=Path(rel.replace("\\","/"))
    if any(t in ("..",".","") for t in pure.parts) or pure.is_absolute():
        raise ValueError(f"Invalid relative path: {rel}")
    if (rel.startswith("TSData/Res/UserData/") and rel not in INSTALLED_NEIGHBORHOOD_ALLOWLIST) or ":" in rel or "\\" in rel:
        raise ValueError(f"User save or unsupported path forbidden: {rel}")
    return pure


def inside(p,parent):
    p,parent=p.resolve(),parent.resolve()
    return p==parent or parent in p.parents


def parse_manifest(bundle):
    data=json.loads((bundle/"manifest.json").read_text(encoding="utf-8"))
    if data.get("schema")!="TSCTW-V08-TEST-1":
        raise ValueError("Unsupported/non-v0.8 TEST bundle")
    rows=data.get("install_files",[])
    if not rows or not isinstance(rows,list):
        raise ValueError("No installable files")
    identities=[]
    for row in rows:
        rel=validate_path(row["path"])
        identities.append(rel.as_posix().casefold())
        for k in ("original_sha256","patched_sha256"):
            value=row.get(k,"")
            if not isinstance(value,str) or len(value)!=64 or any(c not in "0123456789abcdef" for c in value):
                raise ValueError(f"Invalid hash in manifest: {rel}")
        if row["original_sha256"]==row["patched_sha256"]:
            raise ValueError(f"Unchanged original included in payload: {rel}")
        source=bundle/"Payload"/rel
        if not source.is_file() or source.is_symlink() or sha(source)!=row["patched_sha256"]:
            raise ValueError(f"Patch payload missing/mismatch: {rel}")
    if len(set(identities))!=len(identities):
        raise ValueError("Duplicate case-insensitive package path")
    return rows


def check_destinations(rows,game,kind):
    if not (game/"TSData").is_dir():
        raise FileNotFoundError(f"Not a Castaway game installation: {game}")
    for row in rows:
        rel=validate_path(row["path"])
        target=game/rel
        # Reject directory junctions/symlinked ancestors too: checking only
        # the .package leaf would allow writes outside the chosen game root.
        if not inside(target,game) or any(p.is_symlink() for p in (target, *target.parents) if p != game and inside(p,game)):
            raise ValueError(f"Unsafe redirected package target: {target}")
        if not target.is_file() or target.is_symlink():
            raise FileNotFoundError(f"Missing/symlinked target: {target}")
        current=sha(target)
        permitted={row["original_sha256"]} if kind=="apply" else {row["original_sha256"],row["patched_sha256"]}
        if current not in permitted:
            raise ValueError(f"{kind} blocked: installed package has unexpected hash: {target}")


def install(bundle,game,backup,dry_run=True):
    bundle,game,backup=bundle.resolve(),game.resolve(),backup.resolve()
    if inside(bundle,game) or inside(backup,game) or inside(backup,bundle):
        raise ValueError("Bundle and backup must be outside the game, and backup outside bundle")
    rows=parse_manifest(bundle)
    check_destinations(rows,game,"apply")
    if backup.exists():
        raise FileExistsError(f"Backup location already exists: {backup}")
    if dry_run:
        return {"result":"DRY RUN ONLY - all original hashes match","files":len(rows),"backup":str(backup)}
    backed_up=[]
    try:
        for row in rows:
            src=game/validate_path(row["path"])
            backup_file=backup/validate_path(row["path"])
            backup_file.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(src,backup_file)
            if sha(backup_file)!=row["original_sha256"]:
                raise AssertionError(f"Backup hash failed: {src}")
            backed_up.append(row)
        (backup/"restore_manifest.json").write_text(json.dumps({
            "schema":"TSCTW-V08-RESTORE-1","files":rows,"installation":str(game),
        },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        completed=[]
        try:
            for row in rows:
                target=game/validate_path(row["path"])
                tmp=target.with_name(target.name+"."+uuid.uuid4().hex+".tsctwtmp")
                try:
                    shutil.copy2(bundle/"Payload"/validate_path(row["path"]),tmp)
                    if sha(tmp)!=row["patched_sha256"]:
                        raise AssertionError("Staged patch changed unexpectedly")
                    os.replace(tmp,target)
                    completed.append(row)
                finally:
                    tmp.unlink(missing_ok=True)
            for row in rows:
                if sha(game/validate_path(row["path"]))!=row["patched_sha256"]:
                    raise AssertionError("Post-install verify failed; rollback will be attempted.")
        except Exception:
            # Best effort rollback even when post-install hash verification fails.
            # Keep the complete backup if rollback itself is interrupted.
            for row in reversed(completed):
                target=game/validate_path(row["path"])
                back=backup/validate_path(row["path"])
                tmp=target.with_name(target.name+"."+uuid.uuid4().hex+".rollbacktmp")
                try:
                    shutil.copy2(back,tmp)
                    os.replace(tmp,target)
                finally:
                    tmp.unlink(missing_ok=True)
            raise
        return {"result":"INSTALLED TEST PATCH, IN-GAME TEST NOT YET DONE","files":len(rows),"backup":str(backup)}
    except Exception:
        # Backups persist for recovery if an interrupted install needs manual help.
        raise


def restore(game,backup,dry_run=True):
    game,backup=game.resolve(),backup.resolve()
    if inside(backup,game):
        raise ValueError("Backup must be outside the game")
    manifest=json.loads((backup/"restore_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema")!="TSCTW-V08-RESTORE-1" or manifest.get("installation")!=str(game):
        raise ValueError("Backup is not for this game installation")
    rows=manifest["files"]
    for row in rows:
        rel=validate_path(row["path"])
        saved=backup/rel
        if not saved.is_file() or saved.is_symlink() or sha(saved)!=row["original_sha256"]:
            raise ValueError(f"Backup data missing/mismatched: {rel}")
    check_destinations(rows,game,"restore")
    if dry_run:
        return {"result":"DRY RUN ONLY - all patched hashes match","files":len(rows)}
    restored=[]
    for row in rows:
        target=game/validate_path(row["path"])
        if sha(target)==row["original_sha256"]:
            continue  # Already restored; permits safe recovery from interrupted restoration.
        tmp=target.with_name(target.name+"."+uuid.uuid4().hex+".restoretmp")
        try:
            shutil.copy2(backup/validate_path(row["path"]),tmp)
            if sha(tmp)!=row["original_sha256"]:
                raise ValueError("Staged restoration corrupted")
            os.replace(tmp,target)
            restored.append(row)
        finally:
            tmp.unlink(missing_ok=True)
    return {"result":"ORIGINAL PACKAGE BYTES RESTORED","files":len(restored),"backup_retained":str(backup)}


def main():
    ap=argparse.ArgumentParser(description="Castaway local TEST installer; DRY RUN is default and never touches saves")
    mode=ap.add_mutually_exclusive_group()
    mode.add_argument("--apply",action="store_true",help="Explicitly install verified patch onto ORIGINAL package hashes")
    mode.add_argument("--restore",action="store_true",help="Restore original packages from verified backup")
    ap.add_argument("--game-root",required=True,type=Path)
    ap.add_argument("--bundle",type=Path,help="Candidate output from prepare_v08_test.py")
    ap.add_argument("--backup",type=Path,required=True,help="New empty/nonexistent backup folder outside game")
    ap.add_argument("--game-closed",action="store_true",help="Confirm game has been completely exited")
    args=ap.parse_args()
    if (args.apply or args.restore) and not args.game_closed:
        ap.error("Refusing to change packages until --game-closed is explicitly provided")
    if not args.restore and args.bundle is None:
        ap.error("--bundle is required except in --restore mode")
    output=restore(args.game_root,args.backup,not args.restore) if args.restore else install(args.bundle,args.game_root,args.backup,not args.apply)
    print(json.dumps(output,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
