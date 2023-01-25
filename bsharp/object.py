"""Internal Object system for bsharp."""


from typing import Any


NUMBER_OBJ = "NUMBER"
NIL_OBJECT = "NILL"
STRING_OBJ = "STRING"


class Object:
    """Internal Object for all kinds of object."""

    def __init__(self):
        """Construct the Object class."""
        self.value: Any
        self.type: str


class Number(Object):
    """Number Object for evaluation."""

    def __init__(self, val: str):
        """Construct the number."""
        value = None
        try:
            value = int(val)
        except ValueError:
            raise Exception(f"Cannot evaluate {val} as integer.")
        self.value = value
        self.type = NUMBER_OBJ

    def __repr__(self) -> str:
        """Reprsent a Number object as string."""
        return f"{self.value}"


class String(Object):
    """String object for evaluation."""

    def __init__(self, value: str):
        """Construct the string."""
        self.value = value
        self.type = STRING_OBJ

    def __repr__(self) -> str:
        """Represent the string object."""
        return f"{self.value}"


class Nil(Object):
    """None Object for evaluation."""

    def __init__(self):
        """Construct the None object."""
        self.type = NIL_OBJECT
        self.value = "NULL"

    def __repr__(self) -> str:
        """Represent the NIL object."""
        return f"{self.value}"


CONST_NIL = Nil()
