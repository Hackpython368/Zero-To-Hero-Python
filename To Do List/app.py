import pickle

def writeData(data):
    with open('To DO List/data.bin', 'wb') as f:
        pickle.dump(data, f)

    return 1

def readData(): 
    with open('To DO List/data.bin', 'rb') as f:
        try:
            return pickle.load(f)
        except EOFError:
            return None

if readData()==None:
    TodoList = []
else:
    TodoList = readData()

while True:
    print("1. Add Task")
    print("2. View Task")
    print("3. Delete Task")
    print("4. Exit")
    choice = input("Enter choice: ")

    if choice == "1":
        task = input("Enter task: ")
        TodoList.append(task)
    if choice == "2":
        for i in range(len(TodoList)):
            print(i+1, TodoList[i])
    if choice == "3":
        task = input("Enter task to delete: ")
        if task in TodoList:
            TodoList.remove(task)
        else:
            print("Task not found")
    if choice == "4":
        writeData(TodoList)
        break