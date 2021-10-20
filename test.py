def decode(strReg):

    print(strReg)
    opcode = ""
    registerA = ""
    registerB = ""
    destinationRegister = ""

    if strReg[0:4] == '0000':
        opcode = "HALT"
    elif strReg[0:4] == '0001':
        opcode = "ADD"
        destinationRegister = translateregister(strReg[4:7])
        registerA = translateregister(strReg[7:10])
        if strReg[10] == '0':
            registerB = translateregister(strReg[13:16])
            print(opcode + " " + destinationRegister + " " + registerA + " " + registerB)
        else:
            print(opcode + " " + destinationRegister + " " + registerA + " " + strReg[11:16])
    elif strReg[0:4] == '0010':
        opcode = "AND"
        destinationRegister = translateregister(strReg[4:7])
        registerA = translateregister(strReg[7:10])
        if strReg[10] == '0':
            registerB = translateregister(strReg[13:16])
            print(opcode + " " + destinationRegister + " " + registerA + " " + registerB)
        else:
            print(opcode + " " + destinationRegister + " " + registerA + " " + strReg[11:16])
    elif strReg[0:4] == '0011':
        opcode = "NOT"
        destinationRegister = translateregister(strReg[4:7])
        registerA = translateregister(strReg[7:10])
        print(opcode + " " + destinationRegister + " " + registerA)
    elif strReg[0:4] == '0100':
        opcode = "LD"
        destinationRegister = translateregister(strReg[4:7])
        print(opcode + " " + destinationRegister + " " + strReg[7:16])
    elif strReg[0:4] == '0101':
        opcode = "LDI"
        destinationRegister = translateregister(strReg[4:7])
        print(opcode + " " + destinationRegister + " " + strReg[7:16])
    elif strReg[0:4] == '0110':
        opcode = "LDR"
        destinationRegister = translateregister(strReg[4:7])
        registerA = translateregister(strReg[7:10])
        print(opcode + " " + destinationRegister + " " + registerA + " " + strReg[10:16])
    elif strReg[0:4] == '0111':
        opcode = "ST"
        destinationRegister = translateregister(strReg[4:7])
        print(opcode + " " + destinationRegister + " " + strReg[7:16])
    elif strReg[0:4] == '1000':
        opcode = "STI"
        destinationRegister = translateregister(strReg[4:7])
        print(opcode + " " + destinationRegister + " " + strReg[7:16])
    elif strReg[0:4] == '1001':
        opcode = "STR"
        destinationRegister = translateregister(strReg[4:7])
        registerA = translateregister(strReg[7:10])
        print(opcode + " " + destinationRegister + " " + registerA + " " + strReg[10:16])
    elif strReg[0:4] == '1010':
        opcode = "GET"
        destinationRegister = translateregister(strReg[4:7])
    elif strReg[0:4] == '1011':
        opcode = "PUT"
        destinationRegister = translateregister(strReg[4:7])
    elif strReg[0:4] == '1100':
        opcode = "BR"
        print(opcode + " " + strReg[4:7] + " " + strReg[7:16])
    elif strReg[0:4] == '1101':
        if strReg[4] == 0:
            opcode = "JMP"
        else:
            opcode = "JSR"
        print(opcode + " " + strReg[7:16])
    elif strReg[0:4] == '1110':
        if strReg[4] == 0:
            opcode = "JMPR"
        else:
            opcode = "JSRR"
        registerA = translateregister(strReg[7:10])
        print(opcode + " " + registerA + " " + strReg[10:16])
    elif strReg[0:4] == '1111':
        opcode = "RET"
        print(opcode)
    else:
        print("Invalid Command Exception: Given Command Is Not Valid")


def translateregister(regStr):
    regVal = "R" + str(int(regStr, base=2))
    return regVal


instructionRegisterA = [0,0,1,1,0,0,0,0,0,0,1,1,1,1,1,1]
instructionRegisterB = [0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1]
instructionRegisterC = [0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0]
strI1 = "".join([str(x) for x in instructionRegisterA])
strI2 = "".join([str(x) for x in instructionRegisterB])
strI3 = "".join([str(x) for x in instructionRegisterC])
decode(strI1)
decode(strI2)
decode(strI3)
