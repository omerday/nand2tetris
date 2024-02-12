import JackTokenizer
import CompilationEngine
from xml.dom import minidom


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
