import sys

opcodes = {
	"0": "NOP",
	"1": "LD",
	"2": "LDC",
	"3": "AND",
	"4": "ANDC",
	"5": "OR",
	"6": "ORC",
	"7": "XNOR",
	"8": "STO",
	"9": "STOC",
	"A": "IEN",
	"B": "OEN",
	"C": "JMP",
	"D": "RTN",
	"E": "SKZ",
	"F": "NOP"
}

no_operands = [
	"0",
	"D",
	"E",
	"F"
]

if len(sys.argv) == 1:
	print "No argument provided"
	quit()

# Blew it.
def error(message):
	print "\033[91mDissassembly error: %s.\033[0m" % (message) # Those weird characters are colours, thanks Stackoverflow.

operand = False
output = ""

i = 0
while i < len(sys.argv[1]):
	char = sys.argv[1][i]
	i += 1
	if not (char in opcodes): # See it only ranges from 0-F anyways, so this works.
		error("invalid token '%s'" % char)
		quit()

	elif operand:
		output += " %s" % char
		print output
		operand = False
		continue

	output = opcodes[char]

	if (char in no_operands):
		print output
		i += 1

	else:
		operand = True
		
	