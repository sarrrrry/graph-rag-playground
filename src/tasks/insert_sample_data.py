"""
c.f. [Neo4j + Pythonの使い方あれこれ #Python3 - Qiita](https://qiita.com/shiro-manju/items/08cbca27a2258526fc1c)
"""

from graphrag import PROJECT_ROOT
from graphrag.connector import SampleDataTable
from graphrag.infra.dotenv_file import CfgNeo4j
from graphrag.schemas.sample_data import SampleDataSchema


def main():
    data_path = PROJECT_ROOT / "data" / "sample_data.tsv"
    df = SampleDataSchema.DataFrame.read_csv(data_path, separator="\t")

    cfg = CfgNeo4j.from_env(path=PROJECT_ROOT / ".env")

    table = SampleDataTable(cfg)
    table.insert(df)


if __name__ == '__main__':
    main()
