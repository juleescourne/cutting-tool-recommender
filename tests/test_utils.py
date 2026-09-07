import math

import numpy as np
import pytest

from utils import convert_effort, get_distance, safe_math_expression


def test_weighted_distance():
    distance = get_distance([0, 0], [3, 4], [1, 1])
    assert distance == pytest.approx(5.0)


def test_force_transformation_preserves_vector_norm():
    source = np.array([10.0, -4.0, 7.0])
    transformed = np.array(convert_effort(*source, 1200, 0.2, 0.4, 0.1))
    assert np.linalg.norm(transformed) == pytest.approx(np.linalg.norm(source))


def test_safe_math_expression_supports_math_functions():
    assert safe_math_expression("sqrt(y) + 2", 9) == pytest.approx(5.0)
    assert safe_math_expression("sin(pi / 2) * y", 3) == pytest.approx(3.0)


def test_safe_math_expression_rejects_code_execution():
    with pytest.raises(ValueError):
        safe_math_expression("__import__('os').system('echo nope')", 1)
