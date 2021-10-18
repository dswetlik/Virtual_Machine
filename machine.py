
memory = [[None] * 16] * 65536
register = [[None] * 16] * 8
instructionPointer = [None] * 16
instructionRegister = [None] * 16
nzpRegister = [None] * 3


def startmachine():
    initmemory()
    initregisters()


def initmemory():
    for x in range(65536):
        for y in range(16):
            memory[x][y] = 0


def initregisters():
    for x in range(8):
        for y in range(16):
            register[x][y] = 0
    for x in range(16):
        instructionPointer[x] = 0
        instructionRegister[x] = 0
    for x in range(3):
        nzpRegister[x] = 0

