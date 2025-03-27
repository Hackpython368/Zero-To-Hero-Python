import random 


randomNumber = random.randint(1, 100)

ChanceCount = 0

print("Those who guess the number in 5 chances will win the game")


while True:
    userNumber = int(input("Enter a number between 1 and 100: "))
    
    if userNumber < randomNumber:
        print("Number is too low")
        ChanceCount += 1

    elif userNumber > randomNumber:
        print("Number is too high")
        ChanceCount += 1
    
    if ChanceCount == 5:
        print("You have exhausted all your chances")
        print("The number was: ", randomNumber)
        break
    
    elif userNumber == randomNumber:
        print("Congratulations! You guessed the number")
        break