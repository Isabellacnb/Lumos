from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

window = Tk()
window.title('Lumos IDE')
import subprocess

gpath = ''

def runCode():
    global gpath
    output.delete('1.0', END)
    if gpath == '':
        saveMsg = Toplevel()
        msg = Label(saveMsg, text="Please save the file first")
        msg.pack()
        return
    command = f'python3 ../compiler/parser.py'

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    parsedResult, error = process.communicate()
    parsedEditor.insert('1.0', parsedResult)
    parsedEditor.insert('1.0', error)

def openFile():
    path = askopenfilename(filetypes=[('Lumos Files', '*.nox')])
    with open(path, 'r') as file:
        code = file.read()
        textEditor.delete('1.0', END)
        textEditor.insert('1.0', code)
        global gpath
        gpath = path

def saveFileAs():
    global gpath
    if gpath == '':
        path = asksaveasfilename(filetypes=[('Lumos Files', '*.nox')])
    else:
        path = gpath
    with open(path, 'w') as file:
        code = textEditor.get('1.0', END)
        file.write(code)

parsedEditor = Text(width=40)
parsedEditor.config(bg='black',fg='#1dd605', state='disabled')
parsedEditor.pack(side=RIGHT)

textEditor = Text()
textEditor.config(bg='black',fg='white', insertbackground='white')
textEditor.pack()

output = Text(height=10)
output.config(bg='black',fg='#1dd605')
output.pack()

menuBar = Menu(window)

fileBar = Menu(menuBar, tearoff=0)
fileBar.add_command(label='Open', command = openFile)
fileBar.add_command(label='Save', command = saveFileAs)
fileBar.add_command(label='SaveAs', command = saveFileAs)
fileBar.add_command(label='Exit', command = exit)
menuBar.add_cascade(label='File', menu = fileBar)

runBar = Menu(menuBar, tearoff=0)
runBar.add_command(label='Run', command = runCode)
menuBar.add_cascade(label='Run', menu = runBar)

#btnRun = Button(window, text="Run", command=runCode, bg='black',fg='#1dd605', font=("Helvetica", 20))
#btnRun.place(x = 500, y = 270)
#lbl = Label(window, text="Lumos", fg='white', bg='black', font=("Helvetica", 36)) # image can be added
#lbl.place(x = 220, y = 10)

window.config(menu=menuBar)
window.mainloop()