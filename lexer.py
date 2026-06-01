from custom_token import Token
import rules

class Lexer:
    """Analizador lexico (Lexer) que convierte codigo fuente en tokens."""
    
    def __init__(self, code):
        """
        Inicializa el lexer con el codigo fuente.
        
        Args:
            code: String con el codigo fuente a analizar
        """
        self.code = code        # Codigo fuente a procesar
        self.pos = 0            # Posicion actual en el codigo (indice)
        self.tokens = []        # Lista de tokens encontrados
        self.line = 1           # Numero de linea actual (para errores)
        self.column = 1         # Numero de columna actual (para errores)

    def peek(self):
        """Retorna el caracter actual sin avanzar. Retorna None si llegamos al final."""
        if self.pos < len(self.code):
            return self.code[self.pos]
        return None

    def advance(self):
        """
        Avanza una posicion en el codigo.
        Actualiza linea y columna segun corresponda (resetea columna en saltos de linea).
        """
        current = self.peek()

        if current == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.pos += 1

    def tokenize(self):
        """
        Metodo principal: recorre el codigo y genera tokens.
        Distribuye el procesamiento segun el tipo de caracter encontrado.
        
        Returns:
            Lista de tokens encontrados en el codigo
        """
        while self.pos < len(self.code):
            current = self.peek()

            if current is None:
                break

            # COMENTARIOS: comienzan con #
            if current == '#':
                self.handle_comment()

            # ESPACIOS EN BLANCO: espacios, tabulaciones, saltos de linea
            elif current.isspace():
                self.handle_whitespace()

            # IDENTIFICADORES: letras o guiones bajos (nombran variables, funciones)
            elif current.isalpha() or current == '_':
                self.tokens.append(self.handle_identifier())

            # NUMEROS: digitos (pueden incluir puntos para decimales)
            elif current.isdigit():
                self.tokens.append(self.handle_number())

            # CADENAS: texto entre comillas dobles
            elif current == '"':
                self.tokens.append(self.handle_string())

            # SIMBOLOS: operadores y delimitadores
            else:
                self.tokens.append(self.handle_symbol())

        return self.tokens

    def handle_comment(self):
        """
        Procesa comentarios que comienzan con #.
        Los comentarios se ignoran y no se agregan como tokens.
        Se extienden hasta el final de la linea.
        """
        start_line = self.line
        start_col = self.column

        self.advance()  # Saltar el caracter #

        comment_text = ""

        # Leer todo hasta el salto de linea
        while self.peek() and self.peek() != '\n':
            comment_text += self.peek()
            self.advance()

        # Los comentarios se descartan (no generan tokens)

    def handle_whitespace(self):
        """
        Procesa espacios en blanco (espacios, tabulaciones, saltos de linea).
        Los saltos de linea generan tokens NEWLINE (importante para la sintaxis).
        Otros espacios en blanco se ignoran.
        """
        if self.peek() == '\n':
            # Los saltos de linea SI generan tokens (son significativos)
            self.tokens.append(Token("NEWLINE", "\\n", None, self.line, self.column))
        # Otros espacios en blanco se descartan
        self.advance()

    def handle_identifier(self):
        """
        Procesa identificadores: nombres de variables, funciones, etc.
        Los identificadores validos comienzan con letra o guion bajo.
        Tambien detecta palabras clave y las clasifica correctamente.
        """
        start = self.pos
        start_line = self.line
        start_col = self.column

        # ERROR: empieza con numero (validacion defensiva)
        if self.peek().isdigit():
            while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
                self.advance()

            lexeme = self.code[start:self.pos]
            return Token(
                "ERROR",
                lexeme,
                "El identificador no puede empezar con un dígito",
                start_line,
                start_col
            )

        # Consumir letras, digitos y guiones bajos
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            self.advance()

        lexeme = self.code[start:self.pos]

        # Verificar si es una palabra clave
        if lexeme in rules.KEYWORDS:
            return Token(rules.KEYWORDS[lexeme], lexeme, None, start_line, start_col)

        # Es un identificador normal
        return Token("NAME", lexeme, None, start_line, start_col)

    def handle_number(self):
        """
        Procesa numeros (enteros y decimales).
        Soporta numeros enteros (42) y decimales (3.14) con maximo un punto.
        Detecta errores cuando hay mezcla confusa (ej: 2bad, 10abc).
        """
        start = self.pos
        start_line = self.line
        start_col = self.column

        has_dot = False  # Control para un solo punto decimal

        # Consumir digitos y maximo un punto
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            if self.peek() == '.':
                if has_dot:  # Ya habia un punto, detener
                    break
                has_dot = True
            self.advance()

        # ERROR: mezcla confusa como "2bad" o "10abc"
        if self.peek() and self.peek().isalpha():
            # Consumir el resto del token invalido
            while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
                self.advance()

            lexeme = self.code[start:self.pos]
            return Token(
                "ERROR",
                lexeme,
                "Mezcla inválida de número/identificador (comienza o continúa incorrectamente)",
                start_line,
                start_col
            )

        # Numero valido
        lexeme = self.code[start:self.pos]
        return Token("NUMBER", lexeme, None, start_line, start_col)

    def handle_string(self):
        """
        Procesa cadenas de texto entre comillas dobles.
        Las cadenas comienzan y terminan con comillas dobles ("...").
        Detecta errores si la cadena no se cierra correctamente.
        """
        start_line = self.line
        start_col = self.column

        self.advance()  # Saltar la comilla abierta "

        # Guardar posicion del inicio del contenido
        start = self.pos

        # Buscar la comilla de cierre
        while self.peek() and self.peek() != '"':
            self.advance()

        # ERROR: string no cerrada (llegamos al fin sin encontrar cierre)
        if self.peek() != '"':
            lexeme = self.code[start:self.pos]
            return Token(
                "ERROR",
                lexeme,
                "Literal de cadena no terminada",
                start_line,
                start_col
            )

        # Extraer el contenido de la cadena (sin las comillas)
        lexeme = self.code[start:self.pos]
        self.advance()  # Saltar la comilla de cierre

        return Token("STRING", lexeme, None, start_line, start_col)

    def handle_symbol(self):
        """
        Procesa simbolos: operadores (+, -, ==, etc.) y delimitadores (, [, {, etc.).
        
        Estrategia:
        1. Primero intenta reconocer operadores de 2 caracteres (==, !=, <=, >=, etc.)
        2. Luego intenta operadores de 1 caracter (+, -, *, /, etc.)
        3. Luego intenta delimitadores (, [, {, etc.)
        4. Si nada coincide, retorna ERROR con caracter no reconocido
        """
        start_line = self.line
        start_col = self.column

        # Intentar operadores de 2 caracteres primero
        if self.pos + 1 < len(self.code):
            two = self.code[self.pos:self.pos+2]
            if two in rules.OPERATORS:
                self.pos += 2      # Avanzar 2 posiciones
                self.column += 2   # Avanzar 2 columnas
                return Token(rules.OPERATORS[two], two, None, start_line, start_col)

        current = self.peek()

        # Intentar operador de 1 caracter
        if current in rules.OPERATORS:
            self.advance()
            return Token(rules.OPERATORS[current], current, None, start_line, start_col)

        # Intentar delimitador
        if current in rules.DELIMITERS:
            self.advance()
            return Token(rules.DELIMITERS[current], current, None, start_line, start_col)

        # ERROR: caracter no reconocido
        self.advance()
        return Token(
            "ERROR",
            current,
            "Carácter no reconocido",
            start_line,
            start_col
        )