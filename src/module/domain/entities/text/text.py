from pandas import DataFrame


class Text:
    """
    Text Entity
    """

    def __init__(self, text_df: DataFrame):
        self.t_df = text_df

    @property
    def t_df_size(self):
        """
        Text DF Size
        :return: The Text Datafram Memory Usage
        """
        return self.t_df.memory_usage()

    @property
    def t_df_shape(self):
        """
        Text DF Shape
        :return: The Text Dataframe Shape
        """
        return self.t_df.shape

    def get_text_df(self):
        """

        :return:
        """
        return self.t_df
