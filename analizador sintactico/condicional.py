import ply.lex as lex
import ply.yacc as yacc

# Palabras clave reservadas
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    # Agregar otras palabras clave aquí si es necesario
}

# Lista de tokens
tokens = (
    'IF',
    'ELSE',
    'IDENTIFIER',
    'OPEN_PAREN',
    'CLOSE_PAREN',
    'RELATIONAL_OPERATOR',
    'NUMBER',
    'COLON',
    'CONTENT',
    'ILLEGAL'
)

# Definición de patrones para los tokens
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_RELATIONAL_OPERATOR = r'<|>|<=|>=|==|!='
t_COLON = r':'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-z][a-z0-9_]*'  # Solo letras minúsculas para IDENTIFIER
    t.type = reserved.get(t.value, 'IDENTIFIER') if t.value.lower() not in reserved else reserved.get(t.value.lower())
    return t

def t_CONTENT(t):
    r'C'  # Solo la letra C mayúscula para CONTENT
    t.type = 'CONTENT'
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
    declaration : IF OPEN_PAREN IDENTIFIER RELATIONAL_OPERATOR NUMBER CLOSE_PAREN COLON content ELSE COLON content 
                | IF OPEN_PAREN IDENTIFIER RELATIONAL_OPERATOR IDENTIFIER CLOSE_PAREN COLON content ELSE COLON content
    '''
    print("Condicional:", p[3], p[4], p[5], p[9], p[11])
    p[0] = True

def p_error(p):
    print("Error sintáctico en la entrada.")

def p_content(p):
    '''
    content : CONTENT
            | NUMBER
    '''
    p[0] = p[1]
    


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
        valid = True if result else False
    except Exception as e:
        print("Error sintáctico:", e)

    return token_list, lexeme_count, valid
