code = """
$X = @NEWL
$vmStartY = !(FFF - 1E0)
INIT:
    SV !(00 + 7C)
    PV
    SV $X
    PC
    SV @A
    GT LOOP

LOOP:
    PC
    GT LOOP
"""

code = code.split("\n")
real_code = []

for i in code: 
    if len(i.strip()) > 0: real_code.append(i.strip().upper())

labels = {}
variables = {}

def parse_expression(line: str):
    if not "!(" in line: return
    cptr = 0
    for i in range(line.count("!(")):
        cptr = line.find("!(", cptr)
        end = line.find(")", cptr)
        numbers = []
        expression = line[cptr + 2:end]

        for x in range(len(expression.split())):
            try:
                numbers.append([x, int(expression[x], base=16)])
            
            except ValueError: numbers.append([x, expression[x]])
        
        real_exp = expression.split()

        print(numbers)

        for i in numbers:
            real_exp[i[0]] = str(i[1])
        
        print("".join(real_exp))

for i in code:
    parse_expression(i)