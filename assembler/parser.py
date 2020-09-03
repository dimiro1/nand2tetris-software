import re
from typing import List

import command
import dsl

# fmt: off
_destMap = {
    "null": command.Dest.NULL,
    "M":    command.Dest.M,
    "D":    command.Dest.D,
    "MD":   command.Dest.MD,
    "A":    command.Dest.A,
    "AM":   command.Dest.AM,
    "AD":   command.Dest.AD,
    "AMD":  command.Dest.AMD,
}
# fmt: on

# fmt: off
_compMap = {
    "0":   command.Comp.ZERO,
    "1":   command.Comp.ONE,
    "-1":  command.Comp.MINUS_ONE,
    "D":   command.Comp.D,
    "A":   command.Comp.A,
    "!D":  command.Comp.NOT_D,
    "!A":  command.Comp.NOT_A,
    "-D":  command.Comp.MINUS_D,
    "-A":  command.Comp.MINUS_A,
    "D+1": command.Comp.D_PLUS_ONE,
    "A+1": command.Comp.A_PLUS_ONE,
    "D-1": command.Comp.D_MINUS_ONE,
    "A-1": command.Comp.A_MINUS_ONE,
    "D+A": command.Comp.D_PLUS_A,
    "D-A": command.Comp.D_MINUS_A,
    "A-D": command.Comp.A_MINUS_D,
    "D&A": command.Comp.D_AND_A,
    "D|A": command.Comp.D_OR_A,
    "M":   command.Comp.M,
    "!M":  command.Comp.NOT_M,
    "-M":  command.Comp.MINUS_M,
    "M+1": command.Comp.M_PLUS_ONE,
    "M-1": command.Comp.M_MINUS_ONE,
    "D+M": command.Comp.D_PLUS_M,
    "D-M": command.Comp.D_MINUS_M,
    "M-D": command.Comp.M_MINUS_D,
    "D&M": command.Comp.D_AND_M,
    "D|M": command.Comp.D_OR_M,
}
# fmt: on

# fmt: off
_jumpMap = {
    "null": command.Jump.NULL,
    "JGT":  command.Jump.JGT,
    "JEQ":  command.Jump.JEQ,
    "JGE":  command.Jump.JGE,
    "JLT":  command.Jump.JLT,
    "JNE":  command.Jump.JNE,
    "JLE":  command.Jump.JLE,
    "JMP":  command.Jump.JMP,
}
# fmt: on

# fmt: off
_globalSymbols = {
    "R0":     0,
    "R1":     1,
    "R2":     2,
    "R3":     3,
    "R4":     4,
    "R5":     5,
    "R6":     6,
    "R7":     7,
    "R8":     8,
    "R9":     9,
    "R10":    10,
    "R11":    11,
    "R12":    12,
    "R13":    13,
    "R14":    14,
    "R15":    15,
    "SP":     0,
    "LCL":    1,
    "ARG":    2,
    "THIS":   3,
    "THAT":   4,
    "SCREEN": 16384,
    "KBD":    24576,
}
# fmt: on


class Parser:
    def parse(self, source) -> List[command.Command]:
        """
        Parse hack .asm code and convert it to a list of commands.
        """
        symbols = {**_globalSymbols}
        variable_index = 16

        first_pass_commands = []
        final_pass_commands = []

        # 1. Parse file
        for line_number, line in enumerate(source):
            line = re.sub("//(.+)", "", line).strip()

            # Ignore empty lines
            if not line:
                continue
            elif line.startswith("("):
                first_pass_commands.append(
                    self._parse_label_declaration(line, line_number)
                )
            elif line.startswith("@"):
                first_pass_commands.append(self._parse_a_command(line, line_number))
            else:
                first_pass_commands.append(self._parse_c_command(line, line_number))

        # 2. Process labels
        commands_line_number = 0
        for c in first_pass_commands:
            if type(c) == command.L:
                symbols[c.symbol] = commands_line_number
            else:
                final_pass_commands.append(c)
                commands_line_number += 1

        # 3. Update variables
        for c in final_pass_commands:
            if type(c) == command.A.Var:
                try:
                    value = symbols[c.symbol]
                except KeyError:
                    value = variable_index
                    variable_index += 1
                    symbols[c.symbol] = value
                c.value = value

        return final_pass_commands

    def _parse_label_declaration(self, line: str, line_number: int) -> command.Command:
        match = re.match("\\((.+)\\)", line)
        if not match:
            raise ParserError(f"label expected at line {line_number}")

        return dsl.label(symbol=match.group(1).strip())

    def _parse_a_command(self, line: str, line_number: int) -> command.Command:
        literal_match = re.match("@(\\d+)", line)
        if literal_match:
            value = int(literal_match.group(1).strip())
            return dsl.a(value=value)

        variable_match = re.match("@(.+)", line)
        if not variable_match:
            raise ParserError(f"variable expected at line {line_number}")
        symbol = variable_match.group(1).strip()
        return dsl.a(symbol)

    def _parse_c_command(self, line: str, line_number: int) -> command.Command:
        command_parts = re.split("[=;]", line)

        if len(command_parts) == 0:
            raise ParserError(f"malformed command at line {line_number}")
        elif len(command_parts) == 1:
            try:
                decoded_comp = _compMap[command_parts[0]]
                return dsl.c(comp=decoded_comp)
            except KeyError:
                pass
        elif len(command_parts) == 2:
            if _jumpMap.get(command_parts[1], None) is not None:
                # Jump Command
                try:
                    decoded_comp = _compMap[command_parts[0]]
                    decoded_jump = _jumpMap[command_parts[1]]
                    return dsl.c(comp=decoded_comp, jump=decoded_jump)
                except KeyError:
                    pass
            else:
                # Assign command
                try:
                    decoded_dest = _destMap[command_parts[0]]
                    decoded_comp = _compMap[command_parts[1]]
                    return dsl.c(dest=decoded_dest, comp=decoded_comp)
                except KeyError:
                    pass

        elif len(command_parts) == 3:
            try:
                decoded_dest = _destMap[command_parts[0]]
                decoded_comp = _compMap[command_parts[1]]
                decoded_jmp = _jumpMap[command_parts[2]]
                return dsl.c(dest=decoded_dest, comp=decoded_comp, jump=decoded_jmp)
            except KeyError:
                pass

        raise ParserError(f"malformed command at line {line_number}")


class ParserError(Exception):
    pass
