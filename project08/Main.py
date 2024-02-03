import Parser
import CodeWriter
import sys
import os


def parse_file(curr_parser: Parser.Parser, curr_writer: CodeWriter.Writer):
    function_label_prefix = ""
    while curr_parser.has_more_lines():
        curr_parser.advance()
        c_type = curr_parser.command_type()
        print(f"Command - {curr_parser.current_instruction}\nCommandType = {c_type}")
        curr_writer.asm_code += f"// {curr_parser.current_instruction}\n"
        if c_type == "C_FUNCTION":
            function_label_prefix = curr_parser.arg1() + "$"
            curr_writer.write_function(curr_parser.arg1(), curr_parser.arg2())
        elif c_type == "C_LABEL":
            curr_writer.write_label(f"{function_label_prefix}{curr_parser.arg1()}")
        elif c_type == "C_GOTO":
            curr_writer.write_go_to(f"{function_label_prefix}{curr_parser.arg1()}")
        elif c_type == "C_IF":
            curr_writer.write_if(f"{function_label_prefix}{curr_parser.arg1()}")
        elif c_type == "C_CALL":
            curr_writer.write_call(curr_parser.arg1(), curr_parser.arg2())
        elif c_type == "C_RETURN":
            # function_label_prefix = ""
            curr_writer.write_return()
        elif c_type in ["C_POP", "C_PUSH"]:
            curr_writer.write_push_pop(c_type, curr_parser.arg1(), curr_parser.arg2())
        else:
            curr_writer.write_arithmetics(curr_parser.current_instruction.replace(" ", ""))


path = sys.argv[1]

if os.path.isdir(path):
    asm_code = ""
    if path.endswith("/"):
        path = path[:-1]
    first_file = True
    # if "Sys.vm" in os.listdir(path):
    #     parser = Parser.Parser(f"{path}/Sys.vm")
    #     writer = CodeWriter.Writer("Sys")
    #     writer.write_beginning()
    #     parse_file(parser, writer)
    #     asm_code += writer.asm_code
    for file in os.listdir(path):
        if file.endswith(".vm"):
            parser = Parser.Parser(f"{path}/{file}")
            writer = CodeWriter.Writer(file[:-3])
            if first_file:
                first_file = False
                writer.write_beginning()
            parse_file(parser, writer)
            asm_code += writer.asm_code

    folder_name = path.split('/')[-1]
    with open(f"{path}/{folder_name}.asm", "w") as f:
        f.write(asm_code)

else:
    parser = Parser.Parser(path)
    writer = CodeWriter.Writer(path.split("/")[-1][:-3])

    # if parser.has_function():
    #     writer.write_beginning()
    parse_file(parser, writer)

    with open(f"{path[:-3]}.asm", "w") as f:
        f.write(writer.asm_code)
