# -------------- parser.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Parser
# ----------------------------------------


from memory.address_manager import AddressManager
import scanner

# Import lex and yacc
import ply.lex as lex
import ply.yacc as yacc

# Structures
from structures import *

# Setup
quadruples = QuadrupleList()
operandStack = Stack()
operatorStack = Stack()
typeStack = Stack()
jumpStack = Stack()

# Temporary Var data
tVarName = Stack()
tVarType = Stack()
tVarDim = Stack()
# Temporary Function data
tFuncName = ""
tFuncType = ""
tFuncParameters = []
tFuncCallName = Stack()
tFuncCallType = Stack()
tFuncCallArgs = Stack()

# Variable Tables
varsGlobal = VariableTable()
varsLocal = VariableTable()
constantTable = VariableTable()

# Function Tables
dirFuncs = FunctionDirectory()

# Scope
scope = Scope.GLOBAL

# Memory
addressManager = AddressManager()

programName = None

# =================================
# Grammar Rules #
# =================================

# Rule to define program structure
def p_programa(p):
	'''program : LUMOS ID saveProgramID goToMain ";" prog_vars prog_func setScopeLocal setGoToMain main NOX setEnd ";"'''

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

# Arrays
# =============================
# Rule to define whether variable has dimensions or not
def p_var_array(p):
    '''var_array : array_dim initArrayDim
                | empty'''

def p_array_dim(p):
    '''array_dim : "[" CTE_INT addDim "]" mult_dim'''

def p_mult_dim(p):
    '''mult_dim : array_dim 
                | empty'''

def p_arr_assign(p):
    '''arr_assign : ID lookupID array_dim_index "=" addOperator super_expression addAssignQuadruple'''

def p_array_dim_index(p):
    '''array_dim_index : setVarDim "[" addFakeBottom exp delFakeBottom generateVerQuad "]" mult_dim_index addBaseAddress delVarName delVarType delVarDim'''

def p_mult_dim_index(p):
    '''mult_dim_index : dimensionOffset "[" addFakeBottom exp delFakeBottom generateVerQuad "]" displacementUpdate mult_dim_index
                | empty'''

# Statements
# =============================
# Rule to define statement to be used... conditionals and cycles or statements that needs a ;
def p_stmt(p):
    '''stmt : if
            | while
            | stmt_endl ";"'''

# Rule to define whether line will assign, write, return, call function or read
def p_stmt_endl(p):
    '''stmt_endl : assign 
                | arr_assign
                | write 
                | return 
                | call_func 
                | read'''

# Rule to return value in function
def p_return(p):
    '''return : RETURN super_expression setReturn'''

# TODO: CHECK
# TODO: INPUT WITH INDEX SELECTOR
# Rule to raed
def p_read(p):
    '''read : READ "(" ID lookupID addOperandId delVarName delVarType ")" addReadQuadruple 
            | READ "(" ID lookupID addOperandId array_dim_index ")" addReadQuadruple'''

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
    '''factor : '(' addFakeBottom super_expression delFakeBottom ')'
                | value'''

# TODO: ID with index selector
# TODO: call_func and ID
# Rule to define value
def p_value(p):
    '''value : cte addCte addOperandCte
            | call_func
            | ID lookupID addOperandId delVarName delVarType 
            | ID lookupID array_dim_index'''

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
    '''main : MAIN setScopeLocal section setScopeGlobal'''

# Rule to write a function
def p_func(p):
    '''func : TASK setScopeLocal ID saveFunctionName "(" param ")" ":" type_func saveFunctionType addFunction section endFunction setScopeGlobal'''

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
    if(p[1] == 'void'):
        p[0] = Type.VOID
    else:
        p[0] = p[1]

# Rule to define function parameter
def p_param(p):
    '''param : type ID addParameter mult_params
            | empty'''

# Rule to call for multiple function parameters
def p_mult_params(p):
    '''mult_params : "," type ID addParameter mult_params
            | empty'''

# Rule to call a function
def p_call_func(p):
    '''call_func : ID lookupFunc generateEra "(" addFakeBottom params delFakeBottom ")" verifyArguments generateGoSub '''

def p_params(p):
    '''params : super_expression addArgument call_mult_params
                | empty'''

# Rule to call multiple parameters in a function call
def p_call_mult_params(p):
    '''call_mult_params : "," super_expression addArgument call_mult_params
                | empty'''

# Conditionals and cycles
# =============================

# Rule to call decision
def p_if(p):
    '''if : IF "(" super_expression ")" tryIfCondition section if_else endIfCondition'''

# TODO: will we have an else-if?
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
        print("ERROR :: Syntax error at '%s' at line '%d'" % (p.value, p.lineno))
    else:
        print("ERROR :: Syntax error at EOF")
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
    var = Variable(name, type)
    if scope == Scope.GLOBAL:
        var.address = addressManager.nextAddress(Scope.GLOBAL, type)
        varsGlobal.insert(var)
    elif scope == Scope.LOCAL:
        var.address = addressManager.nextAddress(Scope.LOCAL, type)
        varsLocal.insert(var)

def createConstant(constValue):
    global constantTable
    if not constantTable.find(str(constValue)):
        if type(constValue) == bool:
            constType = Type.BOOL
        elif type(constValue) == int:
            constType = Type.INT
        elif type(constValue) == float:
            constType = Type.FLOAT
        elif type(constValue) == str and len(constValue) == 1:
            constType = Type.CHAR
        elif type(constValue) == str:
            constType = Type.STRING
        address = addressManager.nextAddress(Scope.CONSTANT, constType)
        const = Constant(address, str(constValue), constType, constValue)
        constantTable.insert(const)

# =================================
# Array Logic #
# =================================

def p_addDim(p):
    'addDim :'
    dimSize = int(p[-1])
    if scope == Scope.GLOBAL:
        var = varsGlobal.find(tVarName.top())
        var.pushDimension(dimSize)
    elif scope == Scope.LOCAL:
        var = varsLocal.find(tVarName.top())
        if var is None:
            var = varsGlobal.find(tVarName.top())
        if var is None:
            print("ERROR ::", tVarName.top(), "is not a local or global variable!")
            exit()
        var.pushDimension(dimSize)

def p_initArrayDim(p):
    'initArrayDim :'
    if scope == Scope.GLOBAL:
        var = varsGlobal.find(tVarName.top())
        dimSize = var.size() - 1
        if dimSize > 0:
            addressManager.nextAddress(Scope.GLOBAL, var.type, dimSize)
    elif scope == Scope.LOCAL:
        var = varsLocal.find(tVarName.top())
        if var is None:
            var = varsGlobal.find(tVarName.top())
        dimSize = var.size() - 1
        if dimSize > 0:
            addressManager.nextAddress(Scope.LOCAL, var.type, dimSize)

def p_setVarDim(p):
    'setVarDim :'
    global tVarDim
    tVarDim.push(0)

def p_delVarDim(p):
    'delVarDim :'
    global tVarDim
    tVarDim.pop()

def p_generateVerQuad(p):
    'generateVerQuad :'
    global tVarDim, operandStack, quadruples
    dim = tVarDim.pop()
    index = operandStack.top()
    if typeStack.top() is Type.INT:
        if scope == Scope.GLOBAL:
            var = varsGlobal.find(tVarName.top())
        elif scope == Scope.LOCAL:
            var = varsLocal.find(tVarName.top())
            if var is None:
                var = varsGlobal.find(tVarName.top())
        if dim < len(var.dimensions):
            quad = Quadruple("VERIFY", index, 0, var.dimensions[dim])
            quadruples.push(quad)
            tVarDim.push(dim + 1)
        else:
            print("ERROR :: Array dimension is not valid")
            exit()
    else:
        print("ERROR :: Array index should be integer")
        exit()

def p_dimensionOffset(p):
    'dimensionOffset :'
    global tVarDim, quadruples, operandStack, typeStack
    dim = tVarDim.pop() - 1
    if scope == Scope.GLOBAL:
        var = varsGlobal.find(tVarName.top())
    elif scope == Scope.LOCAL:
        var = varsLocal.find(tVarName.top())
        if var is None:
            var = varsGlobal.find(tVarName.top())
    left = operandStack.pop()
    leftType = typeStack.pop()
    dimLimit = var.dimensions[dim]
    createConstant(dimLimit)
    cte = constantTable.find(str(dimLimit))

    address = addressManager.nextAddress(scope, Type.INT)
    quad = Quadruple("*", left, cte.address, address)
    quadruples.push(quad)
    operandStack.push(address)
    typeStack.push(leftType)
    tVarDim.push(dim + 1)

def p_displacementUpdate(p):
    'displacementUpdate :'
    global quadruples, operandStack, typeStack
    right = operandStack.pop()
    typeStack.pop()
    left = operandStack.pop()
    typeStack.pop()
    address = addressManager.nextAddress(scope, Type.INT)
    quad = Quadruple("+", left, right, address)
    quadruples.push(quad)
    operandStack.push(address)
    typeStack.push(Type.INT)

def p_addBaseAddress(p):
    'addBaseAddress :'
    global operandStack, typeStack, quadruples
    left = operandStack.pop()
    typeStack.pop()
    if scope == Scope.GLOBAL:
        var = varsGlobal.find(tVarName.top())
    elif scope == Scope.LOCAL:
        var = varsLocal.find(tVarName.top())
        if var is None:
            var = varsGlobal.find(tVarName.top())
    address = '(' + str(addressManager.nextAddress(scope, Type.INT)) + ')'
    quad = Quadruple("BASE", left, var.address, address)
    quadruples.push(quad)
    operandStack.push(address)
    typeStack.push(var.type)


# =================================
# Arithmetic Quadruple Generation #
# =================================

def p_addOperandId(p):
    'addOperandId :'
    if scope == Scope.GLOBAL:
        var = varsGlobal.find(tVarName.top())
        if var is None:
            print("ERROR ::", tVarName.top(), "is not a global variable!")
    elif scope == Scope.LOCAL:
        var = varsLocal.find(tVarName.top())
        if var is None:
            var = varsGlobal.find(tVarName.top())
        if var is None:
            print("ERROR ::", tVarName.top(), "is not a local or global variable!")
    operandStack.push(var.address)
    typeStack.push(tVarType.top())

def p_addCte(p):
    'addCte : '
    cte = p[-1]
    createConstant(cte)


# TODO: pushConstantOperand --> needs a constant table to push constant adress to operandStack
def p_addOperandCte(p):
    'addOperandCte :'
    global operandStack, typeStack
    constantName = p[-2]
    cte = constantTable.find(str(constantName))
    operandStack.push(cte.address)
    typeStack.push(cte.type)

def p_addOperator(p):
    'addOperator :'
    global operatorStack
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
        print("ERROR :: Variable", operandID, "not found!")
        exit()
    else:
        tVarName.push(var.name)
        tVarType.push(var.type)
        #TODO: delete print("Found: " + str(var))

def generateQuadrupleExpression(operators):
    global operandStack, operatorStack, typeStack, quadruples
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

        # Generate temporary address and push to operand stack
        tmpAddress = addressManager.nextAddress(Scope.TEMPORARY, resultType)
        operandStack.push(tmpAddress)
        typeStack.push(resultType)

        # TODO: Check if global or local temporary variable (maybe not necessary since we don't distinguish global and local temporary variables)
        quadruple = Quadruple(operator, operLeft, operRight, tmpAddress)
        quadruples.push(quadruple)
        #print(str(quadruple) + " " + str(resultType))

def p_logicalQuadruple(p):
    'logicalQuadruple :'
    generateQuadrupleExpression(['and', 'or'])

def p_relationalQuadruple(p):
    'relationalQuadruple :'
    generateQuadrupleExpression(['<', '>', '==', '<>', '<=', '>='])

def p_addsubQuadruple(p):
    'addsubQuadruple :'
    generateQuadrupleExpression(['+', '-'])

def p_multdivQuadruple(p):
    'multdivQuadruple :'
    generateQuadrupleExpression(['*', '/', '%'])

def p_minusQuadruple(p):
    'minusQuadruple :'
    global operandStack, typeStack
    rightOperand = operandStack.pop()
    type = typeStack.pop()
    if type is Type.STRING or type is Type.CHAR or type is Type.BOOL:
        print("ERROR :: Can't negate expression.")
        return
    createConstant(-1)
    cte = constantTable.find("-1")
    resultType = getResultType(cte.type, "*", type)
    address = addressManager.nextAddress(scope, Type.INT)
    quad = Quadruple('*', cte.address, rightOperand, address)
    quadruples.push(quad)
    operandStack.push(address)
    typeStack.push(resultType)

def p_addFakeBottom(p):
    'addFakeBottom :'
    global operatorStack
    operatorStack.push('(')

def p_delFakeBottom(p):
    'delFakeBottom :'
    global operatorStack
    operatorStack.pop()

def p_addAssignQuadruple(p):
    'addAssignQuadruple :'
    global operatorStack, operandStack, typeStack, quadruples
    operator = operatorStack.pop()
    # Operands
    rightOperand = operandStack.pop()
    leftOperand = operandStack.pop()
    # Types
    rightType = typeStack.pop()
    leftType = typeStack.pop()
    resultType = getResultType(leftType, operator, rightType)
    if resultType is not None:
        quadruples.push(Quadruple(operator, rightOperand, None, leftOperand))
    else:
        print("ERROR :: Result type mismatch")
        exit()

def p_addPrintQuadruple(p):
    'addPrintQuadruple :'
    global operandStack, typeStack, quadruples
    output = operandStack.pop()
    typeStack.pop()
    quadruples.push(Quadruple("PRINT", None, None, output))

def p_addNewLineQuadruple(p):
    'addNewLineQuadruple :'
    global quadruples
    quadruples.push(Quadruple("PRINTLN", None, None, None))

def p_addReadQuadruple(p):
    'addReadQuadruple :'
    global operandStack, typeStack, quadruples
    inputValue = operandStack.pop()
    typeStack.pop()
    quadruples.push(Quadruple("READ", None, None, inputValue))

# =================================
# Condition Logic #
# =================================
def p_tryIfCondition(p):
    'tryIfCondition :'
    global operandStack, typeStack, quadruples, jumpStack
    expResult = operandStack.pop() 
    expType = typeStack.pop()
    if expType != Type.BOOL:
        print("ERROR :: Result type mismatch")
        return
    else:
        quadruples.push(Quadruple("GOTOF", expResult, None, -1))
        jumpStack.push(quadruples.size() - 1)

def p_endIfCondition(p):
    'endIfCondition :'
    assignJump(quadruples.size())

def p_tryElseCondition(p):
    'tryElseCondition :'
    global quadruples, jumpStack
    quadruples.push(Quadruple("GOTO", None, None, -1))
    goToFIndex = jumpStack.pop()
    jumpStack.push(quadruples.size() - 1)
    goToFQuad = quadruples.at(goToFIndex)
    goToFQuad.result = quadruples.size()

def p_whileCondition(p):
    'whileCondition :'
    global jumpStack
    jumpStack.push(quadruples.size())

def p_tryWhileCondition(p):
    'tryWhileCondition : tryIfCondition'

def p_endWhileCondition(p):
    'endWhileCondition :'
    global quadruples, jumpStack
    goToFIndex = jumpStack.pop()
    cycleBack = jumpStack.pop()
    quadruples.push(Quadruple("GOTO", None, None, cycleBack))
    goToFQuad = quadruples.at(goToFIndex)
    goToFQuad.result = quadruples.size()

def assignJump(position):
    global jumpStack, quadruples
    jump = jumpStack.pop()
    goToQuad = quadruples.at(jump)
    goToQuad.result = position

# =================================
# Function logic #
# =================================
def p_goToMain(p):
    'goToMain :'
    quad = Quadruple("GOTO", None, None, -1)
    quadruples.push(quad)
    jumpStack.push(quadruples.size() - 1)

def p_setGoToMain(p):
    'setGoToMain :'
    assignJump(quadruples.size())

def p_setEnd(p):
    'setEnd :'
    quad = Quadruple("END", None, None, None)
    quadruples.push(quad)

def p_saveFunctionName(p):
    'saveFunctionName :'
    global tFuncName
    tFuncName = p[-1]
    # print("New function - ", tFuncName)

def p_saveFunctionType(p):
    'saveFunctionType :'
    global tFuncType
    tFuncType = p[-1]

def p_addParameter(p):
    'addParameter :'
    varName = p[-1]
    varType = p[-2]
    createVariable(varName, varType)
    
    paramVar = varsLocal.find(varName)
    tFuncParameters.append(paramVar)

def p_addFunction(p):
    'addFunction :'
    global tFuncName, tFuncType, tFuncParameters
    createFunction(tFuncName, tFuncType, tFuncParameters, quadruples.size())

def p_endFunction(p):
    'endFunction :'
    global tFuncParameters, tFuncName, dirFuncs

    memoryLimits = addressManager.getLimits()
    currFunc = dirFuncs.find(tFuncName)
    currFunc.limits = memoryLimits
    #print(tFuncName, dirFuncs.find(tFuncName).limits)

    varsLocal.clear()
    addressManager.resetAddresses()
    tFuncParameters = []

    quadruple = Quadruple('ENDFUNC', None, None, None)
    quadruples.push(quadruple)

def createFunction(funcName, funcType, params, position):
    global dirFuncs
    function = Function(funcName, funcType, params, position, None) #TODO added none to avoid error
    # Insert function validates duplicate function declarations
    # TODO: function is already declared try and catch
    dirFuncs.insert(function)

def p_lookupFunc(p):
    'lookupFunc :'
    global dirFuncs, tFuncCallName, tFuncCallType
    funcId = p[-1]
    function = dirFuncs.find(funcId)
    if function is None:
        raise Exception("ERROR :: Function not found")
    else:
        tFuncCallName.push(function.name)
        tFuncCallType.push(function.type)

def p_generateEra(p):
    'generateEra :'
    global tFuncCallArgs
    quadruple = Quadruple('ERA', tFuncCallName.top(), None, None)
    quadruples.push(quadruple)
    tFuncCallArgs.push(0)

def p_setReturn(p):
    'setReturn :'
    global operandStack, typeStack, quadruples, tFuncName
    output = operandStack.pop()
    outputType  = typeStack.pop()
    func = dirFuncs.find(tFuncName)
    if outputType != func.type:
        raise Exception("ERROR :: Return type expected ", func.type, " instead got ", outputType)

    quadruples.push(Quadruple("RETURN", None, None, output))
    #TODO keep it ? addressManager.resetAddresses()

def p_addArgument(p):
    'addArgument :'
    global operandStack, typeStack, dirFuncs, tFuncCallName, tFuncCallArgs
    argument = operandStack.pop()
    argumentType = typeStack.pop()
    function = dirFuncs.find(tFuncCallName.top())
    paramType = function.parameters[tFuncCallArgs.top()].type
    if argumentType == paramType:
        args = tFuncCallArgs.pop()
        quadruple = Quadruple('PARAM', argument, None, args)
        quadruples.push(quadruple)
        tFuncCallArgs.push(args + 1)
    else:
        raise Exception("ERROR :: Function parameter type mismatch")

def p_verifyArguments(p):
    'verifyArguments :'
    function = dirFuncs.find(tFuncCallName.top())
    if len(function.parameters) != tFuncCallArgs.top():
        raise Exception("ERROR :: incorrect number of arguments in function, found", tFuncCallArgs.top(), "should be", len(function.parameters))

def p_generateGoSub(p):
    'generateGoSub :'
    global varsGlobal, quadruples, operandStack, typeStack
    function = dirFuncs.find(tFuncCallName.top())
    if function is not None:
        if tFuncCallType.top() != Type.VOID and function.type != None:
            # TODO: Generate temporary variable (check scope)
            # TODO: Quadruple must have memory address
            var = Variable(function.name, function.type)
            var.address = addressManager.nextAddress(Scope.GLOBAL, tFuncType)
            varsGlobal.insert(var)
            
            quadruple = Quadruple('GOSUB', function.name, None, var.address)
            quadruples.push(quadruple)
            operandStack.push(var.address)
            typeStack.push(function.type)
        else:
            quadruple = Quadruple('GOSUB', function.name, None, None)
            quadruples.push(quadruple)
    else:
        raise Exception("ERROR :: Function not found")
    tFuncCallType.pop()
    tFuncCallName.pop()
    tFuncCallArgs.pop()

# =================================
# Extra Functions
# =================================
def p_saveProgramID(p):
    '''saveProgramID :'''
    global programName
    programName = str(p[-1]).lower()

# =================================
# Build lex and yacc #
# =================================

# Build the lexer
lex.lex(module=scanner)
tokens = scanner.tokens

# Build the parser
yacc.yacc()

# =================================
# Build Object Code file for virtual machine to run
# =================================
def generateObjectFile():
    global programName, dirFuncs, constantTable, quadruples
    with open(programName + ".lumos", "w+") as file:
        # Memory
        file.write("@MEMORY\n")
        for i in range(len(Scope)):
            file.write(serializeMemory(i))
            file.write("\n")
        # Functions
        file.write("@FUNCTIONS\n")
        for func in dirFuncs.functions.values():
            file.write(serializeFunction(func))
            file.write("\n")
        # Constants
        file.write("@CONSTANTS\n")
        for const in constantTable.variables.values():
            file.write(serializeConstant(const))
            file.write("\n")
        # Quads List
        file.write("@QUADS\n")
        for idx, quad in enumerate(quadruples.quads):
            file.write(serializeQuad(idx, quad))
            file.write("\n")

def serializeFunction(func:Function):
    # name|returnType|{paramName!paramType!paramAddress}|quadPosition|localLimitsArray|tempLimitsArray
    output = str(func.name) + "|"
    output += str(func.type.value) + "|"
    if func.parameters:
        for paramVar in func.parameters:
            output += paramVar.name + "!" + str(paramVar.type.value) + "!" + str(paramVar.address) + "#"
        output = output[:-1]
    output += "|"
    output += str(func.quadruplePosition) + "|"
    output += str(list(func.limits[0].values())) + "|"
    output += str(list(func.limits[1].values()))
    return output

def serializeConstant(const:Constant):
    #TODO: Confirm if constant need value
    # name|type|value|address
    output = str(const.name) + "|"
    output += str(const.type.value) + "|"
    output += str(const.value) + "|"
    output += str(const.address)
    return output

def serializeQuad(ind:int, quad:Quadruple):
    # operation | 2nd ele | 3rd ele | result
    output = str(ind) + "|"
    output += str(quad.operator) + "|"
    output += str(quad.operLeft) + "|"
    output += str(quad.operRight) + "|"
    output += str(quad.result)
    return output

def serializeMemory(scopeInd:int):
    global addressManager
    # scope | bool | int | float | char | string
    output = ""
    # Global
    if scopeInd == 0:
        output = "global|"
        for t in Type:
            if t == Type.VOID:
                continue
            output += str(addressManager.globalAddresses[t]) + "|"
    # Local
    elif scopeInd == 1:
        output = "local|"
        for t in Type:
            if t == Type.VOID:
                continue
            output += str(addressManager.localAddresses[t]) + "|"
    # Temp
    elif scopeInd == 2:
        output = "temp|"
        for t in Type:
            if t == Type.VOID:
                continue
            output += str(addressManager.tempAddresses[t]) + "|"
    # Constant
    elif scopeInd == 3:
        output = "constant|"
        for t in Type:
            if t == Type.VOID:
                continue
            output += str(addressManager.cteAddresses[t]) + "|"
    
    return output[:-1] # delete last |

# =================================
# Main Function to run parser
# =================================  
if __name__ == '__main__':

    try:
        print("""
    __                              
   / /   __  ______ ___  ____  _____
  / /   / / / / __ `__ \/ __ \/ ___/
 / /___/ /_/ / / / / / / /_/ (__  ) 
/_____/\__,_/_/ /_/ /_/\____/____/  
         """)
        file_name = input('Enter file name: ')
        f = open(file_name, "r")
        # TODO: remove hard coded file
        #f = open("../samples/sort.nox", "r")
        file = f.read()
        f.close()
    except EOFError:
        quit()
    
    #Parse the file using grammar
    yacc.parse(file)
    print("Sucessfully parsed...\n")
    print("Quadruples generated: ")
    print(str(quadruples))
    #print(str(dirFuncs))
    generateObjectFile()
    # print("GLOBAL")
    # print(str(varsGlobal))
    # print("LOCAL")
    # print(str(varsLocal))
