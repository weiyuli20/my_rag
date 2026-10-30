 
 安装docker
 ```
 #拉取镜像
 docker pull pgvector/pgvector:pg16        # 拉不到就换 pg17，两个都行

 # 启动（后台）
docker run -d --name rag-pg \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# ↓↓↓ 下面三条验证必须全过才能继续 ↓↓↓

docker ps --filter name=rag-pg              # 1) 状态必须是 Up，端口显示 0.0.0.0:5432->5432/tcp
docker exec rag-pg pg_isready                # 2) 必须输出 "accepting connections"
docker exec rag-pg psql -U postgres -c \
  "SELECT default_version FROM pg_available_extensions WHERE name='vector';"   # 3) 必须有一行输出（版本号）
 ```

·
 建表
 uv run python schema.py 

 向量化
 uv run python ingest.py

 #查询
 uv run python query.py



 BM25算法（Best Matching） 25是此算法是经过25次迭代后得到的
 BM25算法是一种用于信息检索和文本挖掘的算法，用于评估查询和文档之间的相关性。
BM25算法的主要思想是，对于每个查询词，计算它在每个文档中的权重（相关性贡献），然后将这些权重相加，得到文档与查询的相关性得分。权重计算考虑了以下因素：

1. 词频（Term Frequency, TF）：一个词在文档中出现的次数。TF值越高，表示这个词在文档中越重要。
2. 文档频率（Document Frequency, DF）：包含某个词的文档数量。DF值越高，表示这个词在文档集合中越常见。
3. 平均文档长度（Average Document Length）：文档集合中所有文档的平均长度。
4. 查询长度（Query Length）：查询语句的长度。



BM25算法通过以下公式计算：

<img width="1360" height="516" alt="image" src="https://github.com/user-attachments/assets/7f12cdc8-76fd-40b3-afb5-0ffbc03fc8ca" />

BM25是词语匹配，并不能理解语义


倒排索引：
倒排索引用于快速找到包含query的相关文档，使得不用将query与所有文档进行相关性计算

<img width="1374" height="1798" alt="image" src="https://github.com/user-attachments/assets/89443cd4-3e63-44cd-b39d-2f393a0d2430" />










