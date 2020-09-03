import argparse
import parser
from pathlib import Path

import assembler

if __name__ == "__main__":
    command_line_parser = argparse.ArgumentParser(
        description="nand2tetris Hack assembler"
    )
    command_line_parser.add_argument(
        "source", type=str, nargs=1, help="hack computer .asm file"
    )
    args = command_line_parser.parse_args()

    source = Path(args.source[0]).absolute()
    dest = Path(source.parent) / f"{source.stem}.hack"
    parser = parser.Parser()

    print("🏁 ASSEMBLING 🏁")
    with open(source) as f:
        instructions = parser.parse(f)

    assembler = assembler.Assembler()
    with open(dest, "w") as f:
        f.write(assembler.assemble(instructions))
    print("🏆 DONE 🏆")
