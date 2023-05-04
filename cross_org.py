import re


def import_puz():
    """Import the puz file, validate it, and send it to the process func."""
    while True:
        path = input("Welcome to CrossOrg! Please enter the path to your file: ")
        try:
            raw = open(path, encoding="cp1252")
        except FileNotFoundError:
            print("Puzzle not found! Make sure the path is correct.")
            continue
        else:
            match path.endswith(".puz"):
                case True:
                    puzzle = raw.readlines()
                    raw.close()
                    break
                case _:
                    print("That doesn't look like a .puz file!")
                    raw.close()
                    continue
    process_puz(puzzle)


def process_puz(source):
    """Extract information and format the puzzle."""
    # Initial processing: join the one-item list into a string, strip, split
    # the string on the empty bites to make a new list, filter out empty
    # entries, and pass it back to the source variable.
    source = list(filter(None, ((''.join(source)).strip()).split("\x00")))
    print(source)

    # Slice the list into a few sub-lists.
    metadata = source[0:6]
    clues = source[6:]
    print(metadata)
    print(clues)


def export_puz(blanks, clues):
    """Format the data and write it to a file."""
    while True:
        try:
            depth = int(input("Export the puzzle at what header depth?: "))
        except ValueError:
            print("Please enter a number!")
            continue
        else:
            break
    export = (
        (("*" * depth) + " Title\n\n")
        + (("*" * (depth + 1)) + " Grid\n\n")
        + (((("|" * 8) + "\n") * 7) + "\n")
        + (("*" * (depth + 1)) + " Clues\n\n")
        + ("|Solved?|Across|Notes|\n|-+-+-|\n")


    )
    print(export)



import_puz()
