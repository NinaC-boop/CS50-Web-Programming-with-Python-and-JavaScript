def announce(f):
    def wrapper():
        print("About to run function...")
        f()
        print("Done with function.")
    return wrapper
# You want to pass the function object hi to your loop() function, not the result of a call to hi() (which is None since hi() doesn't return anything).

# use the decorator with the @ symbol
@announce
def hello():
    print("Hello World!")


hello()