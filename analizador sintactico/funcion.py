# archivo: parser.py
import ply.lex as lex
import ply.yacc as yacc

# Palabras clave reservadas
reserved = {
    'def': 'DEF',
}

# Lista de tokens
tokens = (
    'DEF',
    'IDENTIFIER',
    'LPAREN',
    'RPAREN',
    'COLON',
    'CONTENT',
    'ILLEGAL'
)

# Definición de patrones para los tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'

def t_IDENTIFIER(t):
    r'[a-z]+'  # Solo letras para el IDENTIFIER
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Verificar si es una palabra clave
    return t

def t_CONTENT(t):
    r'C'  # Solo la letra C mayúscula para CONTENT
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
    declaration : DEF IDENTIFIER LPAREN IDENTIFIER RPAREN COLON CONTENT
    '''
    if len(p) == 8:
        print("Declaración de función:", p[2], " con parámetro:", p[4], " y contenido:", p[7])
    else:
        print("Declaración de función:", p[2], " sin parámetros", " y contenido:", p[6])
    p[0] = True

def p_error(p):
    raise SyntaxError("Error sintáctico en la entrada.")



def parse_input(input_text):
    parser = yacc.yacc()
    lexer = lex.lex()
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