import pygame

tokens = {
    "PC": 0,
    "PV": 1,
    "SV": 2,
    "SX": 3,
    "SY": 4,
    "IX": 5,
    "IY": 6,
    "DX": 7,
    "DY": 8
}

screen_res = (640, 480)
buffer = pygame.Surface(screen_res)

code = """
IX CR 280
SX 00 IY CR 00
SX 00 SY E1F SS RS
"""

code = """
SV 41 PV
"""

code = code.split()
real_code = []

for i in code: 
    if len(i.strip()) > 0: real_code.append(i.strip().upper())

bytecode = []

for i in real_code:
    if i in tokens.keys(): bytecode.append(tokens[i]); continue
    bytecode.append(int(i, base=16))

pc = 0
mem_pointer = [0, 0]
memory = [[0] * 0xFFF] * 0xFFF

def fetch():
    global pc
    pc += 1
    return bytecode[pc]

def set(value):
    memory[mem_pointer[0]][mem_pointer[1]] = value

def read():
    return memory[mem_pointer[0]][mem_pointer[1]]

while pc < len(bytecode):
    opcode = bytecode[pc]

    match opcode:
        case 0:
            print(chr(read()), end="")
        
        case 1:
            print(read())

        case 2:
            arg = fetch()
            set(arg)

    pc += 1
