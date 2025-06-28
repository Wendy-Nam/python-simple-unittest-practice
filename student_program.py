# Dictionary to store student information
students = {}

def register_student():
    # Define input items and their data types as tuples
    prompts = [("name", str), ("age", int), ("score", float)]
    info = {}

    # Get input for each item
    for label, caster in prompts:
        value = input(f"Enter student {label}: ")
        # Check if the name is already registered
        if label == "name" and value in students:
            print(f"Student {value} is already registered.\n")
            return
        # Convert input value to specified data type and store
        info[label] = caster(value)

    # Store student information in dictionary
    students[info["name"]] = {"age": info["age"], "score": info["score"]}
    print(f"Student {info['name']} has been registered.\n")

def print_all_students():
    # Handle case when no students are registered
    if not students:
        print("No students are registered.\n")
        return
    print("List of all students:")
    # Print name, age, and score of all students
    for name, info in students.items():
        print(f"Name: {name}, Age: {info['age']}, Score: {info['score']}")
    print()

def search_student():
    # Get the name of the student to search for
    name = input("Enter the name of the student to search: ")
    # Using dictionary's get() method to handle non-existent names without errors
    info = students.get(name)
    if info:
        print(f"Student {name} - Age: {info['age']}, Score: {info['score']}\n")
    else:
        print(f"Student {name} not found.\n")

def calculate_average_score():
    # Handle case when no students are registered
    if not students:
        print("No students registered. Cannot calculate average score.\n")
        return
    # Calculate sum of all student scores and divide by number of students
    avg = sum(s["score"] for s in students.values()) / len(students)
    print(f"The average score of all students is {avg:.2f}.\n")

def main():
    # Define menu numbers and functions as a dictionary
    menu = {
        "1": ("Register Student", register_student),
        "2": ("Print All Students", print_all_students),
        "3": ("Search Student", search_student),
        "4": ("Calculate Average Score", calculate_average_score),
        "5": ("Exit Program", exit)
    }

    while True:
        print("Student Information Management Program")
        # Print menu
        for key, (desc, _) in menu.items():
            print(f"{key}. {desc}")
        # Get menu number input from user
        choice = input("Enter the number of the desired function: ")
        action = menu.get(choice)
        if action:
            # Execute selected function
            action[1]()
        else:
            # Handle invalid input
            print("Invalid input. Please try again.\n")

# Entry point of the program
if __name__ == "__main__":
    main()
