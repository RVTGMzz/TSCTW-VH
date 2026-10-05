# Story selector: source correction and remaining verification

Ron confirmed on 2026-10-05 that the already uploaded N001/N002 files came from the requested **Documents save location**. The earlier assumption that these were installation templates was wrong. Do not ask for these same files again.

See `input_provenance.json` for their exact SHA-256 and staged aliases. The `TSData/Res/UserData/...` paths in the extraction inventory are local staging aliases inherited from the earlier assumption; they are not evidence of the upload origin. These two files are active-save inputs and must never be shipped wholesale as installation templates or replacement saves.

The received files contain CTSS selector titles and descriptions. Their full resource keys and row positions are in `catalog.json.gz`, with translations in `translations/ui.json`. Ron's prior v0.7b test still showed English. Simply assuming a different Documents copy is no longer a sufficient explanation.

The actual game-process read path has not been observed. Continue investigating language fallback, alternate selector resources, package precedence and whether the earlier installed patch touched the same resources. The source confirmation is not an in-game fix verification.

Any eventual application to saves must alter only targeted text resources, keep full-key and original-row guards, create backups and preserve every unrelated resource byte. Never replace a neighborhood save with another complete package.
