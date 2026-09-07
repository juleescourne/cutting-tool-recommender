import ast
import math
from math import cos, sin

import numpy as np


def get_distance(p, q, coef_tab):
    """Return the weighted Euclidean distance between two equal-length points."""
    sum_sq_difference = 0
    for p_i, q_i, coeff_i in zip(p, q, coef_tab):
        sum_sq_difference += coeff_i * ((p_i - q_i) ** 2)
    return sum_sq_difference ** 0.5


def convert_effort(fx, fy, fz, freq_rotation, angle_radial, angle_axial, angle_attaque):
    """Convert workpiece forces into cutting-tool coordinates."""
    angle = (freq_rotation * math.pi) / 30

    passage_1 = np.array([
        [cos(angle), sin(angle), 0],
        [-sin(angle), cos(angle), 0],
        [0, 0, 1]
    ])

    passage_2 = np.array([
        [cos(angle_radial), sin(angle_radial), 0],
        [-sin(angle_radial), cos(angle_radial), 0],
        [0, 0, 1]
    ])

    passage_3 = np.array([
        [1, 0, 0],
        [0, cos(angle_axial), sin(angle_axial)],
        [0, -sin(angle_axial), cos(angle_axial)]
    ])

    passage_4 = np.array([
        [cos(angle_attaque), 0, sin(angle_attaque)],
        [-sin(angle_attaque), 0, cos(angle_attaque)],
        [0, 1, 0]
    ])

    effort_piece = np.array([[fx], [fy], [fz]])
    coord_1 = np.dot(passage_1, effort_piece)
    coord_2 = np.dot(passage_2, coord_1)
    coord_3 = np.dot(passage_3, coord_2)
    coord_4 = np.dot(passage_4, coord_3)

    return coord_4[0, 0], coord_4[1, 0], coord_4[2, 0]


_ALLOWED_FUNCTIONS = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_") and callable(getattr(math, name))
}
_ALLOWED_FUNCTIONS.update({"abs": abs, "round": round, "min": min, "max": max})
_ALLOWED_CONSTANTS = {"pi": math.pi, "e": math.e, "tau": math.tau}


def safe_math_expression(expression, y):
    """Evaluate a small mathematical expression containing ``y`` safely.

    Supported operations include +, -, *, /, %, ** and functions from the
    Python ``math`` module (e.g. ``sqrt(y)``, ``log(y)``, ``sin(y)``).
    Arbitrary Python execution, attribute access and imports are rejected.
    """
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.Name):
            if node.id == "y":
                return y
            if node.id in _ALLOWED_CONSTANTS:
                return _ALLOWED_CONSTANTS[node.id]
            raise ValueError(f"Unsupported name: {node.id}")
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp):
            left, right = evaluate(node.left), evaluate(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Mod):
                return left % right
            if isinstance(node.op, ast.Pow):
                return left ** right
            raise ValueError("Unsupported operator")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            func = _ALLOWED_FUNCTIONS.get(node.func.id)
            if func is None:
                raise ValueError(f"Unsupported function: {node.func.id}")
            if node.keywords:
                raise ValueError("Keyword arguments are not supported")
            return func(*(evaluate(arg) for arg in node.args))
        raise ValueError("Unsupported expression")

    return evaluate(tree)
