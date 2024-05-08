from tkinter import *
import basic
import evaluator
import re

def detect_format(input_str): # Define a regular expression pattern
    pattern = r'(.*) Line: \d+'

# Use re.match to check if the input string matches the pattern
    match = re.match(pattern, input_str)

# Return True if there is a match, otherwise return False
    return bool(match)

def readTheCode():

    theCode = codeEditor.get("1.0", "end-1c") # gets the code from the codeEditor
    linesOfCode = theCode.split('\n')         # split the content into lines
    
    results = basic.lexer(linesOfCode) #
    for obj in results:  
        for i in obj:
            print(i.getType() + " " + i.getValue())
    
    eval = evaluator.evaluate_Tokens(results, 0 ,0 ,0) #
    
    for obj in eval:                                                            #
        print(obj.getName() + " " + obj.getDatatype() + " " + obj.getValue())   #
    
    printProgramResults(evaluator.getPrintOut())

    evaluator.clearVariables()
    evaluator.clearPrintOut()

def printProgramResults(results):

    console.configure(state='normal')         # set the textbox state to normal to be able to configure it
    console.delete(1.0, END)                  # clear the console of any text

    for obj in results:          
        if detect_format(obj):
            console.insert(END,  obj + '\n')   
            break
        else:         # display the type and their values
            console.insert(END,  obj + '\n')

    
    console.configure(state='disabled')       # disable textbox so that the contents of the console cannot be modified


window = Tk()
window.title("CMSC141")

run_button = Button(window, text="Run Code", command=readTheCode)
run_button.grid(row=0, column=0, columnspan=2, sticky="nsew")  # Centered button with columnspan=2

codeEditor = Text(window)
codeEditor.configure(background='#1e1e1e', foreground='#a3d5ff', font=('Courier New', 15))
codeEditor.grid(row=1, column=0, sticky="nsew")

console = Text(window)
console.configure(background='#1e1e1e', foreground='#a3d5ff', font=('Courier New', 15), state='disabled')
console.grid(row=1, column=1, sticky="nsew")

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

window.mainloop()