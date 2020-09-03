import enum
from typing import Union


class Comp(enum.Enum):
    # fmt: off
    ZERO        = "0101010"
    ONE         = "0111111"
    MINUS_ONE   = "0111010"
    D           = "0001100"
    A           = "0110000"
    M           = "1110000"
    NOT_D       = "0001101"
    NOT_A       = "0110001"
    NOT_M       = "1110001"
    MINUS_D     = "0001111"
    MINUS_A     = "0110011"
    MINUS_M     = "1110011"
    D_PLUS_ONE  = "0011111"
    A_PLUS_ONE  = "0110111"
    M_PLUS_ONE  = "1110111"
    D_MINUS_ONE = "0001110"
    A_MINUS_ONE = "0110010"
    M_MINUS_ONE = "1110010"
    D_PLUS_A    = "0000010"
    D_PLUS_M    = "1000010"
    D_MINUS_A   = "0010011"
    D_MINUS_M   = "1010011"
    A_MINUS_D   = "0000111"
    M_MINUS_D   = "1000111"
    D_AND_A     = "0000000"
    D_AND_M     = "1000000"
    D_OR_A      = "0010101"
    D_OR_M      = "1010101"
    # fmt: on


class Dest(enum.Enum):
    # fmt: off
    NULL = "000"
    M    = "001"
    D    = "010"
    MD   = "011"
    A    = "100"
    AM   = "101"
    AD   = "110"
    AMD  = "111"
    # fmt: on


class Jump(enum.Enum):
    # fmt: off
    NULL = "000"
    JGT  = "001"
    JEQ  = "010"
    JGE  = "011"
    JLT  = "100"
    JNE  = "101"
    JLE  = "110"
    JMP  = "111"
    # fmt: on


class A:
    class Num:
        """
        Command in the form:
        @1
        @50
        ...
        """

        def __init__(self, value: int):
            self.value = value

        def __str__(self):
            return f"{self.value:016b}"

    class Var:
        """
        Command in the form:
        @LOOP
        @counter
        ...
        """

        def __init__(self, symbol: str, value: int = 0):
            self.symbol = symbol
            self.value = value

        def __str__(self):
            return f"{self.value:016b}"


class L:
    """
    Command in the form:
    (LOOP)
    (LABEL_DEFINITION)
    ...
    """

    def __init__(self, symbol: str):
        self.symbol = symbol

    def __str__(self):
        return ""


class C:
    """
    Command in the form
    dest=comp;jmp
    D=M
    AMD=D;JNE
    0;JMP
    ...
    """

    def __init__(
        self, dest: Dest = Dest.NULL, comp: Comp = Comp.ZERO, jump: Jump = Jump.NULL
    ):
        self.dest = dest
        self.comp = comp
        self.jump = jump

    def __str__(self):
        return f"111{self.comp.value}{self.dest.value}{self.jump.value}"


Command = Union[A.Num, A.Var, L, C]
