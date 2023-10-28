"""Module declares REPL for bsharp."""

from bsharp import lexer
from bsharp import token
from bsharp import parser
from pprint import pprint
from bsharp.environment import Environment

from bsharp.evaluator import Evaluator


def startREPL():
    """REPL function for bsharp."""
    PROMPT = ">>> "

    while True:
        input_string = input(PROMPT)

        l = lexer.Lexer(input_string)
        p = parser.Parser(l)
        program = p.parse_program()
        print(program)
        print(p.errors)
        # evaluator = Evaluator()
        # environment = Environment()
        # pprint(program.expressions)

        # print(evaluator.eval(program, environment))
