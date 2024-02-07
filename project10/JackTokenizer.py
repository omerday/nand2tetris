SYMBOLS = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void',
           'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
KEYWORDS = ['{', '}', '[', ']', '(', ')', '.', ',', ';', '+', '-', '*', '/', '&', '|', '>', '<', '=', '~']


class Tokenizer:
    current_token = ""
    remaining_code = ""

    def __init__(self, filepath: str):
        self.current_token = ""
        with open(filepath, "r") as file:
            self.remaining_code = file.read()

    def has_more_tokens(self):
        return self.remaining_code != ""

    def advance(self):
        while (self.remaining_code.startswith(" ") or self.remaining_code.startswith("\n")
               or self.remaining_code.startswith("\t")):
            self.remaining_code = self.remaining_code[1:]
        while self.has_more_tokens():
            for keyword in KEYWORDS:
                if self.remaining_code.startswith(keyword):
                    self.current_token = keyword
                    self.remaining_code = self.remaining_code[len(keyword):]
                    return
            for symbol in SYMBOLS:
                if self.remaining_code.startswith(symbol):
                    self.current_token = symbol
                    self.remaining_code = self.remaining_code[len(symbol):]
                    return
            if self.remaining_code[0].isdigit():
                i = 1
                while self.remaining_code[i].isdigit():
                    i = i + 1
                self.current_token = int(self.remaining_code[0, i])
                self.remaining_code = self.remaining_code[i:]
                return
            elif self.remaining_code.startswith("\""):
                i = 1
                while self.remaining_code[i] != "\"":
                    i = i + 1
                self.current_token = self.remaining_code[0: i + 1]
                self.remaining_code = self.remaining_code[i + 1:]
                return
            elif self.remaining_code[0].isalpha():
                i = 1
                while (self.remaining_code[i].isdigit() or self.remaining_code[i].isalpha()
                       or self.remaining_code[i] == "_"):
                    i = i + 1
                self.remaining_code = self.remaining_code[:i]
                return
            else:
                self.remaining_code = self.remaining_code[1:]

    def token_type(self):
        if self.current_token in KEYWORDS:
            return "KEYWORD"
        elif self.current_token in SYMBOLS:
            return "SYMBOL"
        elif self.current_token[0] == "\"":
            return "STRING_CONST"
        elif self.current_token[0].isdigit():
            return "INT_CONST"
        else:
            return "IDENTIFIER"

    def keyword(self):
        return self.current_token.upper()

    def symbol(self):
        return self.current_token

    def identifier(self):
        return self.current_token

    def int_val(self):
        return self.current_token

    def string_val(self):
        return self.current_token[1:-1]
