from .asset import Asset


class Simulator:
    def __init__(self, dataset, pair):
        self.root_path = dataset
        self.asset = Asset(*pair.split('-'))
        self.df = self.asset.get_df(smas=200, emas=(12, 26), rsis=14, return_colors=True, dataset=self.root_path)
        self.price = 0

        self.simulation = self.generator()

    def generator(self):
        self.df = self.df.dropna(axis=0)
        for i, row in self.df.iterrows():
            yield row
