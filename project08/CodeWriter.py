class Writer:
    op_num = 0
    filename = ""
    asm_code = ""

    segments = {"local": "LCL",
                "argument": "ARG",
                "this": "THIS",
                "that": "THAT"}

    def __init__(self, file):
        self.op_num = 0
        self.filename = file
        self.asm_code = ""

    def write_arithmetics(self, command: str):
        # add
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
                self.asm_code += "D=M"

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
                          f'D; JLT')

    def write_function(self, function_name: str, nVars: int):
        pass

    def write_call(self, function_name: str, nVars: int):
        pass

    def write_return(self):
        pass
