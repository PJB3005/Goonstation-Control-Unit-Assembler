'''
 Assembler for Goonstation control units.
 http://wiki.ss13.co/Control_Unit
 Use the opcodes on the wiki, please.

 Example of the assembly code:
 
 AND  0 ;ANDs RR with input 0 (!RR), which always results in 0 (set RR to 0)
 IEN  0 ;RR is 0, so this will set IEN to 1
 OEN  0 ;same thing for OEN
 LD   1 ;loads input 1 into RR (this clears it)
 SKZ
 STO  8 ;store it in RAM 1 if it's 1
 LD   2 ;load off input
 SKZ
 STOC 8 ;if off input is on, put 0 in RAM 1
 LD   8 ;get RAM 1
 SKZ
 STO  0 ;output it if RAM 1 is on

 Credits to the Goonstation wiki for that code snippet.
'''

import sys

if len(sys.argv) == 1:
	print "No argument provided"
	quit()

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

# Associative array of opname: valid characters, note that all are case INSENSTIVE (should be written uppercase in this list though).
# Unincluded opcodes are assumed to not having operands.
# To make sure the code doesn't have invalid operands.
valids_num = ["0", "1", "2", "3", "4", "5", "6", "7"]

valids_hex = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

operand_valids = {
	"LD":   valids_hex,
	"LDC":  valids_hex,
	"AND":  valids_num,
	"ANDC": valids_num,
	"OR":   valids_num,
	"ORC":  valids_num,
	"XNOR": valids_num,
	"STO":  valids_hex,
	"STOC": valids_hex,
	"IEN":  valids_num,
	"OEN":  valids_num,
	"JMP":  valids_hex
}

# Blew it.
def error(message, line):
	print "\033[91mAssembly error: %s on line %s.\033[0m" % (message, line) # Those weird characters are colours, thanks Stackoverflow.

file_name = sys.argv[1]

# Cache for the current word.
word = ""

# Have we finished with the word yet?
word_finished = False

# Are we awaiting an operand?
awaiting_operand = False

# Are we in a comment? (;)
comment = False

# Line number we're currently at.
line = 1

# Do I need a comment here?
output = ""

def attempt_word_finish():
	global word_finished
	if len(word) and not (word_finished):
		if not (word in codes):
			error("unknown opcode '%s'" % word, line)
			# print "WIP output:" + output
			quit()

		word_finished = True

		global output
		output += codes[word]

		if word in operand_valids:
			global awaiting_operand
			awaiting_operand = True
		else:
			output += "0" # Opcodes without operand still need a 0 after them.

f = open(file_name)

char = f.read(1)

while char:
	# print "char is " + char
	if char == ";": # Start a comment.
		# print "Starting comment"
		comment = True

	elif char == "\n":
		# print "newline"

		attempt_word_finish()

		comment = False
			
		if awaiting_operand:
			error("missing operand for opcode '%s'" % word, line)
			# print "WIP output:" + output
			quit()

		elif not word in codes:
			error("unknown opcode '%s'" % word, line)
			# print "WIP output:" + output
			quit()

		word = ""
		word_finished = False
		awaiting_operand = False
		line += 1

	elif comment:
		None

	elif char.isspace():
		attempt_word_finish()

	elif awaiting_operand:
		upper = char.upper()

		if not (upper in operand_valids[word]):
			error("invalid operand '%s' for opcode '%s'" % (char, word), line)
			# print "WIP output:" + output
			quit()

		output += char
		awaiting_operand = False

	else:
		if not word_finished and char.isalpha():
			word += char

		else:
			error("unexpected token '%s'" % char, line)
			# print "WIP output:" + output
			quit()

	char = f.read(1)

f.close()
print output
	