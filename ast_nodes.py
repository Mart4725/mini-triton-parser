from dataclasses import dataclass, field


class AstNode:
    def pretty(self, indent=0):
        raise NotImplementedError

    def __str__(self):
        return self.pretty()

    def _indent(self, level):
        return "    " * level


@dataclass
class Program(AstNode):
    kernel: object

    def pretty(self, indent=0):
        return f"{self._indent(indent)}Program\n{self.kernel.pretty(indent + 1)}"


@dataclass
class Kernel(AstNode):
    decorator: str
    name: str
    params: list = field(default_factory=list)
    body: list = field(default_factory=list)

    def pretty(self, indent=0):
        lines = [f"{self._indent(indent)}Kernel(name={self.name}, decorator={self.decorator})"]
        lines.append(f"{self._indent(indent + 1)}Params")
        if self.params:
            for param in self.params:
                lines.append(param.pretty(indent + 2))
        else:
            lines.append(f"{self._indent(indent + 2)}<empty>")

        lines.append(f"{self._indent(indent + 1)}Body")
        if self.body:
            for statement in self.body:
                lines.append(statement.pretty(indent + 2))
        else:
            lines.append(f"{self._indent(indent + 2)}<empty>")

        return "\n".join(lines)


@dataclass
class Param(AstNode):
    name: str
    annotation: str = None

    def pretty(self, indent=0):
        if self.annotation:
            return f"{self._indent(indent)}Param(name={self.name}, annotation={self.annotation})"
        return f"{self._indent(indent)}Param(name={self.name})"


@dataclass
class Assign(AstNode):
    target: str
    value: object

    def pretty(self, indent=0):
        lines = [f"{self._indent(indent)}Assign(target={self.target})"]
        lines.append(self.value.pretty(indent + 1))
        return "\n".join(lines)


@dataclass
class ExprStmt(AstNode):
    expr: object

    def pretty(self, indent=0):
        lines = [f"{self._indent(indent)}ExprStmt"]
        lines.append(self.expr.pretty(indent + 1))
        return "\n".join(lines)


@dataclass
class BinaryOp(AstNode):
    left: object
    op: str
    right: object

    def pretty(self, indent=0):
        lines = [f"{self._indent(indent)}BinaryOp(op={self.op})"]
        lines.append(self.left.pretty(indent + 1))
        lines.append(self.right.pretty(indent + 1))
        return "\n".join(lines)


@dataclass
class Call(AstNode):
    callee: str
    args: list = field(default_factory=list)

    def pretty(self, indent=0):
        lines = [f"{self._indent(indent)}Call(callee={self.callee})"]
        if self.args:
            lines.append(f"{self._indent(indent + 1)}Args")
            for arg in self.args:
                lines.append(arg.pretty(indent + 2))
        else:
            lines.append(f"{self._indent(indent + 1)}Args <empty>")
        return "\n".join(lines)


@dataclass
class Name(AstNode):
    value: str

    def pretty(self, indent=0):
        return f"{self._indent(indent)}Name(value={self.value})"


@dataclass
class Number(AstNode):
    value: str

    def pretty(self, indent=0):
        return f"{self._indent(indent)}Number(value={self.value})"