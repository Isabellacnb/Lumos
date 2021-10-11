# -------------- scanner.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Lexical Rules 
# ----------------------------------------

import ply.lex as lex

# Reserved words
reserved = {
    # General tokens
    'lumos' : 'LUMOS',
    'vars' : 'VARS',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'print' : 'PRINT',
    'read' : 'READ',
    'and' : 'AND',
    'or' : 'OR',
    'nox' : 'NOX',

    # Function tokens
    'return' : 'RETURN',
    'task' : 'TASK',
    'void' : 'VOID',
    'main' : 'MAIN',

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

# Comments
t_ignore_COMMENT = r'\!\!\ \-.*\n'

# Regular expressions
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Ignore white spaces and tabs
t_ignore = " \t"

# New lines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling
def t_error(t):
    print("Illegal character: '%s' in line '%d' " % (t.value[0], t.lineno))
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == "__main__":
    try:
        f = open("demoshort.nox", "r")
        file = f.read()
        f.close()
    except EOFError:
        quit()
    
    # Give the lexer some input
    lexer.input(file)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)