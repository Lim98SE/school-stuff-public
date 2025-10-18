for i in range(5):
    text = input("Do you like fish, dogs, or cats? ")

    match text.lower().strip().lstrip():
        case "fish":
            print("Blub blub!")
        
        case "dog":
            print("Woof!")
        
        case "cat":
            print("Meow!")
        
        case _:
            print("what")