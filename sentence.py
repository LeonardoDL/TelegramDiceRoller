from random import randint
from random import seed
from math import floor

rollSet = None
printEnable = True

class Sentence:
    def __init__(self):
        
        global rollSet
        if rollSet is None:
            rollSet = []
        
        seed()
        pass

    number = -1
    expr = None
    out = ""

    def process(self, ident):
        printF(ident, "Sentence {")
        
        acc = self.expr.process(ident+1)
        self.out += self.expr.out

        printF(ident, "} Sentence")
        return acc

class Expr:
    def __init__(self, prEnable=True):
        global rollSet
        if rollSet is None:
            rollSet = []
        
        global printEnable
        printEnable = prEnable

        self.parcels = []
        self.ops = []
        pass
    
    parcels = None
    ops = None
    out = ""

    def process(self, ident):
        printF(ident, "Expr {")

        acc = self.parcels[0].process(ident+1)
        self.out = self.parcels[0].out
        self.parcels = self.parcels[1:]
        
        while len(self.ops) > 0:
            if self.out != "" and self.out[-1] != '\n':
                self.out += '\n'

            if self.ops[0] == "+":
                acc += self.parcels[0].process(ident+1)
                self.out += " + " + self.parcels[0].out
            elif self.ops[0] == "-":
                acc -= self.parcels[0].process(ident+1)
                self.out += " - " + self.parcels[0].out
            else:
                print("Error, unknown operation")
                
            self.parcels = self.parcels[1:]
            self.ops = self.ops[1:]

        printF(ident, "} Expr")
        return acc

class Parcel:
    def __init__(self):
        self.factors = []
        self.ops = []
        pass

    factors = None
    ops = None
    out = ""

    def process(self, ident):
        printF(ident, "Parcel {")

        acc = self.factors[0].process(ident+1)
        self.out = self.factors[0].out
        self.factors = self.factors[1:]
        
        while len(self.ops) > 0:
            if self.out != "" and self.out[-1] != '\n':
                self.out += '\n'

            if self.ops[0] == "*":
                acc *= self.factors[0].process(ident+1)
                self.out += " * " + self.factors[0].out
            elif self.ops[0] == "/":
                div = self.factors[0].process(ident+1)
                if div != 0:
                    acc /= div
                else:
                    acc = 0
                self.out += " / " + self.factors[0].out
            else:
                print("Error, unknown operation")
                
            self.factors = self.factors[1:]
            self.ops = self.ops[1:]

        printF(ident, "} Parcel")
        return floor(acc)

class Factor:
    def __init__(self):
        self.symbols = []
        pass

    symbols = None
    out = ""

    def process(self, ident):
        printF(ident, "Factor {")
        global rollSet

        acc = self.symbols[0].process(ident+1)
        if len(self.symbols) > 1:
            self.out = ""
        else:
            self.out = self.symbols[0].out
        self.symbols = self.symbols[1:]
        
        while len(self.symbols) > 0:
            die = self.symbols[0].process(ident+1)
            rolls = []
            if self.symbols[0].sentence is None:
                self.out += "Rolling " + str(acc) + "d" + str(die) + ":\n    "
            else:
                self.out += self.symbols[0].out + " = " + str(die)
                if self.out[-1] != '\n':
                    self.out += '\n'
                self.out += "Rolling " + str(acc) + "d" + str(die) + ":\n    "
            accDice = 0
            
            if acc > 0:
                for i in range(acc):
                    r = roll(die)
                    accDice += r
                    rolls.append(r)
                    self.out += str(r) + " + "
            
            if len(rolls) > 0:
                rollSet.append(rolls)
            acc = accDice
            self.out = self.out[:-3] + " = " + str(acc) + "\n"
                
            self.symbols = self.symbols[1:]

        printF(ident, "} Factor")
        return acc

class Symbol:
    def __init__(self):
        pass

    number = -1
    var = '#'
    out = ""
    sentence = None

    def process(self, ident):
        printF(ident, "Symbol {")
        printF(ident, "Number: '" + str(self.number) + "', Var: '" + self.var + "'")
        
        global rollSet
        acc = 0
        self.out = ""

        if self.number == -1:
            acc = 1
        else:
            if self.number > 9999:
                self.number = 9999
            acc = self.number
            self.out = str(self.number)
        
        if self.sentence != None:
            acc = self.sentence.process(ident+1)
            self.out = self.sentence.out

        if self.var != '#':

            if len(rollSet) <= 0:
                acc = 0
                print("Error, no rolls were made yet")
                raise OrderLulException(self.var)
            elif acc > len(rollSet[-1]):
                print("Error, more variables than rolls")
                raise TooManyVarsException()
            else:
                rolls = rollSet[-1]
                print(rollSet)
                rolls.sort()
                print("acc values is " + str(acc))
                print(rolls)
                print(str(rolls[-1]))

                if self.var == 'l' or self.var == 'L':
                    accValues = 0
                    for i in range(acc):
                        accValues += rolls[0]
                        rolls = rolls[1:]
                    acc = accValues

                if self.var == 'h' or self.var == 'H':
                    accValues = 0
                    for i in range(acc):
                        accValues += rolls[-1]
                        rolls = rolls[:-1]
                    acc = accValues

            self.out += self.var + " (" + str(acc) + ")"

        printF(ident, "} Symbol")
        return acc

def printF(value, message=""):
    global printEnable
    if printEnable == False:
        pass

    print("    ", end='')
    for i in range(1, value):
        print(".   ", end='')
    print(message)

def roll(die):
    print("      rolling...  " + str(die))
    if int(die) < 1:
        return int(0)
    else:
        return randint(1, int(die))

class OrderLulException(Exception):
    def __init__(self, var=""):
        self.var = var
        pass

    var = ""

class TooManyVarsException(Exception):
    def __init__(self):
        pass