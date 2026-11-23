"""缄椟（JIANDU）算子单测：名帖完整、行为达标、只增不覆盖。"""
import unittest

from jiandu import Jiandu


class TestJiandu(unittest.TestCase):
    def setUp(self):
        self.op = Jiandu(config={"auth": "令牌"})

    def test_describe(self):
        d = self.op.describe()
        self.assertEqual(d["repo"], "jiandu")
        self.assertEqual(d["code"], "JIANDU")
        self.assertTrue(d["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))
        self.assertTrue(d["mingwen"])

    def test_escrow_release(self):
        handle = self.op.escrow("keyref-001")
        with self.assertRaises(PermissionError):
            self.op.release(handle, None)
        self.assertEqual(self.op.release(handle, "令牌"), "keyref-001")
        with self.assertRaises(KeyError):
            self.op.release("JD-9999", "令牌")


if __name__ == "__main__":
    unittest.main()
