import math

current_num: float = 2
largest_sofar = 0

pow2 = 8.98846567431158e+307
pow11 = 1.7837187326221501e+308

print(pow2 > pow11)

for i in range(100000):
    if current_num > largest_sofar:
        largest_sofar = current_num
        # print(largest_sofar)
    current_num = math.pow(1.1, i)

print(current_num)