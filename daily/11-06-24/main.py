from math import sin, cos, acos

def sign(number):
    if number > 0: return 1
    if number < 0: return -1
    return 0

lat1 = 51.4826
lon1 = 0
lat2 = 41 + (18.5 / 60)
lon2 = -72 - (55 / 60) - (40.44 / 3600)

colat_A = 90 - lat1
colat_B = 90 - lat2

long_diff = abs(lon1 - lon2)

print(long_diff)

difference = acos(cos(colat_A) * cos(colat_B)) + (sin(colat_A) * sin(colat_B) * cos(long_diff)) * 3959

print(difference)

def accept_input(text):
    text = text.split()
    l = len(text)

    if l == 1:
        return float(text[0])
    
    elif l == 2:
        if sign(float(text[0])) == 1:
            return float(text[0]) + (float(text[1]) / 60)
        
        else:
            return float(text[0]) + (-float(text[1]) / 60)
    
    elif l == 3:
        if sign(float(text[0])) == 1:
            return float(text[0]) + (float(text[1]) / 60) + (float(text[2]) / 3600)
        
        else:
            return float(text[0]) + (-float(text[1]) / 60) + (-float(text[2]) / 3600)

print(accept_input("51.4826"))
print(accept_input("41 18.5"))
print(accept_input("-72 55 40.44"))