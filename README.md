# Mini-Triton Parser

Implementación manual de un parser para Mini-Triton usando Recursive Descent Parsing.

El proyecto reutiliza el lexer existente y agrega solo lo necesario para analizar un programa compuesto por un único kernel con sintaxis Mini-Triton.

## Alcance

- Un programa contiene exactamente un kernel.
- El kernel inicia con `@triton.jit`.
- Se soportan parámetros simples y parámetros anotados como `BS: tl.constexpr`.
- Se soportan sentencias de asignación y sentencias con expresiones.
- Las sentencias terminan con `;`.
- Se soportan expresiones con nombres, números, llamadas, paréntesis y los operadores `+`, `-`, `*`, `/`.
- Se soportan llamadas posicionales como `foo(...)`, `tl.load(...)`, `tl.store(...)` y `a.b(...)`.
- No se soportan `if`, `for`, `while`, `return`, kwargs, múltiples funciones ni semántica de ejecución.

## Estructura

- `lexer.py`: lexer reutilizado para convertir el código fuente en tokens.
- `rules.py`: definición de palabras clave, operadores y delimitadores.
- `parser.py`: parser manual con Recursive Descent Parsing.
- `ast_nodes.py`: nodos del AST y método `pretty()` para impresión.
- `parse_error.py`: excepción de error sintáctico.
- `main.py`: ejecuta la suite de pruebas y muestra el AST o el error.
- `test_cases/mini_triton/`: pruebas del parser con metadatos `# expected: valid|invalid`.

## Uso

### Ejecutar la suite de pruebas

```bash
python3 main.py
```

El runner lee todos los archivos `.triton` dentro de `test_cases/mini_triton/`, evalúa si son válidos o inválidos y muestra:

- Resultado por archivo con `✅` o `❌`
- Estado real como `passed` o `error`
- Expectativa del test como `passed` o `error`
- Tabla final con columnas `test | status | expectation | ok`

## Formato de pruebas

Cada archivo de prueba puede incluir una línea inicial como comentario:

```triton
# expected: valid
@triton.jit
def kernel(x): {
	y = x + 1;
}
```

O bien:

```triton
# expected: invalid
@triton.jit
def kernel(x): {
	return x;
}
```

Si el comentario no aparece, el runner asume `valid` por defecto.

## AST

Los nodos principales son:

- `Program`
- `Kernel`
- `Param`
- `Assign`
- `ExprStmt`
- `BinaryOp`
- `Call`
- `Name`
- `Number`

Cada nodo implementa `pretty()` para imprimir el árbol de forma legible.

## Verificación

La suite actual incluye 22 casos de prueba en `test_cases/mini_triton/`.

Cobertura actual:

- Decorador `@triton.jit`
- Declaración de kernel
- Parámetros y anotaciones
- Parámetros vacíos con cuerpo vacío y no vacío
- Asignaciones
- Sentencias de expresión (llamadas sin asignación)
- Precedencia de operadores
- Llamadas anidadas y con acceso por atributo
- Rechazo de kwargs
- Rechazo de `return`, `if`, `for`, `while`
- Rechazo de falta de decorador, decorador incorrecto y falta de `def`
- Rechazo de múltiples kernels
- Errores de sintaxis como falta de `;`, operador incompleto y paréntesis no cerrados

## Nota

Este proyecto no usa ANTLR, PLY, Lark, yacc ni generadores automáticos de parser.