from tests.utils import Parser


def test_001():
    source = '\nvoid main() {\n    printString("Hello, World!");\n}\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_002():
    source = '\nint add(int x, int y) {\n    return x + y;\n}\n\nint multiply(int x, int y) {\n    return x * y;\n}\n\nvoid main() {\n    auto a = readInt();\n    auto b = readInt();\n    \n    auto sum = add(a, b);\n    auto product = multiply(a, b);\n    \n    printInt(sum);\n    printInt(product);\n}\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_003():
    source = '\nvoid main() {\n    auto n = readInt();\n    auto i = 0;\n    \n    while (i < n) {\n        printInt(i);\n        ++i;\n    }\n    \n    for (auto j = 0; j < n; ++j) {\n        if (j % 2 == 0) {\n            printInt(j);\n        }\n    }\n}\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_004():
    source = '\nint factorial(int n) {\n    if (n <= 1) {\n        return 1;\n    } else {\n        return n * factorial(n - 1);\n    }\n}\n\nvoid main() {\n    auto num = readInt();\n    auto result = factorial(num);\n    printInt(result);\n}\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_005():
    source = '\nvoid main() {\n    // With auto and initialization\n    auto x = readInt();\n    auto y = readFloat();\n    auto name = readString();\n    \n    // With auto without initialization\n    auto sum;\n    sum = x + y;              // sum: float (inferred from first usage - assignment)\n    \n    // With explicit type and initialization\n    int count = 0;\n    float total = 0.0;\n    string greeting = "Hello, ";\n    \n    // With explicit type without initialization\n    int i;\n    float f;\n    i = readInt();            // assignment to int\n    f = readFloat();          // assignment to float\n    \n    printFloat(sum);\n    printString(greeting);\n    printString(name);\n    \n    // Note: String concatenation is NOT supported\n    // This is because + operator applies to int or float, not string\n}\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_006():
    source = '\nstruct Point {\n    int x;\n    int y;\n};\n\nstruct Person {\n    string name;\n    int age;\n    float height;\n};\n\nvoid main() {\n    // Struct variable declaration without initialization\n    Point p1;\n    p1.x = 10;\n    p1.y = 20;\n    \n    // Struct variable declaration with initialization\n    Point p2 = {30, 40};\n    \n    // Access and modify struct members\n    printInt(p2.x);\n    printInt(p2.y);\n    \n    // Struct assignment\n    p1 = p2;  // Copy all members\n    \n    // Person struct usage\n    Person person1 = {"John", 25, 1.75};\n    printString(person1.name);\n    printInt(person1.age);\n    printFloat(person1.height);\n    \n    // Modify struct members\n    person1.age = 26;\n    person1.height = 1.76;\n    \n    // Using struct with auto\n    auto p3 = p2;  // p3: Point (inferred from assignment)\n    printInt(p3.x);\n}\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_007():
    source = '\nvoid main() {\n'
    expected = 'Error on line 3 col 0: <EOF>'
    assert Parser(source).parse() == expected

def test_008():
    source = '\nvoid main {}\n'
    expected = 'Error on line 2 col 10: {'
    assert Parser(source).parse() == expected

def test_009():
    source = '\nvoid f9() { }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_010():
    source = '\nint f10() { return a == b; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_011():
    source = '\nfloat f11() { return -2.5; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_012():
    source = '\nstring f12() { return "s12"; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_013():
    source = '\nauto f13() { return 100; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_014():
    source = '\nf14() { return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_015():
    source = '\nvoid f15() { auto a = 256; int b; b = a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_016():
    source = '\nvoid f16() { if (0) return; else return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_017():
    source = '\nvoid f17() { while (1) { break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_018():
    source = '\nvoid f18() { for (auto i = 0; i < 2; ++i) { continue; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_019():
    source = '\nvoid f19() { for (; ; ) { } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_020():
    source = '\nvoid f20() { switch (4) { case 1: break; case 2: break; default: break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_021():
    source = '\nstruct S21 { int a; float b; };\nvoid f21() { S21 s; s.a = 5; s.b = 6.02e23; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_022():
    source = '\nstruct S22 { int a; int b; };\nvoid f22() { S22 s = {6, 9}; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_023():
    source = '\nint g23(int a) { return a; }\nvoid f23() { g23(7); }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_024():
    source = '\nvoid f24() { a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_025():
    source = '\nvoid f25() { a = b = 9; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_026():
    source = '\nstruct S26 { int a; };\nvoid f26() { S26 s; s.a = 10; s.a = s.a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_027():
    source = '\nvoid f27() { ++a; a++; --a; a--; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_028():
    source = '\nvoid f28() { a / (b + 1); a >= b; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_029():
    source = '\nstruct S29 { int a; };\nstruct T29 { S29 s; };\nvoid f29() { T29 t; t.s.a = 100; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_030():
    source = '\nvoid f30() { a < b; return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_031():
    source = '\nvoid f31() { }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_032():
    source = '\nint f32() { return a > b; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_033():
    source = '\nfloat f33() { return 6.02e23; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_034():
    source = '\nstring f34() { return "s34"; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_035():
    source = '\nauto f35() { return 3; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_036():
    source = '\nf36() { return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_037():
    source = '\nvoid f37() { auto a = 5; int b; b = a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_038():
    source = '\nvoid f38() { if (6) return; else return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_039():
    source = '\nvoid f39() { while (7) { break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_040():
    source = '\nvoid f40() { for (auto i = 0; i < 8; ++i) { continue; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_041():
    source = '\nvoid f41() { for (; ; ) { } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_042():
    source = '\nvoid f42() { switch (10) { case 1: break; case 2: break; default: break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_043():
    source = '\nstruct S43 { int a; float b; };\nvoid f43() { S43 s; s.a = 42; s.b = .5; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_044():
    source = '\nstruct S44 { int a; int b; };\nvoid f44() { S44 s = {99, 256}; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_045():
    source = '\nint g45(int a) { return a; }\nvoid f45() { g45(100); }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_046():
    source = '\nvoid f46() { a++--++--; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_047():
    source = '\nvoid f47() { a = b = 256; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_048():
    source = '\nstruct S48 { int a; };\nvoid f48() { S48 s; s.a = 0; s.a = s.a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_049():
    source = '\nvoid f49() { ++a; a++; --a; a--; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_050():
    source = '\nvoid f50() { a - b; a <= b; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_051():
    source = '\nstruct S51 { int a; };\nstruct T51 { S51 s; };\nvoid f51() { T51 t; t.s.a = 3; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_052():
    source = '\nvoid f52() { a / (b + 1); return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_053():
    source = '\nvoid f53() { }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_054():
    source = '\nint f54() { return a < b; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_055():
    source = '\nfloat f55() { return .5; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_056():
    source = '\nstring f56() { return "s56"; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_057():
    source = '\nauto f57() { return 9; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_058():
    source = '\nf58() { return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_059():
    source = '\nvoid f59() { auto a = 42; int b; b = a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_060():
    source = '\nvoid f60() { if (99) return; else return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_061():
    source = '\nvoid f61() { while (100) { break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_062():
    source = '\nvoid f62() { for (auto i = 0; i < 123; ++i) { continue; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_063():
    source = '\nvoid f63() { for (; ; ) { } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_064():
    source = '\nvoid f64() { switch (0) { case 1: break; case 2: break; default: break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_065():
    source = '\nstruct S65 { int a; float b; };\nvoid f65() { S65 s; s.a = 1; s.b = 1.; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_066():
    source = '\nstruct S66 { int a; int b; };\nvoid f66() { S66 s = {2, 5}; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_067():
    source = '\nint g67(int a) { return a; }\nvoid f67() { g67(3); }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_068():
    source = '\nvoid f68() { a = b + 1; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_069():
    source = '\nvoid f69() { a = b = 5; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_070():
    source = '\nstruct S70 { int a; };\nvoid f70() { S70 s; s.a = 6; s.a = s.a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_071():
    source = '\nvoid f71() { ++a; a++; --a; a--; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_072():
    source = '\nvoid f72() { a; a % 2; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_073():
    source = '\nstruct S73 { int a; };\nstruct T73 { S73 s; };\nvoid f73() { T73 t; t.s.a = 9; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_074():
    source = '\nvoid f74() { a - b; return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_075():
    source = '\nvoid f75() { }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_076():
    source = '\nint f76() { return a / (b + 1); }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_077():
    source = '\nfloat f77() { return 1.; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_078():
    source = '\nstring f78() { return "s78"; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_079():
    source = '\nauto f79() { return 256; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_080():
    source = '\nf80() { return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_081():
    source = '\nvoid f81() { auto a = 1; int b; b = a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_082():
    source = '\nvoid f82() { if (2) return; else return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_083():
    source = '\nvoid f83() { while (3) { break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_084():
    source = '\nvoid f84() { for (auto i = 0; i < 4; ++i) { continue; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_085():
    source = '\nvoid f85() { for (; ; ) { } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_086():
    source = '\nvoid f86() { switch (6) { case 1: break; case 2: break; default: break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_087():
    source = '\nstruct S87 { int a; float b; };\nvoid f87() { S87 s; s.a = 7; s.b = 3.14; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_088():
    source = '\nstruct S88 { int a; int b; };\nvoid f88() { S88 s = {8, 42}; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_089():
    source = '\nint g89(int a) { return a; }\nvoid f89() { g89(9); }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_090():
    source = '\nvoid f90() { a.b.c; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_091():
    source = '\nvoid f91() { a = b = 42; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_092():
    source = '\nstruct S92 { int a; };\nvoid f92() { S92 s; s.a = 99; s.a = s.a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_093():
    source = '\nvoid f93() { ++a; a++; --a; a--; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_094():
    source = '\nvoid f94() { a++--++--; a * b; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_095():
    source = '\nstruct S95 { int a; };\nstruct T95 { S95 s; };\nvoid f95() { T95 t; t.s.a = 256; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_096():
    source = '\nvoid f96() { a; return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_097():
    source = '\nvoid f97() { }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_098():
    source = '\nint f98() { return a - b; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_099():
    source = '\nfloat f99() { return 3.14; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_100():
    source = '\nstring f100() { return "s100"; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_101():
    source = '\nauto f101() { return 5; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_102():
    source = '\nf102() { return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_103():
    source = '\nvoid f103() { auto a = 7; int b; b = a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_104():
    source = '\nvoid f104() { if (8) return; else return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_105():
    source = '\nvoid f105() { while (9) { break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_106():
    source = '\nvoid f106() { for (auto i = 0; i < 10; ++i) { continue; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_107():
    source = '\nvoid f107() { for (; ; ) { } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_108():
    source = '\nvoid f108() { switch (99) { case 1: break; case 2: break; default: break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_109():
    source = '\nstruct S109 { int a; float b; };\nvoid f109() { S109 s; s.a = 100; s.b = 1.5; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_110():
    source = '\nstruct S110 { int a; int b; };\nvoid f110() { S110 s = {123, 1}; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_111():
    source = '\nint g111(int a) { return a; }\nvoid f111() { g111(256); }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_112():
    source = '\nvoid f112() { a++; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_113():
    source = '\nvoid f113() { a = b = 1; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_114():
    source = '\nstruct S114 { int a; };\nvoid f114() { S114 s; s.a = 2; s.a = s.a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_115():
    source = '\nvoid f115() { ++a; a++; --a; a--; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_116():
    source = '\nvoid f116() { a = b + 1; a + b; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_117():
    source = '\nstruct S117 { int a; };\nstruct T117 { S117 s; };\nvoid f117() { T117 t; t.s.a = 5; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_118():
    source = '\nvoid f118() { a++--++--; return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_119():
    source = '\nvoid f119() { }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_120():
    source = '\nint f120() { return a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_121():
    source = '\nfloat f121() { return 1.5; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_122():
    source = '\nstring f122() { return "s122"; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_123():
    source = '\nauto f123() { return 42; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_124():
    source = '\nf124() { return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_125():
    source = '\nvoid f125() { auto a = 100; int b; b = a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_126():
    source = '\nvoid f126() { if (123) return; else return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_127():
    source = '\nvoid f127() { while (256) { break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_128():
    source = '\nvoid f128() { for (auto i = 0; i < 0; ++i) { continue; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_129():
    source = '\nvoid f129() { for (; ; ) { } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_130():
    source = '\nvoid f130() { switch (2) { case 1: break; case 2: break; default: break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_131():
    source = '\nstruct S131 { int a; float b; };\nvoid f131() { S131 s; s.a = 3; s.b = -2.5; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_132():
    source = '\nstruct S132 { int a; int b; };\nvoid f132() { S132 s = {4, 7}; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_133():
    source = '\nint g133(int a) { return a; }\nvoid f133() { g133(5); }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_134():
    source = '\nvoid f134() { !a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_135():
    source = '\nvoid f135() { a = b = 7; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_136():
    source = '\nstruct S136 { int a; };\nvoid f136() { S136 s; s.a = 8; s.a = s.a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_137():
    source = '\nvoid f137() { ++a; a++; --a; a--; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_138():
    source = '\nvoid f138() { a.b.c; ++(+a) * (a / (c)); }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_139():
    source = '\nstruct S139 { int a; };\nstruct T139 { S139 s; };\nvoid f139() { T139 t; t.s.a = 42; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_140():
    source = '\nvoid f140() { a = b + 1; return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_141():
    source = '\nvoid f141() { }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_142():
    source = '\nint f142() { return a++--++--; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_143():
    source = '\nfloat f143() { return -2.5; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_144():
    source = '\nstring f144() { return "s144"; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_145():
    source = '\nauto f145() { return 1; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_146():
    source = '\nf146() { return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_147():
    source = '\nvoid f147() { auto a = 3; int b; b = a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_148():
    source = '\nvoid f148() { if (4) return; else return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_149():
    source = '\nvoid f149() { while (5) { break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_150():
    source = '\nvoid f150() { for (auto i = 0; i < 6; ++i) { continue; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_151():
    source = '\nvoid f151() { for (; ; ) { } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_152():
    source = '\nvoid f152() { switch (8) { case 1: break; case 2: break; default: break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_153():
    source = '\nstruct S153 { int a; float b; };\nvoid f153() { S153 s; s.a = 9; s.b = 6.02e23; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_154():
    source = '\nstruct S154 { int a; int b; };\nvoid f154() { S154 s = {10, 100}; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_155():
    source = '\nint g155(int a) { return a; }\nvoid f155() { g155(42); }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_156():
    source = '\nvoid f156() { a && b; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_157():
    source = '\nvoid f157() { a = b = 100; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_158():
    source = '\nstruct S158 { int a; };\nvoid f158() { S158 s; s.a = 123; s.a = s.a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_159():
    source = '\nvoid f159() { ++a; a++; --a; a--; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_160():
    source = '\nvoid f160() { a++; ++--++a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_161():
    source = '\nstruct S161 { int a; };\nstruct T161 { S161 s; };\nvoid f161() { T161 t; t.s.a = 1; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_162():
    source = '\nvoid f162() { a.b.c; return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_163():
    source = '\nvoid f163() { }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_164():
    source = '\nint f164() { return a = b + 1; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_165():
    source = '\nfloat f165() { return 6.02e23; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_166():
    source = '\nstring f166() { return "s166"; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_167():
    source = '\nauto f167() { return 7; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_168():
    source = '\nf168() { return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_169():
    source = '\nvoid f169() { auto a = 9; int b; b = a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_170():
    source = '\nvoid f170() { if (10) return; else return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_171():
    source = '\nvoid f171() { while (42) { break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_172():
    source = '\nvoid f172() { for (auto i = 0; i < 99; ++i) { continue; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_173():
    source = '\nvoid f173() { for (; ; ) { } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_174():
    source = '\nvoid f174() { switch (123) { case 1: break; case 2: break; default: break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_175():
    source = '\nstruct S175 { int a; float b; };\nvoid f175() { S175 s; s.a = 256; s.b = .5; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_176():
    source = '\nstruct S176 { int a; int b; };\nvoid f176() { S176 s = {0, 3}; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_177():
    source = '\nint g177(int a) { return a; }\nvoid f177() { g177(1); }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_178():
    source = '\nvoid f178() { a == b; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_179():
    source = '\nvoid f179() { a = b = 3; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_180():
    source = '\nstruct S180 { int a; };\nvoid f180() { S180 s; s.a = 4; s.a = s.a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_181():
    source = '\nvoid f181() { ++a; a++; --a; a--; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_182():
    source = '\nvoid f182() { !a; (a + b) * (c - d); }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_183():
    source = '\nstruct S183 { int a; };\nstruct T183 { S183 s; };\nvoid f183() { T183 t; t.s.a = 7; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_184():
    source = '\nvoid f184() { a++; return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_185():
    source = '\nvoid f185() { }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_186():
    source = '\nint f186() { return a.b.c; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_187():
    source = '\nfloat f187() { return .5; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_188():
    source = '\nstring f188() { return "s188"; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_189():
    source = '\nauto f189() { return 100; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_190():
    source = '\nf190() { return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_191():
    source = '\nvoid f191() { auto a = 256; int b; b = a; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_192():
    source = '\nvoid f192() { if (0) return; else return; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_193():
    source = '\nvoid f193() { while (1) { break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_194():
    source = '\nvoid f194() { for (auto i = 0; i < 2; ++i) { continue; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_195():
    source = '\nvoid f195() { for (; ; ) { } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_196():
    source = '\nvoid f196() { switch (4) { case 1: break; case 2: break; default: break; } }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_197():
    source = '\nstruct S197 { int a; float b; };\nvoid f197() { S197 s; s.a = 5; s.b = 1.; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_198():
    source = '\nstruct S198 { int a; int b; };\nvoid f198() { S198 s = {6, 9}; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_199():
    source = '\nint g199(int a) { return a; }\nvoid f199() { g199(7); }\n'
    expected = 'success'
    assert Parser(source).parse() == expected

def test_200():
    source = '\nvoid f200() { a > b; }\n'
    expected = 'success'
    assert Parser(source).parse() == expected
