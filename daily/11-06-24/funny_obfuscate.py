import base64

with open("base.py") as file:
    raw = file.read()

output = """
kjhkajhsfue4 = \"\"
lkwhuiehjh = 0
for pwqihgls in %INPUT_ARRAY%:
    kjhkajhsfue4 += chr(int(pwqihgls, base=True << True) ^ (lkwhuiehjh % 0o377))
    lkwhuiehjh += 1

exec(kjhkajhsfue4)
"""

data = []

index = 0

for i in raw:
    data.append(bin(ord(i) ^ (index % 0xFF))[2:].zfill(8))
    index += 1

output = output.replace("%INPUT_ARRAY%", str(data))
output = base64.b64encode(output.encode("utf-8"))

final_script = """
import base64;exec(base64.b64decode(\"%DATA%\"))""".strip().replace("%DATA%", output.decode("utf-8"))

with open("obfuscated.py", "w") as file:
    file.write(final_script)