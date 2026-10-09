"""Source-only regression: all historical row upgrades must still match the audit."""
import collections
import unittest

from safe_rebase_runtime import load_reviewed_legacy_migrations
from validate_runtime import RUNTIME, effective_records, load_maps, load_row_translations, row_identity


class ReviewedMigrationSourceTest(unittest.TestCase):
    def test_every_reviewed_upgrade_matches_real_source_metadata_and_current_approved_vi(self):
        rows,_=effective_records()
        groups=collections.defaultdict(list)
        for row in rows:
            groups[row["package"]].append(row)
        exact={row_identity(r):r for r in load_row_translations()}
        migrations=load_reviewed_legacy_migrations(RUNTIME,groups,load_maps(),exact)
        self.assertGreaterEqual(len(migrations),2)
        for identity,old in migrations.items():
            self.assertEqual(identity[0],old["package"])
            self.assertTrue(old["old_vi"])
            self.assertEqual(len(identity[1]),4)


if __name__=="__main__":
    unittest.main()
