> **Build 29 (2026-10-09):** thêm nút **Lưu báo cáo...** để tự xuất log UTF-8 ra máy khi cài có lỗi (người dùng tự xem trước khi chia sẻ; không tự gửi qua mạng). Bấm **Cài** một lần nữa sau khi đã vá đủ những dòng nguồn xác nhận được sẽ được báo **không có gì cần bổ sung**, thay vì báo lỗi hoặc tạo backup mới. [Windows CI #29](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37861994690) đã PASS kiểm thử dữ liệu dịch và smoke-test EXE đóng gói. Các thay đổi vẫn chỉ được kiểm thử bằng package giả; chưa có kết quả Windows gameplay thật.

> **Build 23 replaces Build 17 after user-reported frozen installer FileNotFoundError**: `castaway-english-strings.json` was incorrectly read by `prepare_v08_test.build` even when running `runtime_only=True`. Fixed in `src/builder/prepare_v08_test.py`: core translation loader/target resolution/v0.6 history now execute ONLY in full Text mode. CI regression explicitly makes core loaders raise; `smoke_frozen_v08.py` creates fake DBPF package and performs build → dry-run → install → restore inside the *packaged Windows EXE* invoked via `--self-test`. [Windows Build 23 CI PASS](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37860653995). [Direct EXE download](https://github.com/RVTGMzz/TSCTW-VH/releases/download/castaway-v08-test-windows-29/VotriValley-Castaway-v08-TEST.exe). Failure on Build 17 happened BEFORE installation/backup, so user need not restore. For successful build 23 install, GUI Restore returns the previously installed state, INCLUDING prior Vietnamese modifications, not the vanilla English originals. Still needs real-game testing.

> **TẢI EXE CÀI BẰNG NHẤN ĐÚP — VOTRI VALLEY v0.8 TEST (2026-10-09).** [Tải trực tiếp **VotriValley-Castaway-v08-TEST.exe**](https://github.com/RVTGMzz/TSCTW-VH/releases/download/castaway-v08-test-windows-4/VotriValley-Castaway-v08-TEST.exe) ([GitHub prerelease](https://github.com/RVTGMzz/TSCTW-VH/releases/tag/castaway-v08-test-windows-4)). Được build thành công bằng GitHub Actions Windows [run #4](https://github.com/RVTGMzz/TSCTW-VH/actions/runs/37837500377), bước smoke-test **EXE đóng gói PASS**. Người dùng **KHÔNG cần cài Python hay công cụ phụ**. EXE có giao diện cài bằng một nút và nút khôi phục, tự tìm `G:/Castaway-Portable`, giữ Text/font v0.7a, không sửa Documents save, từ chối nếu 10 package runtime không khớp hash gốc. **VẪN LÀ TEST:** chưa chạy trên 10 package thật hoặc xác minh in-game, Story Selector vẫn cần xử lý. Mã nguồn GUI: `src/builder/win_v08_installer.py`; workflow: `.github/workflows/v08-windows-installer.yml`; hướng dẫn: `CLICK_TO_INSTALL_WINDOWS.md`. Từ đây ưu tiên thu thập lỗi thực tế/kiểm thử game, không dịch rộng The Sims 2.

> **2026-10-09 v0.8 runnable local candidate:** Start at [V08_LOCAL_TEST_GUIDE.md](V08_LOCAL_TEST_GUIDE.md) and [RUNTIME_HANDOFF_2026-10-09.md](RUNTIME_HANDOFF_2026-10-09.md). `src/builder/prepare_v08_test.py --runtime-only` creates a guarded runtime overlay for Ron's working v0.7a Text/font from **10 exact original runtime packages**; `src/builder/install_v08_local.py` defaults to DRY RUN, enforces original/patched SHA-256 guards, backs up and restores safely. Full core+runtime mode requires eight ORIGINAL English Text packages and explicit confirmation; pretranslated originals are rejected by a v0.6 resource fingerprint guard. Synthetic CI #454 PASS; no user game packages were used, so **NO real v0.8 TEST package released or tested in game**. Prioritize trying the local build and Story Selector read path, not bulk The Sims 2 inherited strings.

> **CASTAWAY-ONLY PRIORITY 2026-10-09:** Ron explicitly requested finishing **The Sims Castaway Stories**, not separately translating The Sims 2 Legacy Collection. Start with [`RUNTIME_HANDOFF_2026-10-09.md`](RUNTIME_HANDOFF_2026-10-09.md), then [`runtime/CASTAWAY_ONLY_FOCUS_2026-10-09.md`](runtime/CASTAWAY_ONLY_FOCUS_2026-10-09.md). Latest verified Source Audit **#425 PASS**: **14,719 candidate rows**, **0 candidate missing/review**, **20,095 inherited unresolved**, **0 parse errors**; old counts below are historical. Story-selector source titles and associated rows are ALREADY translated (17/17 exact candidate matches), but runtime file precedence has not been verified. Re-stage original game packages via strict SHA-256 preflight, verify combined core/runtime package patches, test menu/item/rewards/selector; **v0.8 TEST NOT released**. Avoid broad optional Sims 2 memory sweeps.

> **Latest (2026-10-09):** read [`RUNTIME_HANDOFF_2026-10-09.md`](RUNTIME_HANDOFF_2026-10-09.md) first. Authoritative Source Audit **run 414 PASS** at **`92dbfaf6b`**: **7,038 aggregate mapping entries, 2,047 exact-row translations, 14,582 candidate rows, 0 missing/review candidates, 20,296 inherited rows unresolved, 1,349 auto exclusions, 0 parse errors**. The 2026-10-09 continuation handled 268 translations + 132 exact exclusions. Package QA remains stale (7,502 candidate rows structurally verified), selector runtime path unverified, no v0.8 TEST release. Numerical counts below this banner are historical.

> **Current handoff (2026-10-09):** read [`RUNTIME_HANDOFF_2026-10-09.md`](RUNTIME_HANDOFF_2026-10-09.md) FIRST. Source Audit **run 407 PASS**, commit **`4c4d30e`**, **6,770 map entries / 1,779 exact-row translations / 14,314 candidate rows / 0 missing or review candidates / 20,696 unresolved inherited rows / 1,349 auto-exclusions / 0 parse errors**. Older numeric values below are historical. v0.8 TEST is **NOT RELEASED**, selector runtime source is unverified, package QA remains stale at 7,502 structurally verified rows.

> **Newest handoff (2026-10-08):** read `RUNTIME_HANDOFF_2026-10-08.md` FIRST. It supersedes all older numerical checkpoints below. Latest verified source checkpoint: `ad9adc7`; Source Audit run 351 PASS with **6,294 translation entries / 1,339 exact-row translations, 13,685 candidates, 0 missing/review candidates, 22,322 unresolved inherited rows, 1,349 auto-exclusions, 0 parse errors**. Package QA is stale at 7,502 verified candidates (gap 6,183); selector runtime source is still unverified; no completed v0.8 TEST release exists.

# Prompt mở phiên tiếp theo

Copy/paste nguyên khối dưới đây vào chat mới:

---

Tiếp tục dự án Việt hóa **The Sims Castaway Stories PC** trong repo:
https://github.com/RVTGMzz/TSCTW-VH

Hãy dùng GitHub connector đúng repo `RVTGMzz/TSCTW-VH`, đọc kỹ theo thứ tự:
1. `RUNTIME_HANDOFF_2026-10-08.md`
2. `NEXT_SESSION_PROMPT.md`
3. `CONTINUE_WITH_MODEL.md`
4. `RUNTIME_AUDIT.md`
5. `TRANSLATION_STYLE.md`
6. `BUILD.md`
7. `runtime/README.md`
8. Source Audit mới nhất

Tiếp tục từ checkpoint source `ad9adc7` hoặc mới hơn. Source Audit hiện tại: **6,294 translation entries, 1,339 exact-row translations, 13,685 candidate rows, 0 missing/review candidate, 22,322 inherited unresolved, 1,349 auto-exclusions, 0 parse error**.

Mục tiêu đợt này KHÔNG phải vá từng câu tôi chụp. Tôi muốn làm một **runtime sweep toàn diện** cho mọi text người chơi thật sự nhìn thấy trong Castaway: pie menu/interaction, tên+mô tả item, Story/Career/Aspiration rewards, Wants/Goals/hints, story/neighborhood metadata, gameplay popup/UI/tutorial và story/dialog runtime.

Quan trọng:
- Không dịch mù mọi English trong `objects.package` vì có rất nhiều debug/internal/expansion rác.
- Phải phân loại player-facing theo resource/context rồi dịch theo cụm.
- `objects.package` dùng DBPF index entry 24 byte; TTAs = 0x54544173, CTSS = 0x43545353, STR# = 0x53545223.
- Ron đã test v0.7/v0.7a/v0.7b trong game và vẫn còn English. Đọc `RUNTIME_AUDIT.md` để biết các string/resource đã locate.
- Story selector `Shipwrecked and Single / Wanmami Island` đã patch thử trong N001/N002 nhưng runtime vẫn hiện English, nên phải tìm nguồn game thật sự đang đọc.
- Đừng báo "đã sweep hết" nếu chưa có audit/source file tái lập được và commit lên repo.
- Khi sửa batch/source cũ phải merge/superset, không replace mù.
- Giữ placeholder/token/line break/metadata; narration dùng "mình" trung tính giới tính; thoại tự nhiên, Gen Z vừa phải; UI/hint rõ ngắn.
- Repo source-only: không commit package game gốc hoặc payload đã patch.

Nếu cần package để scan/build, nói chính xác file nào tôi phải upload. Tôi đã có sẵn các package runtime từng dùng: `objects.package`, Text `Wants.package`, `Goals.package`, Wants subsystem, `Behavior.package`, `ObjectScripts.package`, `EPText.package`, `N001_Neighborhood.package`, `N002_Neighborhood.package` và 7 Text package v0.7.

Ưu tiên của tôi: **dịch thật sự toàn bộ phần cần Việt hóa, đừng đợi tôi chụp gì rồi chỉ sửa cái đó**. Sau khi sweep + QA xong, hãy build một **bản tổng hợp v0.8 TEST** để tôi cài một lần và test tiếp.

---



## Checkpoint bổ sung 2026-10-05

Sau khi đọc các tài liệu trên, đọc `runtime/README.md`, `runtime/coverage.json`, `runtime/package_qa.json` và `runtime/SELECTOR_DIAGNOSIS.md`. Tiếp tục từ `runtime/remaining.json.gz` và queue chưa phân loại `runtime/review_queue.json.gz`. Đã có bản dịch runtime theo nhóm, không làm lại hoặc thay thế mù. Đây vẫn là checkpoint chưa hoàn thành; chưa có bản tổng hợp v0.8 TEST. Không lấy số câu đã dịch làm bằng chứng toàn game đã hết English.

### Correction — uploaded save origin (2026-10-05)

Ron confirmed the supplied N001/N002 packages are from Documents saves. Earlier template-origin assumptions are superseded. See `runtime/input_provenance.json` and `runtime/SELECTOR_DIAGNOSIS.md`. Do not request the same files again and do not ship them wholesale as installation templates.

### Runtime translation checkpoint — 2026-10-05 (continued)

Catalog maps now contain 904 entries (899 translated, five intentional unchanged names); six excluded and two review values remain in the tagged catalog audit. Story/career maps contain 974 of 1,544 selected unique values, including adult/junior/pet career descriptions, main plot, and female dialogue variants. Total runtime mapping entries: 3,675. Full scope is still incomplete: 570 story values and the untagged review queue remain; selector runtime source is unverified. See current coverage and package QA, including source hashes. No v0.8 TEST archive has been released. Supplied Documents saves must never be distributed wholesale.

### Latest checkpoint — complete selected story set + inherited menu expansion

Supersedes the preceding numerical checkpoint: runtime maps now contain 4,339 entries. All 1,544 selected story/career values have Vietnamese mappings, including chance-card choices/results and male/female variants. Menu coverage is 923 unique translated values after 510 exact inherited rows (167 labels) were promoted with OBJD ownership evidence; 93 new translations were added, and chess “Cheat” was resolved as “Chơi gian”. Catalog remains 899 translated + five retained map entries.

Source QA passes, but the full sweep remains INCOMPLETE: 17 candidate rows and 38,556 inherited rows remain under review. Continue with `runtime/row_scope_overrides.json`, `runtime/review_context.json.gz`, its summary, and remaining candidate snapshot. Run extraction to completion before generating dependent reports. Selector read-path verification and the consolidated safe installer are still outstanding. No v0.8 TEST archive exists.

### Candidate triage follow-up — 2026-10-05

The prior checkpoint's 17 candidate rows have now all been resolved by exact source context. Candidate coverage reports 0 untranslated/review rows across 7,178 rows: catalog 900 translated / 7 excluded / 5 retained; menu 923 translated / 6 excluded. `Basket Ghost` is translated as `Giỏ ma`; remaining entries were identified as developer placeholders, legacy action, developer age action, expansion potion, marker object or blank description and explicitly excluded in `scope_decisions.json`. This does not resolve the separate 38,556 inherited review rows. The selector runtime source remains unverified, and v0.8 TEST is not built. Ron has no new upload request at this stage; when a consolidated test package is ready, the remaining user step will be one install and focused in-game verification.

### Audit filter correction — 2026-10-05

A reproducible audit bug had treated descriptions containing `! Don't translate.` as inherited review instead of explicit exclusions because the filter only matched `Do not translate`. The filter now recognizes both wordings. Re-running source audit and context extraction reduced the inherited queue from 38,556 to 38,009 rows; the 547 removed rows have explicit non-translation metadata. Candidate coverage remains 0 missing/review rows, with zero package parse errors. User action: none yet; no package needs re-upload. When the consolidated v0.8 test package is ready, Ron's requested step is one installation followed by focused game verification.


### Fire-pit menu batch — 2026-10-05

Added nine player-facing cooking menu translations across 18 exact resource rows for Castaway Outdoor Fire Pit / Fire Pit Survival; source is guarded and reproducible. Menu mappings: 932. Candidate rows: 7,196 with zero missing/review. Untagged inherited review queue: 37,991 rows; selector source remains unverified. Package parser/source checks and disposable package QA pass, but no v0.8 TEST archive exists and in-game testing remains Ron's task. Continue the broad sweep by reviewing evidence-backed player-facing resource families; do not claim completion or ask for the already supplied packages again.


### Latest sweep update — fire-pit menus and catalog (2026-10-05)

Since the previous checkpoint, nine fire-pit cooking menu strings (18 exact TTAs rows) and three missing catalog strings (six exact CTSS rows) were added. Existing translation entries were preserved. Current selected coverage: 7,202 rows, zero missing/review; menu 932 translations; catalog 903 translations + 7 excluded + 5 retained; 4,352 mapping entries. The inherited review queue is 37,985 rows and remains unresolved in broad scope. Package QA is rerunning; no v0.8 TEST has been built, selector source remains unverified, and in-game QA remains untested. Continue the evidence-based sweep without requesting previously supplied files again.


### Latest runtime sweep checkpoint — 2026-10-05

Added three evidence-backed batches beyond the earlier menu/catalog checkpoint: 220 exact visitor-departure dialog rows across Castaway portals; 20 beach-combing/bird/fight popups; 30 dialog and 8 menu rows for Orangutan interactions and other object-specific notices; 22 bird-cage interactions. Current source totals: 4,391 map entries; 938 menu, 35 dialog and 903 catalog values; 834 exact inherited row guards; 7,502 selected candidate rows with zero missing/review; 37,685 inherited rows unresolved; zero package parse errors. Overall runtime completion is not claimed. In-game status remains untested, selector runtime source remains unverified, and no v0.8 TEST archive exists. Continue from updated `runtime/coverage.json`, `runtime/row_scope_overrides.json`, `runtime/translations/`, and `runtime/review_context_summary.json`.


Package QA for the latest 7,502-row candidate snapshot passed structural round-trip, idempotence and unrelated-resource preservation checks. `runtime/coverage.json` intentionally remains `incomplete`: 37,685 inherited rows are unresolved, and selector runtime source/in-game verification remain outstanding.


## Current handoff checkpoint — 2026-10-06

Trust Source Audit over older totals in this file: 4,491 mappings, 7,850 candidate rows, 0 missing/review candidate rows, 37,337 inherited review rows, 0 parse errors. Exact row guards total 1,182 (802 menu, 293 dialog, 77 catalog, 9 story, 1 tutorial) and may now be split across `runtime/row_scope_overrides*.json`. Latest reviewed batches already cover Castaway toy/chair/diary/clothing/easel interactions plus House of Tuzu leaving-neighbor dialogs and Grand Piano Join/Dance. Do not blindly promote developer/debug rows just because the object name starts with `CS -`.

Package-writer QA is stale at 7,502 verified candidates versus 7,850 current and must be rerun against the user-owned baseline packages before any release claim. Story-selector runtime source is still unverified. No v0.8 TEST and no new in-game validation have been completed.


## Current handoff checkpoint — 2026-10-06 inherited classification + tutorial

Trust Source Audit over all older totals: **4,519 translation mappings, 7,894 effective candidate rows, zero missing/review candidate rows, 36,804 inherited review rows, zero parse errors**. Menu has 990 translated values, catalog 953, dialog 37 and tutorial 142.

Exact translation guards total 1,226 rows (816 menu, 297 dialog, 87 catalog, 9 story, 17 tutorial). Exact inherited classification decisions total 489 rows and are stored in `runtime/row_review_decisions*.json`; never replace these with a broad “CS means visible/unused” heuristic. Recent work recovered 16 `Cast Old FIN` Tutorial Controller strings and classified their opaque IDs/helpers separately. Large mixed groups such as `CS - Not Allowed on Floor - Invisible Marker`, Jaguar/Pets templates and duplicated food-stand `Cup O' Ramen` rows remain deliberately unresolved because they mix plausible gameplay with expansion/stale data.

Package-writer QA is stale: 7,502 verified candidates versus 7,894 current. Rerun against the user-owned baseline packages before any release claim. Selector runtime source remains unverified; no v0.8 TEST or new in-game verification exists yet.


## Current handoff checkpoint — 2026-10-06 exact-row translations

Trust Source Audit over older totals: **4,525 translation entries (4,519 ordinary map entries + 6 exact-row translations), 7,900 effective candidate rows, 0 missing/review candidate rows, 36,798 inherited review rows, 0 parse errors**. Catalog has 955 translated source values, menu 990, dialog 37 and tutorial 142.

Use the three exact systems correctly:
- `row_scope_overrides*.json`: promote an inherited row that can reuse a normal category English→Vietnamese map.
- `row_translation_overrides*.json`: promote + translate a specific row when duplicated/stale English must resolve differently by object context.
- `row_review_decisions*.json`: exact exclude/retain after evidence review.

The food stands Mahi-Mahi, Tropical Ribs and Pineapple Surprise are already fixed with six context-specific row translations; do not reintroduce a global `Cup O' Ramen` mapping. Generic exact translation guards total 1,226 and exact inherited review decisions total 489. Package QA remains stale: 7,502 verified candidates versus 7,900 current. Selector runtime source remains unverified; no v0.8 TEST or new in-game verification exists yet.


## 2026-10-07 session handoff

Source-work checkpoint before this documentation sync is commit `942c0d362ac9abc5a68651e7820391de539cefaa` (Source Audit PASS). Trust current Source Audit over all older handwritten totals:

- **5,325 translation entries**, including **591 context-specific exact-row translations**
- **9,085 effective candidate rows**
- **0 missing/review candidate rows**
- **30,862 unresolved inherited review rows**
- **1,349 automatic inherited-row exclusions**
- **0 parse errors**
- category highlights: menu **1,206**, dialog **186**, catalog **955**, tutorial **150**, story **1,552**, object **35**, UI **235**, wants **518**
- selector runtime source still unverified
- package QA still stale at **7,502 verified vs 9,085 current** (gap **1,583**)
- no completed v0.8 TEST release and no new in-game completion claim

The runtime architecture now has four complementary layers. `row_scope_overrides*.json` promotes exact inherited rows that can reuse ordinary category maps. `row_translation_overrides*.json` carries context-specific Vietnamese replacements for exact rows when one inherited English value is ambiguous/stale by object context. `row_review_decisions*.json` records exact manual exclude/retain decisions. Finally, `auto_review_decision()` in `validate_runtime.py` automatically excludes evidence-backed families only when no explicit exact decision overrides them: leading-`*` hidden/helper interactions, metadata marked deleted/not needed/not used/unused, `DEBUG`/`DBG`-prefixed values, and opaque IDs matching eight-hex/`bebe...`/`ecdb...` forms. Accepted exact promotions currently contain zero leading-star, deleted-metadata, opaque-ID or DEBUG/DBG rows; do not weaken these rules without a proven runtime exception.

Large completed sweeps after the older handoff include Castaway phone services/adoption/nanny + House/Birthday/Wedding/Anniversary party flow, human aging/birthday notifications, illness/pregnancy runtime text, household move/inheritance flow, global social interactions, tutorial-controller retained text, story-controller template classification, Pets social/age/disease controller review, hidden-star/deleted/opaque/debug auto-classification, and explicit expansion-only global social residue. Do not redo these families from scratch.

For the next inherited pass, start from the latest Source Audit queue rather than old notes. Highest unresolved families currently include: remaining `CS - Not Allowed on Floor - Invisible Marker` rows such as Teleport/Get In/Catch Flies/Chase Flies/Watch/Play In/Eat/Pee On; ownerless/global social blocks with generic pet/social interactions; stereo/music and lesson menus; retail clothing/browse blocks; plant/garden interactions; pet-purchase dialogs; and a number of low-score controller/test objects. Mixed families must be split by exact evidence. Do not mass-promote because a resource has `CS -` in its owner name, and do not mass-exclude base-game-looking rows when Castaway Free Play demonstrably retains that system.

Physical compressed snapshots still predate most exact work: they represent **7,516 candidates**. Effective math is reconciled as 37,671 review-context rows minus 1,569 pending promotions minus 3,891 manual exact review decisions minus 1,349 automatic exclusions = **30,862 unresolved inherited rows**. Source-only validation is authoritative until the next full extraction/package QA.

### Paste-ready continuation instruction

Continue the Vietnamese localization of The Sims Castaway Stories in `RVTGMzz/TSCTW-VH`. Read `CONTINUE_WITH_MODEL.md`, `NEXT_SESSION_PROMPT.md`, `RUNTIME_AUDIT.md`, `runtime/README.md` and the current Source Audit workflow/logs. Start from source checkpoint `942c0d3` or newer. Current authoritative Source Audit is 5,325 translation entries (591 exact-row), 9,085 candidates, 0 missing/review candidates, 30,862 inherited review rows, 1,349 auto-exclusions and 0 parse errors. Continue the inherited sweep broadly, not screenshot-by-screenshot. Preserve placeholders and context/gender; dialogue may be lively natural Vietnamese, while UI/system text stays clear. Respect the four-layer exact system (scope overrides, exact-row translations, manual review decisions, evidence-backed auto exclusions). Do not redo completed phone/party, aging, illness/pregnancy, move/inheritance, global-social, tutorial/story-controller, Pets-controller or auto-classification sweeps. Prioritize remaining mixed player-facing families from the latest queue and split them by exact resource evidence. Package QA is stale at 7,502 vs 9,085 current; selector source and v0.8/in-game verification remain outstanding. Do not ask Ron to re-upload old packages just to continue source triage.
