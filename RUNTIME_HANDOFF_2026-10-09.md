> **LATEST — 2026-10-09 Build 23 PASS (frozen EXE missing-catalog FIX).** Ron tried the prior Build 17 and reported `FileNotFoundError: C:\\Users\\win\\AppData\\Local\\castaway-english-strings.json` after 10 runtime files were staged and the exact-row verification finished. **The code previously called `build_v07.load_translations()` unconditionally even in `--runtime-only` mode**, which reads `castaway-english-strings.json` from a path absent in the PyInstaller EXE. This is a SOURCE BUG in the installer, not a missing Windows dependency and not a bad game package. Fixed in commit `0a431b48`: runtime-only builds never call `load_translations()`, `derive_targets()`, or `load_v06_history()` and do not need original Text assets. `test_v08_delivery.py` forces missing core loader errors to assert it isn't invoked. **NEW** `smoke_frozen_v08.py` is imported by the GUI `--self-test` and performs a genuine synthetic 24-byte DBPF runtime build, payload validation, dry-run, installation and exact restore *inside the packaged frozen Windows EXE*; workflow runs both source and frozen integration smoke. [CI Windows build 23 PASS](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37860653995), EXE ~15.1MB [DIRECT DOWNLOAD](https://github.com/RVTGMzz/TSCTW-VH/releases/download/castaway-v08-test-windows-23/VotriValley-Castaway-v08-TEST.exe), [Release](https://github.com/RVTGMzz/TSCTW-VH/releases/tag/castaway-v08-test-windows-23). **Not yet tested on Ron's real installed game or actual packages.**

**Restore clarity:** Build 17 stopped on core-loader missing-file error *before* `install_v08_local.install()`; no changes/no backup created and no restoration necessary from that failed attempt. On successful Build 23 install, backup folder `%LOCALAPPDATA%\\Votri Valley\\Castaway v0.8 TEST\\Backups` contains exact package bytes from immediately BEFORE v0.8 installation, including prior Vietnamese patches; the GUI `Khôi phục bản trước` restores those exact prior bytes, NOT a clean/untranslated game. If a future install fails after partial writes, installer attempts rollback and retains backup for recovery. Do not advise replacing or deleting game files. If Build 23 fails, request screenshot and continue debugging exact failure, not bypass safeguards.

---

> **LATEST Castaway installer bugfix — 2026-10-09 (Windows Build 17 PASS).** Ron attempted Build 11 on `G:/Castaway-Portable`; after reading all 10 package files the compatibility audit stopped in `TSData/Res/Objects/objects.package`, DBPF key `(1414807923, 2140262859, 128, 0)`, row `9`, with a pre-existing Vietnamese value (shown in error screenshot) not identical to the currently approved mapping. **No write occurred.** This proves SHA mismatch alone is not the only compatibility issue; old translations can differ from current final copy. [Build 17 direct EXE](https://github.com/RVTGMzz/TSCTW-VH/releases/download/castaway-v08-test-windows-17/VotriValley-Castaway-v08-TEST.exe) · [Release](https://github.com/RVTGMzz/TSCTW-VH/releases/tag/castaway-v08-test-windows-17) · [Windows CI PASS](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37860138523) · [Source Audit PASS](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37860138574). **Not game-tested on Ron's machine yet.**

**Systematic remedy:** `safe_rebase_runtime.inspect_prepatched(... preserve_unrecognized=True)` verifies DBPF index width and total resource count, and exact audited key, row index, language and description. It counts unknown existing values as **preserved and unreviewed**, never as approved. `check_runtime_packages.apply(... preserve_unrecognized=True)` skips them **without writing**, translates only rows that still exactly match the original English, and leaves already-approved Vietnamese unchanged. The opt-in is used ONLY by `prepare_v08_test.build(...allow_prepatched_runtime=True)` in runtime-only GUI overlay. Strict QA/default writer still reject unknown source text; altered metadata or invalid DBPF remain hard failures. The resulting manifest reports `unrecognized_rows_preserved`; GUI logs the preserved count. New synthetic regressions cover unknown old Vietnamese kept, independent English row patched, wrong metadata blocked, idempotence and end-to-end backup/install/restore exact original bytes. GitHub Windows CI Build 17 and packaged EXE smoke test PASS; the 15 MB EXE is a direct prerelease download. The app still needs a real-world test, and may reveal other genuine resource/metadata incompatibilities; do not tell Ron to delete/overwrite files or reinstall. Refer to screenshot issue as row 9 and full key before asking for new diagnostic evidence.

---

> **FIXED WINDOWS INSTALLER, 2026-10-09 — user-reported BASELINE MISMATCH:** Existing v0.8 TEST build 4 reported `baseline_mismatch` for **`TSData/Res/Objects/objects.package` and `TSData/Res/Text/Wants.package`** on Ron's portable install. These two files may have been modified by older localization (not independently verified). **DO NOT ask user to replace, delete or manually patch these files.** [Download new EXE build 11](https://github.com/RVTGMzz/TSCTW-VH/releases/download/castaway-v08-test-windows-11/VotriValley-Castaway-v08-TEST.exe) or [GitHub prerelease page](https://github.com/RVTGMzz/TSCTW-VH/releases/tag/castaway-v08-test-windows-11). [Windows CI build 11 PASS](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37838952810): binary and delivery regression tests, bundled source validation, frozen EXE smoke test, direct prerelease upload. Still **not tested against user's actual game packages**.

**Patch mechanism:** `src/builder/safe_rebase_runtime.py` verifies the exact audited DBPF index width/resource count and every eligible key/row/language/description. Each existing value must be the original audited English or the *exact approved Vietnamese translation*. Unknown value or modified metadata aborts before applying. `prepare_v08_test.py` accepts compatible modified inputs only in explicit `--runtime-only --allow-compatible-modified-runtime` mode; GUI enables that guarded mode after verifying 10 package paths and staging unmodified copies of live files, then checks live input sha again via install manifest, makes backups and supports exact restore. **Never bypass guards or auto-overwrite a mismatched unknown source.** Five new synthetic regression tests validate previously translated + English mixtures, unknown value refusal, index refusal, preservation of unrelated user changes and install/restore of exact previous bytes. If Build 11 still fails on unknown text/metadata, request error screenshot/output and refine evidence for that resource; do not ask for reinstall upfront.

---

> **TẢI EXE CÀI BẰNG NHẤN ĐÚP — VOTRI VALLEY v0.8 TEST (2026-10-09).** [Tải trực tiếp **VotriValley-Castaway-v08-TEST.exe**](https://github.com/RVTGMzz/TSCTW-VH/releases/download/castaway-v08-test-windows-4/VotriValley-Castaway-v08-TEST.exe) ([GitHub prerelease](https://github.com/RVTGMzz/TSCTW-VH/releases/tag/castaway-v08-test-windows-4)). Được build thành công bằng GitHub Actions Windows [run #4](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37837500377), bước smoke-test **EXE đóng gói PASS**. Người dùng **KHÔNG cần cài Python hay công cụ phụ**. EXE có giao diện cài bằng một nút và nút khôi phục, tự tìm `G:/Castaway-Portable`, giữ Text/font v0.7a, không sửa Documents save, từ chối nếu 10 package runtime không khớp hash gốc. **VẪN LÀ TEST:** chưa chạy trên 10 package thật hoặc xác minh in-game, Story Selector vẫn cần xử lý. Mã nguồn GUI: `src/builder/win_v08_installer.py`; workflow: `.github/workflows/v08-windows-installer.yml`; hướng dẫn: `CLICK_TO_INSTALL_WINDOWS.md`. Từ đây ưu tiên thu thập lỗi thực tế/kiểm thử game, không dịch rộng The Sims 2.

> **NEWEST 2026-10-09: LOCAL v0.8 TEST BUILD PATH.** Read [`V08_LOCAL_TEST_GUIDE.md`](V08_LOCAL_TEST_GUIDE.md) first, then `runtime/CASTAWAY_ONLY_FOCUS_2026-10-09.md`. The source-only GitHub repo now has a guarded local candidate builder `src/builder/prepare_v08_test.py`, plus an explicit dry-run-first, hash-gated backup/install/restore utility `src/builder/install_v08_local.py`. **Still not a tested downloadable v0.8 release.** No user-owned package bytes were staged to this GitHub session. Keep Castaway-only priority; DO NOT resume broad The Sims 2 localization.

### What was implemented after Source Audit #444

- `prepare_v08_test.py` assembles original-core Text and runtime package patches, using existing verified builders, into `work/v08_candidate/Payload` plus `manifest.json`; patches ONLY changed package paths, verifies source candidate coverage, 10 original installation runtime SHA-256s, row metadata and runtime writer idempotence. No Documents saves, fonts, executables or auto-install. Output must not overlap inputs, and aborting removes incomplete output.
- Its explicit **`--runtime-only` mode** generates a **runtime overlay TEST** for Ron's existing *v0.7a core Text + working RonVN font* without requiring old Text originals; it does NOT claim full text rebuild. The full original-core mode still requires all 8 English core Text files and explicit `--core-original-confirmed`.
- A source guard `refuse_pretranslated_core` now checks against historical v0.6 Vietnamese exact resource fingerprints so detectable already-patched Text source cannot be mislabeled an original English baseline. This is not a perfect version hash check.
- `install_v08_local.py` defaults to **DRY RUN** and only installs via `--apply --game-closed` onto original hashes, after copying verified backups outside the game. `--restore --game-closed` validates current patched/original hashes, restores original bytes from backups and tolerates interrupted partial restores. Refuses save paths, duplicate paths, unknown hashes, manifest mismatches, or backup overwrite. Font remains as installed; no Documents saves changed.
- `test_v08_delivery.py` uses only fictional binary package fixtures to exercise build, manifest, dry run, installation, backup, restore, altered-file refusal, path safety and patch-core detection. This test suite has 8 tests after final addition (confirm exact CI count in next completed Source Audit). Previous 4 staging + 2 DBPF + 3 selector tests are retained. Do not pretend synthetic tests replace Windows game tests.
- `V08_LOCAL_TEST_GUIDE.md` contains exact step-by-step commands for the 10 package preflight, staging, runtime overlay and full candidate, dry run, explicit install, hash-backed restore and read-only story-selector probe on `G:/Castaway-Portable`.

**Known state:** Source Audit #425 proved 14,719 candidate rows, 0 missing/review candidates, 20,095 unresolved inherited, 0 parse errors, and the 17 selector-related source rows were all translated. Later build-code commits do not change these translation counts. **v0.8 has NOT been built/tested against real game binaries in this session**. The actual selector source/read order remains unverified. Do not publish the runtime overlay as a complete localization, and do not distribute commercial game packages.

**Next task:** run source-only CI to completion; if PASS, obtain original 10 runtime packages available locally in Ron's installation/backups without asking for unrelated files. Execute `stage_runtime_inputs.py` + `prepare_v08_test.py --runtime-only` on the user's Windows PC, then use `install_v08_local.py` first DRY RUN and then with explicit consent after game exit. Ron tests Story Selector, item/rewards/Examine/Use/Want etc and reports remaining English owner families. For full v0.8, add original 8 core Text and verify compatibility with v0.7a font. No false claims of a currently downloadable payload.

---

> **2026-10-09 Castaway-only v0.8 build-gate progress — Source Audit #442 PASS** ([run](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37834920574)). The two new source-focused developments below supersede older notes requiring all 13 baselines for installation QA. Source coverage unchanged: **7,154 aggregate mapping entries / 2,163 exact translations / 14,719 candidate rows / 0 missing-review / 20,095 unresolved inherited / 0 parse errors**. **v0.8 TEST remains UNRELEASED.**

## Newest: source-to-installer isolation and selector read-only probe

**User goal:** finish The Sims Castaway Stories, NOT make a separate The Sims 2 Legacy localization. Do not go back to unrelated inherited-memory sweeps.

- `src/builder/stage_runtime_inputs.py` now **defaults to only 10 game-installation packages** and excludes **3 Documents/user-save snapshots** under `TSData/Res/UserData/`. Optional `--include-save-snapshots --save-root ...` exists for diagnostic QA only. Original SHA-256 strictness remains; both `Text/Wants.package` and `Wants/Wants.package` remain distinct. `--copy-verified` only stages input when every selected hash matches; never overwrites live inputs.
- `src/builder/check_runtime_packages.py` shares `select_inventory()`, so normal development QA also requires just **10 install-owned packages**, not changing N001/N002/NeighborhoodManager snapshots. Its output must remain outside baseline input. It still is NOT a combined Text+Font+Runtime installer.
- `src/builder/test_stage_runtime_inputs.py`: **4** synthetic tests ensure install/save path isolation, two Wants paths, hash rejection.
- `src/builder/test_runtime_dbpf_writer.py`: **2** synthetic real-writer tests exercise both 20- and 24-byte DBPF indices, unchanged unrelated resource, other-language preservation, metadata/padding and idempotent application (and source English mismatch refusal).
- `src/builder/probe_story_selector.py`: **READ-ONLY** local script checks installed template vs live Documents N001/N002 CTSS selector title `(CTSS, 0xFFFFFFFF, 1, 0)`, with language/state/hash/source paths. Writes only `work/selector_probe.json`; does not edit/copy save files or prove actual process read precedence. `src/builder/test_probe_story_selector.py`: **3** synthetic tests PASS.
- CI Source Audit #442 **PASS**, with **9** tests in these three suites. Real binary input package QA and an in-game read-path check **NOT performed**. Read `runtime/README.md`, `runtime/SELECTOR_DIAGNOSIS.md`, and `runtime/RELEASE_READINESS_V08.md` for safely running the tools and release gates.

**Next priorities:** Verify actual ORIGINAL game-owned 10 package baselines (not previously patched install); run `check_runtime_packages.py` on staged copies, verify core Text baseline and compatible existing font, package a reversible combined installer; use selector probe against Ron's current actual save folder to decide whether a separate exact save-resource patch or install-template patch is appropriate. Do **not** publish v0.8 without real binary package QA; never distribute Ron's save packages. No originals mounted in the current source-only GitHub workflow; do not falsely claim full QA just because 9 synthetic tests passed.

---

> **Authoritative Castaway-only checkpoint — 2026-10-09, Source Audit #425 PASS**. **7,154** total mapping entries (**2,163** exact-row translations), **14,719** effective candidates, **0** candidate missing/review, **20,095** inherited unresolved, **1,349** automatic exclusions, **0** parse errors. [Run #425](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37833534628) at `8d57a401a`. Subsequent source tests include safe package-staging unit tests ([run #430](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37833999242) PASS). This supersedes older numbers elsewhere. **v0.8 TEST remains unreleased**: source-only QA is not binary writer QA or game execution; active story selector read path is still unknown.

## Immediate Castaway-only work order (supersedes inherited-memory sweeps)

**DO NOT continue broad The Sims 2 memory/expansion localization as the priority.** Explicit user instruction: finish **The Sims Castaway Stories** first. Read `runtime/CASTAWAY_ONLY_FOCUS_2026-10-09.md` and `runtime/RELEASE_READINESS_V08.md` BEFORE any new inherited review batches. Runtime release gates: real selector read path, fresh baseline package QA, reversible combined core/runtime/font TEST, player in-game validation.

Changes since Source Audit #414:
- `runtime/row_review_decisions_142.json`: 64 exact Nightlife/EP2 date-and-vampire inherited rows excluded.
- `runtime/row_translation_overrides_73.json`: 116 exact household/family memory rows translated (last base-memory batch before refocus).
- `runtime/row_scope_overrides_82.json`: **21** exact likely Castaway shared menu entries (18 `Sleep` from living chairs, three `Call To Meal...`), reusing approved menu translations.
- `runtime/translations/ui.json`: `Reward` standardized to `Phần thưởng`.
- `src/builder/trace_selector_sources.py`: Source Audit now enumerates exact selector-related resource origins, and checks translations in their OWN categories. **17 source candidates, all 17 already translated**: objects.package 2 story strings, N001 1 selector title, N002 14 selector/person/lot descriptions. N001/N002 audited copies came from Documents, not proven runtime installation. `NeighborhoodManager.package` is in inventory but not proven selector-text owner. **Do not fix by replacing whole saves.**
- `.github/workflows/source-audit.yml`: added targeted inherited-triage for reward, Examine/Use and survival strings. EP2/EP7/cheat and chapter-controller hits must be triaged by exact behavior, NOT bulk translated.
- `src/builder/stage_runtime_inputs.py`: source-safe local preflight compares 13 original package SHA-256s against the inventory, separates game installation vs Documents save sources, defaults to read-only and only copies after explicit `--copy-verified` when all hashes pass. It cannot build anything without the user's own actual file bytes. `src/builder/test_stage_runtime_inputs.py`: **three synthetic tests PASS** in CI #430; see `runtime/README.md` for usage. No original commercial files are committed and no current binary QA has been performed.

Next shard numbers if needed (check tree): `row_scope_overrides_83.json`, `row_translation_overrides_74.json`, `row_review_decisions_143.json`. Prioritize exact Castaway-active UI, crafters, rewards, catalog and menu ownership, and the selector + package builder; do not spend cycles classifying the residual inherited pool for its own sake. Source counts are **not an estimated release date**.

---

> **2026-10-09 new checkpoint (source audit run 416 PASS):** aggregate translation map entries **7,154**; exact-row translations **2,163**; effective candidate rows **14,698**; untranslated/review candidates **0**; unresolved inherited **20,116**; automatic exclusions **1,349**; parse errors **0**. Proven by GitHub Actions [run 416](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37829722509) at commit `743a5176019074fd1638de7a99e8181962c1badc` (subsequent commits include a text-polish correction and release-planning doc, awaiting their own CI confirmation). This supersedes previous numerical checkpoints below. **No v0.8 TEST release; selector runtime source and current-package QA remain unverified.**

## Continuation after run 414

Two verified exact-resource batches were added, with the same guard discipline: `runtime/row_review_decisions_142.json` excluded **64** clearly Nightlife (EP2) formal-date or vampire memory rows (16 CTSS resources); `runtime/row_translation_overrides_73.json` translated **116** exact base Sim-memory rows (29 CTSS resources), covering burglary, family/marriage, education, birthdays, romantic events and death-related moments. `runtime/RELEASE_READINESS_V08.md` now documents an explicit **risk-first TEST vs final-release gate**: judge likely player-facing text and runtime safety, not the raw number of inherited legacy rows. It preserves the hard selector, package-writer, installer and focused in-game requirements. The original 7,502-row structural package-QA snapshot is still stale by **7,196** compared to current 14,698 candidates. Never relabel source audit PASS as an in-game check.

Next shards: translation `row_translation_overrides_74.json`, review `row_review_decisions_143.json`, scope `row_scope_overrides_82.json` (inspect repo tree before creating). Prioritize high-confidence Castaway-owned interactions, catalog/reward/Wants and shared base gameplay rather than only accumulating optional base-Sims memories. Selector source/precedence and a reversible v0.8 package are the biggest release blockers. **No re-upload necessary for source-only triage.**

---

> **UPDATE 2026-10-09 — authoritative source checkpoint:** run **414 PASS**, commit **`92dbfaf6b5b3633e874ce4b0d401d2e4b3b2a97c`** or newer. **7,038 translation-map entries**, **2,047 exact-row translations**, **14,582 effective candidate rows**, **0 untranslated/review candidate rows**, **20,296 unresolved inherited rows**, **1,349 automatic exclusions**, **0 parse errors**. This update supersedes all previous counts in this handoff and older docs. Source Audit: https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37827502082. **v0.8 TEST is NOT released.** The story selector runtime source is not verified and package QA is stale at 7,502 rows (current verification gap **7,080**).

## Continuation after run 407 — verified run 414

The 2026-10-09 continuation made **400 exact inherited-row decisions** since run 407: **268 source-level exact translations** and **132 evidence-backed exclusions**. Unresolved inherited decreased **20,696 → 20,296** while all candidate translation gates remained clean.

- `runtime/row_translation_overrides_69.json`: 20 exact base Sim-memory CTSS rows (5 families): moving out, Logic maximum, death, refused engagement, embarrassment at party.
- `runtime/row_translation_overrides_70.json`: 100 exact CTSS rows (25 family/romance/skill/cooking/friendship/fight resources), including English/UK English variants.
- `runtime/row_review_decisions_141.json`: 132 exact inherited CTSS rows from 38 legacy resources excluded because they explicitly refer to Sims 2 University college/scholarships, Sims 2 werewolf/PlantSim transformations, or Seasons Garden Club. This is NOT a blanket exclusion of Castaway animal/garden rows.
- `runtime/row_translation_overrides_71.json`: 80 exact memory rows (20 resources): skill, grandchild, first kiss, promotion, fire, marriage, ghosts, toilet training, love, demotion and adoption. Gender-neutral first-person narration maintained, including a corrected original romance phrase.
- `runtime/row_translation_overrides_72.json`: 68 exact memory rows (17 resources): achievement, cheating, make-out, skills, engagement, infant development, fighting and dating rejection.
- `.github/workflows/source-audit.yml`: added `--include-unowned --object-contains "Memory -" --groups 280 --samples 8` to expose the inherited memory family queue reproducibly.

All exact rows carry original package, full DBPF key, row ordinal, language, English text and description; translated rows preserve $-tokens and original line-break controls. This is **source QA** only: full runtime player visibility and release-readiness have NOT been verified. Latest green Source Audit at run 414 confirms the source-coverage and parse gates.

### Next checkpoint instructions

Read this update FIRST, then the remainder of this handoff and `TRANSLATION_STYLE.md`/`BUILD.md`/`runtime/README.md`. Continue from commit `92dbfaf6b` or newer. Next shard numbers after inspection: **row_translation_overrides_73.json**, **row_review_decisions_142.json**, **row_scope_overrides_82.json**. Use latest source audit triage with --include-unowned, split mixed inherited families per exact row and evidence. Prioritize actual Castaway UI/catalog/interaction reachability and untouched base memory families; do not retranslate the newly handled groups. Do not promote all legacy catalog or expansion-specific objects. Keep the selector diagnosis and package QA as separate release gates. Do not distribute original game packages or Documents saves.

---

# Runtime handoff — 2026-10-09

This supersedes numeric checkpoints in `RUNTIME_HANDOFF_2026-10-08.md`, `NEXT_SESSION_PROMPT.md`, `CONTINUE_WITH_MODEL.md`, `RUNTIME_AUDIT.md`, `runtime/README.md` and the older generated JSON snapshots. The source-only repository is NOT a v0.8 release.

## Authoritative checkpoint
- GitHub commit: **`4c4d30efac9e4a606e2c4c709d44b1e3de308879`** (`4c4d30e`) or newer.
- Source Audit: **run 407**, **PASS** (commit `4c4d30e`).
- **6,770 translation-map entries** (source audit's aggregate count, including exact-row translations).
- **1,779 context-specific exact-row translations**.
- **14,314 effective candidate rows**.
- **0 untranslated/review candidate rows**.
- **20,696 unresolved inherited review rows**.
- **1,349 automatic inherited-row exclusions**.
- **0 parse errors**.
- Selector runtime source: **NOT VERIFIED**; v0.8 TEST: **NOT RELEASED**; in-game validation: **NOT COMPLETED**.

Source Audit link: https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37826382774

## Completed in the 2026-10-09 continuation

Starting from run 404 / commit `ef595a9` (6,634 mappings, 1,643 exact-row translations, 14,164 candidates, 20,846 unresolved inherited):
1. `runtime/row_translation_overrides_67.json` — **76 exact CTSS memory rows** (19 source groups): friendships, romance/rejection, runaway/return, birth, early development, bonus, burned food, moving in and rescue from death. Gender-neutral first-person Vietnamese and exact `$Subject` preservation.
2. `runtime/row_scope_overrides_81.json` — **14 exact TTAs rows** (7 owned modular-stair groups): only `Go Upstairs`/`Go Downstairs`, using approved `menu.json` translations. Mood `Walk...` variants remain unresolved.
3. `runtime/row_translation_overrides_68.json` — **60 exact CTSS memory rows** (15 source groups): losing best friend, bad growing up, learning to talk, inheritance, enemies, quitting job, retirement, three best friends, overachievement, marriage rejection and breakup.

Total **150 inherited rows** moved into candidate translations; run 407 source QA **PASS**, with 0 missing/review candidates and 0 parse errors. These exact translations are source-level coverage, **not proof of in-game reachability**.

## Continue with the broad inherited sweep
- Use `src/builder/triage_review_queue.py --include-unowned` and the latest Source Audit log (run 407), not an old handoff ranking.
- Split mixed resources by exact row and evidence. `row_scope_overrides_NN.json` reuses approved mapping; `row_translation_overrides_NN.json` provides unique context-dependent Vietnamese; `row_review_decisions_NN.json` makes evidence-backed retain/exclude choices.
- New next-shard numbers: scope **82** (scope 81 exists); translation **69** (68 exists); review **141** (140 exists). Always inspect the actual repo tree again before creating a shard.
- Do not blindly classify Castaway-relevant animal, family, social, career or food rows as expansion residue just because they inherit Sims 2 tags. Conversely do not mass-promote all base catalog, memory or expansion leftovers as proven runtime.
- Avoid redoing completed phone, mailbox, computer, emergency calls, fishing/food stock, bills, furniture/menu and earlier catalog sweeps. Refer to the existing 2026-10-08 handoff for completed families.
- Preserve all DBPF key, ordinal, language, English bytes, description metadata and placeholders (including `%s`, `%d`, `$Subject`, `$Object`, `$Local:n`). Narration is neutral `mình`; system UI stays clear, dialogue conversational.
- Repo remains **source-only**. Never commit original or patched commercial game packages or Documents save files.

## Release gates still open
1. **20,696 inherited rows still need review**; avoid claiming this is a full game sweep.
2. Selector `Shipwrecked and Single / Wanmami Island` game-process read path/precedence is **not verified**. N001/N002 supplied previously are Documents saves, not redistributable templates.
3. `runtime/package_qa.json` is stale: last structurally verified snapshot has **7,502 candidate rows**, versus **14,314 now** (difference **6,812**). Do not hand-edit provenance; rerun writer, round-trip, idempotence and unrelated-resource checks with the previously supplied baseline packages when accessible.
4. Consolidated v0.8 installer/font/runtime patch and focused actual in-game validation remain outstanding. No v0.8 TEST release is complete.

## Next-session instruction
Continue translating `RVTGMzz/TSCTW-VH` from `4c4d30e` or newer. Read this file first, then the older handoff, `TRANSLATION_STYLE.md`, `BUILD.md`, `runtime/README.md`, and latest Source Audit logs. Continue the **broad inherited exact-resource sweep**, keep verified metadata and every placeholder intact, commit new shards and verify CI. Do not request Ron to upload the already-supplied packages merely to proceed with source triage. Do not call v0.8 TEST finished.
