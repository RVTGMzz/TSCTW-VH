"""Votri Valley | Castaway Stories v0.8 TEST — click-to-install Windows GUI.

Build with PyInstaller on GitHub Actions. Users do not need Python or any
external runtime. This intentionally includes only translated source/data and
patches the user's locally owned ORIGINAL DBPF package files. It never ships
EA game binaries, overwrites Documents saves, changes fonts, or patches the EXE.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from datetime import datetime

APP_NAME = "Votri Valley | Castaway Việt hóa v0.8 TEST"
FONT_RELATIVE = [
    "TSData/Res/UI/Fonts/RonVN-DejaVuSans.mxf",
    "TSData/Res/UI/Fonts/RonVN-DejaVuSans-Bold.mxf",
]


def embedded_root():
    """Root with runtime/*.gz and the already reviewed translations."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS).resolve()
    return Path(__file__).resolve().parents[2]


def configure_embedded_sources(root=None):
    """Align source-only modules with PyInstaller's read-only _MEIPASS."""
    root = (root or embedded_root()).resolve()
    import validate_runtime
    import stage_runtime_inputs
    import check_runtime_packages
    import prepare_v08_test
    import build_v07
    for module in (validate_runtime, stage_runtime_inputs, check_runtime_packages, prepare_v08_test):
        module.ROOT = root
        module.RUNTIME = root / "runtime"
    build_v07.ROOT = root
    build_v07.CATALOG_PATH = root / "castaway-english-strings.json"
    build_v07.TRANSLATIONS_DIR = root / "translations"
    required = [
        "inventory.json", "catalog.json.gz", "review_queue.json.gz",
        "scope_decisions.json",
    ]
    for name in required:
        if not (root / "runtime" / name).is_file():
            raise FileNotFoundError(f"Ứng dụng thiếu dữ liệu dịch: runtime/{name}. Tải lại bản EXE hoàn chỉnh.")
    for path in (build_v07.CATALOG_PATH,build_v07.TRANSLATIONS_DIR):
        if not path.exists():
            raise FileNotFoundError(f"Thiếu dữ liệu Text đã được biên dịch kèm EXE: {path.name}")
    return stage_runtime_inputs, prepare_v08_test, check_runtime_packages


def find_game_root():
    candidate = Path("G:/Castaway-Portable")
    if (candidate / "TSData").is_dir():
        return candidate
    for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
        candidate = Path(f"{letter}:/Castaway-Portable")
        if (candidate / "TSData").is_dir():
            return candidate
    return None


def backup_base():
    location = os.environ.get("LOCALAPPDATA")
    base = Path(location) if location else Path.home()
    return base / "Votri Valley" / "Castaway v0.8 TEST" / "Backups"


def game_identifier(game):
    return hashlib.sha256(str(game.resolve()).casefold().encode("utf-8")).hexdigest()[:12]


def latest_backup(game):
    base = backup_base() / game_identifier(game)
    if not base.is_dir():
        return None
    for candidate in sorted(base.iterdir(), reverse=True):
        manifest = candidate / "restore_manifest.json"
        if manifest.is_file():
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
                if data.get("installation") == str(game.resolve()):
                    return candidate
            except (OSError, ValueError, json.JSONDecodeError):
                continue
    return None


def game_running():
    """Best-effort Windows guard in addition to the confirmation dialog."""
    if os.name != "nt":
        return False
    try:
        done = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"], stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, timeout=12, check=False,
        )
        listing = done.stdout.decode("utf-8", errors="replace").casefold()
        return any(name in listing for name in (
            '"simscs.exe"', '"simscastawaystories.exe"',
        ))
    except (OSError, subprocess.SubprocessError):
        return False


def preflight(game, progress=lambda x: None):
    from stage_runtime_inputs import select_inventory, inspect
    root = embedded_root()
    if not (game / "TSData").is_dir():
        raise FileNotFoundError("Không tìm thấy thư mục TSData. Hãy chọn đúng thư mục cài Castaway.")
    if game_running():
        raise RuntimeError("Trò chơi có vẻ đang chạy. Hãy thoát hoàn toàn rồi cài lại.")
    missing_font = [rel for rel in FONT_RELATIVE if not (game / rel).is_file()]
    if missing_font:
        raise RuntimeError(
            "Không tìm thấy font Việt hóa đang hoạt động trong game. "
            "Bản v0.8 TEST này là bản mở rộng dành cho v0.7a, "
            "chưa phải gói cài font hoàn chỉnh. Hãy dùng bản cài v0.7a đã có trước đó."
        )
    records = json.loads((root / "runtime" / "inventory.json").read_text(encoding="utf-8"))
    selected = select_inventory(records)
    if len(selected) != 10:
        raise RuntimeError(f"Dữ liệu gốc không khớp: cần 10 package cài đặt, thấy {len(selected)}.")
    progress("Đang đối chiếu 10 package gốc, không thay đổi file...")
    checks = inspect(selected, game, None)
    bad = [x for x in checks if x["status"] not in ("verified", "baseline_mismatch")]
    if bad:
        problems = "\n".join(f"• {r['package']}: {r['status']}" for r in bad[:6])
        raise RuntimeError("Thiếu file package hoặc không thể kiểm tra:\n" + problems)
    modified = [x for x in checks if x["status"] == "baseline_mismatch"]
    if modified:
        progress(f"Phát hiện {len(modified)} file đã thay đổi. Sẽ xác thực cấu trúc DBPF, từng dòng nguồn và ngôn ngữ trước khi vá.")
    return selected


def build_runtime_overlay(game, work, progress=lambda x: None):
    """Stage ORIGINAL packages only in a disposable temp; no Documents saves."""
    from stage_runtime_inputs import sha256
    from prepare_v08_test import build
    inventory = preflight(game, progress)
    work = Path(work)
    stage = work / "original_inputs"
    bundle = work / "candidate"
    core_dummy = work / "unused_core"
    core_dummy.mkdir(parents=True, exist_ok=True)
    for i, entry in enumerate(inventory, start=1):
        path = entry["package"]
        source = game / path
        target = stage / path
        target.parent.mkdir(parents=True, exist_ok=True)
        progress(f"Đọc file gốc {i}/10: {Path(path).name}")
        live_hash = sha256(source)
        shutil.copy2(source, target)
        if sha256(target) != live_hash:
            raise RuntimeError(f"File game thay đổi trong lúc tạo bản sao: {path}")
    progress("Đang xác minh resource, giữ nguyên các câu Việt hóa cũ khác bản hiện tại...")
    manifest = build(core_dummy, stage, bundle, runtime_only=True, allow_prepatched_runtime=True,
                     allow_no_changes=True)
    if manifest["build_mode"] != "runtime-overlay-on-v07a":
        raise RuntimeError("Sai chế độ xây dựng bản thử")
    return bundle, manifest


def capture_selector_sources(game, progress=lambda x: None):
    """Read-only source status; includes install tree and all detected saves."""
    from diagnose_visible_strings import (
        discover_documents_roots, local_package_candidates, selector_source_matrix
    )
    files=local_package_candidates(game)
    for save_root in discover_documents_roots():
        files.extend(local_package_candidates(game, save_root))
    files=list(dict.fromkeys(files))
    return selector_source_matrix(files, progress)


def install_from_game(game, progress=lambda x: None):
    """One-click operation: verify, locally build, verify again, backup and install."""
    configure_embedded_sources()
    from install_v08_local import install
    game = Path(game).resolve()
    with tempfile.TemporaryDirectory(prefix="VV-Castaway-v08-") as work:
        bundle, manifest = build_runtime_overlay(game, Path(work), progress)
        from safe_core_text_overlay import collect_core_overlay
        from build_v07 import CATALOG_PATH, TRANSLATIONS_DIR
        progress("Đang bổ sung các câu Text gốc còn tiếng Anh, giữ nguyên những câu đã Việt hóa...")
        manifest = collect_core_overlay(game,bundle,manifest,CATALOG_PATH,TRANSLATIONS_DIR)
        if not manifest["install_files"]:
            try:
                manifest["selector_post_install"]=capture_selector_sources(game, progress)
            except (OSError, ValueError, AssertionError) as exc:
                manifest["selector_post_install_error"]=f"{type(exc).__name__}: {exc}"
            return {"result": "NO_NEW_ROWS", "files": 0, "backup": None}, manifest
        progress("Đang kiểm tra tính nguyên vẹn của payload và file game...")
        install(bundle, game, backup_base() / game_identifier(game) / "PREVIEW-ONLY",
                dry_run=True)
        now = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        backup = backup_base() / game_identifier(game) / now
        progress("Đang tạo bản sao lưu và cài Việt hóa...")
        result = install(bundle, game, backup, dry_run=False)
    # A post-install scan is evidence only, not proof of active runtime owner.
    try:
        manifest["selector_post_install"]=capture_selector_sources(game, progress)
    except (OSError, ValueError, AssertionError) as exc:
        manifest["selector_post_install_error"]=f"{type(exc).__name__}: {exc}"
    return result, manifest


def restore_game(game, progress=lambda x: None):
    from install_v08_local import restore
    game = Path(game).resolve()
    backup = latest_backup(game)
    if backup is None:
        raise FileNotFoundError("Chưa tìm được bản sao lưu do công cụ này tạo cho thư mục game đã chọn.")
    if game_running():
        raise RuntimeError("Hãy thoát game hoàn toàn trước khi khôi phục.")
    progress("Đang kiểm tra bản sao lưu và file hiện tại...")
    restore(game, backup, dry_run=True)
    progress("Đang khôi phục những package ban đầu...")
    return restore(game, backup, dry_run=False)


def save_diagnostic_report(destination, log):
    """Write user-visible text only, never package bytes/saves, on explicit request."""
    destination = Path(destination)
    destination.write_text(
        "Votri Valley - The Sims Castaway Stories v0.8 TEST\n"
        "Báo cáo tạo thủ công (không tự gửi qua mạng).\n"
        "Xin kiểm tra đường dẫn cá nhân trước khi chia sẻ.\n\n" + log + "\n",
        encoding="utf-8",
    )


class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("690x480")
        self.root.minsize(630, 430)
        self.root.resizable(True, True)
        self.events = queue.Queue()
        self.busy = False
        self.diagnostic_results = None
        self.game = tk.StringVar(value=str(find_game_root() or ""))
        self.status = tk.StringVar(value="Sẵn sàng chọn thư mục Castaway.")

        panel = ttk.Frame(root, padding=20)
        panel.pack(fill="both", expand=True)
        ttk.Label(panel, text="THE SIMS CASTAWAY STORIES",
                  font=("Segoe UI", 17, "bold")).pack(anchor="w")
        ttk.Label(panel, text="Bản Việt hóa Votri Valley — v0.8 TEST",
                  font=("Segoe UI", 11)).pack(anchor="w", pady=(2, 12))
        ttk.Label(panel,
                  text=("Cài bổ sung phần chữ runtime và Text còn thiếu.\n"
                        "Không cần Python, không sửa save; giữ font và bản dịch cũ."),
                  justify="left").pack(anchor="w", pady=(0, 12))
        ttk.Label(panel, text="Thư mục game (chứa TSData):").pack(anchor="w")
        location = ttk.Frame(panel)
        location.pack(fill="x", pady=(4, 12))
        ttk.Entry(location, textvariable=self.game).pack(side="left", fill="x", expand=True)
        self.browse = ttk.Button(location, text="Chọn thư mục...", command=self.choose)
        self.browse.pack(side="left", padx=(8, 0))
        controls = ttk.Frame(panel)
        controls.pack(fill="x", pady=(0, 12))
        self.install_button = ttk.Button(controls, text="Cài Việt hóa v0.8 TEST", command=self.install)
        self.install_button.pack(side="left")
        self.restore_button = ttk.Button(controls, text="Khôi phục bản trước", command=self.restore)
        self.restore_button.pack(side="left", padx=(10, 0))
        self.report_button = ttk.Button(controls, text="Lưu báo cáo...", command=self.save_report)
        self.report_button.pack(side="left", padx=(10, 0))
        self.diagnose_button = ttk.Button(controls, text="Rà chữ còn sót", command=self.diagnose)
        self.diagnose_button.pack(side="left", padx=(10, 0))
        extras = ttk.Frame(panel)
        extras.pack(fill="x", pady=(0,10))
        self.save_patch_button = ttk.Button(extras, text="Việt hóa đảo & tiểu sử...", command=self.patch_saves)
        self.save_patch_button.pack(side="left")
        self.save_restore_button = ttk.Button(extras, text="Khôi phục dữ liệu đảo", command=self.restore_saves)
        self.save_restore_button.pack(side="left",padx=(10,0))
        self.progressbar = ttk.Progressbar(panel, mode="indeterminate")
        self.progressbar.pack(fill="x", pady=(0, 8))
        ttk.Label(panel, textvariable=self.status, wraplength=620).pack(anchor="w", pady=(0, 6))
        self.log = scrolledtext.ScrolledText(panel, height=8, wrap="word",
                                             state="disabled", font=("Consolas", 9))
        self.log.pack(fill="both", expand=True)
        self.write("Lưu ý: Đây là bản TEST. Sau khi cài, hãy kiểm tra gameplay, Rewards, vật phẩm và menu.")
        self.write("File đã Việt hóa trước được kiểm tra theo resource. Bản khác nguồn sẽ được giữ nguyên.")
        self.root.after(125, self.process_events)

    def write(self, value):
        self.log.configure(state="normal")
        self.log.insert("end", str(value) + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def save_report(self):
        """User-initiated local export; never auto-uploads logs or game data."""
        filename = filedialog.asksaveasfilename(
            title="Lưu báo cáo Castaway để gửi hỗ trợ",
            defaultextension=".txt",
            initialfile="Castaway-v08-bao-cao.txt",
            filetypes=[("Tệp văn bản", "*.txt")],
        )
        if not filename:
            return
        data = self.log.get("1.0", "end-1c")
        if self.diagnostic_results is not None:
            data += "\n\n=== CHI TIẾT RESOURCE RÀ CHỮ ===\n" + json.dumps(
                self.diagnostic_results, ensure_ascii=False, indent=2
            )
        try:
            save_diagnostic_report(Path(filename), data)
            messagebox.showinfo("Đã lưu báo cáo",
                "Báo cáo đã lưu trên máy. Hãy mở xem lại trước khi gửi, vì có thể chứa đường dẫn cá nhân.\n\n"
                + filename)
        except OSError as exc:
            messagebox.showerror("Không lưu được báo cáo", str(exc))

    def choose(self):
        chosen = filedialog.askdirectory(title="Chọn thư mục Castaway chứa TSData")
        if chosen:
            self.game.set(chosen)

    def selected_game(self):
        value = self.game.get().strip().strip('"')
        if not value or not (Path(value) / "TSData").is_dir():
            messagebox.showwarning("Chưa chọn đúng game", "Hãy chọn thư mục Castaway có thư mục con TSData.")
            return None
        return Path(value).resolve()

    def choose_save_root(self):
        from diagnose_visible_strings import discover_documents_roots
        roots = discover_documents_roots()
        if len(roots)==1:
            return roots[0]
        chosen = filedialog.askdirectory(title="Chọn thư mục save Castaway có Neighborhoods")
        if chosen and (Path(chosen)/"Neighborhoods").is_dir():
            return Path(chosen).resolve()
        messagebox.showwarning("Chưa có save", "Hãy chọn thư mục dữ liệu Castaway trong Documents có Neighborhoods.")
        return None

    def patch_saves(self):
        game = self.selected_game()
        if game is None:
            return
        save_root = self.choose_save_root()
        if save_root is None:
            return
        if not messagebox.askyesno(
            "Xác nhận sửa dữ liệu đảo (TÙY CHỌN)",
            "Thao tác này KHÁC bản cài Việt hóa thông thường: sẽ sửa đúng các resource chữ "
            "trong SAVE N001/N002 ở Documents. Trình cài sao lưu nguyên file trước khi thay.\n\n"
            "Hãy THOÁT GAME, sao lưu save riêng nếu cần. Nếu chơi và lưu sau khi vá, việc "
            "khôi phục sẽ KHÔNG tự ghi đè tiến trình mới.\n\n"
            "Tiếp tục Việt hóa tiêu đề, tiểu sử và tên địa điểm đã kiểm duyệt?"
        ):
            return
        from patch_neighborhood_text import apply_saved_neighborhood_updates
        if game_running():
            messagebox.showwarning("Game đang mở","Hãy thoát Castaway trước khi sửa save.")
            return
        backup = backup_base() / game_identifier(game) / "SavedNeighborhoods" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        self.start("Vá chữ đảo có sao lưu (Documents)",
                   lambda progress: apply_saved_neighborhood_updates(save_root,backup))

    def restore_saves(self):
        game = self.selected_game()
        if game is None:
            return
        save_root = self.choose_save_root()
        if save_root is None:
            return
        base = backup_base() / game_identifier(game) / "SavedNeighborhoods"
        possible=[]
        if base.is_dir():
            for directory in sorted(base.iterdir(),reverse=True):
                manifest=directory/"restore_manifest.json"
                if manifest.is_file():
                    try:
                        data=json.loads(manifest.read_text(encoding="utf-8"))
                        if data.get("save_root")==str(save_root):
                            possible.append(directory)
                    except (ValueError,OSError):
                        continue
        if not possible:
            messagebox.showinfo("Chưa có sao lưu đảo","Không có bản sao lưu đảo phù hợp với save đang chọn.")
            return
        if game_running():
            messagebox.showwarning("Game đang mở","Hãy thoát Castaway trước khi khôi phục.")
            return
        if not messagebox.askyesno("Khôi phục dữ liệu đảo",
            "Khôi phục N001/N002 về trạng thái ngay trước khi Việt hóa đảo? "
            "Nếu save đã thay đổi sau đó, trình cài sẽ TỪ CHỐI để không xóa tiến trình.\n\n"
            +str(possible[0])):
            return
        from patch_neighborhood_text import restore_saved_neighborhoods
        self.start("Khôi phục gói chữ đảo",
                   lambda progress: restore_saved_neighborhoods(save_root,possible[0]))

    def diagnose(self):
        game = self.selected_game()
        if game is None:
            return
        from diagnose_visible_strings import diagnose
        self.start("Rà nguồn chữ còn sót (chỉ đọc, không sửa game)",
                   lambda progress: diagnose(game,progress))

    def start(self, job, worker):
        if self.busy:
            return
        self.busy = True
        self.install_button.configure(state="disabled")
        self.restore_button.configure(state="disabled")
        self.diagnose_button.configure(state="disabled")
        self.save_patch_button.configure(state="disabled")
        self.save_restore_button.configure(state="disabled")
        self.browse.configure(state="disabled")
        self.progressbar.start(14)
        self.write(f"--- {job} ---")
        def run():
            try:
                result = worker(lambda s: self.events.put(("progress", s)))
                self.events.put(("success", result))
            except Exception as exc:
                self.events.put(("error", f"{type(exc).__name__}: {exc}"))
            finally:
                self.events.put(("done", None))
        threading.Thread(target=run, daemon=True).start()

    def install(self):
        game = self.selected_game()
        if game is None:
            return
        if not messagebox.askyesno(
            "Xác nhận cài v0.8 TEST",
            "Ông đã thoát hẳn Castaway chưa?\n\n"
            "Trình cài sẽ kiểm tra và sao lưu file trước khi vá runtime và Text còn tiếng Anh. "
            "Các câu đã Việt hóa và font cũ được giữ nguyên; không sửa save Documents.\n\n"
            "Tiếp tục?", icon="question",
        ):
            return
        self.start("Cài Việt hóa", lambda progress: install_from_game(game, progress))

    def restore(self):
        game = self.selected_game()
        if game is None:
            return
        backup = latest_backup(game)
        if backup is None:
            messagebox.showinfo("Chưa có bản sao lưu", "Không tìm thấy bản sao lưu do trình cài tạo cho thư mục này.")
            return
        if not messagebox.askyesno(
            "Khôi phục",
            f"Khôi phục package gốc từ bản sao lưu:\n{backup}\n\n"
            "Hãy thoát game trước khi tiếp tục.",
        ):
            return
        self.start("Khôi phục", lambda progress: restore_game(game, progress))

    def process_events(self):
        while True:
            try:
                event, value = self.events.get_nowait()
            except queue.Empty:
                break
            if event == "progress":
                self.status.set(value)
                self.write(value)
            elif event == "success":
                self.status.set("Hoàn tất thao tác.")
                if isinstance(value,dict) and value.get("state") in (
                        "PATCHED_FOR_TEST","RESTORED_PREVIOUS_SAVE_STATE","NO_NEW_ROWS"):
                    self.write("Dữ liệu đảo: "+json.dumps(value,ensure_ascii=False))
                    selector=value.get("selector_status")
                    if selector:
                        labels={"story_title":"Đắm tàu và độc thân — tiêu đề",
                                "story_description":"Đắm tàu và độc thân — mô tả",
                                "island_title":"Đảo Wanmami — tiêu đề",
                                "island_description":"Đảo Wanmami — mô tả"}
                        for key,counts in selector["fields"].items():
                            self.write(f"{labels.get(key,key)}: "
                                       f"{counts['vietnamese']} bản ghi VI, "
                                       f"{counts['english']} bản ghi EN")
                        self.write("Các dòng trên được kiểm trong SAVE; game thật đọc nguồn nào vẫn cần xác nhận.")
                    selector_missing = (selector is not None and any(
                        counts["vietnamese"] == 0 or counts["english"] > 0
                        for counts in selector["fields"].values()
                    ))
                    if selector_missing and value["state"] != "RESTORED_PREVIOUS_SAVE_STATE":
                        self.write("CHƯA HOÀN TẤT: ít nhất một tiêu đề/mô tả "
                                   "chưa tìm thấy bản tiếng Việt trong SAVE đã chọn.")
                    messagebox.showinfo("Dữ liệu đảo",
                        ("Đã khôi phục dữ liệu đảo." if value["state"]=="RESTORED_PREVIOUS_SAVE_STATE" else
                         "Đã kiểm tra SAVE nhưng còn thiếu tiếng Việt ở một hoặc nhiều "
                         "tiêu đề/mô tả. Hãy lưu báo cáo; đừng coi màn chọn chế độ đã hoàn tất."
                         if selector_missing else
                         "Không có câu mới cần sửa; vẫn cần kiểm tra trực tiếp trong game."
                         if value["state"]=="NO_NEW_ROWS" else
                         "Đã xử lý chữ đảo. Hãy thử game để xác nhận nguồn; backup được lưu riêng."))
                elif isinstance(value,dict) and "hits" in value:
                    from diagnose_visible_strings import concise_for_gui
                    self.diagnostic_results = value
                    for line in concise_for_gui(value):
                        self.write(line)
                    self.status.set("Rà chữ xong. Nhấn 'Lưu báo cáo...' để gửi các resource còn sót.")
                    messagebox.showinfo("Đã rà xong",
                        f"Đã tìm {len(value['hits'])} dòng nghi liên quan. "
                        "Nhấn 'Lưu báo cáo...' để lưu vị trí package và resource, rồi gửi tui kiểm tra. "
                        "Không có file game nào bị thay đổi.")
                elif isinstance(value, tuple):
                    report, manifest = value
                    amount = sum(r["changed_rows"] for r in manifest["install_files"])
                    # Log the read-only selector snapshot even when the ordinary
                    # overlay has nothing to change. Never equate this with an
                    # in-game verification of the active screen source.
                    snapshot=manifest.get("selector_post_install")
                    if snapshot:
                        source_rows=snapshot.get("matches",[])
                        for field,label in (
                            ("story_title","Tên Đắm tàu và độc thân"),
                            ("story_description","Mô tả Đắm tàu và độc thân"),
                            ("island_title","Tên Đảo Wanmami"),
                            ("island_description","Mô tả Đảo Wanmami"),
                        ):
                            en=sum(r["state"]=="english" and r["field"]==field for r in source_rows)
                            vi=sum(r["state"]=="vietnamese" and r["field"]==field for r in source_rows)
                            self.write(f"Màn chọn chế độ | {label}: {en} EN / {vi} VI (các nguồn tìm thấy)")
                        if snapshot.get("failed"):
                            self.write(f"CẢNH BÁO: {len(snapshot['failed'])} package không đọc được; kết quả không đầy đủ.")
                        if any(r["state"]=="english" for r in source_rows):
                            self.write("CHƯA HOÀN TẤT: vẫn tìm thấy tiếng Anh trong nguồn màn chọn chế độ.")
                        elif not source_rows:
                            self.write("CHƯA XÁC ĐỊNH: không nhận diện được nguồn chữ màn chọn chế độ.")
                        self.write("Đây là đối chiếu SOURCE; cần xác nhận nguồn game thực sự đọc.")
                    elif manifest.get("selector_post_install_error"):
                        self.write("Không rà được màn chọn chế độ: "+manifest["selector_post_install_error"])
                    if report["result"] == "NO_NEW_ROWS":
                        self.status.set("Không có dòng tiếng Anh phù hợp để bổ sung; game giữ nguyên.")
                        self.write("Không có dòng tiếng Anh khớp nguồn nào cần bổ sung. Không thay đổi file, không tạo backup mới.")
                        messagebox.showinfo("Không cần cài lại",
                            "Không tìm thấy dòng tiếng Anh khớp nguồn nào cần bổ sung ở các package đã kiểm tra.\n"
                            "Game không bị thay đổi. Lưu ý: điều này chưa xác nhận mọi chữ trong game đều đã Việt hóa.")
                        continue
                    self.write(f"Đã cài {report['files']} package, thay đổi {amount} dòng. Sao lưu: {report['backup']}")
                    compatibility = manifest.get("modified_baseline_checks", [])
                    if compatibility:
                        self.write(f"Đã kiểm tra {len(compatibility)} package khác hash gốc: "
                                   + ", ".join(Path(x["package"]).name for x in compatibility))
                        unknown = manifest.get("unrecognized_rows_preserved", 0)
                        if unknown:
                            self.write(f"GIỮ NGUYÊN {unknown} câu từng sửa khác bản dịch hiện tại; "
                                       "không ghi đè và chưa tính những câu này là đã kiểm duyệt.")
                    messagebox.showinfo(
                        "Đã cài bản v0.8 TEST",
                        "Cài đặt đã qua kiểm tra file và sao lưu.\n"
                        "Bản cài chính không sửa save Documents. Hai tên chế độ và đoạn mô tả có thể vẫn tiếng Anh nếu game đọc N001/N002 trong save.\n"
                        "Để thử phần này, dùng nút 'Việt hóa đảo & tiểu sử...' riêng (có xác nhận, sao lưu và khôi phục).\n"
                        "Đây vẫn là bản TEST: cần chơi để xác nhận nguồn hiển thị.\n\n"
                        f"Thư mục sao lưu:\n{report['backup']}",
                    )
                else:
                    self.write(f"Khôi phục: {value}")
                    messagebox.showinfo("Đã khôi phục", "Đã phục hồi các package gốc từ bản sao lưu.")
            elif event == "error":
                self.status.set("Đã dừng an toàn. Xem chi tiết bên dưới.")
                self.write(value)
                messagebox.showerror("Không thể hoàn tất", value + "\n\nNhấn 'Lưu báo cáo...' để lưu thông tin lỗi mà không cần chụp nhiều ảnh.")
            elif event == "done":
                self.busy = False
                self.progressbar.stop()
                for button in (self.install_button,self.restore_button,self.diagnose_button,
                               self.save_patch_button,self.save_restore_button,self.browse):
                    button.configure(state="normal")
        self.root.after(125, self.process_events)


def main():
    if "--self-test" in sys.argv:
        configure_embedded_sources()
        from validate_runtime import assess
        report, _ = assess()
        if report["parse_errors"] or report["untranslated_or_review_candidate_rows"]:
            raise SystemExit("Bundled source QA FAILED")
        # Critical: the binary smoke must actually BUILD a runtime-only patch
        # without any core Text catalog, then install and restore fake bytes.
        from smoke_frozen_v08 import smoke
        if not smoke():
            raise SystemExit("Frozen installer integration smoke FAILED")
        if sys.stdout is not None:
            print("Bundled source QA PASS: candidate_rows="+str(report["candidate_rows"]))
        return
    if os.name != "nt":
        raise SystemExit("Trình cài nhấp đúp này dành cho Windows; chạy kiểm thử nguồn trên nền tảng khác.")
    root = tk.Tk()
    InstallerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
