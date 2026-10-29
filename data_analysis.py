# 安装：uv add numpy pandas duckdb（裸 Python 就 pip install -U）
import numpy as np, pandas as pd, duckdb
from dataclasses import dataclass

@dataclass(slots=True)
class Chunk:
    content: str
    source: str
    score: float

chunks = [
    Chunk("年假制度：入职满一年享有5天带薪年假，满十年10天，满十五年15天。年假最小申请单位为半天。", "员工手册-年假", 0.71),
    Chunk("病假制度：需提供二级以上医院诊断证明，病假期间工资按基本工资的80%发放，全年累计不超过30天。", "员工手册-病假", 0.58),
    Chunk("差旅报销需在行程结束后30天内提交，发票抬头必须为公司全称，超标部分需分管副总裁特批。", "员工手册-报销", 0.81),
    Chunk("考勤制度：标准工时早9晚6。每月允许3次忘打卡豁免，第4次起每次扣款50元。季度全勤奖200元。", "员工手册-考勤", 0.42),
    Chunk("年假最小申请单位为半天，半天=4小时，不足半天按半天计。", "员工手册-年假", 0.66),
]

# 1) numpy：向量就是数组，"语义相似"根本不是玄学
#    假装 embedding：把每个 chunk 压成 4 维"伪向量"（真实是 1024 维）
vecs = np.array([[1.0, 0.0, 0.2, 0.0], [0.0, 1.0, 0.0, 0.1], [0.3, 0.0, 1.0, 0.0], [0.0, 0.1, 0.0, 1.0], [0.9, 0.0, 0.3, 0.0]])
query = np.array([1.0, 0.0, 0.25, 0.0])

def cosine(a, b):
    """支持 (d,) 或 (n,d) 两种输入，返回相似度或相似度向量"""
    a, b = np.atleast_2d(a), np.atleast_2d(b)
    num = a @ b.T
    den = np.linalg.norm(a, axis=1, keepdims=True) * np.linalg.norm(b, axis=1, keepdims=True)
    sims = num / den
    return float(sims[0, 0]) if sims.shape == (1, 1) else sims[:, 0]

print("numpy 算余弦相似度（query=年假）:")
for c, v in zip(chunks, vecs):
    print(f"  {cosine(query, v):.3f}  {c.source}  {c.content[:18]}...")
sims = cosine(vecs, query)          # 一次算全部：矩阵 × 向量
print("top1 是第", int(np.argmax(sims)), "条 chunk（上面决策 4 那个 `<=>` 算的就是它）")

# 2) pandas：一张表看清 chunk 分布，RAG 排障的第一步
df = pd.DataFrame({"source": [c.source for c in chunks],
                   "score": [c.score for c in chunks],
                   "chars": [len(c.content) for c in chunks]})
print("\npandas 统计 chunk:")
print(df.groupby("source")["score"].agg(["count", "max", "min"]).round(3).to_string())
df.to_csv("chunks.csv", index=False)

# 3) DuckDB：不起服务直接对 CSV 跑 SQL
con = duckdb.connect()
print("\nDuckDB 直接查 CSV:")
print(con.execute("select source, count(*) as n, round(max(score),3) as top from 'chunks.csv' "
                  "group by source order by top desc").df().to_string(index=False))
con.close()