#! /usr/bin/env python3

#MAPPINGS, CLOSE MUST BE 0
OPEN = 7
CLOSE = 0
FORWARD = 1
BACKWARD = 2
INC = 3
DEC = 4
READ = 6
WRITE = 5

DEBUG = False
CHUNK_SIZE = 1000
SIZE = 2;
PROGRAM = [""]
point = 0;
Memory = []
Chunks = []
Ponters = []
Returns = [[]]*SIZE


def readData(memory,ponter,layer):
	if ponter[0] in memory:
		return Chunks[layer][memory[ponter[0]]][ponter[1]]
	else:
		memory[ponter[0]] = len(Chunks[layer])
		Chunks[layer].append([0]*CHUNK_SIZE)
		return 0;

def writeData(memory,ponter,layer,data):
	if ponter[0] in memory:
			Chunks[layer][memory[ponter[0]]][ponter[1]] = data
	else:
		memory[ponter[0]] = len(Chunks[layer])
		Chunks[layer].append([0]*CHUNK_SIZE)
		Chunks[layer][memory[ponter[0]]][ponter[1]] = data

def add(memory,ponter,layer):
	writeData(memory,ponter,layer,readData(memory,ponter,layer)+1)

def subtract(memory,ponter,layer):
	writeData(memory,ponter,layer,readData(memory,ponter,layer)-1)

def increment(ponter):
	ponter[1] = ponter[1] + 1
	if ponter[1] == CHUNK_SIZE:
		ponter[0] = ponter[0] + 1
		ponter[1] = 0

def decrement(ponter):
	ponter[1] = ponter[1] - 1
	if ponter[1] == -1:
		ponter[0] = ponter[0] - 1
		ponter[1] = CHUNK_SIZE - 1


def mainLoop(point,first=False):
	temp = point
	while point < len(PROGRAM):
		if readData(Memory[0], Ponters[0][0],0) == 0 and not first:
			temp = 1
			while True:
				point += 1
				if PROGRAM[point] == "]":
					temp -= 1
				if PROGRAM[point] == "[":
					temp += 1
				if temp == 0:
					return point;
		else:
			while PROGRAM[point] != "]" and point < len(PROGRAM):
				point += 1
				if PROGRAM[point] == "[":
					point = mainLoop(point)
				if PROGRAM[point] == "+":
					add(Memory[0], Ponters[0][0],0)
				if PROGRAM[point] == "-":
					subtract(Memory[0], Ponters[0][0],0)
				if PROGRAM[point] == ">":
					increment(Ponters[0][0])
				if PROGRAM[point] == "<":
					decrement(Ponters[0][0])
				if PROGRAM[point] == ",":
					writeData(Memory[0], Ponters[0][0],0,readData(Memory[1],Ponters[1][0],0))
				if PROGRAM[point] == ".":
					sucsess, error = exec(0)
					if not sucsess:
						print(error)
						raise SystemExit
			point = temp

def exec(level):
	index = level +1
	command = readData(Memory[level],Ponters[level][1],level) % 8
#	print(command)
	if index+1 == SIZE:
		if command == INC:
			add(Memory[index], Ponters[index][0],index)
		if command == DEC:
			subtract(Memory[index], Ponters[index][0],index)
		if command == FORWARD:
			increment(Ponters[index][0])
		if command == BACKWARD:
			decrement(Ponters[index][0])
		if command == OPEN:
			if readData(Memory[index], Ponters[index][0],index) != 0:
				Returns[index].append(Ponters[level][1].copy())
			else:
				temp = 1
				while temp != 0:
					increment(Ponters[level][1])
					if readData(Memory[level],Ponters[level][1],level) % 8 == CLOSE:
						temp -= 1
					if readData(Memory[level],Ponters[level][1],level) % 8 == OPEN:
						temp += 1
				increment(Ponters[level][1])
		if command == READ:
			writeData(Memory[index], Ponters[index][0],index,ord(input("\n :")[0]))
		if command == WRITE:
			if DEBUG:
				print(readData(Memory[index], Ponters[index][0],index))
			else:
				print(chr(readData(Memory[index], Ponters[index][0],index)), end='')
		if command == CLOSE:
			if len(Returns[index]) > 0:
				Ponters[level][1] = Returns[index].pop()
				decrement(Ponters[level][1])
			else:
				return False, "End of sub-program " + str(index) + " reached"

	increment(Ponters[level][1])
	return True, "The command exicuted sucsessfuly"


for i in range(SIZE):
	Memory.append({0:0})
	Ponters.append([[0,0],[0,0]])
	Chunks.append([])
	Chunks[i].append([0]*CHUNK_SIZE)

file = open("./run.ff")
init = True
for line in file:
	if init:
		tempPoint=[0,0]
		for char in line.strip():
			writeData(Memory[0],tempPoint,0,int(char))
			increment(tempPoint)
		init = False
	else:
		for char in line.strip():
			if char in "[]<>+-,.":
			#if char == "[" or char == "]" or char == "<" or char == ">" or char == "+" or char == "-" or char == "," or char == ".":
				PROGRAM.append(char)
file.close()
mainLoop(0,True)
