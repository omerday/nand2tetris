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

    def command_type(self):
        command_parts = self.current_instruction.split(" ")
        return f"C_{command_parts[0].upper()}"

    def arg1(self):
        command_parts = self.current_instruction.split(" ")
        if len(command_parts) == 1:
            return command_parts[0]
        else:
            return command_parts[1]

    def arg2(self):
        command_parts = self.current_instruction.split(" ")
        return int(command_parts[2])
