import command


def c(
    dest: command.Dest = command.Dest.NULL,
    comp: command.Comp = command.Comp.ZERO,
    jump: command.Jump = command.Jump.NULL,
):
    return command.C(dest, comp, jump)


def label(symbol: str):
    return command.L(symbol)


def a(symbol: str = "", value: int = 0):
    if symbol:
        return command.A.Var(symbol=symbol, value=value)
    return command.A.Num(value)
