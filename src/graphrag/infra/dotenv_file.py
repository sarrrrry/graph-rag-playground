from pathlib import Path

from dotenv import dotenv_values
from pydantic import BaseModel, SecretStr


class CfgNeo4j(BaseModel):
    uri: str
    user: SecretStr
    password: SecretStr

    @classmethod
    def from_env(cls, path: Path) -> "CfgNeo4j":
        envs = dotenv_values(path)
        return cls(
            uri=envs["NEO4J_URI"],
            user=envs["NEO4J_USERNAME"],
            password=envs["NEO4J_PASSWORD"],
        )

    @property
    def as_auth(self):
        return (self.user.get_secret_value(), self.password.get_secret_value())


class CfgOpenAI(BaseModel):
    openai_api_key: SecretStr
    chatmodel_name: str = "gpt-4o-mini"
    temperature: float = 0.0

    @classmethod
    def from_env(cls, path: Path) -> "CfgOpenAI":
        envs = dotenv_values(path)
        return cls(
            openai_api_key=envs["OPENAI_API_KEY"],
        )
