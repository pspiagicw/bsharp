"""Module tests Lexer for bsharp."""

from typing import List
import unittest
from bsharp import lexer
from bsharp import token


class TestLexer(unittest.TestCase):
    """Class for testing."""

    def test_simple(self) -> None:
        """Simple test for environment confirmation."""
        self.assertEqual(True, True)

    def assertTokens(self, input: str, expectedTokens: List[token.Token]) -> None:
        """Assert if list of tokens is equal to calculated tokens."""
        l = lexer.Lexer(input)
        for expected in expectedTokens:
            actual = l.nextToken()

            self.assertEqual(expected.getType(), actual.getType())
            self.assertEqual(expected.getValue(), actual.getValue())

    def test_arthemetic(self):
        """Test arthemetic symbols."""
        input = "+-*/:'"

        expectedTokens = [
            token.Token(type=token.PLUS, value="+"),
            token.Token(type=token.MINUS, value="-"),
            token.Token(type=token.STAR, value="*"),
            token.Token(type=token.SLASH, value="/"),
            token.Token(type=token.COLON, value=":"),
            token.Token(type=token.QUOTE, value="'"),
            token.Token(type=token.EOF, value=""),
        ]

        self.assertTokens(input, expectedTokens)

    def test_brackets(self) -> None:
        """Test multiple types of brackets."""
        input = "(){}[]"

        expectedTokens = [
            token.Token(type=token.LROUND, value="("),
            token.Token(type=token.RROUND, value=")"),
            token.Token(type=token.LCURLY, value="{"),
            token.Token(type=token.RCURLY, value="}"),
            token.Token(type=token.LSQUARE, value="["),
            token.Token(type=token.RSQUARE, value="]"),
            token.Token(type=token.EOF, value=""),
        ]

        self.assertTokens(input, expectedTokens)

    def test_spacess(self) -> None:
        """Test to ignore spaces/tabs."""
        input = """
       +  - ( )
       -
       """

        expectedTokens = [
            token.Token(type=token.PLUS, value="+"),
            token.Token(type=token.MINUS, value="-"),
            token.Token(type=token.LROUND, value="("),
            token.Token(type=token.RROUND, value=")"),
            token.Token(type=token.MINUS, value="-"),
            token.Token(type=token.EOF, value=""),
        ]

        self.assertTokens(input, expectedTokens)

    def test_numbers(self) -> None:
        """Test numbers."""
        input = "5 10 -6 -20 20.1 -2.1"

        expectedTokens = [
            token.Token(type=token.NUMBER, value="5"),
            token.Token(type=token.NUMBER, value="10"),
            token.Token(type=token.MINUS, value="-"),
            token.Token(type=token.NUMBER, value="6"),
            token.Token(type=token.MINUS, value="-"),
            token.Token(type=token.NUMBER, value="20"),
            token.Token(type=token.NUMBER, value="20.1"),
            token.Token(type=token.MINUS, value="-"),
            token.Token(type=token.NUMBER, value="2.1"),
        ]

        self.assertTokens(input, expectedTokens)

    def test_identifiers(self) -> None:
        """Test identifiers."""
        input = "add ( minus 5) let-them-win"

        expectedTokens = [
            token.Token(type=token.IDENT, value="add"),
            token.Token(type=token.LROUND, value="("),
            token.Token(type=token.IDENT, value="minus"),
            token.Token(type=token.NUMBER, value="5"),
            token.Token(type=token.RROUND, value=")"),
            token.Token(type=token.IDENT, value="let-them-win"),
            token.Token(type=token.EOF, value=""),
        ]

        self.assertTokens(input, expectedTokens)

    def test_strings(self) -> None:
        """Test variations of string."""
        input = '"hello"'
        expectedTokens = [token.Token(type=token.STRING, value="hello")]
        self.assertTokens(input, expectedTokens)

        input = '"hello'
        expectedTokens = [token.Token(type=token.STRING, value="hello")]
        self.assertTokens(input, expectedTokens)

    def test_code(self) -> None:
        """Test a sample of valid bsharp code."""
        input = """
        (print "Value: %n" (- (+ 1 2) 5))
        """

        expectedTokens = [
            token.Token(type=token.LROUND, value="("),
            token.Token(type=token.IDENT, value="print"),
            token.Token(type=token.STRING, value="Value: %n"),
            token.Token(type=token.LROUND, value="("),
            token.Token(type=token.MINUS, value="-"),
            token.Token(type=token.LROUND, value="("),
            token.Token(type=token.PLUS, value="+"),
            token.Token(type=token.NUMBER, value="1"),
            token.Token(type=token.NUMBER, value="2"),
            token.Token(type=token.RROUND, value=")"),
            token.Token(type=token.NUMBER, value="5"),
            token.Token(type=token.RROUND, value=")"),
            token.Token(type=token.RROUND, value=")"),
        ]

        self.assertTokens(input, expectedTokens)
