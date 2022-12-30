"""Test the bsharp parser."""

from unittest import TestCase
from bsharp.lexer import Lexer
from bsharp import token
from bsharp.parser import Parser
from bsharp import ast
import pytest


class TestParser(TestCase):
    """Test the parser."""

    @pytest.mark.simple
    @pytest.mark.parser
    def test_number_expression(self):
        """Test simple function calls."""
        input = "1"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertIsInstance(program, ast.Program)

        self.assertEqual(len(program.expressions), 1)

        statement = program.expressions[0]

        self.assertIsInstance(statement, ast.NumberExpression)
        self.assertEqual(statement.value, "1")
        self.assertEqual(statement.token.getValue(), "1")

    @pytest.mark.simple
    @pytest.mark.parser
    def test_string_expression(self):
        """Test simple function calls."""
        input = '"hello"'

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()
        print(program.expressions)

        self.assertIsInstance(program, ast.Program)

        self.assertEqual(len(program.expressions), 1)

        statement = program.expressions[0]

        self.assertIsInstance(statement, ast.StringExpression)
        self.assertEqual(statement.value, "hello")
        self.assertEqual(statement.token.getValue(), "hello")

    @pytest.mark.complex
    @pytest.mark.parser
    def test_call_expression(self):
        """Test simple function calls."""
        input = "(+ 1 2)"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertIsInstance(program, ast.Program)

        self.assertEqual(len(program.expressions), 1)

        statement = program.expressions[0]

        self.assertIsInstance(statement, ast.CallExpression)
        self.assertEqual(statement.function.getType(), token.PLUS)
        self.assertEqual(statement.function.getValue(), "+")

        args = statement.args
        self.assertEqual(len(args), 2)

        self.assertIsInstance(args[0], ast.NumberExpression)
        self.assertIsInstance(args[1], ast.NumberExpression)

        self.assertEqual(args[0].value, "1")
        self.assertEqual(args[1].value, "2")

    @pytest.mark.complex
    @pytest.mark.parser
    def test_multiple_call_expression(self):
        """Test simple function calls."""
        input = """
        (+ 1 2)
        (* 1 2)
        (sin 1)
        """

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertIsInstance(program, ast.Program)

        self.assertEqual(len(program.expressions), 3)

        statement = program.expressions[0]

        self.assertIsInstance(statement, ast.CallExpression)
        self.assertEqual(statement.function.getType(), token.PLUS)
        self.assertEqual(statement.function.getValue(), "+")

        args = statement.args
        self.assertEqual(len(args), 2)

        self.assertIsInstance(args[0], ast.NumberExpression)
        self.assertIsInstance(args[1], ast.NumberExpression)

        self.assertEqual(args[0].value, "1")
        self.assertEqual(args[1].value, "2")

        statement = program.expressions[1]

        self.assertIsInstance(statement, ast.CallExpression)
        self.assertEqual(statement.function.getType(), token.STAR)
        self.assertEqual(statement.function.getValue(), "*")

        args = statement.args
        self.assertEqual(len(args), 2)

        self.assertIsInstance(args[0], ast.NumberExpression)
        self.assertIsInstance(args[1], ast.NumberExpression)

        self.assertEqual(args[0].value, "1")
        self.assertEqual(args[1].value, "2")

        statement = program.expressions[2]

        self.assertIsInstance(statement, ast.CallExpression)
        self.assertEqual(statement.function.getType(), token.IDENT)
        self.assertEqual(statement.function.getValue(), "sin")

        args = statement.args
        self.assertEqual(len(args), 1)

        self.assertIsInstance(args[0], ast.NumberExpression)

        self.assertEqual(args[0].value, "1")

    @pytest.mark.complex
    @pytest.mark.parser
    def test_ident_call_expression(self):
        """Test expression with ident argument."""
        input = """
        (+ somevariable othervariable)
        (* variable 2)
        (sin reallygoodvariable)
        """

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertIsInstance(program, ast.Program)

        self.assertEqual(len(program.expressions), 3)

        statement = program.expressions[0]

        self.assertIsInstance(statement, ast.CallExpression)
        self.assertEqual(statement.function.getType(), token.PLUS)
        self.assertEqual(statement.function.getValue(), "+")

        args = statement.args

        self.assertEqual(len(args), 2)

        self.assertIsInstance(args[0], ast.IdentifierExpression)
        self.assertIsInstance(args[1], ast.IdentifierExpression)

        self.assertEqual(args[0].value, "somevariable")
        self.assertEqual(args[1].value, "othervariable")

        statement = program.expressions[1]

        self.assertIsInstance(statement, ast.CallExpression)
        self.assertEqual(statement.function.getType(), token.STAR)
        self.assertEqual(statement.function.getValue(), "*")

        args = statement.args
        self.assertEqual(len(args), 2)

        self.assertIsInstance(args[0], ast.IdentifierExpression)
        self.assertIsInstance(args[1], ast.NumberExpression)

        self.assertEqual(args[0].value, "variable")
        self.assertEqual(args[1].value, "2")

        statement = program.expressions[2]

        self.assertIsInstance(statement, ast.CallExpression)
        self.assertEqual(statement.function.getType(), token.IDENT)
        self.assertEqual(statement.function.getValue(), "sin")

        args = statement.args
        self.assertEqual(len(args), 1)

        self.assertIsInstance(args[0], ast.IdentifierExpression)

        self.assertEqual(args[0].value, "reallygoodvariable")

    @pytest.mark.complex
    @pytest.mark.parser
    def test_nested_expressions(self):
        """Test if nested expressions work."""
        input = """ (+  (* variable 2) othervariable (sin reallygoodvariable)) """

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertIsInstance(program, ast.Program)

        self.assertEqual(len(program.expressions), 1)

        statement = program.expressions[0]

        self.assertIsInstance(statement, ast.CallExpression)
        self.assertEqual(statement.function.getType(), token.PLUS)
        self.assertEqual(statement.function.getValue(), "+")

        args = statement.args

        self.assertEqual(len(args), 3)

        arg = statement.args[0]
