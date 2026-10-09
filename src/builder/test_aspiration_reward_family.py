"""Regression: screenshot-verified Elixir aspiration reward family.

No EA package bytes are loaded: checks exact recorded resource ownership,
approved Vietnamese mapping, and source-audited package/row metadata.
"""
import unittest

from validate_runtime import effective_records, load_maps

PACKAGE = "TSData/Res/Objects/objects.package"
GROUP = 2140014299
CTSS = (1129599827, GROUP, 2000, 0)
TTAS = (1414807923, GROUP, 1, 0)
DIALOG = (1398034979, GROUP, 301, 0)


class ElixirRewardFamilyTests(unittest.TestCase):
    def test_visible_reward_name_description_and_drink_interaction_owned_together(self):
        rows, _ = effective_records()
        by_id = {(r["package"], tuple(r["key"]), r["row"]): r
                 for r in rows if r["package"] == PACKAGE
                 and len(r["key"]) == 4 and r["key"][1] == GROUP}
        translations = load_maps()
        expected = (
            (CTSS, 0, "catalog", "Elixir of Life"),
            (CTSS, 1, "catalog", "Perfect for those who like their idle water-cooler chats"),
            (TTAS, 0, "menu", "Drink Elixir of Life"),
        )
        for key, ordinal, category, english_prefix in expected:
            row = by_id[(PACKAGE, key, ordinal)]
            self.assertEqual(row["category"], category)
            self.assertEqual(row["language"], 1)
            self.assertTrue(row["en"].startswith(english_prefix))
            self.assertIn(row["en"], translations[category])
            self.assertTrue(translations[category][row["en"]].strip())

    def test_success_and_failure_dialogs_share_same_reward_owner(self):
        rows, _ = effective_records()
        approved = load_maps()["dialog"]
        expected = {
            0: "I feel rejuvenated!  I believe I've added valuable days to my life!",
            1: "It feels like the end may be closer than I thought.  Valuable days",
            4: "I feel rejuvenated!  I believe I've added valuable days to my life!",
            5: "It feels like the end may be closer than I thought.  Valuable days",
        }
        known = {(r["row"]):r for r in rows if r["package"] == PACKAGE
                 and tuple(r["key"]) == DIALOG}
        for ordinal, prefix in expected.items():
            row = known[ordinal]
            self.assertEqual(row["category"], "dialog")
            self.assertTrue(row["en"].startswith(prefix))
            self.assertIn(row["en"], approved)
            self.assertTrue(approved[row["en"]].strip())


if __name__ == "__main__":
    unittest.main()
