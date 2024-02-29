import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = (
    'WHILE',
    'IDENTIFIER',
    'REL_OP',
    'COLON',
    'CONTENT',
    'ILLEGAL',
    'NUMBER'
)

# Palabras clave reservadas
reserved = {
    'while': 'WHILE',
}

# Definición de patrones para los tokens
t_REL_OP = r'>=|<=|!=|<|>'
t_COLON = r':'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    t.type = 'NUMBER'
    return t

def t_IDENTIFIER(t):
    r'[a-z]+'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Verificar si es una palabra clave
    return t

def t_CONTENT(t):
    r'C'
    t.type = 'CONTENT'
    return t

def t_error(t):
    t.type = 'ILLEGAL'
    t.value = t.value[0]
    t.lexer.skip(1)

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Función para manejar los saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Reglas de la gramática
def p_declaration(p):
    '''
    declaration : WHILE operand REL_OP operand COLON CONTENT
    '''
    print("Ciclo while con condición:", p[2], p[3], p[4], " y contenido:", p[6])
    p[0] = True

def p_operand(p):
    '''
    operand : IDENTIFIER
            | NUMBER
    '''
    p[0] = p[1]

def p_error(p):
    raise SyntaxError("Error sintáctico en la entrada.")

parser = yacc.yacc()

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