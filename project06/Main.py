import HackAssembler
import sys
import os

arg_name = sys.argv[1]
if arg_name.endswith(".asm"):
    file_to_parse = arg_name
    HackAssembler.parse_file(file_to_parse)

else:
    if os.path.isdir(arg_name):
        if arg_name.endswith("/"):
            path = arg_name[:-1]
        else:
            path=arg_name
        for file in os.listdir(path):
            if file.endswith(".asm"):
                HackAssembler.parse_file(f"{path}/{file}")