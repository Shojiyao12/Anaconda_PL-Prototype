import basic
import re

__variables = []
__printOut = []
stop_print = False

class Variable:
    def __init__(self, name, datatype, value):
        self._name = name
        self._datatype = datatype
        self._value = value

    def getName(self):
        return self._name
    
    def getDatatype(self):
        return self._datatype
    
    def getValue(self):
        return self._value
    
    def setValue(self, newValue):
        self._value = newValue

def getPrintOut():
    return __printOut

def clearPrintOut():
    __printOut.clear()

def appendToPrintOut(value):
    __printOut.append(value)

def saveVariable(variable):
    __variables.append(variable)

def getVariable(index):
    return __variables[index]

def clearVariables():
    __variables.clear()

# Checks if the Variable already exists or has already been declared
def variableAlreadyExists(varName):

    for i, variable in enumerate(__variables):
        if variable.getName() == varName:
            return i  # return the index of the variable
    
    return -1         # return -1 if the variable does not exist

# Extracts the values of each token from a line of code
def extractValuesFromVariables(line, token, lineNumber):

    mathExpression = []

    while token < len(line):

        if line[token].getType() == 'variable':                       # If the token is a variable,
            varPos = variableAlreadyExists(line[token].getValue())    # get its index

            if varPos == -1:                                          # If the variable has not been defined,
                appendToPrintOut("Variable " + line[token].getValue() + " does not exist. Line: " + str(lineNumber)) # print out an error
                break
            else:                                                     # If the variable has already been defined, 
                mathExpression.append(getVariable(varPos).getValue()) # get its value

        else:                                                         # If the token is not a variable,
            mathExpression.append(line[token].getValue())             # append it as a part of the math expression
        token += 1

    print(mathExpression) # to be removed (For checking purposes only)

    return mathExpression

################################ For Calculating Mathematical Expressions ################################

def getResultOfMathExpr(line, token, lineNumber):

    mathExpr = extractValuesFromVariables(line, token, lineNumber)
    return str(calculate(mathExpr))

def calculate(mathExpr):

    if None in mathExpr:
        return "Invalid Expression."
    elif '(' in mathExpr and ')' in mathExpr:                    # If the expression contains a pair of parentheses,
        openParIndex = findInnermostOpenPar(mathExpr)            # find the innermost open parenthesis 
        mathExpr, valueInPar, closeParIndex = getValueInParenthesis(mathExpr, openParIndex) # get the value inside the parentheses

        if closeParIndex == -1:                                  # If there is no closing parenthesis, 
            return "Missing Parentheses."                        # print out an error
        else:                                                    # If a closing parenthesis is found,
            mathExpr.insert(closeParIndex, evaluate(valueInPar)) # calculate what is inside the parenthesis
            return calculate(mathExpr)                           
        
    elif ('(' in mathExpr and ')' not in mathExpr) or ('(' not in mathExpr and ')' in mathExpr): # If a parenthesis is missing,
        return "Missing Parentheses."                                                            # print out an error
    else:                                                        # If the expression is only numbers and operators,
        return evaluate(mathExpr)                                # evaluate the expression

def findInnermostOpenPar(mathExpr):

    # Traverse the array to retrieve the innermost open parenthesis
    for i, element in enumerate(mathExpr): 
        if element == '(':                
            openPar_index = i

    return openPar_index

def getValueInParenthesis(mathExpr, i):

    valueInPar = []

    # get the value inside the parenthesis
    while i < len(mathExpr):
        mathExpr.pop(i)                      # pop the parenthesis and its values from the math expression
        if i >= len(mathExpr):               # If no closing parenthesis was found,
            return mathExpr, valueInPar, -1  
        elif mathExpr[i] == ')':             # If a closing parenthesis is found,
            mathExpr.pop(i)                                         
            return mathExpr, valueInPar, i     
        valueInPar.append(mathExpr[i])
    
    return mathExpr, valueInPar, -1  

def split_math_expr(mathExpr, operator):

    arr1 = []
    arr2 = []

    for i, operand in enumerate(mathExpr):
        if operand == operator:
            arr1 = mathExpr[:i]
            arr2 = mathExpr[i+1:]

    return arr1, arr2

def evaluate(expression):

    operators = ['+', '-', '*', '/', '%', '^']

    try:
        if not any(operator in expression for operator in operators):
            if len(expression) > 1:
                expression[0] = float(expression[0]) * expression[1]
                expression.pop(1)
                return evaluate(expression)
            else: 
                return float(expression[0])

        for operator in operators:
            if operator in expression:
                operand1, operand2 = split_math_expr(expression, operator)
                if operator == '+':
                    return evaluate(operand1) + evaluate(operand2)
                elif operator == '-':
                    return evaluate(operand1) - evaluate(operand2)
                elif operator == '*':
                    return evaluate(operand1) * evaluate(operand2)
                elif operator == '/':
                    return evaluate(operand1) / evaluate(operand2)
                elif operator == '%':
                    return evaluate(operand1) % evaluate(operand2)
                elif operator == '^':
                    return evaluate(operand1) ** evaluate(operand2)
    except:
        return None

################################ For Printing Variables and Strings ################################
    
def printFunc(line, lineNumber):
    print("TYPE IS" + line[1]._type)
    if len(line) > 1 and line[1].getType() == "open_par" and line[len(line)-1].getType() == "close_par":

        if line[2].getType() == "string":                       # if the value to be printed is a string surrounded by quotation marks: print("")
            appendToPrintOut(line[2].getValue())                # print string
        elif line[2].getType() == "variable" and line[3].getType() == "close_par":  # if the value to be printed is a variable: print(i)
            var = variableAlreadyExists(line[2].getValue())     # check if the variable has already been declared
            if var > -1:                                        # if the variable exists, print its value
                appendToPrintOut(getVariable(var).getValue())         
            elif var == -1:                                     # if the variable does not exist, print the error
                appendToPrintOut("Variable " + line[2].getValue() + " does not exist. Line: " + str(lineNumber))
        elif line[2].getType() == 'char':
            appendToPrintOut(line[2].getValue()) 
        elif line[2].getType() == 'boolean':
            appendToPrintOut(line[2].getValue()) 
        elif line[2].getType() == "close_par":                  # if there is no value to be printed: print()
           appendToPrintOut("Nothing to Print. Line: " + str(lineNumber))
        else:                                                           # if the value to be printed is a math expression: print(1+5) or print(i+5)
            appendToPrintOut(getResultOfMathExpr(line, 1, lineNumber))  # evaluate the math expression
    
    elif re.match(r'.*ERROR$', line[2].getType()):
        appendToPrintOut("Error in Token. Line: " + str(lineNumber))
    elif line[1].getType() != "open_par" or line[len(line)-1].getType() != "close_par":
        appendToPrintOut("Missing Parentheses. Line: " + str(lineNumber))
    else:
         appendToPrintOut("Error in Print Function. Line: " + str(lineNumber))

    
################################ For Declaring Variables ################################
        
def variableDeclaration(line, lineNumber):

    variablePosition = variableAlreadyExists(line[0].getValue())
    token = 0

    while token < len(line):
        match token:
            case 0: # variable must not have been declared, otherwise, print an error
                if variablePosition == -1:
                    token += 1
                else: 
                    appendToPrintOut("Variable " + line[0].getValue() + " already exists.")
            case 1: # the token after the variable must be 'is', otherwise, print an error
                if line[token].getValue() == "is":
                    token += 1
                else: 
                    appendToPrintOut("Must be keyword is. Line: " + str(lineNumber))
                    break
            case 2: # the token after the 'is' token must be a datatype, otherwise, print an error
                if line[token].getType() == "datatype":
                    token += 1
                else: 
                    appendToPrintOut("Must be a valid datatype. Line: " + str(lineNumber))
                    break
            case 3: # the token after the datatype must be '=', otherwise, print an error
                if line[token].getType() == "equals":
                    token += 1
                else: 
                    appendToPrintOut("Must be an equal sign. Line: " + str(lineNumber))
                    break
            case 4: # the value
                if len(line) > 5:                                                            # If the value is a math expression,
                    mathExpr = getResultOfMathExpr(line, token, lineNumber)                  # get the result of the math expression
                    saveVariable(Variable(line[0].getValue(), line[2].getValue(), mathExpr)) # save the declared variable
                    break
                else:                                                                           # If the value is a single value or variable,
                    reAssignedVariablePosition = variableAlreadyExists(line[token].getValue())
                    print("VAR DEC")   
                    print(line[2].getValue())    
                    print(line[4].getType()) 
                    if basic.isDatatype(line[token].getType()):                       # Check if the datatypes match, then save
                        if line[2].getValue() == line[4].getType(): 
                            saveVariable(Variable(line[0].getValue(), line[2].getValue(), line[4].getValue()))
                            break
                        else:                                                                   # Otherwise, print an error
                            appendToPrintOut("Datatype Mismatch. Line: " + str(lineNumber))     
                            break
                    elif reAssignedVariablePosition > -1:                                       # If the value to be saved is the value from a variable,
                        if line[2].getValue() == getVariable(reAssignedVariablePosition).getDatatype(): # Check if the datatypes match, then save
                            saveVariable(Variable(line[0].getValue(), line[2].getValue(), getVariable(reAssignedVariablePosition).getValue()))
                            break
                        else:                                                                   # Otherwise, print an error
                            appendToPrintOut("Datatype Mismatch. Line: " + str(lineNumber))
                            break
                    else: 
                        appendToPrintOut("Value Error. Line: " + str(lineNumber))
                        break

################################ For Re-assigning Variable Values ################################
                    
def variableReAssignment(line, lineNumber):

    variablePosition = variableAlreadyExists(line[0].getValue())
    token = 0

    while token < len(line):
        match token:
            case 0:
                if variablePosition == -1:
                    appendToPrintOut("Variable " + line[0].getValue() + " has not been defined. Line: " + str(lineNumber))
                    break
                else: 
                    token += 1
            case 1:
                if line[token].getType() == "equals":
                    token += 1
                else: 
                    appendToPrintOut("Must be an equal sign. Line: " + str(lineNumber))
                    break
            case 2:
                if len(line) > 3:
                    mathExpr = getResultOfMathExpr(line, token, lineNumber)
                    getVariable(variablePosition).setValue(mathExpr)
                    break
                else:
                    reAssignedVariablePosition = variableAlreadyExists(line[token].getValue())
                    if basic.isDatatype(line[token].getType()) and reAssignedVariablePosition == -1:
                        if getVariable(variablePosition).getDatatype() == line[token].getType(): 
                            getVariable(variablePosition).setValue(line[token].getValue()) 
                            break
                        else:
                            appendToPrintOut("Datatype Mismatch. Line: " + str(lineNumber))
                            break
                    elif reAssignedVariablePosition > -1:
                        if getVariable(variablePosition).getDatatype() == getVariable(reAssignedVariablePosition).getDatatype(): 
                            getVariable(variablePosition).setValue(getVariable(reAssignedVariablePosition).getValue())
                            break
                        else:
                            appendToPrintOut("Datatype Mismatch. Line: " + str(lineNumber))
                            break
                    else: 
                        appendToPrintOut("Value Error. Line: " + str(lineNumber))
                        break

################################ For Conditional Statements ################################
                              
def isIf(line, lineNumber, notindentedline):
    condition = evaluate_condition(line, lineNumber, notindentedline)      
    return condition[0]
def is_float(input_str):
    # Check if the string contains a period and all characters on both sides are numeric
    if '.' in input_str and all(char.isdigit() or char == '.' for char in input_str):
        return True
    else:
        return False
def evaluate_condition(line, lineNumber, notindentedline):
    operand1 = None  #first operand of condition, can be a variable or a number
    operand2 = None  #second operand of condition, can be a variable or a number
    operator = None  #operator of condition, can be ==, !=, <, >, <=, >=
    token = line[lineNumber]
    for index in range(lineNumber, len(line)):
        token = line[lineNumber]
        if lineNumber < len(line)-1:
            nexttoken = line[lineNumber+1] #for last token in line
        else:
            nexttoken = None
        print("token value is" + str(token.getValue()))
        if token._type == 'variable':
                varPos = variableAlreadyExists(token.getValue())
                print("var pos is" + str(varPos))
                if (varPos != -1):
                    if operand1 is None:  
                        operand1 = str(getVariable(varPos).getValue())
                        print("operand 1 is" + operand1)
                        if is_float(operand1):                 
                            operand1 = float(operand1)
                        else:
                            operand1 = int(operand1)

                    else:
                        operand2 = str(getVariable(varPos).getValue())
                        if is_float(operand2):
                            operand2 = float(operand2)
                        else:
                            operand2 = int(operand2)
                        break     
                else: 
                    appendToPrintOut("Variable Does Not Exist. Line: " + str(notindentedline))
                if nexttoken._value != 'is':
                    appendToPrintOut("Missing Is. Line: " + str(notindentedline))
        elif token._type == 'int':
            if operand1 is None:
                operand1 = int(token.getValue())
            else:
                operand2 = int(token.getValue())
                break
        elif token._type == 'float':
            if operand1 is None:
                operand1 = float(token.getValue())
            else:
                operand2 = float(token.getValue())
                break
        elif token.getValue() == 'is':
            if nexttoken._type == 'equalto':
                if nexttoken.getValue() == '==':
                    operator = nexttoken.getValue()
            elif nexttoken._type == 'notequalto':
                if nexttoken.getValue() == '!=':
                    operator = nexttoken.getValue()
            elif nexttoken._type == 'lessthan':
                if nexttoken.getValue() == '<':
                    operator = nexttoken.getValue()
            elif nexttoken._type == 'lessthanorequalto':
                if nexttoken.getValue() == '<=':
                    operator = nexttoken.getValue()
            elif nexttoken._type == 'greaterthan':
                if nexttoken.getValue() == '>':
                    operator = nexttoken.getValue()
            elif nexttoken._type == 'greaterthanorequalto':
                if nexttoken.getValue() == '>=':
                    operator = nexttoken.getValue()
            else: 
                appendToPrintOut("Invalid Operator. Line: " + str(lineNumber))
        lineNumber += 1  
    # Evaluate the condition based on the operator
    if operator == '==':
        print(type(operand1))
        print(type(operand2))
        return [operand1 == operand2, index]
    elif operator == '!=':
        return [operand1 != operand2, index]
    elif operator == '>':
        return [operand1 > operand2, index]
    elif operator == '<':
        return [operand1 < operand2, index]
    elif operator == '>=':
        return [operand1 >= operand2, index]
    elif operator == '<=':
        return [operand1 <= operand2, index]
    else:
        appendToPrintOut("Invalid Operator. Line: " + str(lineNumber))
        return [None, index]
    
isindented = 0  #the evaluate_Tokens is split into two parts, one for indented blocks (no variable declaration or nested if/else), so
#this is set to 1 upon block execution, and set back to zero upon end of block execution.
iholder = 0  #since evaluate_tokens is called from the start inside a block, this helps skip all lines until the correct indentation block is reached
#set to 0 on default, but set to whatever i value the called indentation block is located in
skipline = 0  #to skip if execute block has multiple inputs, so if the indentation ends on line 9, upon end of if/elif/else, 
# the code will loop until it is equal to that, since its last "i" value was before the indentation
 #used to create an error if "if" does not exist before elif or else
def evaluate_Tokens(tokens, isindented, iholder, skipline): 
    ifexists = 0   #isindented checks if its inside an else, where it will stop executing if the starting of the line is not indent                                          #line will make sure that inside the else, it starts executing on the indented line
    condition = False                  #This helps execute the code block wherein the condition is true
    dontexecelse = 0     
    if isindented == 1:
        for i, line in enumerate(tokens):
            print("about to start")
            print("the current line is (indented)" + str(i+1))
            lineLength = len(line)         
            if i >= iholder:  #### so since eval_tokens is called from the start, this helps the code skip until it reaches the indentation area
                if line[0]._type != 'indentation':
                    return i                
                if line[1].getValue() == 'print':
                    line.pop(0)
                    printFunc(line, i+1)
                    
                elif line[1]._type == 'variable':
                    if line[2].getValue() == 'is' and lineLength >= 5:
                        line.pop(0)
                        variableDeclaration(line, i+1)
                    elif line[2].getValue() == '=' and lineLength >= 3:
                        line.pop(0)
                        variableReAssignment(line, i+1)
                    else: 
                        appendToPrintOut("Invalid Syntax. Line: " + str(i+1))
                        break
                elif line[0]._type == 'newline':
                    continue
                elif line[0]._type == 'NAME_ERROR':
                    appendToPrintOut(line[0].getValue() + " is invalid. Line: " + str(i+1))
                else:
                    print("Value of first of line is" + str(line[0].getValue()))
                    print("Type of first of line is" + str(line[0]._type))
                    print("nothing was recognized")
                    appendToPrintOut("Invalid Syntax. Line: " + str(i+1))
                    break
    else:     
        for i, line in enumerate(tokens):
            if i >= skipline:
                skipline = 0
                print("the current line (not indent) is" + str(i+1))
                lineLength = len(line)
                if line[0].getValue() == 'print':
                    print("i am the pritn i go print print")
                    printFunc(line, i+1)
                elif line[0].getValue() == 'if':
                    ifexists = 1
                    dontexecelse = 0
                    print("if gaming")
                    conditionres = isIf(line, 1, i+1)
                    condition = conditionres
                    if condition == True:
                        print("if is true")
                        dontexecelse = 1     
                elif line[0].getValue() == 'elif':
                    print("elif gaming")
                    if ifexists == 0:
                        print("no if here sir")
                        appendToPrintOut("No If Located. Line: " + str(i+1))
                    conditionres = isIf(line, 1, i+1)
                    condition = conditionres
                    if condition == True:
                        print("elif true")
                        dontexecelse = 1 
                elif line[0].getValue() == 'else':
                    if ifexists == 0:
                        appendToPrintOut("No If Located. Line: " + str(i+1))
                    if dontexecelse == 0:
                        condition = True
                    else:
                        condition = False
                elif line[0]._type == 'indentation':
                    print("INDENATATION")
                    if condition == True:
                        print("when me")
                        skipline = evaluate_Tokens(tokens, 1, i, 0)        
                        print("when me")
                    condition == False
                elif line[0]._type == 'variable':
                    if line[1].getValue() == 'is' and lineLength >= 5:
                        variableDeclaration(line, i+1)
                    elif line[1].getValue() == '=' and lineLength >= 3:
                        variableReAssignment(line, i+1)
                    else: 
                        appendToPrintOut("Invalid Syntax. Line: " + str(i+1))
                        break
                elif line[0]._type == 'newline':
                    continue
                elif line[0]._type == 'NAME_ERROR':
                    appendToPrintOut(line[0].getValue() + " is invalid. Line: " + str(i+1))
                else:
                    print("Value of first of line is" + str(line[0].getValue()))
                    print("Type of first of line is" + str(line[0]._type))
                    print("nothing was recognized")
                    appendToPrintOut("Invalid Syntax. Line: " + str(i+1))
                    break          
    return __variables