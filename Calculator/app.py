firstNumber = int(input("Enter first number: "))
secondNumber = int(input("Enter second number: "))

print("Enter the operation you want to perform:")
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")   
operation = input("Enter operation: ")

if operation == "1":
    print("Result: ", firstNumber + secondNumber)

elif operation == "2":
    print("Result: ", firstNumber - secondNumber)

elif operation == "3":
    print("Result: ", firstNumber * secondNumber)

elif operation == "4":
    print("Result: ", firstNumber / secondNumber)

else:
    print("Invalid operation")