# Runtime sweep — v0.8 work in progress

This is a reproducible **partial translation checkpoint**, not a release or a claim that the game is fully localized. See `coverage.json` for exact counts and the remaining work. No v0.8 TEST payload has been released from this checkpoint.

## Source and scope

- `inventory.json`: staged package paths, SHA-256, resource/index counts, parse results and explicitly preserved legacy technical tables.
- `catalog.json.gz`: English candidate rows, including exact package, full DBPF key, row ordinal, language, metadata and selection reason.
- `review_queue.json.gz`: untagged/legacy text whose player visibility is unresolved. It is **not** treated as translated or safe to discard.
- `translations/*.json`: exact source-to-Vietnamese maps by category. New runtime maps supplement existing `translations/extra*.json`; the original v0.6 history and v0.7 sources are unchanged.
- `scope_decisions.json`: explicit decisions to retain proper names, exclude diagnostic dumps/asset identifiers, or defer suspicious menu entries for review.
- `remaining.json.gz`: unresolved candidate rows, generated from the maps and decisions.
- `coverage.json`: source QA and coverage; source validation passing does not mean coverage is complete or the game has been tested.

Gzip files contain UTF-8 JSON using escaped characters to preserve invalid legacy bytes losslessly. Decompress with Python's `gzip` module. The gzip timestamp is fixed to zero for reproducible artifacts.

## Uploaded neighborhood provenance

Ron confirmed the supplied N001/N002 files came from Documents saves. See `input_provenance.json`. Their paths under `TSData/Res/UserData` in this audit are staging aliases, not their real origin. Never package these whole saves as installation-template replacements. No re-upload is needed.

## Reproduce

Use Python 3.11+ and stage the packages at the exact paths listed in `inventory.json` under `work/input/`. The duplicated uploads are **Text/Wants.package** (4,486,248 bytes) and **Wants/Wants.package** (633,090 bytes); do not interchange them.

```sh
python src/builder/audit_runtime.py --input work/input --output runtime
python src/builder/validate_runtime.py --write
python src/builder/check_runtime_packages.py
```

The auditor writes human-readable local JSON as well as the committed gzip snapshots. Source-only QA needs no game packages:

```sh
python src/builder/validate_runtime.py
python src/builder/build_v07.py --audit-only
```

`validate_runtime.py --require-complete` intentionally fails while unresolved work remains. Do not remove this gate to label a partial sweep complete.

`check_runtime_packages.py` creates **development QA output only**, outside the baseline inputs. It checks input hashes, exact row/metadata identity, full chained placeholders, control-character sequence, compression round trips, table padding, 20/24-byte indices, DIR sizes, preservation of unrelated resources and byte-identical results on a second application. It does not combine core Text patches, fonts or an installer and is not a v0.8 release builder.

## Outstanding

1. Translate remaining catalog and story/career/dialog rows; reconcile item labels across hints, menus and catalog.
2. Review inherited/untagged resources with object and behavior context. Cast metadata is a useful seed, not proof of runtime reachability. Default exclusions outside confirmed scope are heuristic, not a claim that all untagged STR# text is internal.
3. Verify the selector's actual runtime source. See `SELECTOR_DIAGNOSIS.md`. Do not overwrite a user's active neighborhood save with an installation template.
4. Build one consolidated v0.8 TEST only after source coverage, scope review, package QA and font/installer QA. In-game testing remains Ron's verification; do not claim it has happened here.

## Reviewed inherited interactions

`row_scope_overrides.json` promotes 510 exact rows (167 unique interaction labels) from the inherited review queue into menu scope. Each row is guarded by full DBPF key, row ordinal, language, original value and original description. Object names from same-group OBJD resources document the evidence. The audit rejects duplicate, stale or unused overrides. This is a curated list of functional interaction labels on Castaway objects, not a rule that every CS or EP string must be translated.

Run `python src/builder/review_runtime_context.py` after completing extraction to attach same-group object names and Cast text ownership to the remaining queue. `review_context.json.gz` and its summary are evidence for further review; they do not claim runtime reachability and do not silently remove rows from coverage. Do not run dependent validation while extraction is still writing its snapshots.

Current source includes all 1,544 selected unique story/career values, 923 translated menu values and 899 translated catalog values. There are still 17 candidate rows under review and 38,556 inherited rows awaiting classification. Story-selector runtime source remains unverified. No consolidated v0.8 TEST release has been produced.
