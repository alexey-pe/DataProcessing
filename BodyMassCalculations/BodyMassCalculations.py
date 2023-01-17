
data = open(r"D:\planning\operations\Масса_тела.txt", "r")
total = 0.0
count = 0
shitTotal = 0.0
weightNumbers = []
for line in data.readlines():
    lastSpaceIndex = line.rfind(" ")
    if lastSpaceIndex < 0:
        continue

    weightStr = line[lastSpaceIndex + 1:]

    if weightStr[0] == "(" and weightStr[-2] == ")":
        withShitStr = weightStr[1:-2]
        beforeLastSpaceIndex = line.rfind(" ", 0, lastSpaceIndex)
        shitlessStr = line[beforeLastSpaceIndex + 1:lastSpaceIndex]
        withShitNumber = float(withShitStr)
        shitlessNumber = float(shitlessStr)
        shitNumber = withShitNumber - shitlessNumber
        shitTotal += shitNumber
        print(weightStr[:-1], withShitStr, beforeLastSpaceIndex, shitlessStr, round(shitNumber, 2))
        continue

    if weightStr[:-1].isalpha():
        continue

    weightNumber = float(weightStr)
    weightNumbers.append(weightNumber)
    total += weightNumber
    # print(weightNumber, len(weightNumbers), total)

print(f"Average equals {round(total / len(weightNumbers), 2)}")

print(f"Total shit equals {round(shitTotal, 2)}")

# print(weightNumbers)

print(max(weightNumbers))
print(min(weightNumbers))
