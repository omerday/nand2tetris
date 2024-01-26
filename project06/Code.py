COMP = {"0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "M": "1110000",
        "!D": "0001101",
        "!A": "0110001",
        "!M": "1110001",
        "-D": "0001111",
        "-A": "0110011",
        "-M": "1110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "M+1": "1110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "M-1": "1110010",
        "D+A": "0000010",
        "D+M": "1000010",
        "D-A": "0010011",
        "D-M": "1010011",
        "A-D": "0000111",
        "M-D": "1000111",
        "D&A": "0000000",
        "D&M": "1000000",
        "D|A": "0010101",
        "D|M": "1010101"}

JUMP = {
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


def comp(code: str):
    return COMP[code]


def dest(code: str):
    binary = ['0', '0', '0']
    if code is None:
        return "".join(binary)
    if code.find("A") != -1:
        binary[0] = '1'
    if code.find("D") != -1:
        binary[1] = '1'
    if code.find("M") != -1:
        binary[2] = '1'
    return "".join(binary)


def jump(code: str):
    if code == "":
        return "000"
    else:
        return JUMP[code]
