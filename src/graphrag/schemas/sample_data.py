import patito as pt
import polars as pl


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
