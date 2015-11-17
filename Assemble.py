# Assembler for goonstation control units.
# http://wiki.ss13.co/Control_Unit
# Use the opcodes on the wiki, please.

# Associative array of opname: opcode.
codes = {
	"NOP":  "0", # Yes NOP can also be F but it doesn't matter.
	"LD":   "1",
	"LDC":  "2",
	"AND":  "3",
	"ANDC": "4",
	"OR":   "5",
	"ORC":  "6",
	"XNOR": "7",
	"STO":  "8",
	"STOC": "9",
	"IEN":  "A",
	"OEN":  "B",
	"JMP":  "C",
	"RTN":  "D",
	"SKZ":  "E"
}
