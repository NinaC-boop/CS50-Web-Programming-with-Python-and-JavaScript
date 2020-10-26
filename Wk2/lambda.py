people = [
    {"name": "Nina", "house": "Parramatta"},
    {"name": "Johnson", "house": "Epping"},
    {"name": "Chrissy", "house": "Blacktown"},
]

def f(person):
    return person["house"]

# lambda input: returns output
# function that takes an input and returns an output based on it
people.sort(key=lambda person: person["name"])

print(people)