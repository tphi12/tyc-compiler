from tests.utils import ASTGenerator
from src.utils.nodes import *

def test_001():
    source = """
void main() {
    printString("Hello, World!");
}
"""
    expected = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(
                    FuncCall("printString", [StringLiteral("Hello, World!")])
                )
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_002():
    source = """
int add(int x, int y) {
    return x + y;
}

int multiply(int x, int y) {
    return x * y;
}

void main() {
    auto a = readInt();
    auto b = readInt();
    
    auto sum = add(a, b);
    auto product = multiply(a, b);
    
    printInt(sum);
    printInt(product);
}
"""
    expected = Program([
        FuncDecl(
            IntType(),
            "add",
            [Param(IntType(), "x"), Param(IntType(), "y")],
            BlockStmt([
                ReturnStmt(
                    BinaryOp(Identifier("x"), "+", Identifier("y"))
                )
            ])
        ),
        FuncDecl(
            IntType(),
            "multiply",
            [Param(IntType(), "x"), Param(IntType(), "y")],
            BlockStmt([
                ReturnStmt(
                    BinaryOp(Identifier("x"), "*", Identifier("y"))
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "a", FuncCall("readInt", [])),
                VarDecl(None, "b", FuncCall("readInt", [])),
                VarDecl(None, "sum", FuncCall("add", [Identifier("a"), Identifier("b")])),
                VarDecl(None, "product", FuncCall("multiply", [Identifier("a"), Identifier("b")])),
                ExprStmt(FuncCall("printInt", [Identifier("sum")])),
                ExprStmt(FuncCall("printInt", [Identifier("product")]))
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_003():
    source = """
void main() {
    auto n = readInt();
    auto i = 0;
    
    while (i < n) {
        printInt(i);
        ++i;
    }
    
    for (auto j = 0; j < n; ++j) {
        if (j % 2 == 0) {
            printInt(j);
        }
    }
}
"""
    expected = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "n", FuncCall("readInt", [])),
                VarDecl(None, "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", Identifier("n")),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(PrefixOp("++", Identifier("i")))
                    ])
                ),
                ForStmt(
                    VarDecl(None, "j", IntLiteral(0)),
                    BinaryOp(Identifier("j"), "<", Identifier("n")),
                    PrefixOp("++", Identifier("j")),
                    BlockStmt([
                        IfStmt(
                            BinaryOp(
                                BinaryOp(Identifier("j"), "%", IntLiteral(2)),
                                "==",
                                IntLiteral(0)
                            ),
                            BlockStmt([
                                ExprStmt(FuncCall("printInt", [Identifier("j")]))
                            ]),
                            None
                        )
                    ])
                )
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_004():
    source = """
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

void main() {
    auto num = readInt();
    auto result = factorial(num);
    printInt(result);
}
"""
    expected = Program([
        FuncDecl(
            IntType(),
            "factorial",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("n"), "<=", IntLiteral(1)),
                    BlockStmt([
                        ReturnStmt(IntLiteral(1))
                    ]),
                    BlockStmt([
                        ReturnStmt(
                            BinaryOp(
                                Identifier("n"),
                                "*",
                                FuncCall(
                                    "factorial",
                                    [BinaryOp(Identifier("n"), "-", IntLiteral(1))]
                                )
                            )
                        )
                    ])
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "num", FuncCall("readInt", [])),
                VarDecl(None, "result", FuncCall("factorial", [Identifier("num")])),
                ExprStmt(FuncCall("printInt", [Identifier("result")]))
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_005():
    source = """
void main() {
    // With auto and initialization
    auto x = readInt();
    auto y = readFloat();
    auto name = readString();
    
    // With auto without initialization
    auto sum;
    sum = x + y;              // sum: float (inferred from first usage - assignment)
    
    // With explicit type and initialization
    int count = 0;
    float total = 0.0;
    string greeting = "Hello, ";
    
    // With explicit type without initialization
    int i;
    float f;
    i = readInt();            // assignment to int
    f = readFloat();          // assignment to float
    
    printFloat(sum);
    printString(greeting);
    printString(name);
}
"""
    expected = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "x", FuncCall("readInt", [])),
                VarDecl(None, "y", FuncCall("readFloat", [])),
                VarDecl(None, "name", FuncCall("readString", [])),

                VarDecl(None, "sum", None),
                ExprStmt(
                    AssignExpr(
                        Identifier("sum"),
                        BinaryOp(Identifier("x"), "+", Identifier("y"))
                    )
                ),

                VarDecl(IntType(), "count", IntLiteral(0)),
                VarDecl(FloatType(), "total", FloatLiteral(0.0)),
                VarDecl(StringType(), "greeting", StringLiteral("Hello, ")),

                VarDecl(IntType(), "i", None),
                VarDecl(FloatType(), "f", None),
                ExprStmt(
                    AssignExpr(Identifier("i"), FuncCall("readInt", []))
                ),
                ExprStmt(
                    AssignExpr(Identifier("f"), FuncCall("readFloat", []))
                ),

                ExprStmt(FuncCall("printFloat", [Identifier("sum")])),
                ExprStmt(FuncCall("printString", [Identifier("greeting")])),
                ExprStmt(FuncCall("printString", [Identifier("name")]))
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)
def test_006():
    source = """void main() { auto a = 1 + 2 * 3 / 4 % 5 - 6; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = BinaryOp(BinaryOp(IntLiteral(1), +, BinaryOp(BinaryOp(BinaryOp(IntLiteral(2), *, IntLiteral(3)), /, IntLiteral(4)), %, IntLiteral(5))), -, IntLiteral(6)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_007():
    source = """void main() { auto a = (1 + 2) * (3 / (4 % 5)); }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), *, BinaryOp(IntLiteral(3), /, BinaryOp(IntLiteral(4), %, IntLiteral(5)))))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_008():
    source = """void main() { auto a = a == b != c < d <= e > f >= g; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = BinaryOp(BinaryOp(Identifier(a), ==, Identifier(b)), !=, BinaryOp(BinaryOp(BinaryOp(BinaryOp(Identifier(c), <, Identifier(d)), <=, Identifier(e)), >, Identifier(f)), >=, Identifier(g))))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_009():
    source = """void main() { auto a = 1 && 2 || 3 && 4 || 5; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = BinaryOp(BinaryOp(BinaryOp(IntLiteral(1), &&, IntLiteral(2)), ||, BinaryOp(IntLiteral(3), &&, IntLiteral(4))), ||, IntLiteral(5)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_010():
    source = """void main() { auto a = !a && !!b || !!!c; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = BinaryOp(BinaryOp(PrefixOp(!Identifier(a)), &&, PrefixOp(!PrefixOp(!Identifier(b)))), ||, PrefixOp(!PrefixOp(!PrefixOp(!Identifier(c))))))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_011():
    source = """void main() { auto a = - - 1; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PrefixOp(-PrefixOp(-IntLiteral(1))))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_012():
    source = """void main() { auto a = + + 1; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PrefixOp(+PrefixOp(+IntLiteral(1))))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_013():
    source = """void main() { auto a = - + - 1; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PrefixOp(-PrefixOp(+PrefixOp(-IntLiteral(1)))))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_014():
    source = """void main() { auto a = ++--++a; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PrefixOp(++PrefixOp(--PrefixOp(++Identifier(a)))))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_015():
    source = """void main() { auto a = a++--++; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PostfixOp(PostfixOp(PostfixOp(Identifier(a)++)--)++))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_016():
    source = """void main() { auto a = ++a++; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PrefixOp(++PostfixOp(Identifier(a)++)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_017():
    source = """void main() { auto a = --a--; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PrefixOp(--PostfixOp(Identifier(a)--)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_018():
    source = """void main() { auto a = ++a++--; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PrefixOp(++PostfixOp(PostfixOp(Identifier(a)++)--)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_019():
    source = """void main() { auto a = -a++; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PrefixOp(-PostfixOp(Identifier(a)++)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_020():
    source = """void main() { auto a = !a++; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PrefixOp(!PostfixOp(Identifier(a)++)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_021():
    source = """void main() { auto a = a = b = c = 1; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = AssignExpr(Identifier(a) = AssignExpr(Identifier(b) = AssignExpr(Identifier(c) = IntLiteral(1)))))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_022():
    source = """void main() { auto a = (a = 1) + (b = 2); }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = BinaryOp(AssignExpr(Identifier(a) = IntLiteral(1)), +, AssignExpr(Identifier(b) = IntLiteral(2))))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_023():
    source = """void main() { auto a = (a = 1 + 2) * 3; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = BinaryOp(AssignExpr(Identifier(a) = BinaryOp(IntLiteral(1), +, IntLiteral(2))), *, IntLiteral(3)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_024():
    source = """void main() { auto a = f().x = 1; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = AssignExpr(MemberAccess(FuncCall(f, []).x) = IntLiteral(1)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_025():
    source = """void main() { auto a = (a+b).x = 1; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = AssignExpr(MemberAccess(BinaryOp(Identifier(a), +, Identifier(b)).x) = IntLiteral(1)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_026():
    source = """void main() { auto a = f(1+2, g(3), h(4, 5)); }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = FuncCall(f, [BinaryOp(IntLiteral(1), +, IntLiteral(2)), FuncCall(g, [IntLiteral(3)]), FuncCall(h, [IntLiteral(4), IntLiteral(5)])]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_027():
    source = """void main() { auto a = f(a = 1, b = 2); }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = FuncCall(f, [AssignExpr(Identifier(a) = IntLiteral(1)), AssignExpr(Identifier(b) = IntLiteral(2))]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_028():
    source = """void main() { auto a = f({1, 2}, {3, 4}); }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = FuncCall(f, [StructLiteral({IntLiteral(1), IntLiteral(2)}), StructLiteral({IntLiteral(3), IntLiteral(4)})]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_029():
    source = """void main() { auto a = f().x.y; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = MemberAccess(MemberAccess(FuncCall(f, []).x).y))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_030():
    source = """void main() { auto a = ++a.b.c; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PrefixOp(++MemberAccess(MemberAccess(Identifier(a).b).c)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_031():
    source = """void main() { auto a = a.b.c++; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PostfixOp(MemberAccess(MemberAccess(Identifier(a).b).c)++))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_032():
    source = """void main() { auto a = ++a.b.c++; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = PrefixOp(++PostfixOp(MemberAccess(MemberAccess(Identifier(a).b).c)++)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_033():
    source = """void main() { auto a = {}; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = StructLiteral({}))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_034():
    source = """void main() { auto a = {1}; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = StructLiteral({IntLiteral(1)}))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_035():
    source = """void main() { auto a = {1, 2, 3}; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = StructLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3)}))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_036():
    source = """void main() { auto a = {{1, 2}, {3, 4}}; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = StructLiteral({StructLiteral({IntLiteral(1), IntLiteral(2)}), StructLiteral({IntLiteral(3), IntLiteral(4)})}))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_037():
    source = """void main() { auto a = {1+2, 3*4, f()}; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = StructLiteral({BinaryOp(IntLiteral(1), +, IntLiteral(2)), BinaryOp(IntLiteral(3), *, IntLiteral(4)), FuncCall(f, [])}))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_038():
    source = """void main() { auto a = {a=1, b=2}; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = StructLiteral({AssignExpr(Identifier(a) = IntLiteral(1)), AssignExpr(Identifier(b) = IntLiteral(2))}))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_039():
    source = """struct Empty {};"""
    expected = """Program([StructDecl(Empty, [])])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_040():
    source = """struct Point { int x; };"""
    expected = """Program([StructDecl(Point, [MemberDecl(IntType(), x)])])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_041():
    source = """struct Point { int x; float y; string z; };"""
    expected = """Program([StructDecl(Point, [MemberDecl(IntType(), x), MemberDecl(FloatType(), y), MemberDecl(StringType(), z)])])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_042():
    source = """struct Line { Point p1; Point p2; };"""
    expected = """Program([StructDecl(Line, [MemberDecl(StructType(Point), p1), MemberDecl(StructType(Point), p2)])])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_043():
    source = """void main() { Point p; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(Point), p)]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_044():
    source = """void main() { Point p = {1, 2}; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(Point), p = StructLiteral({IntLiteral(1), IntLiteral(2)}))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_045():
    source = """void main() { Line l = {{1, 2}, {3, 4}}; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(Line), l = StructLiteral({StructLiteral({IntLiteral(1), IntLiteral(2)}), StructLiteral({IntLiteral(3), IntLiteral(4)})}))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_046():
    source = """void main() { auto a; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a)]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_047():
    source = """void main() { int a; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), a)]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_048():
    source = """void main() { float a; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(FloatType(), a)]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_049():
    source = """void main() { string a; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StringType(), a)]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_050():
    source = """void main() { auto a = 1; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = IntLiteral(1))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_051():
    source = """void main() { int a = 1; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), a = IntLiteral(1))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_052():
    source = """void main() { float a = 1.0; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(FloatType(), a = FloatLiteral(1.0))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_053():
    source = """void main() { string a = "str"; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StringType(), a = StringLiteral('str'))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_054():
    source = """void main() { auto a = 1.5e-10; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = FloatLiteral(1.5e-10))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_055():
    source = """void main() { auto a = .123; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = FloatLiteral(0.123))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_056():
    source = """void main() { auto a = 1.; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = FloatLiteral(1.0))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_057():
    source = """void main() { if (1) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_058():
    source = """void main() { if (1) {} else {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then BlockStmt([]), else BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_059():
    source = """void main() { if (1) if (2) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then IfStmt(if IntLiteral(2) then BlockStmt([])))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_060():
    source = """void main() { if (1) if (2) {} else {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then IfStmt(if IntLiteral(2) then BlockStmt([]), else BlockStmt([])))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_061():
    source = """void main() { if (1) {} else if (2) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then BlockStmt([]), else IfStmt(if IntLiteral(2) then BlockStmt([])))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_062():
    source = """void main() { if (1) {} else if (2) {} else {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then BlockStmt([]), else IfStmt(if IntLiteral(2) then BlockStmt([]), else BlockStmt([])))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_063():
    source = """void main() { if (1) { if (2) {} } else { if (3) {} } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then BlockStmt([IfStmt(if IntLiteral(2) then BlockStmt([]))]), else BlockStmt([IfStmt(if IntLiteral(3) then BlockStmt([]))]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_064():
    source = """void main() { if (a=1) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if AssignExpr(Identifier(a) = IntLiteral(1)) then BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_065():
    source = """void main() { if (a++) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if PostfixOp(Identifier(a)++) then BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_066():
    source = """void main() { while (1) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while IntLiteral(1) do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_067():
    source = """void main() { while (1) if (2) break; else continue; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while IntLiteral(1) do IfStmt(if IntLiteral(2) then BreakStmt(), else ContinueStmt()))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_068():
    source = """void main() { while (1) { while (2) {} } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while IntLiteral(1) do BlockStmt([WhileStmt(while IntLiteral(2) do BlockStmt([]))]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_069():
    source = """void main() { while (a=1) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while AssignExpr(Identifier(a) = IntLiteral(1)) do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_070():
    source = """void main() { while (a.b.c > 5) { a.b.c--; } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while BinaryOp(MemberAccess(MemberAccess(Identifier(a).b).c), >, IntLiteral(5)) do BlockStmt([ExprStmt(PostfixOp(MemberAccess(MemberAccess(Identifier(a).b).c)--))]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_071():
    source = """void main() { for (;;) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; None do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_072():
    source = """void main() { for (auto a=1;;) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(auto, a = IntLiteral(1)); None; None do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_073():
    source = """void main() { for (a=1;;) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for ExprStmt(AssignExpr(Identifier(a) = IntLiteral(1))); None; None do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_074():
    source = """void main() { for (;1;) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; IntLiteral(1); None do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_075():
    source = """void main() { for (;;a=1) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; AssignExpr(Identifier(a) = IntLiteral(1)) do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_076():
    source = """void main() { for (;;a++) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; PostfixOp(Identifier(a)++) do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_077():
    source = """void main() { for (;;++a) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; PrefixOp(++Identifier(a)) do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_078():
    source = """void main() { for (;;a.b++) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; PostfixOp(MemberAccess(Identifier(a).b)++) do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_079():
    source = """void main() { for (;;f()) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; FuncCall(f, []) do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_080():
    source = """void main() { for (auto a=1; a<10; a++) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(auto, a = IntLiteral(1)); BinaryOp(Identifier(a), <, IntLiteral(10)); PostfixOp(Identifier(a)++) do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_081():
    source = """void main() { for (a=1; a<10; a=a+1) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for ExprStmt(AssignExpr(Identifier(a) = IntLiteral(1))); BinaryOp(Identifier(a), <, IntLiteral(10)); AssignExpr(Identifier(a) = BinaryOp(Identifier(a), +, IntLiteral(1))) do BlockStmt([]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_082():
    source = """void main() { for (;;) { for(;;) {} } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; None do BlockStmt([ForStmt(for None; None; None do BlockStmt([]))]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_083():
    source = """void main() { for (int i = 0;; i++) if (i > 10) break; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); None; PostfixOp(Identifier(i)++) do IfStmt(if BinaryOp(Identifier(i), >, IntLiteral(10)) then BreakStmt()))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_084():
    source = """void main() { switch (1) {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [])]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_085():
    source = """void main() { switch (1) { case 1: } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case IntLiteral(1): [])])]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_086():
    source = """void main() { switch (1) { default: } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [], default DefaultStmt(default: []))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_087():
    source = """void main() { switch (1) { case 1: break; case 2: break; } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case IntLiteral(1): [BreakStmt()]), CaseStmt(case IntLiteral(2): [BreakStmt()])])]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_088():
    source = """void main() { switch (1) { case 1: break; default: break; } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case IntLiteral(1): [BreakStmt()])], default DefaultStmt(default: [BreakStmt()]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_089():
    source = """void main() { switch (1) { case 1: break; case 2: break; default: break; } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case IntLiteral(1): [BreakStmt()]), CaseStmt(case IntLiteral(2): [BreakStmt()])], default DefaultStmt(default: [BreakStmt()]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_090():
    source = """void main() { switch (1) { default: break; case 1: break; case 2: break; } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case IntLiteral(1): [BreakStmt()]), CaseStmt(case IntLiteral(2): [BreakStmt()])], default DefaultStmt(default: [BreakStmt()]))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_091():
    source = """void main() { switch (1) { case 1: default: case 2: } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case IntLiteral(1): []), CaseStmt(case IntLiteral(2): [])], default DefaultStmt(default: []))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_092():
    source = """void main() { switch (1) { case 1: if (2) break; } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case IntLiteral(1): [IfStmt(if IntLiteral(2) then BreakStmt())])])]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_093():
    source = """void main() { switch (1) { case 1: switch (2) { case 3: } } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case IntLiteral(1): [SwitchStmt(switch IntLiteral(2) cases [CaseStmt(case IntLiteral(3): [])])])])]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_094():
    source = """void main() { switch (a+b) { case 1+2: default: } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch BinaryOp(Identifier(a), +, Identifier(b)) cases [CaseStmt(case BinaryOp(IntLiteral(1), +, IntLiteral(2)): [])], default DefaultStmt(default: []))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_095():
    source = """void main() { {} }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([BlockStmt([])]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_096():
    source = """void main() { { {} } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([BlockStmt([BlockStmt([])])]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_097():
    source = """void main() { { int a; { float b; } } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([BlockStmt([VarDecl(IntType(), a), BlockStmt([VarDecl(FloatType(), b)])])]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_098():
    source = """void main() { { { { { int a; } } } } }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([BlockStmt([BlockStmt([BlockStmt([BlockStmt([VarDecl(IntType(), a)])])])])]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_099():
    source = """void main() { return; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ReturnStmt(return)]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_100():
    source = """void main() { return 1; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ReturnStmt(return IntLiteral(1))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_101():
    source = """void main() { return 1+2; }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ReturnStmt(return BinaryOp(IntLiteral(1), +, IntLiteral(2)))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_102():
    source = """void main() { return f(); }"""
    expected = """Program([FuncDecl(VoidType(), main, [], BlockStmt([ReturnStmt(return FuncCall(f, []))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_103():
    source = """int f() { return 1; }"""
    expected = """Program([FuncDecl(IntType(), f, [], BlockStmt([ReturnStmt(return IntLiteral(1))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_104():
    source = """float f() { return 1.0; }"""
    expected = """Program([FuncDecl(FloatType(), f, [], BlockStmt([ReturnStmt(return FloatLiteral(1.0))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_105():
    source = """string f() { return "str"; }"""
    expected = """Program([FuncDecl(StringType(), f, [], BlockStmt([ReturnStmt(return StringLiteral('str'))]))])"""
    assert str(ASTGenerator(source).generate()) == expected

