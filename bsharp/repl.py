"""Module declares REPL for bsharp."""

from bsharp import lexer
from bsharp import token


def startREPL():
    """REPL function for bsharp."""
    PROMPT = ">>> "

    while True:
        input_string = input(PROMPT)

        l = lexer.Lexer(input_string)

        curToken = l.nextToken()

        while curToken.getType() != token.EOF:
            print(curToken)
            curToken = l.nextToken()
