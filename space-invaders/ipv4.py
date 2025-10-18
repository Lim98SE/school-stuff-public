address = "192.168.0.1".split(".")
valid = True

if len(address) != 4: valid = False

for i in address:
    if int(i) < 0 or int(i) > 0xFF:
        valid = False

print("Valid" if valid else "Invalid")

