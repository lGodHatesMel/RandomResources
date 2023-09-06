input_file = "decimalseeds.txt"
output_file = "hexadecimal-seeds.txt"

with open(input_file, "r") as f1, open(output_file, "w") as f2:
    for line in f1:
        decimal = int(line.strip())
        hexadecimal = hex(decimal)[2:]
        f2.write(hexadecimal.upper() + "\n")
