"""Lexer provides lexical analysis for bsharp."""
from bsharp import token


class Lexer:
    """Lexer class accepts and input and provides methods to generate tokens..

    Input:
        Lexer only needs the string to consume.

        - input: String:  A string to tokenize

    Exported Methods:
        Only a single method is exported. This is the `nextToken()`.
        All others are not needed by the external caller.

        -  nextToken():  Returns a token according to current position. Gives EOF tokens on overflow.
    At These are the internal variables initialized by the lexer

    Internal Attributes:
        These attributes are tracked by the lexer internally and not exported to the caller.

        - _readPos
        - _curPos
        - _eof
        - _validWhitespaces

    - `_readPos` stores the reading position. This position is always 1 position ahead then the current position. This is used to peek at the input, to consume complex 2 char symbols `>=`, `<=`, `==`

    - `_curPos` stores the current position. This is used to make token decision.

    - `_eof` only indicates whether input string is exhausted or not.

    - `_validWhitespaces` is a set of symbols ignored by the lexer entirely.



    """

    def __init__(self, input: str) -> None:
        """Constuctor for Lexer class."""
        self.input: str = input
        self._readPos: int = 0
        self._curPos: int = 0
        self._eof: bool = False
        self._validWhitespaces: set[str] = set([" ", "\t", "\n"])

    def advancePos(self) -> None:
        """Advances position for the lexer.

        The function moves `_readPos` and `_curPos` attributes.
        Also calculates if input is exhausted and sets `_eof` to True.
        """
        self._curPos = self._readPos

        if self._curPos >= len(self.input):
            self._eof = True

        self._readPos += 1

    def reversePos(self) -> None:
        """Reverse the position for the lexer.

        This function does the exact opposite of `advancePos`.
        It reverses the position of `_readPos` and `_curPos`

        Useful because of the design of the lexer.
        """
        self._readPos = self._curPos - 1

        self._curPos -= -2

        self.advancePos()

    def consumeWhitespace(self) -> None:
        """Consume whitespaces without returning a token, essentially ignoring them.

        Checks if the current symbol is a valid whitespace and ignores it.
        Does this till reaching first non-whitespace character.
        """
        while not self._eof and self.input[self._curPos] in self._validWhitespaces:
            self.advancePos()

    def peekToken(self) -> str:
        """Peek into next character.

        Read the character stored in `_readPos`.
        Useful when consuming complex symbols like `>=` or `==`.
        """
        if self._eof:
            return ""
        return self.input[self._readPos]

    def nextToken(self) -> token.Token:
        """Consume the current input and return a TOKEN.

        Returns a `token.Token` object at every call.

        This lexer advances the position of the input before consuming it.
        This means

        - `_curPos` is uninitalized before calling this function for the first time.
        - `_readPos` is set to `0` before calling this function for the first time.

        This also means when consuming some bounded tokens like `integers`, and `strings` or `identifiers`.
        You may need reversing the position.

        Reads the current symbol using `_curPos`.
        Once input is exhausted, only returns EOF Tokens.
        """
        self.advancePos()
        self.consumeWhitespace()

        if self._eof:
            return token.Token(type=token.EOF, value="")

        curInput = self.input[self._curPos]

        if curInput.isnumeric():
            number = self.consumeNumber()
            return token.Token(type=token.NUMBER, value=number)

        if curInput.isalpha():
            ident = self.consumeIdentifier()
            return token.Token(type=token.IDENT, value=ident)

        if curInput == '"':
            string = self.consumeString()
            return token.Token(type=token.STRING, value=string)

        match curInput:
            case "+":
                return token.Token(type=token.PLUS, value=curInput)
            case "-":
                return token.Token(type=token.MINUS, value=curInput)
            case "*":
                return token.Token(type=token.STAR, value=curInput)
            case "/":
                return token.Token(type=token.SLASH, value=curInput)
            case "(":
                return token.Token(type=token.LROUND, value=curInput)
            case ")":
                return token.Token(type=token.RROUND, value=curInput)
            case "{":
                return token.Token(type=token.LCURLY, value=curInput)
            case "}":
                return token.Token(type=token.RCURLY, value=curInput)
            case "[":
                return token.Token(type=token.LSQUARE, value=curInput)
            case "]":
                return token.Token(type=token.RSQUARE, value=curInput)
            case ":":
                return token.Token(type=token.COLON, value=curInput)
            case _:
                return token.Token(type=token.ILLEGAL, value=curInput)

    def consumeIdentifier(self) -> str:
        """Consume alphabetical characters and return IDENTIFIER token.

        Because it reads till the first non-alphabetical character. The lexer would call `advancePos()` when invoked next time.
        Thus ignoring the input adjacent to the identifier.


        - `hello) 1`. The function moves till and including ). Which means the `nextToken()` method when called, would ignore the `)`.
        - This is the reason the `reversePos` function is used.
        """
        start = self._curPos
        while self._curPos < len(self.input) and self.input[self._curPos].isalpha():
            self.advancePos()
        end = self._curPos

        # Need to call or else input adjacent to the identifier would be ignored.
        self.reversePos()

        return self.input[start:end]

    def consumeNumber(self) -> str:
        """Consume numeric input and return NUMBER token..

        It consumes all the numric characters including infinite number of `.`(periods).
        This means `1.23.4.4.5` is a valid number for the `lexer.`. But the `parser`.
        Would consider not a valid number and generate syntax error.

        Because it reads till the first non-numerical character.
        The lexer would call `advancePos()` when invoked next time.
        Thus ignoring the input adjacent to the identifier.
        """
        start = self._curPos
        while self._curPos < len(self.input) and (
            self.input[self._curPos].isnumeric() or self.input[self._curPos] == "."
        ):
            self.advancePos()

        end = self._curPos

        # Need to call or else input adjacent to the identifier would be ignored.
        self.reversePos()

        return self.input[start:end]

    def consumeString(self) -> str:
        """Consume input between quotes and return STRING token..

        It consumes all the characters till either input is exhausted or `"` is reached.
        Technically `"hello` is a valid string in `bsharp`.
        """
        start = self._readPos

        while True:
            self.advancePos()

            if self._eof or self.input[self._curPos] == '"':
                break

        string = self.input[start : self._curPos]
        return string
