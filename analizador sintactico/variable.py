import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = (
    'DATA_TYPE',
    'IDENTIFIER',
    'SEMICOLON',
    'ASSIGN',
    'ILLEGAL'
)

# Definición de patrones para los tokens
t_ASSIGN = r'='
t_SEMICOLON = r';'

def t_IDENTIFIER(t):
    r'[a-zA-Z_]+'
    keywords = {'int', 'float', 'string'}
    if t.value.lower() in keywords:
        t.type = 'DATA_TYPE'
    else:
        t.type = 'IDENTIFIER'
    return t

def t_error(t):
    t.type = 'ILLEGAL'
    t.value = t.value[0]
    t.lexer.skip(1)

t_ignore = ' \t\n'  # Ignorar espacios en blanco

# Función para manejar los saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



# Reglas de la gramática
def p_declaration(p):
    '''
    declaration : DATA_TYPE IDENTIFIER SEMICOLON
    '''
    print("Declaración de variable:", p[1], p[2])
    p[0] = True

def p_error(p):
    raise SyntaxError("Error sintáctico en la entrada.")



def parse_input(input_text):
    lexer = lex.lex()
    parser = yacc.yacc()
    lexer.input(input_text)
    token_list = []
    lexeme_count = {}
    valid = False

    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type != 'ILLEGAL':  # Ignorar tokens ilegales
            token_list.append((tok.type, tok.value))
            if tok.value in lexeme_count:
                lexeme_count[tok.value] += 1
            else:
                lexeme_count[tok.value] = 1

    try:
        result = parser.parse(input_text)
        valid = True
    except SyntaxError as e:
        print("Error sintáctico:", e)

    return token_list, lexeme_count, valid