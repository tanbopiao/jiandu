"""缄椟（JIANDU）算子单测：名帖完整、三官行为达标、防篡改现形、回归重放。

命名映射：缄（封）→ escrow；启（取）→ release；察（验）→ inspect/ledger/seal/verify。
"""
import unittest

from jiandu import Jiandu


class TestMingtie(unittest.TestCase):
    """名帖：名、代号、职责、铭文、体系锚。"""

    def setUp(self):
        self.op = Jiandu(config={"auth": "令牌"})

    def test_describe_repo(self):
        self.assertEqual(self.op.describe()["repo"], "jiandu")

    def test_describe_code(self):
        self.assertEqual(self.op.describe()["code"], "JIANDU")

    def test_describe_anchor(self):
        self.assertTrue(self.op.describe()["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))

    def test_describe_mingwen(self):
        self.assertTrue(self.op.describe()["mingwen"])


class TestJianGuan(unittest.TestCase):
    """缄官：缄封锁固，托管给执据。"""

    def setUp(self):
        self.op = Jiandu(config={"auth": "令牌"})

    def test_escrow_returns_handle(self):
        handle = self.op.escrow("keyref-001")
        self.assertEqual(len(handle), 32)

    def test_escrow_handles_differ(self):
        h1 = self.op.escrow("keyref-001")
        h2 = self.op.escrow("keyref-002")
        self.assertNotEqual(h1, h2)

    def test_escrow_ledger_records(self):
        handle = self.op.escrow("keyref-001")
        self.assertEqual(self.op.ledger()[0]["event"], "escrow")
        self.assertEqual(self.op.ledger()[0]["handle"], handle)

    def test_escrow_no_secret_in_ledger(self):
        """凭据本体不入流水：流水里不得出现明文。"""
        self.op.escrow("机密甲乙丙")
        self.assertNotIn("机密甲乙丙", str(self.op.ledger()))


class TestQiGuan(unittest.TestCase):
    """启官：非时不启，凭授权取用。"""

    def setUp(self):
        self.op = Jiandu(config={"auth": "令牌"})
        self.handle = self.op.escrow("keyref-001")

    def test_release_without_auth(self):
        with self.assertRaises(PermissionError):
            self.op.release(self.handle, None)

    def test_release_wrong_auth(self):
        with self.assertRaises(PermissionError):
            self.op.release(self.handle, "错牌")

    def test_release_with_auth(self):
        self.assertEqual(self.op.release(self.handle, "令牌"), "keyref-001")

    def test_release_unknown_handle(self):
        with self.assertRaises(KeyError):
            self.op.release("JD-9999", "令牌")


class TestChaGuan(unittest.TestCase):
    """察官：对牌验封、流水防篡改。"""

    def setUp(self):
        self.op = Jiandu(config={"auth": "令牌"})

    def test_inspect_match(self):
        handle = self.op.escrow("keyref-001")
        self.assertTrue(self.op.inspect(handle, "keyref-001"))

    def test_inspect_mismatch(self):
        handle = self.op.escrow("keyref-001")
        self.assertFalse(self.op.inspect(handle, "keyref-002"))

    def test_inspect_unknown_handle(self):
        with self.assertRaises(KeyError):
            self.op.inspect("JD-9999", "keyref-001")

    def test_ledger_deep_copy(self):
        """流水外改不伤内账：深拷贝防篡改。"""
        self.op.escrow("keyref-001")
        snapshot = self.op.ledger()
        snapshot.append({"event": "伪造"})
        self.assertEqual(len(self.op.ledger()), 1)

    def test_seal_returns_digest(self):
        self.op.escrow("keyref-001")
        digest = self.op.seal()
        self.assertEqual(len(digest), 64)

    def test_verify_clean(self):
        self.op.escrow("keyref-001")
        self.op.seal()
        self.assertTrue(self.op.verify())

    def test_tamper_detected(self):
        """篡改现形：封存前缀内流水被改，验封即 False。"""
        self.op.escrow("keyref-001")
        self.op.seal()
        self.op.events[0]["event"] = "越权伪造"
        self.assertFalse(self.op.verify())

    def test_append_after_seal_not_tamper(self):
        """封存后新增长的合法条目不算篡改。"""
        self.op.escrow("keyref-001")
        self.op.seal()
        self.op.escrow("keyref-002")
        self.assertTrue(self.op.verify())

    def test_verify_with_expect(self):
        self.op.escrow("keyref-001")
        digest = self.op.seal()
        self.assertTrue(self.op.verify(expect=digest))
        self.assertFalse(self.op.verify(expect="0" * 64))


class TestRegression(unittest.TestCase):
    """回归重放：v1 骨架既有行为不回退。"""

    def test_v1_flow_replay(self):
        op = Jiandu(config={"auth": "令牌"})
        handle = op.escrow("keyref-001")
        with self.assertRaises(PermissionError):
            op.release(handle, None)
        self.assertEqual(op.release(handle, "令牌"), "keyref-001")
        with self.assertRaises(KeyError):
            op.release("JD-9999", "令牌")
        d = op.describe()
        self.assertEqual(d["repo"], "jiandu")
        self.assertEqual(d["code"], "JIANDU")


if __name__ == "__main__":
    unittest.main()
