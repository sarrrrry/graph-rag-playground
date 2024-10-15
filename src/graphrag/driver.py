from pathlib import Path

from neo4j import GraphDatabase
from pydantic import BaseModel, SecretStr


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


def build_neo4j_driver(cfg: CfgNeo4j):
    URI = 'neo4j://localhost:7687'
    driver = GraphDatabase.driver(URI, auth=cfg.as_auth)
    return driver
