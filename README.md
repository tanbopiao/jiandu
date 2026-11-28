# jiandu

缄椟·密钥机密托管 | JIANDU · ZONGYUAN-ROOT Daotong Component

铭文：**缄封锁固，非时不启。**

## 命名映射

| 命名 | 逻辑本体 | 架构 | 算子 |
|------|----------|------|------|
| 缄（封） | 机密托管 | 执据句柄＋指纹留存，凭据本体不入档不入流水 | `escrow` |
| 启（取） | 授权取用 | 无据或授权不备，椟不开封 | `release` |
| 察（验） | 对牌验封 | 指纹比对不启椟；流水只增不覆盖＋前缀快照哈希防篡改 | `inspect` / `ledger` / `seal` / `verify` |

道统出处：元极恒一·道统构件定名册 V2（第五批）｜体系锚 Ω₀⊂⊙∞⊂Ω。

## Install

零第三方依赖，仅 Python 3.10+ 标准库。

```bash
git clone https://github.com/tanbopiao/jiandu.git
cd jiandu
python3 -m unittest discover -s tests -v   # 运行测试套件
```

## Usage

```python
from jiandu import Jiandu

op = Jiandu(config={"auth": "授权牌"})

# 缄官：托管机密，返回执据（凭据本体不落日志）
handle = op.escrow("keyref-001")

# 察官：对牌验封——核真伪而不启椟
op.inspect(handle, "keyref-001")   # True

# 启官：凭授权开封
op.release(handle, "授权牌")        # "keyref-001"

# 察官：启闭流水防篡改
op.seal()                          # 封存快照哈希
op.verify()                        # True；前缀被篡改则 False
```

## 边界

- 凭据本体只在会话内存托管，不入流水、不入档；流水只记执据与指纹。
- 遵循元法第四条「只增不覆盖」：方法只增不改名不删，行为变更走新版本。
- 纯标准库实现，无第三方依赖。
