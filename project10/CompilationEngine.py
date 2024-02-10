CLASS_VARS = ["static", "field"]
METHOD_DEC = ["constructor", "method", "function"]
VAR_TYPES = ["int", "char", "boolean", "void"]

KEYWORD_CONSTANTS = ["true", "false", "null", "this"]
OPS = ['+', '-', '*', '/', '|', '&', '<', '>', '=']
UNARY_OPS = ['-', '~']

class Compiler:
    tokenizer = None

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def compile_class(self):
        xml_code = (f"<class>\n"
                    f"<keyword> {self.__process__('class')} </keyword>\n")
        xml_code += self.compile_identifier()
        xml_code += f"<symbol> {self.__process__('{')} </symbol>\n"

        while self.tokenizer.current_token in CLASS_VARS:
            xml_code += self.compile_class_var_dec()

        while self.tokenizer.current_token != '}':
            if self.tokenizer.current_token in METHOD_DEC:
                xml_code += self.compile_subroutine()
            else:
                xml_code += self.compile_var_dec()

        xml_code += f"<symbol> {self.__process__('}')} </symbol>\n"
        xml_code += "</class>\n"

    def compile_class_var_dec(self):
        xml_code = (f"<classVarDec>\n"
                    f"<keyword> {self.__process__(self.tokenizer.current_token)} </keyword\n")

        if self.tokenizer.current_token in VAR_TYPES:
            xml_code += f"<keyword> {self.__process__(self.tokenizer.current_token)} </keyword\n"
        else:
            xml_code += self.compile_identifier()

        xml_code += self.compile_identifier()
        while self.tokenizer.current_token != ";":
            xml_code += f"<symbol> {self.__process__(',')} </symbol>\n"
            xml_code += self.compile_identifier()
        xml_code += f"<symbol> {self.__process__(';')} </symbol>\n"
        xml_code += "</classVarDec>\n"

        return xml_code

    def compile_subroutine(self):
        xml_code = (f"<subroutineDec>\n"
                    f"<keyword> {self.__process__(self.tokenizer.current_token)} </keyword>")

        if self.tokenizer.current_token in VAR_TYPES:
            xml_code += f"<keyword> {self.__process__(self.tokenizer.current_token)} </keyword>\n"
        else:
            xml_code += self.compile_identifier()

        xml_code += self.compile_identifier()
        xml_code += f"<symbol> {self.__process__('(')} </symbol>\n"
        xml_code += self.compile_parameter_list()
        xml_code += f"<symbol> {self.__process__(')')} </symbol>\n"
        xml_code += self.compile_subroutine_body()
        return xml_code

    def compile_parameter_list(self):
        xml_code = f"<parameterList>\n"
        if self.tokenizer.current_token != ")":
            if self.tokenizer.current_token in VAR_TYPES:
                xml_code += f"<keyword> {self.__process__(self.tokenizer.current_token)} </keyword>\n"
            else:
                xml_code += self.compile_identifier()
            xml_code += self.compile_identifier()

        while self.tokenizer.current_token != ")":
            xml_code += f"<symbol> {self.__process__(',')} </symbol>\n"
            if self.tokenizer.current_token in VAR_TYPES:
                xml_code += f"<keyword> {self.__process__(self.tokenizer.current_token)} </keyword>\n"
            else:
                xml_code += self.compile_identifier()
            xml_code += self.compile_identifier()

        xml_code += f"</parameterList>\n"
        return xml_code

    def compile_subroutine_body(self):
        xml_code = (f"<subroutineBody>\n"
                    f"<symbol> {self.__process__('{')} </symbol>\n")

        while self.tokenizer.current_token != '}':
            xml_code += "<statements>\n"
            xml_code += self.compile_statement()
            xml_code += "</statements>\n"

        xml_code += (f"<symbol> {self.__process__('}')} </symbol>\n"
                     f"</subroutineBody>\n")
        return xml_code

    def compile_statement(self):
        if self.tokenizer.current_token == "var":
            return self.compile_var_dec()
        elif self.tokenizer.current_token == "let":
            return self.compile_let()
        elif self.tokenizer.current_token == "do":
            return self.compile_do()
        elif self.tokenizer.current_token == "if":
            return self.compile_if()
        elif self.tokenizer.current_token == "while":
            return self.compile_while()
        elif self.tokenizer.current_token == "return":
            return self.compile_if()
        else:
            return

    def compile_var_dec(self):
        xml_code = f"<varDec>\n"
        if self.tokenizer.current_token in VAR_TYPES:
            xml_code += f"<keyword> {self.__process__(self.tokenizer.current_token)} </keyword>\n"
        else:
            xml_code += self.compile_identifier()
        xml_code += self.compile_identifier()

        while self.tokenizer.current_token != ";":
            xml_code += f"<symbol> {self.__process__(',')} </symbol>\n"
            xml_code += self.compile_identifier()

        xml_code += (f"<symbol> {self.__process__(';')} </symbol>\n"
                     f"</varDec>\n")
        return xml_code

    def compile_let(self):
        xml_code = (f"<letStatement>\n"
                    f"<keyword> {self.__process__('let')} </keyword>\n")
        xml_code += self.compile_identifier()
        if self.tokenizer.current_token == '[':
            xml_code += f"<symbol> {self.__process__('[')} </symbol>\n"
            xml_code += self.compile_expression()
            xml_code += f"<symbol> {self.__process__(']')} </symbol>\n"
        xml_code += f"<symbol> {self.__process__('=')} </symbol>\n"
        xml_code += self.compile_expression()
        xml_code += (f"<symbol> {self.__process__(';')} </symbol>\n"
                     f"</letStatement>\n")
        return xml_code

    def compile_if(self):
        xml_code = (f"<ifStatement>\n"
                    f"<keyword> {self.__process__('if')} </keyword>\n"
                    f"<keyword> {self.__process__('(')} </keyword>\n")

        xml_code += self.compile_expression()

        xml_code += (f"<keyword> {self.__process__(')')} </keyword>\n"
                     f"<keyword> {self.__process__('{')} </keyword>\n")

        while self.tokenizer.current_token != "}":
            xml_code += self.compile_statement()

        xml_code += (f"<keyword> {self.__process__('}')} </keyword>\n"
                     f"</ifStatement>\n")

    def compile_while(self):
        xml_code = (f"<whileStatement>\n"
                    f"<keyword> {self.__process__('while')} </keyword>\n"
                    f"<keyword> {self.__process__('(')} </keyword>\n")

        xml_code += self.compile_expression()

        xml_code += (f"<keyword> {self.__process__(')')} </keyword>\n"
                     f"<keyword> {self.__process__('{')} </keyword>\n")

        while self.tokenizer.current_token != "}":
            xml_code += self.compile_statement()

        xml_code += (f"<keyword> {self.__process__('}')} </keyword>\n"
                     f"</whileStatement>\n")
        return xml_code

    def compile_do(self):
        xml_code = (f"<doStatement>\n"
                    f"<keyword> {self.__process__('do')} </keyword>\n")

        xml_code += self.compile_identifier()
        if self.tokenizer.current_token == ".":
            xml_code += f"<symbol> {self.__process__('.')} </symbol>\n"
            xml_code += self.compile_identifier()

        xml_code += (f"<symbol> {self.__process__('(')} </symbol>\n"
                     f"<expressionList>\n")
        xml_code += self.compile_expression()
        while self.tokenizer.current_token != ')':
            xml_code += f"<symbol> {self.__process__(',')} </symbol>\n"
            xml_code += self.compile_expression()
        xml_code += (f"</expressionList>\n"
                     f"<symbol> {self.__process__(')')} </symbol>\n"
                     f"</doStatement>\n")
        return xml_code

    def compile_return(self):
        xml_code = (f"<returnStatement>\n"
                    f"<keyword> {self.__process__('return')} </keyword>\n")

        if self.tokenizer.current_token != ';':
            xml_code += self.compile_expression()
        xml_code += f"<symbol> {self.__process__(';')} </symbol>\n"

        return xml_code

    def compile_expression(self):
        pass

    def compile_identifier(self):
        xml_code = ""
        if self.tokenizer.token_type() == "IDENTIFIER":
            xml_code = f"<identifier>{self.__process__(self.tokenizer.current_token)}</identifier>\n"
        return xml_code

    def __process__(self, string):
        return_str = ""
        if self.tokenizer.current_token == string:
            return_str = string
        self.tokenizer.advance()
        return return_str
