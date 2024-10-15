"""
c.f. [Neo4j + Pythonの使い方あれこれ #Python3 - Qiita](https://qiita.com/shiro-manju/items/08cbca27a2258526fc1c)
"""
from pathlib import Path

import patito as pt
import polars as pl
from neo4j import GraphDatabase
from pydantic import BaseModel, SecretStr

from graphrag import PROJECT_ROOT


class SampleDataSchema(pt.Model):
    relation: str
    from_node_type: str
    from_node: str
    to_node_type: str
    to_node: str


@pl.api.register_dataframe_namespace("pd")
class PolarsPd:
    """for pycharm
    df = SampleDataSchema.DataFrame
    df.pd.dfでpandasのDataFrameに変換される
    """

    def __init__(self, df: pt.Model | pl.DataFrame):
        self.df = df.to_pandas()


class CfgNeo4j(BaseModel):
    user: SecretStr
    password: SecretStr

    @classmethod
    def from_env(cls, path: Path) -> "CfgNeo4j":
        from dotenv import dotenv_values
        envs = dotenv_values(path)
        return cls(
            user=envs["NEO4J_USER"],
            password=envs["NEO4J_PASSWORD"],
        )

    @property
    def as_auth(self):
        return (self.user.get_secret_value(), self.password.get_secret_value())


class SpyFamilyTable:
    def __init__(self, cfg: CfgNeo4j):
        URI = 'neo4j://localhost:7687'
        driver = GraphDatabase.driver(URI, auth=cfg.as_auth)
        self.driver = driver

    def insert(self, df: SampleDataSchema):
        # nodeの追加
        with self.driver.session() as session:
            session.execute_write(self._add_node, df)
        # relationの追加
        with self.driver.session() as session:
            session.execute_write(self._add_relation, df)

    @staticmethod
    def _add_node(tx, df: SampleDataSchema):
        def fn(node: str, node_type: str):
            query = f'CREATE (f:{node_type}:character {{name: $name}}) RETURN f'
            tx.run(query, name=node)

        cols = ["from_node", "from_node_type", "to_node", "to_node_type"]
        use_df = df.select(*cols)
        for row in use_df.iter_rows():
            fn(row[0], row[1])
            fn(row[2], row[3])

    @staticmethod
    def _add_relation(tx, df: SampleDataSchema):
        cols = ["from_node", "to_node", "relation"]
        use_df = df.select(*cols)
        for row in use_df.iter_rows():
            from_node, to_node, relation = row
            query = (
                'MATCH (f1:character {name: $from_node})'
                'MATCH (f2:character {name: $to_node})'
                f'CREATE (f1)-[:{relation}]->(f2)'
            )
            tx.run(query, from_node=from_node, relation=relation, to_node=to_node)


def main():
    # データ読み込み
    data_path = PROJECT_ROOT / "sample_data.tsv"
    df = SampleDataSchema.DataFrame.read_csv(data_path, separator="\t")

    cfg = CfgNeo4j.from_env(path=PROJECT_ROOT / ".env")

    table = SpyFamilyTable(cfg)
    table.insert(df)


if __name__ == '__main__':
    main()
