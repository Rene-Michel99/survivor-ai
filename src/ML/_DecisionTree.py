import joblib

from ._BaseAI import BaseAI


class DecisionTree(BaseAI):
    def __init__(self, model_path):
        super(DecisionTree).__init__()

        self._algorithm = joblib.load(open(model_path, 'rb'))

    def make_decision(self, data: list):
        return self._algorithm.predict([data])
