from ast_nodes import Assign, BinaryOp, Call, ExprStmt, Kernel, Name, Number, Param, Program
from parse_error import ParseError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parseProgram(self):
        self._raise_on_lexer_error()
        self._skip_newlines()
        kernel = self.parseKernel()
        self._skip_newlines()
        if not self._at_end():
            raise ParseError("Solo se permite un kernel", self._current())
        return Program(kernel)

    def parseKernel(self):
        decorator = self.parseDecorator()
        self._expect("DEF", "Se esperaba 'def' después del decorador")
        name_token = self._expect("NAME", "Se esperaba el nombre del kernel")
        self._expect("LPAREN", "Se esperaba '(' después del nombre del kernel")
        params = self.parseParams()
        self._expect("RPAREN", "Se esperaba ')' al final de la lista de parámetros")
        self._expect("COLON", "Se esperaba ':' después de la firma del kernel")
        self._expect("LBRACE", "Se esperaba '{' para abrir el cuerpo del kernel")
        body = self.parseStmtList()
        self._expect("RBRACE", "Se esperaba '}' para cerrar el cuerpo del kernel")
        return Kernel(decorator=decorator, name=name_token.value, params=params, body=body)

    def parseDecorator(self):
        self._skip_newlines()
        self._expect("AT", "Se esperaba '@' al inicio del decorador")
        first = self._expect("NAME", "Se esperaba 'triton' en el decorador")
        self._expect("DOT", "Se esperaba '.' en el decorador")
        second = self._expect("NAME", "Se esperaba 'jit' en el decorador")
        if first.value != "triton" or second.value != "jit":
            raise ParseError("El decorador debe ser '@triton.jit'", first)
        return "@triton.jit"

    def parseParams(self):
        params = []
        self._skip_newlines()
        if self._check("RPAREN"):
            return params

        while True:
            params.append(self.parseParam())
            self._skip_newlines()
            if self._match("COMMA"):
                self._skip_newlines()
                if self._check("RPAREN"):
                    raise ParseError("No se permiten comas finales en la lista de parámetros", self._current())
                continue
            break

        return params

    def parseParam(self):
        name_token = self._expect("NAME", "Se esperaba un nombre de parámetro")
        annotation = None
        self._skip_newlines()
        if self._match("COLON"):
            self._skip_newlines()
            annotation = self._parseQualifiedName()
        return Param(name=name_token.value, annotation=annotation)

    def parseStmtList(self):
        statements = []
        while True:
            self._skip_newlines()
            if self._check("RBRACE"):
                break
            if self._at_end():
                raise ParseError("Se esperaba '}' al final del cuerpo del kernel", self._previous())

            statements.append(self.parseStmt())
            self._skip_newlines()
            self._expect("SEMICOLON", "Toda sentencia debe terminar con ';'")

        return statements

    def parseStmt(self):
        self._skip_newlines()
        if self._check("NAME") and self._lookahead_non_newline(1) and self._lookahead_non_newline(1).type == "ASSIGN":
            return self.parseAssign()
        return self.parseExprStmt()

    def parseAssign(self):
        target = self._expect("NAME", "Se esperaba un identificador en la asignación")
        self._expect("ASSIGN", "Se esperaba '=' en la asignación")
        value = self.parseExpr()
        return Assign(target=target.value, value=value)

    def parseExprStmt(self):
        expr = self.parseExpr()
        return ExprStmt(expr=expr)

    def parseExpr(self):
        return self.parseAddExpr()

    def parseAddExpr(self):
        expr = self.parseMulExpr()
        while True:
            self._skip_newlines()
            if self._match("PLUS"):
                right = self.parseMulExpr()
                expr = BinaryOp(expr, "+", right)
                continue
            if self._match("MINUS"):
                right = self.parseMulExpr()
                expr = BinaryOp(expr, "-", right)
                continue
            break
        return expr

    def parseMulExpr(self):
        expr = self.parsePrimary()
        while True:
            self._skip_newlines()
            if self._match("TIMES"):
                right = self.parsePrimary()
                expr = BinaryOp(expr, "*", right)
                continue
            if self._match("DIVIDE"):
                right = self.parsePrimary()
                expr = BinaryOp(expr, "/", right)
                continue
            break
        return expr

    def parsePrimary(self):
        self._skip_newlines()
        if self._match("NUMBER"):
            return Number(self._previous().value)
        if self._check("NAME"):
            return self.parseNameOrCall()
        if self._match("LPAREN"):
            expr = self.parseExpr()
            self._expect("RPAREN", "Se esperaba ')' para cerrar la expresión")
            return expr
        if self._check("RETURN") or self._check("IF") or self._check("FOR") or self._check("WHILE"):
            raise ParseError("Esa sentencia no está soportada en Mini-Triton", self._current())
        raise ParseError("Se esperaba una expresión", self._current())

    def parseNameOrCall(self):
        callee = self._parseQualifiedName()
        self._skip_newlines()
        if self._match("LPAREN"):
            args = self.parseArgs()
            self._expect("RPAREN", "Se esperaba ')' al final de la llamada")
            return Call(callee=callee, args=args)
        return Name(callee)

    def parseArgs(self):
        args = []
        self._skip_newlines()
        if self._check("RPAREN"):
            return args

        while True:
            self._skip_newlines()
            if self._check("NAME") and self._lookahead_non_newline(1) and self._lookahead_non_newline(1).type == "ASSIGN":
                raise ParseError("Solo se permiten argumentos posicionales", self._current())

            args.append(self.parseExpr())
            self._skip_newlines()
            if self._match("COMMA"):
                self._skip_newlines()
                if self._check("RPAREN"):
                    raise ParseError("No se permiten comas finales en la lista de argumentos", self._current())
                continue
            break

        return args

    def _parseQualifiedName(self):
        token = self._expect("NAME", "Se esperaba un nombre")
        parts = [token.value]
        while True:
            self._skip_newlines()
            if not self._match("DOT"):
                break
            next_name = self._expect("NAME", "Se esperaba un identificador después de '.'")
            parts.append(next_name.value)
        return ".".join(parts)

    def _current(self):
        if self._at_end():
            return self._previous()
        return self.tokens[self.pos]

    def _previous(self):
        if self.pos == 0:
            return None
        return self.tokens[self.pos - 1]

    def _at_end(self):
        return self.pos >= len(self.tokens)

    def _skip_newlines(self):
        while not self._at_end() and self._current().type == "NEWLINE":
            self.pos += 1

    def _check(self, token_type):
        self._skip_newlines()
        return not self._at_end() and self._current().type == token_type

    def _match(self, token_type):
        if self._check(token_type):
            self.pos += 1
            return True
        return False

    def _expect(self, token_type, message):
        self._skip_newlines()
        if self._at_end() or self._current().type != token_type:
            raise ParseError(message, self._current())
        token = self._current()
        self.pos += 1
        return token

    def _lookahead_non_newline(self, distance):
        index = self.pos
        remaining = distance
        while index < len(self.tokens):
            token = self.tokens[index]
            if token.type != "NEWLINE":
                if remaining == 0:
                    return token
                remaining -= 1
            index += 1
        return None

    def _raise_on_lexer_error(self):
        for token in self.tokens:
            if token.type == "ERROR":
                message = token.error or "Error léxico"
                raise ParseError(message, token)