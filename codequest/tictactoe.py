sample_input = "OXOXXOXOX"

def check_rows(data):
    for i in range(1, 9, 3):
        row = data[i - 1:i + 2]

        if row[0] == row[1] and row[1] == row[2]:
            return row[0]
    
    return False

def check_columns(data):
    for i in range(3):
        a = 0 + i
        b = 3 + i
        c = 6 + i
        row = data[a] + data[b] + data[c]
        if row[0] == row[1] and row[1] == row[2]:
            return row[0]
    
    return False

def check_diagonal_a(data):
    a = data[0]
    b = data[4]
    c = data[8]

    if a == b and b == c:
        return a
    
    return False

def check_diagonal_b(data):
    a = data[2]
    b = data[4]
    c = data[6]

    if a == b and b == c:
        return a
    
    return False

tests = int(input(""))

for _ in range(tests):
    sample_input = input("").strip().upper()

    funct_tests = [check_rows(sample_input), check_columns(sample_input), check_diagonal_a(sample_input), check_diagonal_b(sample_input)]

    found = 0

    print(sample_input, end="")

    for i in funct_tests:
        if i == "-": continue
        if i:
            print(f" = {i.upper()} WINS")
            found = 1
            break
    
    if not found: print(f" = TIE")