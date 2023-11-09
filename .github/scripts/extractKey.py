import re
import sys

# Define a regular expression pattern to match variable assignments.
VAR_REGEX = re.compile(r"\w+ = (\w+)")

# Define a function to convert a hexadecimal string to an integer.
def toInt(num: str) -> int:
    if num.startswith("0x"):
        return int(num, 16)
    return int(num)

# Define a function to extract pairs of integers from a script.
def getPairs(file: str) -> list[list[int]]:
    with open(file, "r", encoding="utf-8") as script:
        scriptText = script.read()

        # Find the "switch" code block.
        switchIndex = scriptText.rfind("switch")
        breakIndex = scriptText.index(" = partKey")
        switchCode = scriptText[switchIndex:breakIndex]

        # print("Found 'switch' code block:")
        # print(switchCode)

        indexes = []
        # Iterate through variables in the "switch" code block.
        for variable in VAR_REGEX.findall(switchCode):
            # Create a regular expression pattern to find assignments to the variable.
            regex = re.compile(rf" {variable} = (\w+)[,|;|\n]")
            match = regex.search(scriptText)
            if match is not None:
                index_value = match.group(1)
                int_index = toInt(index_value)
                indexes.append(int_index)
                # print(f"Variable '{variable}' found with value: {index_value}, converted to integer: {int_index}")

        # Chunk the list of indexes into pairs.
        pairs = [indexes[i:i + 2] for i in range(0, len(indexes), 2)]
        # print("Generated pairs:")
        # print(pairs)
        return pairs

# Check if the correct number of command-line arguments is provided.
if len(sys.argv) == 3:
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # print(f"Input file: {input_file}")
    # print(f"Output file: {output_file}")

    pairs = getPairs(input_file)

    # Write the pairs to the output file.
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(str(pairs))
