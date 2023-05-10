"""Script to input a .puz file and export as an Org-Mode table."""


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
    # Variable setup for later.
    grid = "| "
    columns = 0
    across = ""
    down = ""

    # Read user input and perform string comprehension to get integer sets for
    # puzzle size and clue distribution.
    while True:
        try:
            wh = list(int(x) for x in input("Please enter the dimensions of the puzzle in the format WxH with no spaces: ").lower().split("x")) # noqa
        except ValueError:
            print("Please make sure you're entering the dimensions correctly!")
            continue
        else:
            match len(wh):
                case 2:
                    break
                case _:
                    print("Please make sure you're entering the dimensions correctly!") # noqa
                    continue
    while True:
        try:
            cluecount = list(int(x) for x in input("Please enter the number of across and down clues in the form AxD: ").lower().split("x")) # noqa
        except ValueError:
            print("Please make sure you're entering the numbers correctly!")
            continue
        else:
            match len(wh):
                case 2:
                    break
                case _:
                    print("Please make sure you're entering the numbers correctly!") # noqa
                    continue

    # Form the source list by splitting and then filtering empty entries.
    source = list(filter(None, ((''.join(source)).strip()).split("\x00")))

    # Form the metadata by splitting, removing some information, adding the
    # "by" join and rejoining into a string. Title is pulled as a string."
    metadata = '-'.join((' by '.join(source[4:6])).split("-")[1:])
    title = metadata[(wh[0] * wh[1] - 1):]

    # Use puz conventions ("-" is empty and "." is black) to build the grid.
    for i in metadata:
        columns += 1
        match i:
            case "-":
                grid += "| "
            case ".":
                grid += "|#"
            case _:
                break

        if columns == wh[0]: grid += "\n| "; columns = 0
    grid += "|"
    columns = 0

    # Assemble clues table by filtering every other entry into the relevant list.
    for i in source[7:(len(source)-1)]:
        if source.index(i) % 2 == 0:
            down += "||" + str(i) + "||\n"
        else:
            across += "||" + str(i) + "||\n"

    export_puz(title, grid, across, down)


def export_puz(title, grid, across, down):
    """Format the data and write it to a file."""
    # Get header depth to export at.
    while True:
        try:
            depth = int(input("Export the puzzle at what header depth?: "))
        except ValueError:
            print("Please enter a number!")
            continue
        else:
            break

    # Assemble the export, a string containing various formatting details plus
    # the grid and clues.
    export = (
        ("\n" + ("*" * depth) + " " + title + "\n\n")
        + (("*" * (depth + 1)) + " Grid\n\n")
        + (grid + "\n\n")
        + (("*" * (depth + 1)) + " Clues\n\n")
        + ("|Solved?|Across|Notes|\n|-+-+-|\n")
        + (across)
        + ("|-+-+-|\n||Down||\n|-+-+-|\n")
        + (down)
    )

    print(f"\nHere's your formatted puzzle:\n{export}")

    # Append the puzzle to an existing file or create the file if it doesn't exist.
    while True:
        expath = input("Where would you like to export the puzzle to?: ")
        try:
            save = open(expath, "a")
        except FileNotFoundError:
            print("Path broken! Make sure the folders exist and try entering an absolute path.")
            continue
        else:
            print(f"Appending {title} to {expath}")
            save.write(export)
            save.close()
            print("Save complete!")
            break


# Functional call to run the program.
import_puz()

#  LocalWords:  noqa WxH
