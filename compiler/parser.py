# -------------- parser.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Parser
# ----------------------------------------


import scanner
# Import lex and yacc
import ply.lex as lex
import ply.yacc as yacc

# Structures
from structures import *

# Setup
operandStack = Stack() # poper
operatorStack = Stack()
typeStack = Stack()
quadruples = QuadrupleList()
jumpStack = Stack()

# Temporary
tVarName = Stack()
tVarType = Stack()
tFuncName = Stack()
tFuncType = Stack()

# Variable Tables
varsGlobal = VariableTable()
varsLocal = VariableTable()

# Function Tables
functions = FunctionDirectory()

# Scope
scope = Scope.GLOBAL

# =================================
# Grammar Rules #
# =================================

# Rule to define program structure
def p_programa(p):
	'''program : LUMOS ID ";" prog_vars prog_func setScopeLocal main setScopeGlobal NOX ";"'''

# Rule to define program types
def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR
            | STRING
            | BOOL'''
    if(p[1] == 'int'):
        p[0] = Type.INT
    elif(p[1] == 'float'):
        p[0] = Type.FLOAT
    elif(p[1] == 'char'):
        p[0] = Type.CHAR
    elif(p[1] == 'string'):
        p[0] = Type.STRING
    elif(p[1] == 'bool'):
        p[0] = Type.BOOL
    
# Variables
# =============================
# Rule to define whether program will have global variables
def p_prog_vars(p):
    '''prog_vars : vars 
                | empty'''

# Rule to use 'VARS' call
def p_vars(p):
    '''vars : VARS vars_line'''

# Rule to define type of variables in given line
def p_vars_line(p):
    '''vars_line : type saveVarType var_list ";" delVarType vars_mult_lines'''

# Rule to generate multiple types of variables (multiple lines)
def p_vars_mult_lines(p):
    '''vars_mult_lines : vars_line 
                    | empty'''

# Rule to define variable names
# TODO: array dimensions
def p_var_list(p):
    '''var_list : ID saveVarName storeVar var_array delVarName var_comma'''

# Rule to call for more variables of same type
def p_var_comma(p):
    '''var_comma : "," var_list 
                | empty'''

# Rule to define whether variable has dimensions or not
# TODO: array dimensions
def p_var_array(p):
    '''var_array : array_dim 
                | empty'''

# TODO: arrays (check if [exp] is calling correct rule)
# Arrays
# ----------------------------
def p_array_dim(p):
    '''array_dim : "[" exp "]" mult_dim'''

def p_mult_dim(p):
    '''mult_dim : array_dim 
                | empty'''

# Statements
# =============================
# Rule to define statement to be used... conditionals and cycles or statements that needs a ;
def p_stmt(p):
    '''stmt : if
            | while
            | loop
            | stmt_endl ";"'''

# Rule to define whether line will assign, write, return, call function or read
def p_stmt_endl(p):
    '''stmt_endl : assign 
                | write 
                | return 
                | call_func 
                | read'''

# Rule to return value in function
def p_return(p):
    '''return : RETURN super_expression'''

# TODO: CHECK
# TODO: INPUT WITH INDEX SELECTOR
# Rule to raed
def p_read(p):
    '''read : READ "(" ID lookupID addOperandId delVarName delVarType ")" addReadQuadruple '''

# Rule to write
def p_write(p):
    '''write : PRINT "(" super_expression addPrintQuadruple mul_write ")"
            | PRINTLN "(" super_expression addPrintQuadruple mul_write addNewLineQuadruple ")"'''

# Rule to write multiple parameters
def p_mul_write(p):
    '''mul_write : "," super_expression addPrintQuadruple mul_write
                | empty'''

# Rule to assign value to a variable
def p_assign(p):
    '''assign : ID lookupID addOperandId delVarName delVarType "=" addOperator super_expression addAssignQuadruple'''

# Expressions
# =============================
# Rule to call logical expressions 'AND' and 'OR'
def p_super_expression(p):
    '''super_expression : expression logicalQuadruple
                        | expression logicalQuadruple AND addOperator super_expression
                        | expression logicalQuadruple OR addOperator super_expression'''    

# Rule to call relational expressions '>', '<', NE, EQ, LTE, GTE
def p_expression(p):
    '''expression : exp relationalQuadruple
                | exp relationalQuadruple '>' addOperator expression
                | exp relationalQuadruple '<' addOperator expression
                | exp relationalQuadruple NE addOperator expression
                | exp relationalQuadruple EQ addOperator expression
                | exp relationalQuadruple LTE addOperator expression
                | exp relationalQuadruple GTE addOperator expression'''

# Rule to call addition and substraction expressions '+' and '-'
def p_exp(p):
    ''' exp : term addsubQuadruple
            | term addsubQuadruple '+' addOperator exp    
            | term addsubQuadruple '-' addOperator exp'''  

# Rule to call multiplication and divition expressions '*', '/' and '%'
def p_term(p):
    '''term : factor_sign multdivQuadruple
            | factor_sign multdivQuadruple '*' addOperator term
            | factor_sign multdivQuadruple '/' addOperator term
            | factor_sign multdivQuadruple '%' addOperator term'''

# Rule to define whether value has a negative or positive sign
def p_factor_sign(p):
    '''factor_sign : factor
                    | "-" factor minusQuadruple'''     

# Rule to determine order with parenthesis
def p_factor(p):
    '''factor : '(' addBottom super_expression delBottom ')'
                | value'''

# TODO: ID with index selector
# TODO: call_func and ID
# Rule to define value
def p_value(p):
    '''value : cte addCte addOperandCte
            | call_func
            | ID lookupID addOperandId delVarName delVarType 
            | ID id_dim'''

# Constants
# =============================
def p_cte_float(p):
    "cte : CTE_FLOAT"
    p[0] = float(p[1])

def p_cte_string(p):
    "cte : CTE_STRING"
    p[0] = str(p[1])

def p_cte_char(p):
    "cte : CTE_CHAR"
    p[0] = chr(p[1])

# TODO: related to arrays
def p_id_dim(p):
    '''id_dim : array_dim
                | empty'''

def p_cte_int(p):
    "cte : CTE_INT"
    p[0] = int(p[1])

def p_cte_bool(p):
    '''cte : TRUE
        | FALSE'''
    if p[1] == 'true':
        p[0] = True
    elif p[1] == 'false':
        p[0] = False

# Functions
# =============================
# Rule to call function rule
def p_prog_func(p):
    '''prog_func : func prog_func 
                | empty'''

# Rule to call main function
def p_main(p):
    '''main : MAIN section'''

# Rule to write a function
# TODO: falta addfunction despues de saveFunctionType
def p_func(p):
    '''func : TASK setScopeLocal ID saveFunctionName "(" param ")" ":" type_func saveFunctionType section setScopeGlobal'''

# Rule to set structure of a function with brackets, variable definition and statements
def p_section(p):
    '''section : "{" prog_vars stmt mul_sec "}"'''

# Rule to define multiple statements
def p_mul_sec(p):
    '''mul_sec : stmt mul_sec
                | empty'''

# Rule to define type of function
def p_type_func(p):
    '''type_func : type
                | VOID'''

# TODO: check for functions without parameters
# Rule to define function parameter
def p_param(p):
    '''param : type ID mult_params'''

# Rule to call for multiple function parameters
def p_mult_params(p):
    '''mult_params : "," param
            | empty'''

# Rule to call a function
def p_call_func(p):
    '''call_func : ID "(" super_expression call_mult_exp ")"'''
    p[0] = p[1]

# Rule to call multiple parameters in a function call
def p_call_mult_exp(p):
    '''call_mult_exp : "," super_expression call_mult_exp
                | empty'''

# Conditionals and cycles
# =============================
# Rule to call loop
def p_loop(p):
    '''loop : FOR "(" assign ";" super_expression ")" section'''

# Rule to call decision
def p_if(p):
    '''if : IF "(" super_expression ")" tryIfCondition section if_else endIfCondition'''

# TODO: will we have a else-if?
# Rule to call else
def p_if_else(p):
    '''if_else : ELSE tryElseCondition section
                | empty'''

# Rule to call while cycle
def p_while(p):
    '''while : WHILE whileCondition "(" super_expression ")" tryWhileCondition section endWhileCondition'''

# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at '%s' at line '%d'" % (p.value, p.lineno))
    else:
        print("Syntax error at EOF")
    exit(1)

# Empty rule
def p_empty(p):
  'empty :'
  pass

# =================================
# Scope Management #
# =================================

def p_setScopeLocal(p):
  'setScopeLocal :'
  global scope 
  scope = Scope.LOCAL

def p_setScopeGlobal(p):
  'setScopeGlobal :'
  global scope 
  scope = Scope.GLOBAL

# =================================
# Variable Quadruple Generation #
# =================================

def p_saveVarType(p):
    'saveVarType :'
    tVarType.push(p[-1])

def p_delVarType(p):
    'delVarType :'
    tVarType.pop()

def p_saveVarName(p):
    'saveVarName :'
    tVarName.push(p[-1])

def p_delVarName(p):
    'delVarName :'
    tVarName.pop()

def p_storeVar(p):
    'storeVar :'
    createVariable(tVarName.top(), tVarType.top())

def createVariable(name, type):
    global varsGlobal, varsLocal
    var = Variable(name, type);
    if scope == Scope.GLOBAL:
        varsGlobal.insert(var)
        # TODO: Address addition
    elif scope == Scope.LOCAL:
        varsLocal.insert(var)
        # TODO: Address addition
    print(name)

# =================================
# Arithmetic Quadruple Generation #
# =================================

def p_addOperandId(p):
    'addOperandId :'
    if scope == Scope.GLOBAL:
        var = varsGlobal.find(tVarName.top())
        if var is None:
            print(tVarName.top(), "is not a global variable!")
    elif scope == Scope.LOCAL:
        var = varsLocal.find(tVarName.top())
        if var is None:
            var = varsGlobal.find(tVarName.top())
        if var is None:
            print(tVarName.top(), "is not a local or global variable!")
    operandStack.push(tVarName.top())
    typeStack.push(tVarType.top())

def p_addCte(p):
    'addCte : '
    cte = p[-1]
    # TODO: addConstant(cte) #add constant and generate new address

# TODO: pushConstantOperand --> needs a constant table to push constant adress to operandStack
def p_addOperandCte(p):
    'addOperandCte :'
    constantName = str(p[-2])
    constantType = -1
    # constant lookup in constant table with name
    operandStack.push(constantName)
    typeStack.push(constantType)

def p_addOperator(p):
    'addOperator :'
    operatorStack.push(p[-1])

def p_lookupID(p):
    'lookupID :'
    operandID = p[-1]
    if scope == Scope.GLOBAL:
        var = varsGlobal.find(operandID)
    elif scope == Scope.LOCAL:
        var = varsLocal.find(operandID)
        if var is None:
            var = varsGlobal.find(operandID)
    
    if var is None:
        print("Error: Variable not found!")
        return
    else:
        print("Found: " + str(var))

def generateQuadrupleExpression(operators):
    global operandStack, operatorStack, typeStack
    operator = operatorStack.top()
    if operator in operators:
        operator = operatorStack.pop()
        # Operands
        operRight = operandStack.pop()
        operLeft = operandStack.pop()
        # Types
        typeRight = typeStack.pop()
        typeLeft = typeStack.pop()
        resultType = getResultType(typeLeft, operator, typeRight)
        # TODO: Check if global or local temporary variable
        quadruple = Quadruple(operator, operLeft, operRight, -1)
        quadruples.push(quadruple)
        # Push temporary
        typeStack.push(resultType)
        # TODO: push temporary variable to operand stack (address)
        operandStack.push(-1)
        print(str(quadruple) + " " + resultType)

def p_logicalQuadruple(p):
    'logicalQuadruple :'
    generateQuadrupleExpression(['and', 'or'])

# TODO: should != be NE
def p_relationalQuadruple(p):
    'relationalQuadruple :'
    generateQuadrupleExpression(['<', '>', '==', '!=', '<=', '>='])

def p_addsubQuadruple(p):
    'addsubQuadruple :'
    generateQuadrupleExpression(['+', '-'])

def p_multdivQuadruple(p):
    'multdivQuadruple :'
    generateQuadrupleExpression(['*', '/', '%'])

def p_minusQuadruple(p):
    'minusQuadruple :'
    rightOperand = operandStack.pop()
    type = typeStack.pop()
    if type is Type.STRING or type is Type.CHAR or type is Type.BOOL:
        print("Can't negate expression.")
        return
    # TODO: addCte(-1) lookup constant in constant table
    # get symbol
    # check scope and generate temporary
    #quadruple_list.push(Quadruple('*', -1, rightOperand, -1))
    # push temporary to operand stack
    # push result type to type stack

def p_addBottom(p):
    'addBottom :'
    operatorStack.push('(')

def p_delBottom(p):
    'delBottom :'
    operatorStack.pop()

def p_addAssignQuadruple(p):
    'addAssignQuadruple :'
    operator = operatorStack.pop()
    rightOperand = operandStack.pop()
    leftOperand = operandStack.pop()
    rightType = typeStack.pop()
    leftType = typeStack.pop()
    resultType = getResultType(leftType, operator, rightType)
    if resultType is not None:
        quadruple_list.push(Quadruple(operator, rightOperand, None, leftOperand))
    else:
        print("Error: Result type mismatch")
        return

def p_addPrintQuadruple(p):
    'addPrintQuadruple :'
    output = operandStack.pop()
    typeStack.pop()
    quadruple_list.push(Quadruple("PRINT", None, None, output))

def p_addNewLineQuadruple(p):
    'addNewLineQuadruple :'
    quadruple_list.push(Quadruple("PRINTLN", None, None, None, None))

def p_addReadQuadruple(p):
    'addReadQuadruple :'
    inputValue = operandStack.pop()
    typeStack.pop()
    quadruple_list.push(Quadruple("READ", None, None, inputValue))

# =================================
# Condition Logic #
# =================================
def p_tryIfCondition(p):
    'tryIfCondition :'
    expResult = operandStack.pop()
    expType = typeStack.pop()
    if expType != Type.BOOL:
        print("Error: Result type mismatch")
        return
    else:
        quadruple_list.push(Quadruple("GOTOF", expResult, None, -1))
        Quadruple()
        jumpStack.push(quadruple_list.size() - 1)

def p_endIfCondition(p):
    'endIfCondition :'
    assignJump(quadruple_list.size())

def p_tryElseCondition(p):
    'tryElseCondition :'
    quadruple_list.push(Quadruple("GOTO", None, None, -1))
    goToFIndex = jumpStack.pop()
    jumpStack.push(quadruple_list.size() - 1)
    assignJump(goToFIndex)

def p_whileCondition(p):
    'whileCondition :'
    jumpStack.push(quadruple_list.size())

def p_tryWhileCondition(p):
    'tryWhileCondition : tryIfCondition'

def p_endWhileCondition(p):
    'endWhileCondition :'
    goToFIndex = jumpStack.pop()
    cycleBack = jumpStack.pop()
    quadruple_list.push(Quadruple("GOTO", None, None, cycleBack))
    goToFQuad = quadruple_list[goToFIndex]
    goToFQuad.result = quadruple_list.size()

def assignJump(position):
    global jumpStack, quadruple_list
    jump = jumpStack.pop()
    goToFQuad = quadruple_list[jump]
    goToFQuad.result = position

# =================================
# Function logic #
# =================================

def p_saveFunctionName(p):
    'saveFunctionName :'
    global tFuncName
    tFuncName = p[-1]

def p_saveFunctionType(p):
    'saveFunctionType :'
    global tFuncType
    tFuncType = p[-1]

# =================================
# Build lex and yacc #
# =================================

# Build the lexer
lex.lex(module=scanner)
tokens = scanner.tokens

# Build the parser
yacc.yacc()

if __name__ == '__main__':

    try:
        f = open("../samples/demofile.nox", "r")
        file = f.read()
        f.close()
    except EOFError:
        quit()
    
    #Parse the file using grammar
    yacc.parse(file)
    print("Sucessfully parsed...")
    # print("GLOBAL")
    # print(str(varsGlobal))
    # print("LOCAL")
    # print(str(varsLocal))
