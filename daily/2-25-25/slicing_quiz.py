data = list(range(1, 11))
for i in range(len(data)):
    data[i] = str(data[i])

print(data)

def reverse(data):
    return data[::-1]