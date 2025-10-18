def avg():
    a = float(input("? "))
    b = float(input("? "))
    c = float(input("? "))
    data = [a, b, c]
    result = 0
    seen = 0

    for i in data:
        result += i
        seen += 1
    
    result /= seen
    
    print(result)

avg()