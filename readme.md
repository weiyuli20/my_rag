 
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