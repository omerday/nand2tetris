import JackTokenizer
import CompilationEngine
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
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            print(f"token - {self.tokenizer.current_token}, token type = {self.tokenizer.token_type()}")