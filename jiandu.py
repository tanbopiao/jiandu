"""缄椟（JIANDU）· 密钥机密托管

道统出处：元极恒一·道统构件定名册 V2 ｜ 第五批
体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002

工程映射：密钥机密托管。

边界：本件为算子骨架 v0——接口先立、实现随进化轮补齐；遵循元法第四条「只增不覆盖」，
方法只增不改名不删，行为变更走新版本；凭据不入档，宣称与事实分离。
"""

class Jiandu:
    """缄椟（JIANDU）算子骨架 v0。"""

    ANCHOR = "Ω₀⊂⊙∞⊂Ω｜DID-BR-000002"
    CODE = "JIANDU"

    def __init__(self, config=None):
        self.config = dict(config or {})
        self.events = []  # 只增不覆盖：会话内事件留痕

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

    def escrow(self, key_ref):
        """缄封锁固：机密托管，返回执据（凭据本体不入档）（骨架桩：实现随进化轮补齐）。"""
        raise NotImplementedError("JIANDU.escrow 骨架桩，候进化轮补齐")

    def release(self, handle, auth):
        """非时不启：凭授权取用托管件（骨架桩：实现随进化轮补齐）。"""
        raise NotImplementedError("JIANDU.release 骨架桩，候进化轮补齐")
