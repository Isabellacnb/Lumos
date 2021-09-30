# -------------- scanner.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : lexical rules 


# Reserved words
reserved = {
    # General tokens
    'lumos' : 'LUMOS',
    'var' : 'VAR',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'print' : 'PRINT',
    'write' : 'WRITE',
    'and' : 'AND',
    'or' : 'OR',
    'nox' : 'NOX',

    # Function tokens
    'return' : 'RETURN',
    'task' : 'TASK',
    'main' : 'MAIN',
    # 'break' : 'BREAK',
    # 'continue' : 'CONTINUE',

    # Conditional tokens
    'if' : 'IF',
    'else' : 'ELSE',

    # Cycle tokens
    'for' : 'FOR',
    'while' : 'WHILE',

    # Primitive types
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'string' : 'STRING',
    'bool' : 'BOOL',
}

# Literals
literals = [';','=',',','+','-','*','/','(',')','{','}','[',']',':','>','<']

# Tokens
tokens = [
    'CTE_STRING',
    'CTE_INT',
    'CTE_FLOAT',
    'CTE_CHAR',
    'ID',
    'EQ',
    'NE',
    'GTE',
    'LTE'
] + list(reserved.values())

# Tokens regular expressions
t_CTE_STRING = r'"([^\\"\n]+|\\.)*"'
t_CTE_INT = r'[-+]?\d+'
t_CTE_FLOAT = r'[-+]?[0-9]+\.[0-9]+([Ee][\+-]?[0-9+])?'
t_CTE_CHAR = r'\'(?:\\.|[^\'\\])\''
t_EQ = r'=='
t_NE = r'<>'
t_GTE = r'>='
t_LTE = r'<='

# Regular expressions
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Ignore white spaces and tabs
t_ignore = r' \t'

# New lines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Comments
def t_COMMENT(t):
    r'\!\! \-'
    pass
    # No return value. Token discarded

# Error handling
def t_error(t):
    print("Illegal character: '%s'" % t.value[0])
    t.lexer.skip(1)
