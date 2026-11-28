"""缄椟（JIANDU）· 密钥机密托管

道统出处：元极恒一·道统构件定名册 V2 ｜ 第五批
体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002

工程映射：密钥机密托管。

命名映射：缄（封）→ escrow 托管给执据；启（取）→ release 凭授权开封；
察（验）→ inspect 对牌验封不启椟，ledger 只增不覆盖，seal/verify 快照哈希防篡改。

边界：本件为算子 v0.1——三官齐备；遵循元法第四条「只增不覆盖」，
方法只增不改名不删，行为变更走新版本；凭据本体不入档不入日志，宣称与事实分离。
纯标准库，Python 3.10+。
"""

import copy
import hashlib
import json


class Jiandu:
    """缄椟（JIANDU）算子 v0.1：缄官封、启官取、察官验。"""

    ANCHOR = "Ω₀⊂⊙∞⊂Ω｜DID-BR-000002"
    CODE = "JIANDU"

    def __init__(self, config=None):
        self.config = dict(config or {})
        self.events = []  # 只增不覆盖：启闭流水，会话内留痕
        self.vault = {}   # 执据 → 托管件（凭据本体仅会话内存，不入档）
        self._seq = 0
        self._snapshots = []  # 已封存的流水快照哈希

    # ---------- 名帖 ----------

    def describe(self):
        """构件名帖：名、代号、职责、铭文、体系锚。"""
        return {
            "repo": "jiandu",
            "cn": "缄椟",
            "code": self.CODE,
            "duty": "密钥机密托管",
            "mingwen": "缄封锁固，非时不启",
            "anchor": self.ANCHOR,
        }

    # ---------- 缄官：缄封锁固 ----------

    def escrow(self, key_ref):
        """缄封锁固：机密托管，返回执据（凭据本体不入档不入流水）。"""
        self._seq += 1
        handle = hashlib.sha256(
            ("%d|%s" % (self._seq, key_ref)).encode("utf-8")).hexdigest()[:32]
        self.vault[handle] = {
            "ref": str(key_ref),
            "fingerprint": self._fingerprint(key_ref),
        }
        self.events.append({"event": "escrow", "handle": handle,
                            "fingerprint": self.vault[handle]["fingerprint"]})
        return handle

    # ---------- 启官：非时不启 ----------

    def release(self, handle, auth):
        """非时不启：凭授权取用托管件；无据或授权不备，椟不开封。"""
        if handle not in self.vault:
            raise KeyError("无此执据： %s" % handle)
        if not auth or auth != self.config.get("auth"):
            raise PermissionError("授权不备，椟不开封")
        self.events.append({"event": "release", "handle": handle})
        return self.vault[handle]["ref"]

    # ---------- 察官：对牌验封 ----------

    def inspect(self, handle, claimed):
        """对牌验封：比对指纹核真伪，不返回托管件本体。"""
        if handle not in self.vault:
            raise KeyError("无此执据： %s" % handle)
        return self.vault[handle]["fingerprint"] == self._fingerprint(claimed)

    def ledger(self):
        """启闭流水：只增不覆盖，返回深拷贝防外改。"""
        return copy.deepcopy(self.events)

    def seal(self):
        """封流水：对当前流水取前缀快照哈希存证（封存动作本身不入流水），返回哈希值。"""
        digest = self._ledger_hash()
        self._snapshots.append((len(self.events), digest))
        return digest

    def verify(self, expect=None):
        """验封：重算哈希与最近封存比对；前缀内篡改现形返回 False，
        封存之后新增长的合法条目不算篡改。expect 给定时按全量哈希比对。"""
        if expect is not None:
            return self._ledger_hash() == expect
        if not self._snapshots:
            return True  # 尚无封存，无可篡之征
        n, digest = self._snapshots[-1]
        return self._hash_prefix(n) == digest

    # ---------- 内部 ----------

    @staticmethod
    def _fingerprint(value):
        return hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:16]

    def _ledger_hash(self):
        return self._hash_prefix(len(self.events))

    def _hash_prefix(self, n):
        canonical = json.dumps(self.events[:n], ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
