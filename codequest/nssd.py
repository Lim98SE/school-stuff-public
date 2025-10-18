cases = int(input())

for i in range(cases):
    inp = input()

    speed = float(inp.split(":")[0])
    distance = float(inp.split(":")[1])

    if (speed == 0): speed = 0.000001

    if (distance / speed) <= 1:
        print("SWERVE")

    elif (distance / speed) <= 5:
        print("BRAKE")

    else:
        print("SAFE")