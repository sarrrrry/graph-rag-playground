# graph-rag-playground

## prepare environment

- launch neo4j with docker
    ```bash
    docker run --publish=7474:7474 --publish=7687:7687 --volume=./data/db/neo4j/:/data neo4j
    ```

- create .env file referring to .env.example
    ```dotenv
    NEO4J_USER=neo4j
    NEO4J_PASSWORD=neo4j
    ```

- install dependencies
    ```bash
    uv sync
    ```

- サンプルデータを登録
    ```bash
    uv run src/graphrag/insert_sample_data.py
    ```
## run

```dotenv
uv run src/graphrag/main.py
```