"""Provides Syntax Tree bsharp."""

from typing import List

from bsharp import token
from io import StringIO
from pprint import pformat


class Expression:
    """Statement is bsharp is a function with it's corresponding arguments.

    A statement in bsharp is (function arg1 arg2 arg3).

    These args can be statement in themselves.
    """

    def __init__(self):
        """Construct a expression."""
        self.token: token.Token
        self.value: str
        self.function: token.Token
        self.args: list[Expression]
        self.body: list[Expression]
        self.elements: list[Expression]
        self.expressions: list[Expression]


class Program(Expression):
    """Class contains a list of statements."""

    def __init__(self):
        """Construct a Program."""
        self.expressions = []

    def __repr__(self) -> str:
        """Represent a Program as string."""
        builder = StringIO()

        builder.write(" Program ")
        builder.write(pformat(self.expressions))

        return builder.getvalue()


class NumberExpression(Expression):
    """NUmber Expression contains a Number."""

    def __init__(self):
        """Construct a Number Expression."""
        super().__init__()

    def __repr__(self) -> str:
        """Represent Number as a AST Object."""
        return f" Integer({self.value}) "


class StringExpression(Expression):
    """String Expression contains a single string."""

    def __init__(self):
        """Construct a string expression."""
        super().__init__()

    def __repr__(self) -> str:
        """Represent a string expression as str."""
        return f" String({self.value}) "


class IdentifierExpression(Expression):
    """Identifier Expression contains a identifier."""

    def __init__(self):
        """Construt a identifier expression."""
        super().__init__()

    def __repr__(self) -> str:
        """Represent a ident expression as string."""
        return f" Identifier({self.value}) "


class ArrayExpression(Expression):
    """Array Expression contains a array representation."""

    def __init__(self):
        """Construct a array expression."""
        super().__init__()

    def __repr__(self) -> str:
        """Represent a array expression."""
        builder = StringIO()

        builder.write(" Array ")

        builder.write(pformat(self.elements))

        return builder.getvalue()


class CallExpression(Expression):
    """Call Expression contains a representation of a function call."""

    def __init__(self):
        """Construct a Call Expression."""
        super().__init__()

    def __repr__(self) -> str:
        """Represent a call expression as string."""
        builder = StringIO()

        builder.write(f" Call ( Name( {self.function.getValue()} ) ")
        builder.write(pformat(self.args, indent=2))
        builder.write(" ) ")

        return builder.getvalue()


class FunctionExpression(Expression):
    """Function Expression contains a representation of a function declaration."""

    def __init__(self):
        """Construct a function expression."""
        super().__init__()

    def __repr__(self):
        """Represent a Function Expression."""
        builder = StringIO()

        builder.write(" Function ( Name ( ")
        builder.write(str(self.function))
        builder.write(" ) ")

        builder.write(pformat(self.args))

        builder.write(pformat(self.body))

        builder.write(" ) ")

        return builder.getvalue()
