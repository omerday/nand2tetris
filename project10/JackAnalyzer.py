import JackTokenizer
import CompilationEngine
import sys
import os

path = sys.argv[1]

if os.path.isdir(path):
    asm_code = ""
    if path.endswith("/"):
        path = path[:-1]
    for file in os.listdir(path):
        if file.endswith('.jack'):
            filepath_src = path + '/' + file
            filepath_dest = path + '/' + file[:-5] + ".xml"
            tokenizer = JackTokenizer.Tokenizer(filepath_src)
            compiler = CompilationEngine.Compiler(tokenizer)

            xml_code = compiler.compile_class()
            with open(filepath_dest, 'w') as f:
                f.write(xml_code)
            del tokenizer
            del compiler

else:
    if path.endswith('.jack'):
        filepath_src = path
        filepath_dest = path[:-5] + ".xml"
        tokenizer = JackTokenizer.Tokenizer(filepath_src)
        compiler = CompilationEngine.Compiler(tokenizer)

        xml_code = compiler.compile_class()
        with open(filepath_dest, 'w') as f:
            f.write(xml_code)
        del tokenizer
        del compiler



class Analyzer:
    filepath = ""
    xml_content = ""
    tokenizer = None
    compiler = None

    def __init__(self, path):
        self.filepath = path
        self.xml_content = ""
        self.tokenizer = JackTokenizer.Tokenizer(path)
        self.compiler = CompilationEngine.Compiler(self.tokenizer)

    def analyze(self):
        xml_code = self.compiler.compile_class()
        xml_path = self.filepath[:-5] + "1.xml"
        with open(xml_path, 'w') as file:
            file.write(xml_code)
