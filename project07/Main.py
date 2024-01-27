import Parser
import CodeWriter
import sys

file = sys.argv[1]
parser = Parser.Parser(file)
writer = CodeWriter.Writer(file.split("/")[-1][:-3])

while parser.has_more_lines():
    parser.advance()
    c_type = parser.command_type()
    # writer.asm_code += f"// {parser.current_instruction}\n"
    if c_type in ["C_POP", "C_PUSH"]:
        writer.write_push_pop(c_type, parser.arg1(), parser.arg2())
    else:
        writer.write_arithmetics(parser.arg1())

with open(f"{file[:-3]}.asm", "w") as f:
    f.write(writer.asm_code)
