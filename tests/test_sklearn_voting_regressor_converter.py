"""Tests VotingRegressor converter."""

import unittest
import numpy
from sklearn.linear_model import LinearRegression
try:
    from sklearn.ensemble import VotingRegressor
except ImportError:
    # New in 0.21
    VotingRegressor = None
from sklearn.tree import DecisionTreeRegressor
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import (
    FloatTensorType, Int64TensorType
)
from test_utils import dump_data_and_model, fit_regression_model


def model_to_test():
    return VotingRegressor([
        ('lr', LinearRegression()),
        ('dt', DecisionTreeRegressor()),
    ])


class TestVotingRegressorConverter(unittest.TestCase):

    @unittest.skipIf(VotingRegressor is None,
                     reason="new in 0.21")
    def test_model_voting_regression(self):
        model, X = fit_regression_model(model_to_test())
        model_onnx = convert_sklearn(
            model, "voting regression",
            [("input", FloatTensorType([None, X.shape[1]]))])
        self.assertIsNotNone(model_onnx)
        dump_data_and_model(
            X.astype(numpy.float32),
            model,
            model_onnx,
            basename="SklearnVotingRegressor-Dec4",
            allow_failure="StrictVersion("
            "onnxruntime.__version__)"
            "<= StrictVersion('0.2.1')",
            comparable_outputs=[0]
        )

    @unittest.skipIf(VotingRegressor is None,
                     reason="new in 0.21")
    def test_model_voting_regression_int(self):
        model, X = fit_regression_model(model_to_test(), is_int=True)
        model_onnx = convert_sklearn(
            model, "voting regression",
            [("input", Int64TensorType([None, X.shape[1]]))])
        self.assertIsNotNone(model_onnx)
        dump_data_and_model(
            X,
            model,
            model_onnx,
            basename="SklearnVotingRegressorInt-Dec4",
            allow_failure="StrictVersion("
            "onnxruntime.__version__)"
            "<= StrictVersion('0.2.1')",
            comparable_outputs=[0]
        )


if __name__ == "__main__":
    unittest.main()
