from langchain_openai import ChatOpenAI

from graphrag.infra.dotenv_file import CfgOpenAI


def build_llm(cfg: CfgOpenAI):
    chat_model = ChatOpenAI(
        api_key=cfg.openai_api_key.get_secret_value(),
        model=cfg.chatmodel_name,
        # streaming=True,
        temperature=cfg.temperature,
    )
    return chat_model
