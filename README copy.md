# Lexer - Analizador Léxico

Un analizador léxico completo escrito en Python que convierte código fuente en tokens. Este proyecto forma parte del estudio de compiladores y demuestra los principios fundamentales del análisis léxico en el proceso de traducción de lenguajes de programación.

## 📋 Descripción

El lexer procesa código fuente carácter por carácter y genera una secuencia de tokens, identificando:
- **Palabras clave reservadas** (def, return, if, for, while, etc.)
- **Identificadores** (nombres de variables, funciones, etc.)
- **Números** (enteros y flotantes)
- **Cadenas** (strings entre comillas simples y dobles)
- **Operadores** (aritméticos, comparación, asignación, lógicos, bitwise)
- **Delimitadores** (paréntesis, corchetes, llaves, comas, puntos, etc.)
- **Saltos de línea y espacios en blanco**

Cada token almacena información detallada incluyendo su tipo, valor literal, número de línea y columna para facilitar el reporte de errores.

## 🏗️ Estructura del Proyecto

```
lexer/
├── lexer.py              # Clase principal del analizador léxico
├── custom_token.py       # Definición de la clase Token
├── rules.py              # Palabras clave y operadores del lenguaje
├── main.py               # Script de prueba para ejecutar el lexer
├── input.txt             # Archivo de entrada de ejemplo
├── README.md             # Este archivo
└── test_cases/
    ├── basics/           # Casos de prueba básicos (.txt)
    └── triton/           # Casos de prueba avanzados (.triton)
```

## 🚀 Uso Rápido

### Opción 1: Con archivos de prueba

```bash
python main.py
```

Esto procesará todos los archivos `.triton` en `test_cases/triton/` (configurable en `main.py`).

### Opción 2: Procesar un archivo específico

Edita `input.txt` con tu código y ejecuta:

```bash
python main.py
```

O usa el lexer directamente en tu código:

```python
from lexer import Lexer

code = """
def suma(a, b):
    return a + b
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

for token in tokens:
    print(token)
```

## 📝 Ejemplo

### Entrada (input.txt)

```python
def suma(a, b):
    return a + b

x = 10
y = 20
resultado = suma(x, y)

if resultado >= 30:
    print("mayor o igual")
```

### Salida

```
       DEF |        def |                      — | 1:1
      NAME |       suma |                      — | 1:5
     LPAREN |          ( |                      — | 1:9
      NAME |          a |                      — | 1:10
     COMMA |          , |                      — | 1:11
      NAME |          b |                      — | 1:13
     RPAREN |          ) |                      — | 1:14
     COLON |          : |                      — | 1:15
    NEWLINE |         \n |                      — | 1:16
    RETURN |     return |                      — | 2:5
      NAME |          a |                      — | 2:12
      PLUS |          + |                      — | 2:14
      NAME |          b |                      — | 2:16
    NEWLINE |         \n |                      — | 2:17
```

## 📚 Características

### Palabras Clave Soportadas

Control de flujo: `def`, `return`, `if`, `else`, `elif`, `for`, `while`, `break`, `continue`, `pass`

Operadores lógicos: `and`, `or`, `not`, `in`, `is`

Valores: `True`, `False`, `None`

### Operadores Soportados

**Aritméticos:** `+`, `-`, `*`, `/`, `//`, `**`, `%`

**Comparación:** `==`, `!=`, `<`, `>`, `<=`, `>=`

**Asignación:** `=`, `+=`, `-=`, `*=`, `/=`

**Lógicos:** `and`, `or`, `not`

**Bitwise:** `<<`, `>>`, `&`, `|`, `^`, `~`

**Especiales:** `->` (anotación de tipos)

### Delimitadores

Paréntesis: `()`, Corchetes: `[]`, Llaves: `{}`, Comas: `,`, Puntos: `.`, Dos puntos: `:`

## 🧪 Casos de Prueba

El proyecto incluye dos conjuntos de casos de prueba:

- **basics/**: Pruebas básicas en formato `.txt`
  - Identificadores válidos e inválidos
  - Números válidos e inválidos
  - Cadenas correctas y con errores
  - Operadores complejos
  - Delimitadores
  - Espacios y nuevas líneas

- **triton/**: Casos de estrés y complejos en formato `.triton`
  - Código básico mixto
  - Expresiones complejas
  - Casos extremos de operadores
  - Errores de cadenas y símbolos
  - Entrada sucia y combinaciones variadas

## 🔧 Componentes

### lexer.py

Clase `Lexer`: Núcleo del analizador
- `peek()`: Obtiene el carácter actual
- `advance()`: Avanza una posición
- `tokenize()`: Método principal que genera tokens

### custom_token.py

Clase `Token`: Representa un token individual
- `type`: Tipo del token (DEF, NAME, NUMBER, etc.)
- `value`: Valor literal del token
- `error`: Mensaje de error si aplica
- `line`, `column`: Posición en el código

### rules.py

Define:
- `KEYWORDS`: Palabras clave del lenguaje
- `OPERATORS`: Operadores soportados

## 📌 Notas Importantes

- Los espacios en blanco se ignoran
- Los saltos de línea se registran como tokens `NEWLINE`
- Cada token incluye información de línea y columna para debugging
- **Limitación actual**: El lexer no gestiona tokens de indentación (`INDENT`, `DEDENT`)
- La detección de errores se incluye en algunos casos (strings malformados, símbolos inválidos)

## 🎓 Propósito Educativo

Este proyecto demuestra:
- Conceptos fundamentales del análisis léxico
- Máquinas de estados simples
- Manejo de caracteres especiales
- Generación de tokens con información de contexto
- Buenas prácticas en validación y reporte de errores

## 📄 Licencia

Proyecto educativo - Libre para usar y modificar.
