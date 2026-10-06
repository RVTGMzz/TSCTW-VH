# Runtime inherited-triage checkpoint — 2026-10-07

Continue from source-work commit `2beb0102c8cbacf97745efb1f4392b6c3cff7897` or newer. Source Audit run 179 passed.

## Authoritative source totals

- 5,374 translation entries, including 640 context-specific exact-row translations
- 9,156 effective candidate rows
- 0 missing/review candidate rows
- 30,606 unresolved inherited review rows
- 1,349 automatic inherited-row exclusions
- 0 parse errors
- selector runtime source remains unverified
- package-writer QA remains stale at the older 7,502 verified-candidate snapshot
- no completed v0.8 TEST release and no new in-game completion claim

## Player-facing coverage added in this pass

Promoted or translated exact rows for:

- Castaway invisible-floor marker core actions: Get In / Teleport Here
- Global Time Control trunk story thoughts
- Pirate Ship wooden-stair catalog title/description
- Social Worker Dismiss / Fire
- base clothing Browse / Try On / Buy / Dress for Work
- shared plant Water / Stomp / Dispose / Go Here
- stereo Turn On/Off, Dance Solo, Ask to Join, and station-switch labels
- career-object lesson and global join actions, preserving $Object and $NameLocal:0 placeholders
- Ultra Clean
- shared Clean

Context-specific exact translations are in numbered `runtime/row_translation_overrides_08.json` through `row_translation_overrides_13.json`. Generic-map promotions continue through `runtime/row_scope_overrides_31.json`.

## Inherited residue classified in this pass

Exact review decisions now continue through `runtime/row_review_decisions_49.json`. Newly classified residue includes:

- EP6/EP7 fly/wolf/pee marker actions
- Open for Business retail controls
- Pets pet-store purchase dialogs
- duplicated destination expansion actions
- direct Castaway debug/test/helper objects
- death-state / Create Ghost / Mourn Debug menus
- Pet Debug rows
- clothing diagnostic dumps
- PlantSim / plantbaby messages
- HSN/debug labels
- snow and age-state residue
- a narrow set of unmistakable dog/cat/Pets-only interactions such as Check Collar, Cat Teaser, Try For Puppy/Kitten, pet work/walk
- internal Food Resource controller commands Snapfu / Make NPC / Schedule NPC / Fire NPC

Do not mass-exclude the remaining EP6 animal block. Generic animal interactions such as Play, Cuddle, Pick Up, Scold and Praise remain unresolved intentionally because Castaway has its own animal gameplay.

## Highest-value unresolved queue

Continue from the latest successful Source Audit logs rather than old handwritten notes. Important unresolved families include:

- ownerless Trim / Use collision; the known Use row must remain review-only without reliable ownership evidence
- large ownerless/global social blocks
- remaining generic pet/social interactions
- Pirate Ship Walk.../Normal/Happy/Mad/Sad/Run routing-style rows
- mixed pizza/outcome dialog resource
- Chapter 1 - Almost Paradise; keep traceable while selector runtime read-path is still unverified
- Interaction - Cuddle
- Get Paid / Take on CS - Controller - Food Resource

Split mixed instances by exact row evidence. Do not promote or exclude whole resources merely to reduce the queue.

## Release gates still open

1. inherited review queue is not complete
2. story-selector runtime source/read path is not verified
3. package-writer QA is stale against current source
4. focused in-game verification for the consolidated v0.8 build has not happened

Therefore do not label v0.8 complete or ask Ron to install a new build yet.
