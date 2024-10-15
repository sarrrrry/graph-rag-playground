from neo4j import GraphDatabase

from graphrag.infra.dotenv_file import CfgNeo4j


def build_neo4j_driver(cfg: CfgNeo4j):
    driver = GraphDatabase.driver(cfg.uri, auth=cfg.as_auth)
    return driver
