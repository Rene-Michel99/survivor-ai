import joblib

from ._BaseAI import BaseAI


class RandomForest(BaseAI):
    def __init__(self, model_path):
        super(RandomForest).__init__()

        self._algorithm = joblib.load(open(model_path, 'rb'))

    def make_decision(self, data: list):
        return self._algorithm.predict([data])
