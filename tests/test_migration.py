import unittest
from migration_rehearsal import plan
class Tests(unittest.TestCase):
    def test_add(self):
        r=plan([{"action":"add_column","table":"users","column":"age","type":"INTEGER"}])
        self.assertIn("ADD COLUMN",r["forward"][0])
    def test_rename(self):
        r=plan([{"action":"rename_column","table":"users","from":"old","to":"new"}])
        self.assertIn('"new" TO "old"',r["rollback"][0])
    def test_drop_warns(self):
        r=plan([{"action":"drop_column","table":"users","column":"old"}])
        self.assertEqual(len(r["warnings"]),1)
    def test_reject_identifier(self):
        with self.assertRaises(ValueError): plan([{"action":"drop_column","table":"bad table","column":"id"}])
    def test_reject_type(self):
        with self.assertRaises(ValueError): plan([{"action":"add_column","table":"users","column":"age","type":"UNKNOWN"}])
    def test_rollback_order(self):
        r=plan([{"action":"add_column","table":"users","column":"a","type":"TEXT"},{"action":"add_column","table":"users","column":"b","type":"TEXT"}])
        self.assertIn('"b"',r["rollback"][0])
if __name__=="__main__": unittest.main()
