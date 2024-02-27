"""Environment stores mapping between function, variables and their declaration."""

from bsharp.object import Object
from bsharp import ast


class Environment:
    """Environment contains defnition of functions and variables."""

    def __init__(self):
        """Initialize a empty environment."""
        self.variables: dict[Object, Object] = {}

        self.functions: dict[Object, ast.FunctionExpression] = {}
