from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer

from graphrag import PROJECT_ROOT
from graphrag.driver import build_neo4j_driver
from graphrag.infra.dotenv_file import CfgOpenAI, CfgNeo4j
from graphrag.llm.engins.builder import build_llm
from langchain.chains import GraphCypherQAChain



cfg_openai = CfgOpenAI.from_env(path=PROJECT_ROOT / ".env")
llm = build_llm(cfg_openai)

# ret = llm.invoke('hello')
# print(ret)

cfg_neo4j = CfgNeo4j.from_env(path=PROJECT_ROOT / ".env")


graph = Neo4jGraph(
    url=cfg_neo4j.uri,
    username=cfg_neo4j.user.get_secret_value(),
    password=cfg_neo4j.password.get_secret_value(),
)
CYPHER_GENERATION_TEMPLATE = """
Task: グラフデータベースに問い合わせるCypher文を生成する。

指示:
schemaで提供されている関係タイプとプロパティのみを使用してください。
提供されていない他の関係タイプやプロパティは使用しないでください。

schema:
{schema}

注意: 回答に説明や謝罪は含めないでください。
Cypher ステートメントを作成すること以外を問うような質問には回答しないでください。
生成された Cypher ステートメント以外のテキストを含めないでください。

例) 以下は、特定の質問に対して生成されたCypher文の例です:
# アイゼンの弟子は？
MATCH (p1:Person)-[:MASTER]->(p2:Person)
WHERE p1.id = 'アイゼン'
RETURN p2.id, p2.text
# ゼーリエの弟子の弟子は？
MATCH (p1:Person)-[:MASTER]->(p2:Person)-[:MASTER]->(p3:Person)
WHERE p1.id = 'ゼーリエ'
RETURN p3.id, p3.text

質問: {question}"""
chain = GraphCypherQAChain.from_llm(
    llm=llm, graph=graph, verbose=True,
    allow_dangerous_requests=True
)

ret = chain.invoke("ロイド・フォージャーとフランキーの関係は？")


print(ret)
# docs = load_pdf()
# tgt_chunks = split_text(docs)
#
# llm_transformer = LLMGraphTransformer(llm=llm)
# graph_documents = llm_transformer.convert_to_graph_documents(tgt_chunks)
# graph.add_graph_documents(graph_documents)
