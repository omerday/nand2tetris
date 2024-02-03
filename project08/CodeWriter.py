class Writer:
    op_num = 0
    function_calls = 0
    filename = ""
    asm_code = ""

    segments = {"local": "LCL",
                "argument": "ARG",
                "this": "THIS",
                "that": "THAT"}

    def __init__(self, file):
        self.function_calls = 0
        self.filename = file
        self.asm_code = ""

    def write_arithmetics(self, command: str):
        # add
        print(f"Received Command {command}.")
        if command == "add":
            self.asm_code += (f"@SP\n"
                              f"M=M-1\n"
                              f"A=M\n"
                              f"D=M\n"
                              f"A=A-1\n"
                              f"D=D+M\n"
                              f"M=D\n")
        # sub
        elif command == "sub":
            self.asm_code += (f"@SP\n"
                              f"M=M-1\n"
                              f"A=M\n"
                              f"D=-M\n"
                              f"A=A-1\n"
                              f"D=D+M\n"
                              f"M=D\n")
        # neg
        elif command == "neg":
            self.asm_code += (f"@SP\n"
                              f"A=M-1\n"
                              f"M=-M\n")
        # eq / gt / lt are all written in the same way
        elif command in ["eq", "gt", "lt"]:
            self.asm_code += (f"@SP\n"
                              f"M=M-1\n"
                              f"A=M\n"
                              f"D=-M\n"
                              f"A=A-1\n"
                              f"D=D+M\n"
                              f"@TRUE{self.op_num}\n")
            if command == "eq":
                self.asm_code += "D;JEQ\n"
            elif command == "gt":
                self.asm_code += "D;JGT\n"
            else:
                self.asm_code += "D;JLT\n"
            self.asm_code += (f"D=0\n"
                              f"@CONT{self.op_num}\n"
                              f"0;JMP\n"
                              f"(TRUE{self.op_num})\n"
                              f"D=-1\n"
                              f"(CONT{self.op_num})\n"
                              f"@SP\n"
                              f"A=M-1\n"
                              f"M=D\n")
            self.op_num += 1
        # And
        elif command == "and":
            self.asm_code += (f"@SP\n"
                              f"M=M-1\n"
                              f"A=M\n"
                              f"D=M\n"
                              f"A=A-1\n"
                              f"D=D&M\n"
                              f"M=D\n")
        # Or
        elif command == "or":
            self.asm_code += (f"@SP\n"
                              f"M=M-1\n"
                              f"A=M\n"
                              f"D=M\n"
                              f"A=A-1\n"
                              f"D=D|M\n"
                              f"M=D\n")
        # not
        else:
            self.asm_code += (f"@SP\n"
                              f"A=M-1\n"
                              f"M=!M\n")

    def write_push_pop(self, command: str, segment: str, index: int):
        if command == "C_POP":

            # Temporarily change ARG/LCL/THIS/THAT to the addition
            if segment in self.segments.keys():
                self.asm_code += (f"@{index}\n"
                                  f"D=A\n"
                                  f"@{self.segments[segment]}\n"
                                  f"M=M+D\n")

            # Remove from stack
            self.asm_code += (f"@SP\n"
                              f"M=M-1\n"
                              f"A=M\n"
                              f"D=M\n")

            # Put in temp block
            if segment == "temp":
                self.asm_code += (f"@{5 + index}\n"
                                  f"M=D\n")

            # Put in THIS/THAT
            elif segment == "pointer":
                if index == 0:
                    self.asm_code += "@THIS\n"
                else:
                    self.asm_code += "@THAT\n"
                self.asm_code += "M=D\n"

            # Put in @filname.i
            elif segment == "static":
                self.asm_code += (f"@{self.filename}.{index}\n"
                                  f"M=D\n")

            # Insert value and remove the index back
            elif segment in self.segments.keys():
                self.asm_code += (f"@{self.segments[segment]}\n"
                                  f"A=M\n"
                                  f"M=D\n"
                                  f"@{index}\n"
                                  f"D=A\n"
                                  f"@{self.segments[segment]}\n"
                                  f"M=M-D\n")

        elif command == "C_PUSH":
            # Get value from ARG/THIS/THAT/LCL
            if segment in self.segments.keys():
                self.asm_code += (f"@{index}\n"
                                  f"D=A\n"
                                  f"@{self.segments[segment]}\n"
                                  f"D=D+M\n"
                                  f"A=D\n"
                                  f"D=M\n")

            # Get value from 5+index
            elif segment == "temp":
                self.asm_code += (f"@{5 + index}\n"
                                  f"D=M\n")

            # Get @THIS/THAT content
            elif segment == "pointer":
                if index == 0:
                    self.asm_code += "@THIS\n"
                else:
                    self.asm_code += "@THAT\n"
                self.asm_code += "D=M\n"

            elif segment == "static":
                self.asm_code += (f"@{self.filename}.{index}\n"
                                  f"D=M\n")

            elif segment == "constant":
                self.asm_code += (f"@{index}\n"
                                  f"D=A\n")

            # Add D to stack and raise by 1
            self.asm_code += (f"@SP\n"
                              f"A=M\n"
                              f"M=D\n"
                              f"@SP\n"
                              f"M=M+1\n")

    def write_label(self, label: str):
        self.asm_code += f'({label})\n'

    def write_go_to(self, label: str):
        self.asm_code += (f'@{label}\n'
                          f'0;JMP\n')

    def write_if(self, label: str):
        self.asm_code += (f"@SP\n"
                          f"M=M-1\n"
                          f"A=M\n"
                          f"D=M\n"
                          f'@{label}\n'
                          f'D; JNE\n')

    def write_function(self, function_name: str, nVars: int):
        self.asm_code += f"({function_name})\n"
        for i in range(nVars):
            self.asm_code += f"// Push 0 #{i + 1}\n"
            self.write_push_pop("C_PUSH", "constant", 0)

    def write_call(self, function_name: str, nVars: int):
        self.asm_code += f"// Push Return Address\n"
        self.asm_code += (f"@{function_name}$ret.{self.function_calls}\n"
                          f"D=A\n"
                          f"@SP\n"
                          f"A=M\n"
                          f"M=D\n"
                          f"@SP\n"
                          f"M=M+1\n")

        self.asm_code += f"// Push caller's LCL Value\n"
        self.asm_code += (f"@LCL\n"
                          f"D=M\n"
                          f"@SP\n"
                          f"A=M\n"
                          f"M=D\n"
                          f"@SP\n"
                          f"M=M+1\n")

        self.asm_code += f"// Push caller's ARG Value\n"
        self.asm_code += (f"@ARG\n"
                          f"D=M\n"
                          f"@SP\n"
                          f"A=M\n"
                          f"M=D\n"
                          f"@SP\n"
                          f"M=M+1\n")

        self.asm_code += f"// Push caller's THIS Value\n"
        self.asm_code += (f"@THIS\n"
                          f"D=M\n"
                          f"@SP\n"
                          f"A=M\n"
                          f"M=D\n"
                          f"@SP\n"
                          f"M=M+1\n")

        self.asm_code += f"// Push caller's THAT Value\n"
        self.asm_code += (f"@THAT\n"
                          f"D=M\n"
                          f"@SP\n"
                          f"A=M\n"
                          f"M=D\n"
                          f"@SP\n"
                          f"M=M+1\n")

        self.asm_code += f"// ARG = SP - 5 - nVars\n"
        self.asm_code += (f"@SP\n"
                          f"D=M\n"
                          f"@{5 + nVars}\n"
                          f"D=D-A\n"
                          f"@ARG\n"
                          f"M=D\n")

        self.asm_code += f"// LCL = SP\n"
        self.asm_code += ("@SP\n"
                          "D=M\n"
                          "@LCL\n"
                          "M=D\n")

        self.write_go_to(function_name)
        self.asm_code += f"({function_name}$ret.{self.function_calls})\n"
        self.function_calls += 1

    def write_return(self):
        self.asm_code += ("// endFrame = LCL\n"
                          "@LCL\n"
                          "D=M\n"
                          "@R13\n"
                          "M=D\n"
                          "// retAddr = *(endFrame - 5)\n"
                          "@5\n"
                          "D=D-A\n"
                          "A=D\n"
                          "D=M\n"
                          "@R14\n"
                          "M=D\n")

        self.asm_code += ("// *ARG = pop()\n"
                          "@SP\n"
                          "M=M-1\n"
                          "A=M\n"
                          "D=M\n"
                          "@ARG\n"
                          "A=M\n"
                          "M=D\n")

        self.asm_code += ("// SP = ARG + 1\n"
                          "@ARG\n"
                          "D=M\n"
                          "D=D+1\n"
                          "@SP\n"
                          "M=D\n")

        self.asm_code += ("// THAT = *(endFrame - 1)\n"
                          "@R13\n"
                          "D=M\n"
                          "D=D-1\n"
                          "A=D\n"
                          "D=M\n"
                          "@THAT\n"
                          "M=D\n")

        self.asm_code += ("// THIS = *(endFrame - 2)\n"
                          "@R13\n"
                          "D=M\n"
                          "@2\n"
                          "D=D-A\n"
                          "A=D\n"
                          "D=M\n"
                          "@THIS\n"
                          "M=D\n")

        self.asm_code += ("// ARG = *(endFrame - 3)\n"
                          "@R13\n"
                          "D=M\n"
                          "@3\n"
                          "D=D-A\n"
                          "A=D\n"
                          "D=M\n"
                          "@ARG\n"
                          "M=D\n")

        self.asm_code += ("// LCL = *(endFrame - 4)\n"
                          "@R13\n"
                          "D=M\n"
                          "@4\n"
                          "D=D-A\n"
                          "A=D\n"
                          "D=M\n"
                          "@LCL\n"
                          "M=D\n")

        self.asm_code += ("@R14\n"
                          "A=M\n"
                          "0;JMP\n")

    def write_beginning(self):
        self.asm_code += ("// SP = 256\n"
                          "@256\n"
                          "D=A\n"
                          "@SP\n"
                          "M=D\n"
                          "// call Sys.init\n")
        self.write_call("Sys.init", 0)
