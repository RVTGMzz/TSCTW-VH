# On-device read-only report triage — 2026-10-09

User supplied `Castaway-v08-bao-cao.txt` produced by Build 66's **Rà chữ còn sót** before any new confirmed live-game verification.

## Evidence and conclusions

- 20 package files read; 67 keyword hits; 0 files failed. This is a **keyword search**, NOT complete inventory of all untranslated gameplay text. Hits may be duplicated across groups/languages.
- A complete owner was discovered for previously unlocated neighborhood decorative trees: `TSData/Res/Catalog/CANHObjects/catcanhobjects.bundle.package`, STR# type `1398034979`, instance `123`, language 1:
  - group 2143531697, row 0: `Row of Trees` → proposed **Hàng cây**.
  - group 2142521860, 2140068512 and 2144203450, row 0: `Pine Tree` → proposed **Cây thông**.
  - This catalog bundle is **not confirmed to be in current installer write allowlist**. Add safely with original-byte backup/restore and a dedicated synthetic round-trip and unrelated-resource test before shipping.
- Exact untranslated longer chemistry/CAS help: `TSData/Res/Text/CAS.package`, STR# (1398034979, 4294967295, 141), row 51, language 2, `CAST UI COM`, begins `Please select your Sim's Turn-Ons and Turn-Off.`. Proposed complete translation preserving 2 paragraph breaks:
  `Hãy chọn những đặc điểm khiến Sim của bạn bị thu hút hoặc mất hứng. Nhấn vào từng ô phía trên để chọn một đặc điểm.\n\nSim của bạn sẽ dễ rung động trước những Sim có đặc điểm được chọn trong mục Thu hút. Ngược lại, Sim sẽ ít bị hấp dẫn bởi những đặc điểm trong mục Mất hứng.\n\nBạn có thể thay đổi các lựa chọn này về sau bằng phần thưởng Khát vọng Quả cầu ReNuYuSenso. Giờ thì đi tìm người hợp gu thôi!`
- Exact Gold Aspiration warning: `TSData/Res/Text/Live.package`, STR# (1398034979, 4294967295, 145), row 80, language 2: `Negative side effects may occur if used below Gold Aspiration. Consult your Aspiration Meter before use.` → proposed `Có thể xảy ra tác dụng phụ nếu dùng khi mức Khát vọng chưa đạt Vàng. Hãy kiểm tra thanh Khát vọng trước khi sử dụng.`
- Other English found: `objects.package` TTAs `Make Potion.../Elixir of Life` and `Drink Elixir of Life`, plus CTSS `Elixir of Life Potion` (Cast Catalog COM), `Elixir of Life` (Cast Catalog INC / inherited), `Conveniently Cozy Rock Couch` name+description. Some already have approved source translations; **seeing original-English resource rows in a pre-install read-only scan does not prove a Build 66 patch failed**. Trace by exact key, language and owner, and test installed bytes.
- `N002_Neighborhood.package` in **game installation** path `TSData/Res/UserData/Neighborhoods/N002/` has English descriptions of Candy, Linje, Murray/Barretts, Orson, Linea, Folons, lots/locations. These are NOT the same path as `Documents/Neighborhoods`. Before editing, verify actual game read precedence and save profile; respect separate save backup opt-in.
- A `UIText.package` location `(1398034979,4294967295,750)` row 0 was already in Vietnamese; the keyword merely matched `Wanmami`, not untranslated text.
- Apparent `ReNuYuSenso` strings of forms `a2o-reNuYuSenso-start` and `o2a-reNuYuSenso-getOut` are likely animation/internal IDs (no user-facing prose). Do **not** translate blindly.
- Credit hit `UIText.package`, instance 1, rows 267/268 is **application title in the Windows title bar**, not the graphical splash subtitle. **In-game `Việt hóa bởi Votri Valley` is still unimplemented.** Inspect the real splash/title UI layout or texture safely; do not overwrite EA credits or window title.
- This report neither proves real-game translation success nor authorizes patching all 67 hits.

## Implementer checklist

1. Add source-verified row/key-aware translations for CAS 141/51, Live 145/80. Preserve language-specific resource attributes, newline structure, untouched foreign languages and gameplay tokens.
2. Add scoped catalog-bundle reader/writer handling and safe one-click installer staging only when structural integrity/rollback tests pass; cover the full decorative-tree family, not image-only replacements.
3. Confirm currently approved aspiration/rock couch/menu translations actually apply at correct runtime keys after install; avoid overwriting unrelated existing Vietnamese patches.
4. Distinguish *installed* neighborhood path vs *Documents* save, determine selector read precedence, then patch approved neighborhood descriptions with separate safeguards.
5. Search actual title UI owner for `Việt hóa bởi Votri Valley`; do not call credit done until visually verified.
6. Validate source audit, packaged EXE smoke and actual Ron Windows gameplay; only then claim fixed.

**Provenance:** exact keys/text are transcribed from Ron's Build 66 exported read-only report. No commercial package bytes included.
