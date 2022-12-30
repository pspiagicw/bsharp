"""Token provides tokens for bsharp."""

PLUS = "PLUS"
MINUS = "MINUS"
STAR = "STAR"
SLASH = "SLASH"
COLON = "COLON"


LROUND = "LROUND"
RROUND = "RROUND"
LCURLY = "LCURLY"
RCURLY = "RCURLY"
LSQUARE = "LSQUARE"
RSQUARE = "RSQUARE"

NUMBER = "NUMBER"
IDENT = "IDENT"

STRING = "STRING"

EOF = "EOF"
ILLEGAL = "ILLEGAL"


class Token:
    """Token class stores the type and value of a token.

    Attributes:
        Token only needs whay kind of token it is and value of it.

        - Value(str): Actual string value of the token.
        - Type(str): Type of token. Defined by constants.

    Methods:
        These are methods used to check the type of tokens.

        - getType() -> str: Method to retrieve it's type
        - getValue() -> str: Method to retrieve it's value.
    """

    def __init__(self, type: str, value: str) -> None:
        """Construct the token class.

        Initialize the class with it's attributes.
        - Value(str)
        - Type(str)
        """
        self._type = type
        self._value = value

    def getType(self) -> str:
        """Return the token's type."""
        return self._type

    def getValue(self) -> str:
        """Return the token's value."""
        return self._value

    def __str__(self) -> str:
        """Pretty print the token's value/state."""
        return f"Token(type={self._type}, value='{self._value}')"

    def __repr__(self) -> str:
        """Pretty print the token's value/state."""
        return f"Token(type={self._type}, value='{self._value}')"
