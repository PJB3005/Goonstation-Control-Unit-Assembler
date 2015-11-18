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

import re

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

# Associative array of opname: operand regex, note that all are case INSENSTIVE.
# Unincluded opcodes are assumed to not having operands.
# To make sure the code doesn't have invalid operands.
operand_regex = {
	"LD":   "[0-9a-f]",
	"LDC":  "[0-9a-f]",
	"AND":  "[0-7]",
	"ANDC": "[0-7]",
	"OR":   "[0-7]",
	"ORC":  "[0-7]",
	"XNOR": "[0-7]",
	"STO":  "[0-9a-f]",
	"STOC": "[0-9a-f]",
	"IEN":  "[0-7]",
	"OEN":  "[0-7]",
	"JMP":  "[0-9a-f]"
}

# Makes the above array have the actual regex objects as associative value.
def construct_op_regex():
	for opcode in operand_regex:
		regex = re.compile(operand_regex[opcode])
		operand_regex[opcode] = regex

# Blew it.
def error(message, line):
	print "\033[91mAssembly error: %s on line %s.\033[0m" % (message, line) # Those weird characters are colours, thanks Stackoverflow.

construct_op_regex()

file_name = "test.txt"

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

print file(file_name)

f = open(file_name)

char = f.read(1)

while char:
	print "char is " + char
	if char == ";": # Start a comment.
		print "Starting comment"
		comment = True

	elif char == "\n":
		print "newline"
		line += 1
		comment = False
		if awaiting_operand:
			error("missing operand for opcode '%s'" % word, line)
			print "WIP output:" + output
			quit()

		elif not word in codes:
			error("unknown opcode '%s'" % word, line)
			print "WIP output:" + output
			quit()

		word = ""
		word_finished = False
		awaiting_operand = False

	elif comment:
		None

	elif char.isspace():
		if len(word) and not word_finished:
			if not (word in codes):
				error("unknown opcode '%s'" % word, line)
				print "WIP output:" + output
				quit()
	
			word_finished = True
	
			output += codes[word]
	
			if word in operand_regex:
				awaiting_operand = True

	elif awaiting_operand:
		regex = operand_regex[word]
		print regex.search(char, re.IGNORECASE)
		if regex.search(char, re.IGNORECASE) != None:
			error("invalid operand '%s' for opcode '%s'" % (char, word), line)
			print "WIP output:" + output
			quit()

		output += char
		awaiting_operand = False

	else:
		if not word_finished and char.isalpha():
			word += char

		else:
			error("unexpected token '%s'" % char, line)
			print "WIP output:" + output
			quit()

	char = f.read(1)

f.close()
print output