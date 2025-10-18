import sys

def better_round(val:float, n_digits:int = 0):
    val *= 10**n_digits
    result = int(val + (0.5 if val >= 0 else -0.5))
    return result / 10**n_digits

def operate_on(text):
    operator = ""

    if "+" in text: operator = "+"
    elif "-" in text: operator = "-"
    elif "*" in text: operator = "*"
    elif "/" in text: operator = "/"
    else: print("skill issue")

    data = text.split(operator)

    print( better_round(float(eval(f"{data[0]}{operator}{data[1]}")), 1),
        better_round(float(eval(f"{data[1]}{operator}{data[0]}")), 1))

inps = []

cases = int(sys.stdin.readline().rstrip())
for caseNum in range(cases):
    inps.append(sys.stdin.readline().rstrip())

for i in inps:
    operate_on(i)