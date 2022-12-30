"""Provides Syntax Tree bsharp."""

from typing import List

from bsharp import token
from io import StringIO


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


class Program:
    """Class contains a list of statements."""

    def __init__(self):
        """Construct a Program."""
        self.expressions = []

    def __repr__(self) -> str:
        """Represent a Program as string."""
        builder = StringIO()

        for expression in self.expressions:
            builder.write(str(expression))
            builder.write("\n")

        return builder.getvalue()


class NumberExpression(Expression):
    """NUmber Expression contains a Number."""

    def __init__(self):
        """Construct a Number Expression."""
        super().__init__()

    def __repr__(self) -> str:
        """Represent Number as a AST Object."""
        return f"Integer({self.value})"


class StringExpression(Expression):
    """String Expression contains a single string."""

    def __init__(self):
        """Construct a string expression."""
        super().__init__()

    def __repr__(self) -> str:
        """Represent a string expression as str."""
        return f"String({self.value})"


class IdentifierExpression(Expression):
    """Identifier Expression contains a identifier."""

    def __init__(self):
        """Construt a identifier expression."""
        super().__init__()

    def __repr__(self) -> str:
        """Represetn a ident expression as string."""
        return f"Identifier({self.value})"


class CallExpression(Expression):
    """Call Expression contains a representation of a function call."""

    def __init__(self):
        """Construct a Call Expression."""
        super().__init__()

    def __repr__(self) -> str:
        """Represent a call expression as string."""
        builder = StringIO()

        builder.write(f"Call(function={self.function.getValue()})")
        builder.write("\n")
        builder.write("Arguments: \n")
        for arg in self.args:
            builder.write(str(arg))
            builder.write("\n")

        builder.write("CALLEND")

        return builder.getvalue()
