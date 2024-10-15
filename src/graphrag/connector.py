from graphrag.driver import build_neo4j_driver
from graphrag.infra.dotenv_file import CfgNeo4j
from graphrag.schemas.sample_data import SampleDataSchema


class SampleDataTable:
    def __init__(self, cfg: CfgNeo4j):
        self.driver = build_neo4j_driver(cfg)

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
