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
    for module in (validate_runtime, stage_runtime_inputs, check_runtime_packages, prepare_v08_test):
        module.ROOT = root
        module.RUNTIME = root / "runtime"
    required = [
        "inventory.json", "catalog.json.gz", "review_queue.json.gz",
        "scope_decisions.json",
    ]
    for name in required:
        if not (root / "runtime" / name).is_file():
            raise FileNotFoundError(f"Ứng dụng thiếu dữ liệu dịch: runtime/{name}. Tải lại bản EXE hoàn chỉnh.")
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
    bad = [x for x in checks if x["status"] != "verified"]
    if bad:
        problems = "\n".join(
            f"• {r['package']}: {r['status']}" for r in bad[:6]
        )
        raise RuntimeError(
            "Một số file game không khớp bản gốc đã audit (có thể từng bị patch):\n"
            + problems +
            "\nChưa có file nào bị thay đổi. Không ép cài hoặc chép đè package."
        )
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
        shutil.copy2(source, target)
        if sha256(target) != entry["sha256"]:
            raise RuntimeError(f"Bản sao đầu vào thay đổi khi chép: {path}")
    progress("Đang tạo và kiểm tra bản Việt hóa runtime v0.8...")
    manifest = build(core_dummy, stage, bundle, runtime_only=True)
    if manifest["build_mode"] != "runtime-overlay-on-v07a":
        raise RuntimeError("Sai chế độ xây dựng bản thử")
    return bundle, manifest


def install_from_game(game, progress=lambda x: None):
    """One-click operation: verify, locally build, verify again, backup and install."""
    configure_embedded_sources()
    from install_v08_local import install
    game = Path(game).resolve()
    with tempfile.TemporaryDirectory(prefix="VV-Castaway-v08-") as work:
        bundle, manifest = build_runtime_overlay(game, Path(work), progress)
        progress("Đang kiểm tra tính nguyên vẹn của payload và file game...")
        install(bundle, game, backup_base() / game_identifier(game) / "PREVIEW-ONLY",
                dry_run=True)
        now = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        backup = backup_base() / game_identifier(game) / now
        progress("Đang tạo bản sao lưu và cài Việt hóa...")
        result = install(bundle, game, backup, dry_run=False)
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


class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("690x480")
        self.root.minsize(630, 430)
        self.root.resizable(True, True)
        self.events = queue.Queue()
        self.busy = False
        self.game = tk.StringVar(value=str(find_game_root() or ""))
        self.status = tk.StringVar(value="Sẵn sàng chọn thư mục Castaway.")

        panel = ttk.Frame(root, padding=20)
        panel.pack(fill="both", expand=True)
        ttk.Label(panel, text="THE SIMS CASTAWAY STORIES",
                  font=("Segoe UI", 17, "bold")).pack(anchor="w")
        ttk.Label(panel, text="Bản Việt hóa Votri Valley — v0.8 TEST",
                  font=("Segoe UI", 11)).pack(anchor="w", pady=(2, 12))
        ttk.Label(panel,
                  text=("Cài bổ sung phần chữ runtime trên nền bản v0.7a đang dùng.\n"
                        "Không cần Python, không sửa save, không chép đè font đã cài."),
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
        self.progressbar = ttk.Progressbar(panel, mode="indeterminate")
        self.progressbar.pack(fill="x", pady=(0, 8))
        ttk.Label(panel, textvariable=self.status, wraplength=620).pack(anchor="w", pady=(0, 6))
        self.log = scrolledtext.ScrolledText(panel, height=8, wrap="word",
                                             state="disabled", font=("Consolas", 9))
        self.log.pack(fill="both", expand=True)
        self.write("Lưu ý: Đây là bản TEST. Sau khi cài, hãy kiểm tra gameplay, Rewards, vật phẩm và menu.")
        self.write("File game phải khớp bản gốc. Nếu bị mod sẵn, trình cài sẽ dừng an toàn.")
        self.root.after(125, self.process_events)

    def write(self, value):
        self.log.configure(state="normal")
        self.log.insert("end", str(value) + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

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

    def start(self, job, worker):
        if self.busy:
            return
        self.busy = True
        self.install_button.configure(state="disabled")
        self.restore_button.configure(state="disabled")
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
            "Trình cài sẽ kiểm tra file gốc, tự tạo bản vá runtime, sao lưu rồi cài. "
            "Nó sẽ giữ nguyên Text/font v0.7a và save trong Documents.\n\n"
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
                if isinstance(value, tuple):
                    report, manifest = value
                    amount = sum(r["changed_rows"] for r in manifest["install_files"])
                    self.write(f"Đã cài {report['files']} package, thay đổi {amount} dòng. Sao lưu: {report['backup']}")
                    messagebox.showinfo(
                        "Đã cài bản v0.8 TEST",
                        "Cài đặt đã qua kiểm tra file và sao lưu.\n"
                        "Đây vẫn là bản TEST: cần chơi để xác nhận toàn bộ giao diện.\n\n"
                        f"Thư mục sao lưu:\n{report['backup']}",
                    )
                else:
                    self.write(f"Khôi phục: {value}")
                    messagebox.showinfo("Đã khôi phục", "Đã phục hồi các package gốc từ bản sao lưu.")
            elif event == "error":
                self.status.set("Đã dừng an toàn. Xem chi tiết bên dưới.")
                self.write(value)
                messagebox.showerror("Không thể hoàn tất", value)
            elif event == "done":
                self.busy = False
                self.progressbar.stop()
                for button in (self.install_button, self.restore_button, self.browse):
                    button.configure(state="normal")
        self.root.after(125, self.process_events)


def main():
    if "--self-test" in sys.argv:
        configure_embedded_sources()
        from validate_runtime import assess
        report, _ = assess()
        if report["parse_errors"] or report["untranslated_or_review_candidate_rows"]:
            raise SystemExit("Bundled source QA FAILED")
        print("Bundled source QA PASS: candidate_rows="+str(report["candidate_rows"]))
        return
    if os.name != "nt":
        raise SystemExit("Trình cài nhấp đúp này dành cho Windows; chạy kiểm thử nguồn trên nền tảng khác.")
    root = tk.Tk()
    InstallerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
