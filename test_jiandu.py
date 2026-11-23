"""缄椟（JIANDU）算子骨架单测：名帖完整、桩位齐整、只增不覆盖。"""
import unittest

from jiandu import Jiandu


class TestJiandu(unittest.TestCase):
    def setUp(self):
        self.op = Jiandu()

    def test_describe(self):
        d = self.op.describe()
        self.assertEqual(d["repo"], "jiandu")
        self.assertEqual(d["code"], "JIANDU")
        self.assertTrue(d["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))
        self.assertTrue(d["mingwen"])

    def test_escrow_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.escrow(None)

    def test_release_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.release(None, None)


if __name__ == "__main__":
    unittest.main()
