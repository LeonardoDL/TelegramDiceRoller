from sentence import Sentence
from sentence import Expr
from sentence import Factor
from sentence import Parcel
from sentence import Symbol
import re

class DiceCompiler:
    def __init__(self, doPrint=True):
        self.doPrint = doPrint
        pass

    code = ""
    token = ""
    sentence = None

    doPrint = True
    stop = False
    ident = 1
    message = ""

    def CompileSentence(self, parcode):
        print("Code is \'" + parcode + "\'\n")
        self.code = parcode
        self.nextToken()
        self.sentence = self.Expr()

################## Compiler ###############################################################################################################

    def Sentence(self):
        self.openPrint("Sentence")
        sent = Sentence()

        if self.token == "(":
            self.nextToken()
            
            sent.expr = self.Expr()

            if self.token == ")":
                self.nextToken()
            else:
                self.error("Sentence :: Closing bracket missing!")
        else:
            sent.expr = self.Expr()

        self.closePrint("Sentence")
        return sent
    
    def Expr(self):
        self.openPrint("Expr")
        exp = Expr(prEnable=self.doPrint)
        
        exp.parcels.append(self.Parcel())

        while self.token == "+" or self.token == "-":
            exp.ops += self.token
            self.nextToken()
            if self.token == "+" or self.token == "-" or self.token == "*" or self.token == "/":
                self.error("Token '+', '-', '*' or '/' found where it shouldnt be")

            exp.parcels.append(self.Parcel())
        
        self.closePrint("Expr")
        return exp
    
    def Parcel(self):
        self.openPrint("Parcel")
        parc = Parcel()
        
        parc.factors.append(self.Factor())

        while self.token == "*" or self.token == "/":
            parc.ops += self.token
            self.nextToken()
            if self.token == "+" or self.token == "-" or self.token == "*" or self.token == "/":
                self.error("Token '+', '-', '*' or '/' found where it shouldnt be")

            parc.factors.append(self.Factor())
        
        self.closePrint("Parcel")
        return parc
    
    def Factor(self):
        self.openPrint("Factor")
        fac = Factor()

        fac.symbols.append(self.Symbol())

        while self.token == "d" or self.token == "D":
            self.nextToken()
            if self.token == "+" or self.token == "-" or self.token == "*" or self.token == "/":
                self.error("Token '+', '-', '*' or '/' found where it shouldnt be")
            fac.symbols.append(self.Symbol())

        self.closePrint("Factor")
        return fac

    def Symbol(self):
        self.openPrint("Symbol")
        sym = Symbol()

        if self.token == '(':
            sym.sentence = self.Sentence()

        if self.token.isdigit():
            lookAhead = self.lookToken()
            
            #if lookAhead == '+' or lookAhead == '-' or lookAhead == '*' or lookAhead == '/' or lookAhead == 'd' or lookAhead == 'D':
                #sym.sentence = self.Sentence()

            #else:
            sym.number = self.Number()
            if self.token == "l" or self.token == "L" or self.token == "h" or self.token == "H":
                sym.var = self.Var()

        elif self.token == "l" or self.token == "L" or self.token == "h" or self.token == "H":
            sym.var = self.Var()

        self.closePrint("Symbol")
        return sym

    def Number(self):
        self.openPrint("Number")
        number = -1

        if self.token.isdigit():
            number = int(self.token)
            self.nextToken()
        else:
            self.error("Number :: Token 'number' is missing")
        
        self.closePrint("Number")
        return number

    def Var(self):
        self.openPrint("Var")
        var = '#'

        if self.token == "l" or self.token == "L" or self.token == "h" or self.token == "H":
            var = self.token
            self.nextToken()
        else:
            self.error("Var :: Token 'var' is missing")
        
        self.closePrint("Var")
        return var

################## Print and Error ########################################################################################################

    def openPrint(self, namePrint):
        if self.doPrint == False:
            pass

        print("    ", end='')
        for i in range(1, self.ident):
            print(".   ", end='')
        
        print(namePrint + " ::")
        self.ident += 1
        pass

    def closePrint(self, namePrint):
        if self.doPrint == False:
            pass
        self.ident -= 1
        
        print("    ", end='')
        for i in range(1, self.ident):
            print(".   ", end='')
        
        print(":: " + namePrint)
        pass

    def error(self, message):
        self.stop = True
        print(message)
        if self.message == "":
            self.message = message

################## Lexer ##################################################################################################################

    def nextToken(self):
        old_token = self.token
        self.token = ""
        tok = ""
        toktype = ""
        
        while True:
            if self.code == '':
                break

            if toktype == "end":
                while True:
                    if self.code[0] == ' ':
                        self.code = self.code[1:]
                    else:
                        break
                break
            
            elif self.code[0] == ' ':
                while True:
                    if self.code[0] == ' ':
                        self.code = self.code[1:]
                    else:
                        break
                break
            
            elif self.code[0] == '0' or self.code[0] == '1' or self.code[0] == '2' or self.code[0] == '3' or self.code[0] == '4' or self.code[0] == '5' \
              or self.code[0] == '6' or self.code[0] == '7' or self.code[0] == '8' or self.code[0] == '9':
                
                if toktype == "" or toktype == "number":
                    toktype = "number"
                    tok += self.code[0]
                    self.code = self.code[1:]
                else:
                    break
            
            elif self.code[0] == 'd' or self.code[0] == 'D' or self.code[0] == 'l' or self.code[0] == 'L' or self.code[0] == 'h' or self.code[0] == 'H' \
              or self.code[0] == '(' or self.code[0] == ')' or self.code[0] == '+' or self.code[0] == '-' or self.code[0] == '/' or self.code[0] == '*':

                if toktype == "":
                    tok = self.code[0]
                    self.code = self.code[1:]
                
                #print("Tok/Token are '" + tok + "' / '" + old_token + "'")
                
                toktype = "end"
            
            else:
                self.stop = True
                toktype = "end"
        
        self.token = tok
        print("Token is '" + self.token + "'")
        pass

    def lookToken(self):
        code = self.code
        tok = ""
        toktype = ""
        
        while True:
            if code == '':
                break

            if toktype == "end":
                while True:
                    if code[0] == ' ':
                        code = code[1:]
                    else:
                        break
                break
            
            elif code[0] == ' ':
                while True:
                    if code[0] == ' ':
                        code = code[1:]
                    else:
                        break
                break
            
            elif code[0] == '0' or code[0] == '1' or code[0] == '2' or code[0] == '3' or code[0] == '4' or code[0] == '5' \
              or code[0] == '6' or code[0] == '7' or code[0] == '8' or code[0] == '9':
                
                if toktype == "" or toktype == "number":
                    toktype = "number"
                    tok += code[0]
                    code = code[1:]
                else:
                    break
            
            elif code[0] == 'd' or code[0] == 'D' or code[0] == 'l' or code[0] == 'L' or code[0] == 'h' or code[0] == 'H' \
              or code[0] == '(' or code[0] == ')' or code[0] == '+' or code[0] == '-' or code[0] == '/' or code[0] == '*':

                if toktype == "":
                    tok += code[0]
                    code = code[1:]
                
                toktype = "end"
            
            else:
                self.stop = True
                toktype = "end"
        
        return tok