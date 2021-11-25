from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from time import sleep
import subprocess

gpath = ''

def runCode():
    global gpath

    parsedEditor.config(state="normal")
    parsedEditor.delete('1.0', END)
    parsedEditor.config(state="disabled")

    if gpath == '':
        saveMsg = Toplevel()
        msg = Label(saveMsg, text="Please save the file first")
        msg.pack()
        return
    
    command = f'python3 compiler/parser.py {gpath}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    parsedResult, error = process.communicate()
    
    parsedEditor.config(state="normal")
    parsedEditor.insert('1.0', parsedResult)
    parsedEditor.insert('1.0', error)
    parsedEditor.config(state="disabled")

    # Get program name from output
    programName = str(parsedResult).split(' ', 4)[3]
    print(f'python3 compiler/virtual_machine.py {programName}')

    # Run virtual machine with object code .lumos
    command = f'python3 compiler/virtual_machine.py {programName}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    vmResult, error = process.communicate()

    output.config(state="normal")
    output.insert('1.0', vmResult)
    output.insert('1.0', error)
    output.config(state="disabled")

def openFile():
    global gpath
    path = askopenfilename(filetypes=[('Lumos Files', '*.nox')])
    with open(path, 'r') as file:
        code = file.read()
        textEditor.delete('1.0', END)
        textEditor.insert('1.0', code)
        gpath = path
        window.title("Lumos IDE - " + gpath)

def saveFileAs():
    global gpath
    if gpath == '':
        path = asksaveasfilename(filetypes=[('Lumos Files', '*.nox')])
    else:
        path = gpath
    with open(path, 'w') as file:
        code = textEditor.get('1.0', END)
        file.write(code)


if __name__ == '__main__':
    # MAIN Window
    window = Tk()
    window.title('Lumos IDE')
    window.config(bg='black')
    window.maxsize(850, 500)
    window.minsize(850, 500)

    # RIGHT Window to output quads after compilation
    parsedEditor = Text(width=40, height=100)
    parsedEditor.config(bg='black',fg='#1dd605', state='disabled')
    parsedEditor.pack(side=RIGHT)

    # TEXT Window to edit source code
    textEditor = Text()
    textEditor.config(bg='black',fg='white', insertbackground='white')
    textEditor.pack()

    # OUTPUT Window to display LVM output
    output = Text(height=30)
    output.config(bg='black',fg='#1dd605')
    output.pack()

    # MENU BAR to handle commands available
    menuBar = Menu(window)

    fileBar = Menu(menuBar, tearoff=0)
    fileBar.add_command(label='Open', command = openFile)
    fileBar.add_command(label='Save', command = saveFileAs)
    fileBar.add_command(label='Save As', command = saveFileAs)
    fileBar.add_command(label='Exit', command = exit)
    menuBar.add_cascade(label='File', menu = fileBar)

    runBar = Menu(menuBar, tearoff=0)
    runBar.add_command(label='Run', command = runCode)
    menuBar.add_cascade(label='Run', menu = runBar)

    #btnRun = Button(window, text="Run", command=runCode, bg='black',fg='#1dd605', font=("Helvetica", 20))
    #btnRun.place(x = 500, y = 270)

    window.config(menu=menuBar)
    window.mainloop()