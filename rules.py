# Diccionario de palabras clave reservadas del lenguaje
# Mapea cada palabra clave en el codigo fuente a su tipo de token correspondiente
KEYWORDS = {
    "def": "DEF",              # Definir funcion
    "return": "RETURN",        # Retornar valor
    "if": "IF",                # Condicional si
    "else": "ELSE",            # Alternativa si
    "elif": "ELIF",            # Otra alternativa si
    "for": "FOR",              # Bucle for
    "while": "WHILE",          # Bucle while
    "in": "IN",                # Operador de membresita
    "is": "IS",                # Comparacion de identidad
    "and": "AND",              # Operador logico AND
    "or": "OR",                # Operador logico OR
    "not": "NOT",              # Operador logico NOT
    "TRUE": "TRUE",            # Valor verdadero
    "FALSE": "FALSE",          # Valor falso
    "None": "NONE",            # Valor nulo
    "pass": "PASS",            # Operacion nula (placeholder)
    "break": "BREAK",          # Salir del bucle
    "continue": "CONTINUE"     # Continuar con siguiente iteracion
}

# Diccionario de operadores del lenguaje
# Incluye operadores de 2 caracteres primero (se verifican antes que los de 1 caracter)
# Mapea cada operador a su nombre de token correspondiente
OPERATORS = {
    # Operadores de comparacion (2 caracteres)
    "==": "EQ",               # Igualdad
    "!=": "NE",               # Desigualdad
    "<=": "LE",               # Menor o igual
    ">=": "GE",               # Mayor o igual
    
    # Operadores aritmeticos avanzados (2 caracteres)
    "//": "FLOORDIV",         # Division entera (floor division)
    "**": "POWER",             # Potencia (exponenciacion)
    
    # Operadores de asignacion compuesta (2 caracteres)
    "+=": "PLUSEQ",            # Suma y asigna
    "-=": "MINUSEQ",           # Resta y asigna
    "*=": "TIMESEQ",           # Multiplica y asigna
    "/=": "DIVEQ",             # Divide y asigna
    
    # Operadores de desplazamiento de bits (2 caracteres)
    "<<": "LSHIFT",            # Desplazamiento a la izquierda
    ">>": "RSHIFT",            # Desplazamiento a la derecha
    "->": "ARROW",             # Flecha (anotacion de tipo)

    # Operadores aritmeticos basicos (1 caracter)
    "+": "PLUS",               # Suma
    "-": "MINUS",              # Resta
    "*": "TIMES",              # Multiplicacion
    "/": "DIVIDE",             # Division
    "%": "MOD",                # Modulo (residuo)
    
    # Operadores de comparacion (1 caracter)
    "<": "LT",                 # Menor que
    ">": "GT",                 # Mayor que
    
    # Asignacion
    "=": "ASSIGN"              # Asignacion
}

# Diccionario de delimitadores (simbolos de puntuacion y estructuracion)
# Mapea cada delimitador a su nombre de token correspondiente
DELIMITERS = {
    # Parentesis (para funciones y expresiones)
    "(": "LPAREN",              # Parentesis abierto izquierdo
    ")": "RPAREN",              # Parentesis cerrado derecho
    
    # Corchetes (para listas e indexing)
    "[": "LBRACKET",            # Corchete abierto izquierdo
    "]": "RBRACKET",            # Corchete cerrado derecho
    
    # Llaves (para diccionarios y bloques)
    "{": "LBRACE",              # Llave abierta izquierda
    "}": "RBRACE",              # Llave cerrada derecha
    
    # Puntuacion general
    ",": "COMMA",               # Coma (separador)
    ":": "COLON",               # Dos puntos (definicion de bloque)
    ";": "SEMICOLON",           # Fin de sentencia
    ".": "DOT",                 # Punto (acceso a atributos)
    
    # Operadores bit a bit y especiales
    "@": "AT",                  # Arroba (decorador)
    "~": "TILDE",               # Tilde (NOT bit a bit)
    "&": "AMPERSAND",           # Ampersand (AND bit a bit)
    "|": "PIPE",                # Barra vertical (OR bit a bit)
    "^": "CARET"                # Circunflejo (XOR bit a bit)
}