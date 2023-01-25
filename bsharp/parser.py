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

    def parse_call(self, name: token.Token) -> ast.Expression | None:
        """Parse a call expression declaring a function."""
        expression = ast.CallExpression()

        expression.token = token.Token(type=token.LROUND, value="(")

        expression.function = name

        new_token = self.lexer.nextToken()

        args = list()

        while new_token.getType() != token.RROUND:
            if new_token.getType() == token.EOF:
                self.add_parser_error(f"Reached EOF while parsing.")
                return None
            arg_expression = self.parse_expression(new_token)
            if arg_expression == None:
                self.add_parser_error(f"Element at token {new_token} was not parsed.")
            args.append(arg_expression)
            new_token = self.lexer.nextToken()

        expression.args = args

        return expression

    def parse_defun(self, curToken: token.Token) -> ast.Expression | None:
        """Parse call expression."""
        expression = ast.FunctionExpression()

        expression.token = curToken

        new_token = self.lexer.nextToken()

        expression.function = new_token

        new_token = self.lexer.nextToken()

        args = self.parse_expression(new_token)

        if args == None:
            self.add_parser_error(f"Error in parsing arguments")
            return None

        for arg in args.elements:
            if not isinstance(arg, ast.IdentifierExpression):
                self.add_parser_error(f"Expected identifier, got expression")

        expression.args = args.elements

        new_token = self.lexer.nextToken()

        body = list()

        while new_token.getType() != token.RROUND:
            if new_token.getType() == token.EOF:
                self.add_parser_error(f"Reached EOF while parsing")
                return None

            ex = self.parse_expression(new_token)
            if ex == None:
                self.add_parser_error(f"Element at token{new_token} was not parsed")
            body.append(ex)
            new_token = self.lexer.nextToken()

        expression.body = body

        return expression

    def parse_round_bracket(self, curToken: token.Token) -> ast.Expression | None:
        """Parse a function call expression."""
        new_token = self.lexer.nextToken()

        match new_token.getType():
            case token.IDENT:
                match new_token.getValue():
                    case token.DEFUN:
                        return self.parse_defun(curToken)
                    case _:
                        return self.parse_call(new_token)
            case token.PLUS | token.STAR | token.MINUS | token.SLASH:
                return self.parse_call(new_token)
            case _:
                self.add_parser_error(f"Function name cannot be {new_token.getType()}")

        return None

    def parse_array_expression(self, curToken: token.Token) -> ast.Expression | None:
        """Parse a arrary expression."""
        expression = ast.ArrayExpression()
        expression.token = curToken

        new_token = self.lexer.nextToken()

        elements = list()

        while new_token.getType() != token.RSQUARE:

            if new_token.getType() == token.EOF:
                self.add_parser_error(f"Reached EOF while parsing.")
                return None

            element = self.parse_expression(new_token)

            if element == None:
                self.add_parser_error(f"Element at token {new_token} was not parsed.")
                return None

            elements.append(element)
            new_token = self.lexer.nextToken()

        expression.elements = elements

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
            case token.LSQUARE:
                expression = self.parse_array_expression(curToken)
            case token.LROUND:
                expression = self.parse_round_bracket(curToken)
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
