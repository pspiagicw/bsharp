"""Evaluator module."""

from bsharp import ast
from bsharp import object
from bsharp.environment import Environment
import sys


class Evaluator:
    """Class is the evaluator for bsharp."""

    def error(self, message: str) -> None:
        """Convey the error and exit gracefully."""
        print(message)
        sys.exit(1)

    def extend_environment(
        self,
        toMatch: list[ast.Expression],
        givenArgs: list[ast.Expression],
        old: Environment,
    ) -> Environment:
        """Extend the environment with the current arguments."""
        new_environment = Environment()
        new_environment.functions = old.functions
        new_environment.variables = old.variables

        if len(toMatch) != len(givenArgs):
            self.error(f"Given arguments does not match, required arguments")

        for wanted, given in zip(toMatch, givenArgs):
            print(toMatch, givenArgs, wanted, given)

        return new_environment

    def evaluateFunction(
        self, fn: ast.Expression, environment: Environment
    ) -> object.Object:
        """Evaluate function using the environment."""
        if fn.value in environment.functions:
            func = environment.functions[fn.value]
            new_environment = self.extend_environment(func.args, fn.args, environment)
            return_value = object.CONST_NIL
            for expression in func.expressions:
                return_value = self.eval(expression, new_environment)
            return return_value
        else:
            return object.CONST_NIL

    def evaluateCall(
        self, fn: ast.Expression, environment: Environment
    ) -> object.Object:
        """Evaluate any call expression."""
        name = fn.function.getValue()
        if name not in environment.functions:
            return object.Error(message=f"No function named {name} found")
        return object.CONST_NIL

    def eval(self, ex: ast.Expression, env: Environment) -> object.Object:
        """Evaluate any given expression."""
        match type(ex):
            case ast.StringExpression:
                return object.String(ex.value)
            case ast.NumberExpression:
                return object.Number(ex.value)
            case ast.FunctionExpression:
                return self.evaluateFunction(ex, env)
            case ast.CallExpression:
                return self.evaluateCall(ex, env)
            case ast.Program:
                evaluate = object.CONST_NIL
                for expression in ex.expressions:
                    evaluate = self.eval(expression, env)

                return evaluate
        return object.CONST_NIL
