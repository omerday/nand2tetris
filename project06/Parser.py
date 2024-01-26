class Parser:
    lines = []
    current_line = -1
    current_instruction = ""

    def __init__(self, file):
        self.lines = []
        self.current_line = -1
        self.current_instruction = ""
        with open(file, "r") as f:
            file_lines = f.readlines()
            for line in file_lines:
                line = line.replace(" ", "")
                line = line.replace("\n", "")
                comment_position = line.find("/")
                if comment_position != -1:
                    line = line[:comment_position]
                if line != "":
                    self.lines.append(line)

    def has_more_lines(self):
        return self.current_line + 1 < len(self.lines)

    def advance(self):
        self.current_line += 1
        self.current_instruction = self.lines[self.current_line]

    def instruction_type(self):
        if self.current_instruction[0] == '@':
            return "A_INSTRUCTION"
        elif self.current_instruction[0] == '(' and self.current_instruction[-1] == ')':
            return "L_INSTRUCTION"
        else:
            return "C_INSTRUCTION"

    def symbol(self):
        if self.current_instruction[0] == '@':
            return self.current_instruction[1:]
        else:
            return self.current_instruction[1:-1]

    def dest(self):
        equal_index = self.current_instruction.find("=")
        if equal_index == -1:
            return None
        else:
            return self.current_instruction[:equal_index]

    def comp(self):
        equal_index = self.current_instruction.find("=")
        end_sign = self.current_instruction.find(";")

        if end_sign == -1:
            if equal_index == -1:
                return self.current_instruction
            else:
                return self.current_instruction[equal_index + 1:]
        else:
            if equal_index == -1:
                return self.current_instruction[:end_sign]
            else:
                return self.current_instruction[equal_index + 1:end_sign]

    def jump(self):
        start_sign = self.current_instruction.find(";")
        if start_sign == -1:
            return ""
        else:
            return self.current_instruction[start_sign + 1:]
