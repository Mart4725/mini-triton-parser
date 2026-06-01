import os
from dataclasses import dataclass

from lexer import Lexer
from parser import Parser
from parse_error import ParseError


TESTS_SUBDIR = "test_cases/mini_triton"
TEST_EXTENSION = ".triton"


@dataclass
class TestCaseResult:
    name: str
    expected: str
    actual: str
    passed: bool


def outcome_label(outcome):
    if outcome == "valid":
        return "passed"
    if outcome == "invalid":
        return "error"
    return outcome


def parse_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        code = file.read()

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parseProgram()


def read_expected_outcome(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line:
                continue
            if not line.startswith("#"):
                break

            comment = line[1:].strip().lower()
            if comment.startswith("expected:"):
                expected = comment.split(":", 1)[1].strip()
                if expected in {"valid", "invalid"}:
                    return expected

    return "valid"


def run_test(filepath):
    expected = read_expected_outcome(filepath)
    filename = os.path.basename(filepath)

    try:
        parse_file(filepath)
        actual = "valid"
    except ParseError:
        actual = "invalid"

    return TestCaseResult(
        name=filename,
        expected=expected,
        actual=actual,
        passed=expected == actual,
    )


def print_test_result(result):
    symbol = "✅" if result.passed else "❌"
    status = outcome_label(result.actual)
    expectation = outcome_label(result.expected)
    print(f"{symbol} {result.name} | {status} | {expectation} | {'si' if result.passed else 'no'}")


def print_summary_table(results):
    print("\nFinal summary")
    print("-" * 56)
    print(f"{'test':<34} | {'status':<8} | {'expectation':<11} | {'ok':<2}")
    print(f"{'-' * 34} | {'-' * 8} | {'-' * 11} | {'-' * 2}")
    for result in results:
        status = outcome_label(result.actual)
        expectation = outcome_label(result.expected)
        ok = "✅" if result.passed else "❌"
        print(f"{result.name:<34} | {status:<8} | {expectation:<11} | {ok:<2}")


def main():
    base_dir = os.path.dirname(__file__)
    tests_dir = os.path.join(base_dir, TESTS_SUBDIR)

    results = []

    for filename in sorted(os.listdir(tests_dir)):
        if not filename.endswith(TEST_EXTENSION):
            continue

        filepath = os.path.join(tests_dir, filename)

        print(f"\n📄 Procesando: {filename}")
        print("-" * 40)

        result = run_test(filepath)
        results.append(result)

        try:
            ast = parse_file(filepath)
            print("✅ parse correcto")
            print(ast.pretty())
        except ParseError as error:
            print(f"❌ error sintáctico: {error}")

        print_test_result(result)

    print_summary_table(results)


if __name__ == "__main__":
    main()