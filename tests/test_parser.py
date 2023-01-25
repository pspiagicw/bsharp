"""Test the bsharp parser."""

from unittest import TestCase
from bsharp.lexer import Lexer
from bsharp import token
from bsharp.parser import Parser
from bsharp import ast
import pytest


class TestParser(TestCase):
    """Test the parser."""

    @pytest.mark.complex
    @pytest.mark.parser
    def test_defun_expression(self):
        """Test array expression."""
        input = "(fn foo [x y] 10)"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(parser.errors, [])
        self.assertIsInstance(program, ast.Program)
        self.assertEqual(parser.errors, [])

        self.assertEqual(len(program.expressions), 1)

        statement = program.expressions[0]

        print(type(statement))
        self.assertIsInstance(statement, ast.FunctionExpression)

        self.assertEqual(statement.function.getType(), token.IDENT)
        self.assertEqual(statement.function.getValue(), "foo")

        self.assertEqual(len(statement.args), 2)

        arg = statement.args[0]

        self.assertIsInstance(arg, ast.IdentifierExpression)
        self.assertEqual(arg.token.getValue(), "x")
        self.assertEqual(arg.value, "x")

        arg = statement.args[1]

        self.assertIsInstance(arg, ast.IdentifierExpression)
        self.assertEqual(arg.token.getValue(), "y")
        self.assertEqual(arg.value, "y")

        self.assertEqual(len(statement.body), 1)

        self.assertIsInstance(statement.body[0], ast.NumberExpression)
        self.assertEqual(statement.body[0].value, "10")
        self.assertEqual(statement.body[0].token.getValue(), "10")

    @pytest.mark.simple
    @pytest.mark.parser
    def test_integer_array_expression(self):
        """Test array expression."""
        input = "[1 2 3]"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(parser.errors, [])
        self.assertIsInstance(program, ast.Program)

        self.assertEqual(len(program.expressions), 1)

        statement = program.expressions[0]
        self.assertIsInstance(statement, ast.ArrayExpression)
        for element, value in zip(statement.elements, [1, 2, 3]):
            self.assertIsInstance(element, ast.NumberExpression)
            self.assertEqual(element.value, str(value))
            self.assertEqual(element.token.getValue(), str(value))

    @pytest.mark.simple
    @pytest.mark.parser
    def test_string_array_expression(self):
        """Test array expression."""
        input = '[ "hello" "something" "more" ]'

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertIsInstance(program, ast.Program)
        self.assertEqual(parser.errors, [])

        self.assertEqual(len(program.expressions), 1)

        statement = program.expressions[0]
        self.assertIsInstance(statement, ast.ArrayExpression)
        for element, value in zip(statement.elements, ["hello", "something", "more"]):
            self.assertIsInstance(element, ast.StringExpression)
            self.assertEqual(element.value, str(value))
            self.assertEqual(element.token.getValue(), str(value))

    @pytest.mark.simple
    @pytest.mark.parser
    def test_mixed_arrary_expression(self):
        """Test array expression."""
        input = '[ 1 "something" "more" foo ]'

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertIsInstance(program, ast.Program)
        self.assertEqual(parser.errors, [])

        self.assertEqual(len(program.expressions), 1)

        statement = program.expressions[0]
        self.assertIsInstance(statement, ast.ArrayExpression)
        for element, value, clas in zip(
            statement.elements,
            ["1", "something", "more", "foo"],
            [
                ast.NumberExpression,
                ast.StringExpression,
                ast.StringExpression,
                ast.IdentifierExpression,
            ],
        ):
            self.assertIsInstance(element, clas)
            self.assertEqual(element.value, str(value))
            self.assertEqual(element.token.getValue(), str(value))

    @pytest.mark.simple
    @pytest.mark.parser
    def test_number_expression(self):
        """Test simple function calls."""
        input = "1"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(parser.errors, [])
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

        self.assertEqual(parser.errors, [])
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

        self.assertEqual(parser.errors, [])
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

        self.assertEqual(parser.errors, [])
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
        (dump)
        """

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(parser.errors, [])
        self.assertIsInstance(program, ast.Program)

        self.assertEqual(len(program.expressions), 4)

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

        statement = program.expressions[3]
        self.assertIsInstance(statement, ast.CallExpression)
        self.assertEqual(statement.function.getType(), token.IDENT)
        self.assertEqual(statement.function.getValue(), "dump")

    @pytest.mark.complex
    @pytest.mark.parser
    def test_nested_expressions(self):
        """Test if nested expressions work."""
        input = """ (+  (* variable 2) othervariable (sin reallygoodvariable)) """

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(parser.errors, [])
        self.assertIsInstance(program, ast.Program)

        self.assertEqual(len(program.expressions), 1)

        statement = program.expressions[0]

        self.assertIsInstance(statement, ast.CallExpression)
        self.assertEqual(statement.function.getType(), token.PLUS)
        self.assertEqual(statement.function.getValue(), "+")

        args = statement.args

        self.assertEqual(len(args), 3)

        arg = statement.args[0]

        self.assertIsInstance(arg, ast.CallExpression)

        self.assertEqual(arg.function.getType(), token.STAR)
        self.assertEqual(arg.function.getValue(), "*")

        subargs = arg.args

        self.assertEqual(len(subargs), 2)

        self.assertIsInstance(subargs[0], ast.IdentifierExpression)
        self.assertIsInstance(subargs[1], ast.NumberExpression)

        self.assertEqual(subargs[0].value, "variable")
        self.assertEqual(subargs[1].value, "2")

        arg = statement.args[1]

        self.assertIsInstance(arg, ast.IdentifierExpression)
        self.assertEqual(arg.token.getType(), token.IDENT)
        self.assertEqual(arg.token.getValue(), "othervariable")
        self.assertEqual(arg.value, "othervariable")

        arg = statement.args[2]

        self.assertIsInstance(arg, ast.CallExpression)
        self.assertEqual(arg.function.getType(), token.IDENT)
        self.assertEqual(arg.function.getValue(), "sin")

        subargs = arg.args

        self.assertEqual(len(subargs), 1)

        self.assertIsInstance(subargs[0], ast.IdentifierExpression)

        self.assertEqual(subargs[0].value, "reallygoodvariable")
