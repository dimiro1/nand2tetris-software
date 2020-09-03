import parser
import unittest
from pathlib import Path

import assembler
import command
import dsl


class ATestCase(unittest.TestCase):
    def test_translation(self):
        test_cases = [
            (0, "0000000000000000"),
            (1, "0000000000000001"),
            (10, "0000000000001010"),
            (32, "0000000000100000"),
            (32767, "0111111111111111"),
        ]

        for case in test_cases:
            cmd = dsl.a(value=case[0])
            self.assertEqual(case[1], str(cmd))


class CTestCase(unittest.TestCase):
    def test_translate(self):
        test_cases = [
            (
                dsl.c(dest=command.Dest.D, comp=command.Comp.M),
                "1111110000010000",
            ),
            (
                dsl.c(dest=command.Dest.D, comp=command.Comp.D_MINUS_M),
                "1111010011010000",
            ),
            (
                dsl.c(dest=command.Dest.A, comp=command.Comp.D_MINUS_ONE),
                "1110001110100000",
            ),
            (dsl.c(dest=command.Dest.M, comp=command.Comp.D), "1110001100001000"),
            (dsl.c(comp=command.Comp.D, jump=command.Jump.JMP), "1110001100000111"),
            (dsl.c(comp=command.Comp.ZERO, jump=command.Jump.JMP), "1110101010000111"),
            (dsl.c(comp=command.Comp.M, jump=command.Jump.JGT), "1111110000000001"),
        ]
        for case in test_cases:
            self.assertEqual(case[1], str(case[0]))


class AssemblerTestCase(unittest.TestCase):
    def test_assemble(self):
        test_cases = [
            ("Rect.asm", "Rect_expected.hack"),
            ("Max.asm", "Max_expected.hack"),
            ("Pong.asm", "Pong_expected.hack"),
        ]

        for case in test_cases:
            source = Path(case[0])
            expected = Path(case[1]).read_text()

            _parser = parser.Parser()
            with open(source) as f:
                commands = _parser.parse(f)

            _assembler = assembler.Assembler()
            hack_code = _assembler.assemble(commands)

            self.assertEqual(expected.strip(), hack_code.strip())


if __name__ == "__main__":
    unittest.main()
