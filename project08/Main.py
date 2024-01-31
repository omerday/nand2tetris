import Parser
import CodeWriter
import sys
import os

path = sys.argv[1]

if os.path.isdir(path):
    asm_code = ""
    if path.endswith("/"):
        path = path[:-1]
    for file in os.listdir(path):
        if file.endswith(".vm"):
            parser = Parser.Parser(f"{path}/{file}")
            writer = CodeWriter.Writer(file[:-3])

            while parser.has_more_lines():
                parser.advance()
                c_type = parser.command_type()
                # writer.asm_code += f"// {parser.current_instruction}\n"
                if c_type in ["C_POP", "C_PUSH"]:
                    writer.write_push_pop(c_type, parser.arg1(), parser.arg2())
                else:
                    writer.write_arithmetics(parser.arg1())
            asm_code += writer.asm_code
    folder_name = path.split('/')[-1]
    with open(f"{path}/{folder_name}.asm", "w") as f:
        f.write(asm_code)

else:
    parser = Parser.Parser(path)
    writer = CodeWriter.Writer(path.split("/")[-1][:-3])

    while parser.has_more_lines():
        parser.advance()
        c_type = parser.command_type()
        writer.asm_code += f"// {parser.current_instruction}\n"
        if c_type in ["C_POP", "C_PUSH"]:
            writer.write_push_pop(c_type, parser.arg1(), parser.arg2())
        else:
            writer.write_arithmetics(parser.arg1())

    with open(f"{path[:-3]}.asm", "w") as f:
        f.write(writer.asm_code)
