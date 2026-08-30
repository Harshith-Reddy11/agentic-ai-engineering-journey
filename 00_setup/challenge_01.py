expression = input("Input:")
calculation = expression.replace("calculate","").strip()
parts = calculation.split()
if len(parts) != 3:
    print("I don't know how to handle that request.")
    exit()
num1 = int(parts[0])
operator = parts[1]
num2 = int(parts[2])
if num2 == 0 and operator == "/":
    print("I don't know how to handle that request.")
    exit()
if operator == "+":
    res = num1+num2
elif operator == "-":
    res = num1-num2
elif operator == "*":
    res = num1*num2
elif operator == "/":
    res = num1/num2
else:
    print("I don't know how to handle that request.")
    # res = None
print("output:", res)
