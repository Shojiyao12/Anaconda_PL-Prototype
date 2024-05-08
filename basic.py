import re


class Token:
    def __init__(self, type, value):
        self._type = type
        self._value = value

    def getType(self):
        return self._type
    
    def getValue(self):
        return self._value

def isKeyword(word):
    keywords = ["is", "print", "if", "else", "elif"]

    if word in keywords:
        return True
    else:
        return False
    
def isDatatype(word):
    datatypes = ["int", "float", "string", "boolean", "char"]

    if word in datatypes:
        return True
    else:
        return False
    
def isNumber(num):
    pattern = r'^[+-]?\d+(\.\d+)?$'

    if re.match(pattern, num):
        return True
    else:
        return False
    
def isBoolean(word):
    keywords = ["TRUE", "FALSE"]

    if word in keywords:
        return True
    else:
        return False
    
def isCharacter(c):
    if len(c) == 3 and c[0] == "'" and c[1].isalpha() and c[2] == "'":
        return True
    else:
        return False
    
def isString(word):

    if word[0] == "\"" and word[len(word)-1] == "\"":
        return True
    else:
        return False
    
def isVariableName(var):
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'

    if re.match(pattern, var) and len(var) <= 32:
        return True
    else:
        return False


def isMathOperators(c):
    arithmeticOperators = ["+", "-", "*", "/", "%", "^", "(", ")"]

    if c in arithmeticOperators:
        return True
    else:
        return False
    
def getMathOperator(c):
    if c == "+":
        return "add_operator"
    elif c == "-":
        return "minus_operator"
    elif c == "*":
        return "mult_operator"
    elif c == "/":
        return "div_operator"
    elif c == "%":
        return "mod_operator"
    elif c == "^":
        return "exponent"
    elif c == "(":
        return "open_par"
    elif c == ")":
        return "close_par"
    
def isConditionalOperator(c):
    conditionalOperators = ["=", "!", "<", ">"]

    if c in conditionalOperators:
        return True
    else:
        return False

def getConditionalOperator(cc):
    if cc == "=":
        return "equals"
    elif cc == "==":
        return "equalto"
    elif cc == "!":
        return "not"
    elif cc == "!=":
        return "notequalto"
    elif cc == ">":
        return "greaterthan"
    elif cc == ">=":
        return "greaterthanorequalto"
    elif cc == "<":
        return "lessthan"
    elif cc == "<=":
        return "lessthanorequalto"
    else:
        return None

def getNumericalDatatype(num):
    if isinstance(eval(num), int):
        return "int"
    else:
        return "float"
    
def lexer(linesOfCode):

    oneLineOfTokens = []
    tokens = []

    for line in linesOfCode:  # for every line in the code
        pos = 0
        while pos < len(line):  # for every character in the line
            temp = ""
            
            if line[pos].isdigit():                     # if the character is a digit, append all digits
                while pos < len(line) and (line[pos].isdigit() or line[pos] == "."): 
                    temp += line[pos]    
                    pos += 1
                if isNumber(temp):                        # if the number is valid, add as a token
                    oneLineOfTokens.append(Token(getNumericalDatatype(temp), temp)) 
                else:                                     # if number is invalid, print error
                    oneLineOfTokens.append(Token('NUMBER_ERROR', temp))
                    break
            elif line[pos] == "\"":                       # if a quotation mark is encountered, could be a string
                temp += line[pos]
                pos += 1
                while pos < len(line) and line[pos] != "\"":
                    temp += line[pos]
                    pos += 1     
                try:
                    temp += line[pos]
                except:
                    oneLineOfTokens.append(Token('STRING_ERROR', temp))
                    break
                if isString(temp):                        # if the word is a string, add as token
                    oneLineOfTokens.append(Token('string', temp[1:-1]))  
                    if(pos < len(line)):
                        pos += 1
                else:                                     # if it is invalid
                    oneLineOfTokens.append(Token('STRING_ERROR', temp))
                    break
            elif line[pos] == "'":                        # if a quotation mark is encountered, could be a string
                temp += line[pos]
                pos += 1
                while pos < len(line) and line[pos] != "'":
                    temp += line[pos]
                    pos += 1     
                try:
                    temp += line[pos]
                except:
                    oneLineOfTokens.append(Token('CHARACTER_ERROR', temp))
                    break
                if isCharacter(temp):                      # if the word is a character, add as token
                    oneLineOfTokens.append(Token('char', temp[1:-1]))  
                    if(pos < len(line)):
                        pos += 1
                else:                                     # if it is invalid
                    oneLineOfTokens.append(Token('CHARACTER_ERROR', temp))
                    break
            elif line[pos].isalpha(): 
                while pos < len(line) and (line[pos].isalpha() or line[pos] == "_" or line[pos].isdigit()):
                    temp += line[pos]
                    pos += 1
                if isKeyword(temp):                       # if the word is a keyword, add as a token
                    oneLineOfTokens.append(Token('keyword', temp))  
                elif isDatatype(temp):
                    oneLineOfTokens.append(Token('datatype', temp))
                elif isBoolean(temp):                     # if the word is boolean, add as a token
                    oneLineOfTokens.append(Token('boolean', temp))
                elif isVariableName(temp.lower()):        # if the word is a valid variable name, add as a token
                    oneLineOfTokens.append(Token('variable', temp.lower()))
                else:                                     # if the word is invalid
                    oneLineOfTokens.append(Token('NAME_ERROR', temp))
                    break
            elif isConditionalOperator(line[pos]):        # if it is a conditional operator, determine the specific operator and add as token
                while pos < len(line) and isConditionalOperator(line[pos]):
                    temp += line[pos]
                    pos += 1
                res = getConditionalOperator(temp)
                if res != None:
                    oneLineOfTokens.append(Token(getConditionalOperator(temp), temp))
                else:
                    print("HELLLO")
                    oneLineOfTokens.append(Token("CONDITIONAL_ERROR", temp))
                    break
            elif re.match(r'^ {4}', line[pos:]):          # Match exactly four spaces at the beginning of the line
                oneLineOfTokens.append(Token('indentation', '    '))
                pos += 4
            elif isMathOperators(line[pos]):              # if it is a math operator, determine the specific operator and add as token
                oneLineOfTokens.append(Token(getMathOperator(line[pos]), line[pos]))
                pos += 1
            elif line[pos] == " ":                        # move to the next position if space is encountered
                pos += 1
            else:                                         # anything else, its probably invalid
                oneLineOfTokens.append(Token('CODE_ERROR', temp))
                break

        if len(oneLineOfTokens) == 0: 
            oneLineOfTokens.append(Token('newline', '\n')) 

        tokens.append(oneLineOfTokens)  
        oneLineOfTokens = []
          

    return tokens
