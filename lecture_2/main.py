print("Hello! ")
user_name = input("Please enter your full name: ")
birth_year_str = input("please enter your birth year: ")
birth_year = int(birth_year_str)
current_age = 2025 - birth_year

def generate_profile(age):
    if age >= 0 and age <= 12:
        return "Child"
    elif age >= 13 and age <= 19:
        return "Teenager"
    elif age >= 20:
        return "Adult"
    else:
        return "Invalid age"

hobbies = []
while True:
    hobby = input("Enter your favourite hobby or 'stop' to finish: ")
    if hobby.lower() == "stop":
        break
    hobbies.append(hobby)

life_stage = generate_profile(current_age)

user_profile = {"name": user_name, "age": current_age, "stage": life_stage, "hobbies": hobbies}

print("Profile summary: ")
print(f"Name: {user_name}")
print(f"Age: {current_age}")
print(f"Stage: {life_stage}")
if not user_profile["hobbies"]:
    print("You didn't mention any hobbies.")
else:
    print(f"Favourite hobbies ({len(user_profile['hobbies'])}):")
    for hobby in user_profile["hobbies"]:
        print(hobby)
