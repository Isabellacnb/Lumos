# -------------- parser.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : grammar rules 
# ----------------------------------------


import scanner
# Import lex and yacc
import ply.lex as lex
import ply.yacc as yacc

def p_programa(p):
	'''program : LUMOS ID ";" prog_vars prog_func main NOX ";"'''

def p_prog_vars(p):
    '''prog_vars : vars 
                | empty'''

def p_prog_func(p):
    '''prog_func : func prog_func 
                | empty'''

def p_vars(p):
    '''vars : VARS vars_line'''

def p_vars_line(p):
    '''vars_line : type var_list ";" vars_line2'''

def p_vars_line2(p):
    '''vars_line2 : vars_line 
                    | empty'''

def p_var_list(p):
    '''var_list : ID var_array var_comma'''

def p_var_array(p):
    '''var_array : array_dim 
                | empty'''

def p_var_comma(p):
    '''var_comma : "," var_list 
                | empty'''

def p_array_dim(p):
    '''array_dim : "[" exp "]" mult_dim'''

def p_mult_dim(p):
    '''mult_dim : array_dim 
                | empty'''

def p_stmt(p):
    '''stmt : condition 
            | stmt_endl ";"'''

def p_stmt_endl(p):
    '''stmt_endl : assign 
                | write 
                | return 
                | loop 
                | call_func 
                | read'''

def p_var_cte(p):
    '''var_cte : CTE_STRING 
                | CTE_INT 
                | CTE_FLOAT 
                | CTE_CHAR 
                | bool
                | call_func
                | ID id_dim'''

def p_bool(p):
    '''bool : TRUE
            | FALSE'''

def p_id_dim(p):
    '''id_dim : array_dim
                | empty'''

def p_return(p):
    '''return : RETURN expression'''

def p_read(p):
    '''read : READ "(" expression ")"'''

def p_main(p):
    '''main : MAIN section'''

def p_write(p):
    '''write : PRINT "(" expression mul_write ")"
    '''

def p_mul_write(p):
    '''mul_write : "," expression'''

def p_assign(p):
    '''assign : ID "=" expression'''

def p_expression(p):
    '''expression : exp expr'''

def p_expr(p):
    '''expr : expr_symbol exp 
            | empty'''

def p_expr_symbol(p):
    '''expr_symbol : ">"
                    | "<"
                    | NE
                    | EQ
                    | AND
                    | OR
                    | LTE
                    | GTE'''

def p_exp(p):
    ''' exp : term exp_symb'''

def p_exp_symb(p):
    '''exp_symb : "+" exp 
                | "-" exp 
                | empty'''

def p_term(p):
    '''term : factor term_symb'''

def p_term_symb(p):
    '''term_symb : "*" term
                | "/" term
                | empty'''

def p_factor(p):
    '''factor : "(" expression ")"
                | var_symb'''

def p_var_symb(p):
    '''var_symb : var_cte
                | "+" var_cte
                | "-" var_cte'''

def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR
            | STRING
            | BOOL'''

def p_func(p):
    '''func : TASK ID "(" param ")" ":" type_func section'''

def p_section(p):
    '''section : "{" prog_vars stmt mul_sec "}"'''

def p_mul_sec(p):
    '''mul_sec : stmt mul_sec
                | empty'''

def p_type_func(p):
    '''type_func : type
                | VOID'''

def p_param(p):
    '''param : type ID param2'''

def p_param2(p):
    '''param2 : "," param
            | empty'''

def p_call_func(p):
    '''call_func : ID "(" expression call_exp ")"'''

def p_call_exp(p):
    '''call_exp : "," expression
                | empty'''

def p_loop(p):
    '''loop : FOR "(" assign ";" expression ")" section'''

def p_condition(p):
    '''condition : IF "(" expression ")" section cond_else
                | WHILE "(" expression ")" section'''

def p_cond_else(p):
    '''cond_else : ELSE section
                | empty'''

# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at '%s' at line '%d'" % (p.value, p.lineno))
    else:
        print("Syntax error at EOF")
    exit(1)

def p_empty(p):
  'empty :'
  pass



# Build the lexer
lex.lex(module=scanner)
tokens = scanner.tokens

# Build the parser
yacc.yacc()

if __name__ == '__main__':
    try:
        f = open("/samples/demofile.nox", "r")
        file = f.read()
        f.close()
    except EOFError:
        quit()
    
    #Parse the file using grammar
    yacc.parse(file)
    print("Sucessfully parsed...")
