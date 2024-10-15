# graph-rag-playground

## prepare environment
launch neo4j with docker
```bash
docker run --publish=7474:7474 --publish=7687:7687 --volume=./data/db/neo4j/:/data neo4j
```

re-write .env file
```dotenv
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j
```

install dependencies
```bash
uv sync
```

## run
```dotenv
uv run src/graphrag/main.py
```