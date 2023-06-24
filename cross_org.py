#!/usr/bin/env python3

"""Script to input a .puz file and export as an Org-Mode table."""
import sys
from pathlib import Path


def main(args=None):
    """Init and pass into interactive or automatic mode."""
    match len(args):
        case 3 | 4:
            automatic_mode(args)
        case 0:
            import_puz()
        case _:
            print("Please use three or four args for automatic mode or none for interactive mode.")
            exit()


def import_puz():
    """Import the puz file, validate it, and send it to the process func."""
    while True:
        path = str(Path("__file__").parent / Path(input("Welcome to CrossOrg! Please enter the path to your file: ")))
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

    process_puz(puzzle, wh)


def process_puz(source, wh):
    """Extract information and format the puzzle."""
    # Variable setup for later.
    grid = "| "
    columns = 0
    across = ""
    down = ""

    # Read user input and perform string comprehension to get integer sets for
    # puzzle size and clue distribution.

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
    # NOTE: Ask for across/down of clue for each clue.
    for i in source[7:]:
        if source.index(i) % 2 == 0:
            down += "||" + str(i) + "||\n"
        else:
            across += "||" + str(i) + "||\n"

    match len(sys.argv):
        case 4 | 5:
            return (title, grid, across, down)
        case _:
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
        "\n" + ("*" * depth) + " " + title + "\n\n"
        + ("*" * (depth + 1)) + " Grid\n\n"
        + grid + "\n\n"
        + ("*" * (depth + 1)) + " Clues\n\n"
        + "|Solved?|Across|Notes|\n|-+-+-|\n"
        + across
        + "|-+-+-|\n||Down||\n|-+-+-|\n"
        + down
    )

    print(f"\nHere's your formatted puzzle:\n{export}")

    # Append the puzzle to an existing file or create the file if it doesn't exist.
    while True:
        expath = str(Path("__file__").parent / Path(input("Where would you like to export the puzzle to?: ")))
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


def automatic_mode(args):
    """Non-interactive mode."""
    path = str(Path("_file__").parent / Path(args[0]))

    try:
        raw = open(path, encoding="cp1252")
    except FileNotFoundError:
        print("Puzzle not found! Make sure the path is correct.")
        exit()
    else:
        match path.endswith(".puz"):
            case True:
                puzzle = raw.readlines()
                raw.close()
            case _:
                print("That doesn't look like a .puz file!")
                raw.close()
                exit()

    try:
        wh = list(int(x) for x in args[2].lower().split("x")) # noqa
    except ValueError:
        print("Please make sure you're entering the dimensions correctly!")
        exit()
    else:
        match len(wh):
            case 2:
                title, grid, across, down = process_puz(puzzle, wh)
            case _:
                print("Please make sure you're entering the dimensions correctly!") # noqa
                exit()

    match len(sys.argv):
        case 5:
            try:
                depth = int(args[3])
            except ValueError:
                print("Please enter the depth as a positive integer!")
                exit()
            else:
                if depth < 1: print("Please enter depth as a positive integer!"); exit()
        case _:
            depth = 1

    export = (
        "\n" + ("*" * depth) + " " + title + "\n\n"
        + ("*" * (depth + 1)) + " Grid\n\n"
        + grid + "\n\n"
        + ("*" * (depth + 1)) + " Clues\n\n"
        + "|Solved?|Across|Notes|\n|-+-+-|\n"
        + across
        + "|-+-+-|\n||Down||\n|-+-+-|\n"
        + down
    )

    expath = str(Path("__file__").parent / Path(args[1]))

    try:
        save = open(expath, "a")
    except FileNotFoundError:
        print("Export path broken! Please make sure all the directories exist!")
        exit()
    else:
        save.write(export)
        save.close()
        print(f"\nHere's your formatted puzzle:\n{export}\n\nSaved to {expath}!")


# Function call to run the program.
if __name__ == "__main__":
    main(sys.argv[1:])

#  LocalWords:  noqa WxH
