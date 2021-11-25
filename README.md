<img width="327" alt="Screen Shot 2021-11-24 at 11 25 49" src="https://user-images.githubusercontent.com/31547303/143286325-7af3d2e7-a3f6-4fe2-aff4-8e36e03eaeea.png">

_New to Lumos?_ Lumos is an imperative procedural programming language that can be executed in almost ANY platform.

## Getting started

### Environment Setup

#### Install Python

Lumos is built on top of Python so it is necessary to have it installed on your computer to be able to compile and execute any nox file (source code), specifically Python 3. To check if Python is installed you can run the `python --version` command in your terminal and it should output the current version. In the case it isn’t installed, please refer to the Python documentation.

#### Install LC and LVM + LIDE

Before we can start coding with Lumos we need the Lumos Compiler (LC) to create our object code, known as lumos file, and the Lumos Virtual Machine (LVM) to be able to execute it. You can get all the tools from the Github repository. You can simply download the zip file and you will have all the necessary modules to run your first Lumos program. Inside the Lumos directory you will find the LC as the “parser.py” script and the LVM as “virtual_machine.py”.

Lastly, an optional extra step is to include the use of the Lumos Integrated Development Environment (LIDE), which is our in-house tool to work with nox files directly without a command line. This tool allows you to run without having to link the virtual machine with the lumos file (object code file). LIDE is already included inside the Lumos directory under the ide directory. It is important to note that the LIDE doesn’t support inputs, so it won’t work with the read statement.

### Hello World

Now you are ready to code your first Lumos program! To start, open your favorite text editor and a terminal window. In general the most basic nox file, or Lumos source code program, needs three basic things, a program ID which is set at the beginning of the file as “lumos HelloWorld;”. This ID will be used to generate the lumos file, output object file, NOT the name of the nox file. The other thing a nox file requires is a main task, which is followed by code block surrounded with brackets:

    main {
        !! - This is a comment
        !! - Write your code here
    }

The example above has no code and only has two comments, which are ignored by the LC. When the LVM starts executing your lumos file, it will start on this task. Last element needed for the most basic program is an ending statement, which in Lumos is the “nox;” command. With our three main elements we are now able to include our “Hello World” output command. To print things to the console, Lumos has two options: “print” or “println”. The main difference is that println prints a new line at the end. Putting all these together will leave us with a nox file named “helloworld.nox” that contains:

    lumos HelloWorld;

    main {
        !! - Your first Lumos program
        println("Hello World");
    }

    nox;

To be able to run this program, start by compiling it into a lumos file by executing “python3 parser.py” and give the file name (in this case “helloworld.nox”). It should successfully output a “helloworld.lumos” file into the Lumos directory. Then you can execute “python3 virtual_machine.py helloworld.lumos”, which will output your “Hello World”. Congratulations you have successfully created your first Lumos program!

## Documentation

### Data Primitives

Lumos has a pre-set number of primitives for you to be able to manipulate data with when coding your programs. Lumos has the following data primitives:

- bool: Booleans represent one of two values: true or false.
- int: Integers are zero, positive or negative whole numbers without a fractional part and having unlimited precision,

        e.g. 0, 100, -10. The following are valid integer literals in Lumos:

        0
        100
        -10
        123456789
        5000000000000000000000000000000000000000000000000000000

- float: Floats are zero, positive or negative whole numbers have a fractional part.
  The following are valid float literals in Lumos:
        0.1
        -1.1
        -0.01
- char: Characters are symbols with one single character.
  The following are valid examples of char:
        “A”
        “&”
        “9”
- string: Strings are a series of characters, it is important to note that strings are immutable and are not considered arrays in Lumos.
  The following are valid examples of strings:
        “Hello world”
        “Lumos”
        “Harry”

### Data Structures

Lumos has two built-in data structures for you to be able to manipulate data, array, also known as vectors, and matrices, also known as multidimensional arrays.

#### Array

An array in Lumos is a single dimension structure that has a fixed size, which is specified in its declaration. Each array has a name and a dimension size specified between brackets, for example:

    int vector[5];

You can then proceed to access each cell of the array by using index accessing, it is important to remember that the LVM will throw an error if an out of range index is given. To access or setting an index you can do the following:

    vector[0] = 1;
    vector[x - 1] = 2;
    vector[5]; !! - Out of range: Lumos uses a 0 based indexing.

#### Matrices

A matrix in Lumos is a multidimensional structure that, as the array, has fixed dimension sizes. The same can be said about accessing and setting matrixes cells, you can use their name and an index for each dimension:

    float square[3][3]; !! - Declaration
    float i;

    square[2][2] = 1.1; !! - Setting cell
    i = square[2][2]; !! - Getting cell value

### Program Structure

As mentioned in the Hello World example, there are three main components for a Lumos program to be able to run:

- Program ID: Identifier to generate lumos file (object code file)
- Main task: Where the program starts executing instructions
- Nox command: End program

Now these are the basic elements of a Lumos program, but there is more. A nox file can have global variables, tasks, and local variables inside each task. Global variables are to be declared after the program ID at the beginning of the file. In the case of local variables, they are to follow a task signature. Both of these variable declarations have to be lead by a “vars” keyword. Finally are the tasks, which are to be declared above the main function and below the global variables. For it to be more easy to understand, here is an example of a Lumos program that uses all the elements:

    lumos DemoProgram;
    vars
    int globalMax;

    task max(int a, int b) : int {
        vars
        int answer;

        if (a > b) {
            answer = a;
            return answer;
        } else {
            answer = b;
            return answer;
        }
    }

    main {
        vars
        int x, i;

        x = 10;
        i = 12;

        globalMax = max(x, i);

        println(globalMax);
    }

    nox;

### Reserved Words

In Lumos there are a number of set words that have been reserved to identify different parts of a program, here is the following list:

- lumos
- vars
- bool, int, float, char, string, void
- task, return
- main
- nox
- true, false
- or, and
- print, println

### Notation Conventions

- **Program ID (Obligatory)**

The ID of a program is declared at the beginning of a nox file after the keyword “lumos” and followed by a “;”. It is important to note that this ID will be used to generate the lumos file, object code file, after compiling.

_Example_:

        lumos HelloWorld;

- **Global/local vars (optional)**

The variable declaration starts with the keyword “vars”, each following line with the variables to declare. You can declare more than one variable of the SAME type in a single line. The scope of the variable depends if it is after the program ID or at the beginning of a task. Another thing to note is that you can’t assign variables during declaration.

_Example_:

        vars
        bool flag;
        int i, j;
        float pi;
        char symbol;
        string word;

- **Tasks (Optional)**

The n number of tasks can be defined after the program ID or global vars and it is defined with the “task” keyword, followed by a task name and a x number of parameters with their types surrounded by brackets. After the parameters the return type of the task must be specified. If the task has no return, use void. The task instructions follow the task return type and are surrounded by brackets.

_Example_:

    VOID

    task printMax(int a, int b) : void {
        if (a > b) {
            println(a);
        } else {
            println(b);
        }
    }


    NON-VOID

    task printMax(int a, int b) : int {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }

- **Main (Obligatory)**
  The main task is where every Lumos program starts executing instructions and it is at the end of the file, just before the nox command. This task starts with the “main” keyword and it is followed by a bracket statements block.

_Example_:

    main {
        vars
        int i, j;

        println(“This is the main task!”);
    }

- **Nox (Obligatory)**
  The nox command is used to end the program and it goes after the main task.

_Example_:

    nox;

- **Statement (Optional)**

A statement can be multiple commands inside a Lumos program, they are to be used to manipulate the data primitives, the data structures and the I/O of a program. Here are some of the statement examples:

- Assign
- A[i] = i + 1;
- Arithmetics
- i + 1
- i - 1
- i / 1
- i \* 1
- i % 1
- Conditionals
- i > 1
- i < 1
- i >= 1
- i <= 1
- i and j
- i or j
- i == j
- Console I/O
- print(“Hello”);
- prinln(“Hello in a new line”);
- read(x);

### Compilation

If you aren’t using our LVM and want to manually compile your Lumos program (nox file), you can use the parser.py script. Once you have finished coding your program you can go into the terminal of the directory where the Lumos directory is and run the following command:

        python3 parser.py [path to .nox file]

If the program compiles successfully, a lumos file (object code file) will be generated on the compiler directory. You can now use our LVM to execute this program, check the next section.

### Execution

For the execution of a Lumos program you currently have two options. You can either use our in-house IDE for automatic execution or you can manually run it through a terminal with our LVM. If you wrote your Lumos program in another text editor and wish to use the LIDE, you can open it and start editing/executing it from there. To open the IDE you can run the ide.py script from the Lumos directory:

        python3 ide/ide.py

If you want to manually run your program from terminal you can identifty the absolute or relative path of your lumos file and run the following command from the Lumos compiler directory:

    	python3 virtual_machine.py [path to .lumos file]

### Limitations

- Global variables can’t be named as functions
- Formatting symbols don’t work when printing strings, ex: \n \t \r
- Vectors and matrices have fixed sizes
