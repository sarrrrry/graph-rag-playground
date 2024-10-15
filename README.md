# graph-rag-playground

## prepare environment

- launch neo4j with docker
    ```bash
    bash 
    ```

- create .env file referring to .env.example
    ```dotenv
    NEO4J_USER=neo4j
    NEO4J_PASSWORD=neo4j
    ```

- access to localhost:7474 and set username and password for neo4j
  - http://localhost:7474
  - default password is `neo4j`

- install dependencies
    ```bash
    uv sync
    ```

- insert sample data
    ```bash
    uv run src/tasks/insert_sample_data.py
    ```

## run

```dotenv
uv run src/graphrag/main.py
```
