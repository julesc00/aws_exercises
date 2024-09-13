
def do_something():
    try:
        a = None
        for i in a:
            return i
    except Exception as e:
        print(e)
    finally:
        print("Cheers!")


def loop_practice():
    lst = [1, 2, 3, 4, 5, 6]
    for n in lst:
        print(n)
        if n == 2:
            print("gotcha!")


def countdown(start):
    while start > 0:
        yield start
        start -= 1

# Example usage of the generator
for number in countdown(5):
    print(number)


