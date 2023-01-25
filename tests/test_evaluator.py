"""Test the evalutor."""

from bsharp.environment import Environment
from bsharp.lexer import Lexer
from bsharp.parser import Parser
from bsharp.evaluator import Evaluator
from bsharp import object
from unittest import TestCase
import pytest


class TestEvaluator(TestCase):
    """Test the evaluator."""

    @pytest.mark.simple
    @pytest.mark.evaluator
    def test_numerical_expression(self):
        """Test numerical expressions."""
        input = "5"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        eval = Evaluator()
        env = Environment()

        self.assertEqual(eval.eval(program, env).value, 5)
        self.assertEqual(eval.eval(program, env).type, object.NUMBER_OBJ)

    @pytest.mark.simple
    @pytest.mark.evaluator
    def test_last_evaluated(self):
        """Test numerical expressions."""
        input = "5 5 1 5"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        eval = Evaluator()
        env = Environment()

        self.assertEqual(eval.eval(program, env).value, 5)
        self.assertEqual(eval.eval(program, env).type, object.NUMBER_OBJ)

    @pytest.mark.simple
    @pytest.mark.evaluator
    def test_string_expression(self):
        """Test numerical expressions."""
        input = '"hello"'

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        eval = Evaluator()
        env = Environment()

        self.assertEqual(eval.eval(program, env).value, "hello")
        self.assertEqual(eval.eval(program, env).type, object.STRING_OBJ)

    @pytest.mark.simple
    @pytest.mark.evaluator
    def test_add_expression(self):
        """Test numerical expressions."""
        input = "(+ 1 2)"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        eval = Evaluator()
        env = Environment()

        self.assertEqual(eval.eval(program, env).value, 3)
        self.assertEqual(eval.eval(program, env).type, object.NUMBER_OBJ)
