import Code, Parser, SymbolTable


def parse_file(file_to_parse: str):
    file_parser = Parser.Parser(file_to_parse)
    table = SymbolTable.Symbols()

    hack_lines=[]

    while file_parser.has_more_lines():
        file_parser.advance()
        if file_parser.instruction_type() == "L_INSTRUCTION":
            table.add_entry(symbol=file_parser.symbol(), address=file_parser.current_line)
            file_parser.lines.remove(file_parser.current_instruction)
            file_parser.current_line -= 1

    file_parser.current_line = -1

    while file_parser.has_more_lines():
        file_parser.advance()
        if file_parser.instruction_type() == "C_INSTRUCTION":
            new_hack_line = "111"
            new_hack_line += Code.comp(file_parser.comp())
            new_hack_line += Code.dest(file_parser.dest())
            new_hack_line += Code.jump(file_parser.jump())
            hack_lines.append(new_hack_line + "\n")
        elif file_parser.instruction_type() == "A_INSTRUCTION":
            sym = file_parser.symbol()
            try:
                address = int(sym)
            except ValueError:
                if table.contain(sym):
                    address = table.get_address(sym)
                else:
                    address = table.add_entry(sym)
            address = bin(address)[2:]
            address = "0000000000000000"[0:16-len(address)] + address + "\n"
            hack_lines.append(address)

    with open(f'{file_to_parse[:file_to_parse.find(".asm")]}.hack', "w") as file:
        file.writelines(hack_lines)

    del table
    del file_parser
    del hack_lines
