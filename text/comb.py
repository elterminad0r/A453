import re

rjlines = []

with open("shakespeare.txt", "r") as sh:
    l = sh.readline()
    while l != "THE TRAGEDY OF ROMEO AND JULIET\n" and l != "":
        l = sh.readline()

    while l != "THE END\n" and l != "":
        l = sh.readline()
        rjlines.append(l)

shake = "".join(rjlines)

for i in re.findall(r"\bp[a-z]*x[a-z]*\b", shake, re.IGNORECASE):
    print(i)
