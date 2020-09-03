from typing import List

import command


class Assembler:
    def assemble(self, commands: List[command.Command]):
        """
        Assemble commands from parser into its binary form.
        """
        # Ignore empty lines, which are generated from L commands.
        return "\n".join([str(i) for i in commands if str(i)])
