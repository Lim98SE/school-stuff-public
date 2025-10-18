import math

def largest_digit(remaining, current_largest = -100):
    current_digit = remaining % 10

    remaining = math.floor(remaining / 10)

    if (current_digit > current_largest):
        current_largest = current_digit

    if remaining == 0:
        return current_largest
    
    return largest_digit(remaining, current_largest)

def reverse(n):
    n = list(str(n))
    n2 = ""

    for i in range(len(n) - 1, -1, -1):
        n2 += n[i]

    return int(n2)

print(126481, largest_digit(126481))
print(789012, reverse(123456))