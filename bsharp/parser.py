"""Parser provides parsing for bsharp."""


from bsharp.lexer import Lexer
from bsharp import ast
from bsharp import token


class Parser:
    """Parser class accepts a Lexer and provides methods generate a parse tree.

    Input:
        - lexer: Lexer: A lexical analyzer, that provides tokens.

    Exported Methods:

        - parse(): Returns a Program.

    """

    def __init__(self, lexer: Lexer) -> None:
        """Construct the Parser class."""
        self.lexer = lexer
        self.errors = []

    def add_parser_error(self, error: str) -> None:
        """Add a error to the errors array."""
        self.errors.append(error)

    def parse_call_expression(self, curToken: token.Token) -> ast.CallExpression | None:
        """Parse a function call expression."""
        expression = ast.CallExpression()

        expression.token = curToken

        new_token = self.lexer.nextToken()

        if new_token.getType() in [token.STRING, token.NUMBER]:
            self.add_parser_error(f"Function name cannot be {new_token.getType()}")
            return None

        expression.function = new_token

        new_token = self.lexer.nextToken()

        args = list()

        while new_token.getType() != token.RROUND:
            arg_expression = self.parse_expression(new_token)
            args.append(arg_expression)
            new_token = self.lexer.nextToken()

        expression.args = args

        return expression

    def parse_expression(self, curToken: token.Token) -> ast.Expression | None:
        """Parse any given arbitary expression."""
        expression = None

        match curToken.getType():
            case token.NUMBER:
                expression = ast.NumberExpression()
                expression.token = curToken
                expression.value = curToken.getValue()
            case token.STRING:
                expression = ast.StringExpression()
                expression.token = curToken
                expression.value = curToken.getValue()
            case token.IDENT:
                expression = ast.IdentifierExpression()
                expression.token = curToken
                expression.value = curToken.getValue()
            case token.LROUND:
                expression = self.parse_call_expression(curToken)
            case _:
                self.add_parser_error(
                    f"No parse expression for token {curToken.getType()}"
                )
        return expression

    def parse_program(self) -> ast.Program:
        """Return a parsed ast.Program."""
        program = ast.Program()

        curToken = self.lexer.nextToken()

        while curToken.getType() != token.EOF:
            expression = self.parse_expression(curToken)
            program.expressions.append(expression)
            curToken = self.lexer.nextToken()

        return program
