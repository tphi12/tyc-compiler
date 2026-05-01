
"""Comprehensive static semantic checker tests for TyC."""

from tests.utils import Checker


def _assert_checker(source: str, expected: str = "Static checking passed"):
    assert Checker(source).check_from_source() == expected

def test_001_valid_basic_ints():
    """valid_basic_ints"""
    source = """
void main() {
    int x = 5;
    int y = x + 1;
}
"""
    _assert_checker(source)

def test_002_valid_auto_literals():
    """valid_auto_literals"""
    source = """
void main() {
    auto x = 10;
    auto y = 3.14;
    auto z = "hello";
}
"""
    _assert_checker(source)

def test_003_valid_auto_from_builtin_assignment():
    """valid_auto_from_builtin_assignment"""
    source = """
void main() {
    auto x;
    x = readInt();
    printInt(x);
}
"""
    _assert_checker(source)

def test_004_valid_auto_from_builtin_argument():
    """valid_auto_from_builtin_argument"""
    source = """
void main() {
    auto x;
    printInt(x);
}
"""
    _assert_checker(source)

def test_005_valid_struct_member_assignment():
    """valid_struct_member_assignment"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p;
    p.x = 10;
    p.y = 20;
}
"""
    _assert_checker(source)

def test_006_valid_block_shadowing():
    """valid_block_shadowing"""
    source = """
void main() {
    int x = 1;
    {
        int x = 2;
        int y = x;
    }
}
"""
    _assert_checker(source)

def test_007_valid_if_body_inner_scope():
    """valid_if_body_inner_scope"""
    source = """
void main() {
    int a;
    int b;
    if (1) int a = b;
}
"""
    _assert_checker(source)

def test_008_valid_while_body_inner_scope():
    """valid_while_body_inner_scope"""
    source = """
void main() {
    int x = 1;
    while (x) int x = 2;
}
"""
    _assert_checker(source)

def test_009_valid_switch_shadow_outer_variable():
    """valid_switch_shadow_outer_variable"""
    source = """
void main() {
    int a;
    switch (1) {
        case 1:
            int a;
            break;
        default:
            int b;
    }
}
"""
    _assert_checker(source)

def test_010_valid_for_auto_init_infers_int():
    """valid_for_auto_init_infers_int"""
    source = """
void main() {
    for (auto i; ; ) {
        int x = i;
        break;
    }
}
"""
    _assert_checker(source)

def test_011_valid_for_assign_init():
    """valid_for_assign_init"""
    source = """
void main() {
    int i;
    for (i = 0; i < 3; ++i) {
        printInt(i);
    }
}
"""
    _assert_checker(source)

def test_012_valid_for_update_postfix():
    """valid_for_update_postfix"""
    source = """
void main() {
    int i = 0;
    for (; i < 3; i++) {
        printInt(i);
    }
}
"""
    _assert_checker(source)

def test_013_valid_builtins():
    """valid_builtins"""
    source = """
void main() {
    int x = readInt();
    float y = readFloat();
    string z = readString();
    printInt(x);
    printFloat(y);
    printString(z);
}
"""
    _assert_checker(source)

def test_014_valid_inferred_return_function():
    """valid_inferred_return_function"""
    source = """
foo() {
    return 1;
}
void main() {
    int x = foo();
}
"""
    _assert_checker(source)

def test_015_valid_explicit_recursive_call():
    """valid_explicit_recursive_call"""
    source = """
int foo() {
    return foo();
}
"""
    _assert_checker(source)

def test_016_valid_struct_literal_typed():
    """valid_struct_literal_typed"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p = {1, 2};
}
"""
    _assert_checker(source)

def test_017_valid_assignment_expr_initializer():
    """valid_assignment_expr_initializer"""
    source = """
void main() {
    int x;
    int y = (x = 5) + 7;
}
"""
    _assert_checker(source)

def test_018_valid_chained_assignment():
    """valid_chained_assignment"""
    source = """
void main() {
    int a;
    int b;
    int c;
    a = b = c = 10;
}
"""
    _assert_checker(source)

def test_019_valid_member_assignment_expr():
    """valid_member_assignment_expr"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p = {1, 2};
    int r = (p.x = 15) + 5;
}
"""
    _assert_checker(source)

def test_020_valid_switch_constant_cases():
    """valid_switch_constant_cases"""
    source = """
void main() {
    switch (1) {
        case +1:
            break;
        case 1 + 2:
            break;
        default:
            break;
    }
}
"""
    _assert_checker(source)

def test_021_valid_continue_in_loop():
    """valid_continue_in_loop"""
    source = """
void main() {
    int i = 0;
    while (i < 10) {
        ++i;
        continue;
    }
}
"""
    _assert_checker(source)

def test_022_valid_auto_from_int_anchor():
    """valid_auto_from_int_anchor"""
    source = """
void main() {
    auto b;
    auto c = b + 1;
}
"""
    _assert_checker(source)

def test_023_valid_auto_from_known_int_operand():
    """valid_auto_from_known_int_operand"""
    source = """
void main() {
    auto a;
    auto b;
    a = 1;
    a + b;
}
"""
    _assert_checker(source)

def test_024_valid_struct_and_function_same_name():
    """valid_struct_and_function_same_name"""
    source = """
struct foo {
    int x;
};
int foo(int y) {
    return y;
}
void main() {
    foo f;
    int x = foo(1);
}
"""
    _assert_checker(source)

def test_025_valid_for_body_shadows_init_name():
    """valid_for_body_shadows_init_name"""
    source = """
void main() {
    for (int i = 0; i < 3; ++i) {
        int i = 10;
        printInt(i);
    }
}
"""
    _assert_checker(source)

def test_026_valid_declared_function_use():
    """valid_declared_function_use"""
    source = """
int add(int x, int y) {
    return x + y;
}
void main() {
    int z = add(1, 2);
}
"""
    _assert_checker(source)

def test_027_valid_switch_case_constant_binary():
    """valid_switch_case_constant_binary"""
    source = """
void main() {
    switch (3) {
        case 1 + 2:
            break;
    }
}
"""
    _assert_checker(source)

def test_028_valid_switch_case_constant_unary():
    """valid_switch_case_constant_unary"""
    source = """
void main() {
    switch (1) {
        case -(-1):
            break;
    }
}
"""
    _assert_checker(source)

def test_029_valid_struct_argument_and_return():
    """valid_struct_argument_and_return"""
    source = """
struct Point {
    int x;
    int y;
};
Point id(Point p) {
    return p;
}
void main() {
    Point p = {1, 2};
    Point q = id(p);
}
"""
    _assert_checker(source)

def test_030_valid_switch_default_only():
    """valid_switch_default_only"""
    source = """
void main() {
    switch (1) {
        default:
            break;
    }
}
"""
    _assert_checker(source)

def test_031_redeclared_struct():
    """redeclared_struct"""
    source = """
struct Point { int x; };
struct Point { int y; };
"""
    expected = "Redeclared(Struct, Point)"
    _assert_checker(source, expected)

def test_032_redeclared_function():
    """redeclared_function"""
    source = """
int foo() { return 1; }
int foo() { return 2; }
"""
    expected = "Redeclared(Function, foo)"
    _assert_checker(source, expected)

def test_033_redeclared_member():
    """redeclared_member"""
    source = """
struct Point {
    int x;
    int x;
};
"""
    expected = "Redeclared(Member, x)"
    _assert_checker(source, expected)

def test_034_redeclared_parameter():
    """redeclared_parameter"""
    source = """
int foo(int x, int x) {
    return x;
}
"""
    expected = "Redeclared(Parameter, x)"
    _assert_checker(source, expected)

def test_035_redeclared_variable_same_block():
    """redeclared_variable_same_block"""
    source = """
void main() {
    int x;
    float x;
}
"""
    expected = "Redeclared(Variable, x)"
    _assert_checker(source, expected)

def test_036_redeclared_parameter_shadow_nested_if():
    """redeclared_parameter_shadow_nested_if"""
    source = """
void main(int x) {
    if (1) {
        int x;
    }
}
"""
    expected = "Redeclared(Variable, x)"
    _assert_checker(source, expected)

def test_037_redeclared_switch_scope_across_cases():
    """redeclared_switch_scope_across_cases"""
    source = """
void main() {
    switch (1) {
        case 1:
            int b;
        case 2:
            float b;
    }
}
"""
    expected = "Redeclared(Variable, b)"
    _assert_checker(source, expected)

def test_038_redeclared_for_init_same_scope():
    """redeclared_for_init_same_scope"""
    source = """
void main() {
    int i;
    for (int i; ; ) {}
}
"""
    expected = "Redeclared(Variable, i)"
    _assert_checker(source, expected)

def test_039_redeclared_same_case():
    """redeclared_same_case"""
    source = """
void main() {
    switch (1) {
        case 1:
            int a;
            int a;
    }
}
"""
    expected = "Redeclared(Variable, a)"
    _assert_checker(source, expected)

def test_040_undeclared_identifier_initializer():
    """undeclared_identifier_initializer"""
    source = """
void main() {
    int x = y;
}
"""
    expected = "UndeclaredIdentifier(y)"
    _assert_checker(source, expected)

def test_041_undeclared_identifier_other_function():
    """undeclared_identifier_other_function"""
    source = """
void foo() {
    int x = 1;
}
void main() {
    int y = x;
}
"""
    expected = "UndeclaredIdentifier(x)"
    _assert_checker(source, expected)

def test_042_undeclared_function_later_decl():
    """undeclared_function_later_decl"""
    source = """
void main() {
    foo();
}
void foo() {}
"""
    expected = "UndeclaredFunction(foo)"
    _assert_checker(source, expected)

def test_043_undeclared_struct_variable():
    """undeclared_struct_variable"""
    source = """
void main() {
    Point p;
}
"""
    expected = "UndeclaredStruct(Point)"
    _assert_checker(source, expected)

def test_044_undeclared_struct_parameter():
    """undeclared_struct_parameter"""
    source = """
void foo(Point p) {}
"""
    expected = "UndeclaredStruct(Point)"
    _assert_checker(source, expected)

def test_045_undeclared_identifier_case_label():
    """undeclared_identifier_case_label"""
    source = """
void foo() {
    switch (1) {
        case x:
    }
}
"""
    expected = "UndeclaredIdentifier(x)"
    _assert_checker(source, expected)

def test_046_undeclared_function_exprstmt():
    """undeclared_function_exprstmt"""
    source = """
void main() {
    missing();
}
"""
    expected = "UndeclaredFunction(missing)"
    _assert_checker(source, expected)

def test_047_undeclared_identifier_member_base():
    """undeclared_identifier_member_base"""
    source = """
void main() {
    p.x;
}
"""
    expected = "UndeclaredIdentifier(p)"
    _assert_checker(source, expected)

def test_048_infer_unused_auto_block():
    """infer_unused_auto_block"""
    source = """
void main() {
    auto x;
}
"""
    expected = "TypeCannotBeInferred(BlockStmt([VarDecl(auto, x)]))"
    _assert_checker(source, expected)

def test_049_infer_unused_auto_switch():
    """infer_unused_auto_switch"""
    source = """
void unused_auto() {
    switch (1) {
        case 1:
            auto c;
    }
}
"""
    expected = "TypeCannotBeInferred(SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case IntLiteral(1): [VarDecl(auto, c)])]))"
    _assert_checker(source, expected)

def test_050_infer_ambiguous_assignment():
    """infer_ambiguous_assignment"""
    source = """
void main() {
    auto x;
    auto y;
    x = y;
}
"""
    expected = "TypeCannotBeInferred(AssignExpr(Identifier(x) = Identifier(y)))"
    _assert_checker(source, expected)

def test_051_infer_typed_initializer_two_unknown_operands():
    """infer_typed_initializer_two_unknown_operands"""
    source = """
void main() {
    auto a;
    auto b;
    int c = a + b;
}
"""
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(a), +, Identifier(b)))"
    _assert_checker(source, expected)

def test_052_infer_relational_operand_unknown():
    """infer_relational_operand_unknown"""
    source = """
void main() {
    auto b;
    int c = b > 2;
}
"""
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(b), >, IntLiteral(2)))"
    _assert_checker(source, expected)

def test_053_infer_unknown_function_return_at_call():
    """infer_unknown_function_return_at_call"""
    source = """
foo() {
    int a = foo();
    return 1;
}
"""
    expected = "TypeCannotBeInferred(FuncCall(foo, []))"
    _assert_checker(source, expected)

def test_054_infer_return_unknown_auto():
    """infer_return_unknown_auto"""
    source = """
foo() {
    auto x;
    return x;
}
"""
    expected = "TypeCannotBeInferred(ReturnStmt(return Identifier(x)))"
    _assert_checker(source, expected)

def test_055_infer_compound_argument_unknown():
    """infer_compound_argument_unknown"""
    source = """
void main() {
    auto x;
    auto y;
    printInt(x + y);
}
"""
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(x), +, Identifier(y)))"
    _assert_checker(source, expected)

def test_056_infer_struct_literal_without_expected_type():
    """infer_struct_literal_without_expected_type"""
    source = """
void main() {
    {1, 2};
}
"""
    expected = "TypeCannotBeInferred(StructLiteral({IntLiteral(1), IntLiteral(2)}))"
    _assert_checker(source, expected)

def test_057_infer_float_plus_unknown():
    """infer_float_plus_unknown"""
    source = """
void main() {
    auto b;
    int c = 1.0 + b;
}
"""
    expected = "TypeCannotBeInferred(BinaryOp(FloatLiteral(1.0), +, Identifier(b)))"
    _assert_checker(source, expected)

def test_058_stmt_typed_init_string_to_int():
    """stmt_typed_init_string_to_int"""
    source = """
void main() {
    int a = "x";
}
"""
    expected = "TypeMismatchInStatement(VarDecl(IntType(), a = StringLiteral('x')))"
    _assert_checker(source, expected)

def test_059_stmt_if_condition_string():
    """stmt_if_condition_string"""
    source = """
void main() {
    string s = "x";
    if (s) {}
}
"""
    expected = "TypeMismatchInStatement(IfStmt(if Identifier(s) then BlockStmt([])))"
    _assert_checker(source, expected)

def test_060_stmt_while_condition_float():
    """stmt_while_condition_float"""
    source = """
void main() {
    float f = 1.0;
    while (f) {}
}
"""
    expected = "TypeMismatchInStatement(WhileStmt(while Identifier(f) do BlockStmt([])))"
    _assert_checker(source, expected)

def test_061_stmt_for_init_string_var():
    """stmt_for_init_string_var"""
    source = """
void main() {
    for (string s; ; ) {}
}
"""
    expected = "TypeMismatchInStatement(ForStmt(for VarDecl(StringType(), s); None; None do BlockStmt([])))"
    _assert_checker(source, expected)

def test_062_stmt_for_init_float_assign():
    """stmt_for_init_float_assign"""
    source = """
void main() {
    float b;
    for (b = 1.0; ; ) {}
}
"""
    expected = "TypeMismatchInStatement(ForStmt(for ExprStmt(AssignExpr(Identifier(b) = FloatLiteral(1.0))); None; None do BlockStmt([])))"
    _assert_checker(source, expected)

def test_063_stmt_for_update_string_assign():
    """stmt_for_update_string_assign"""
    source = """
void main() {
    string s;
    for (; ; s = "x") {}
}
"""
    expected = "TypeMismatchInStatement(ForStmt(for None; None; AssignExpr(Identifier(s) = StringLiteral('x')) do BlockStmt([])))"
    _assert_checker(source, expected)

def test_064_stmt_switch_expression_float():
    """stmt_switch_expression_float"""
    source = """
void main() {
    switch (1.0) {
        case 1:
    }
}
"""
    expected = "TypeMismatchInStatement(SwitchStmt(switch FloatLiteral(1.0) cases [CaseStmt(case IntLiteral(1): [])]))"
    _assert_checker(source, expected)

def test_065_stmt_switch_case_float_label():
    """stmt_switch_case_float_label"""
    source = """
void main() {
    switch (1 || 2) {
        case 1.0:
    }
}
"""
    expected = "TypeMismatchInStatement(SwitchStmt(switch BinaryOp(IntLiteral(1), ||, IntLiteral(2)) cases [CaseStmt(case FloatLiteral(1.0): [])]))"
    _assert_checker(source, expected)

def test_066_stmt_switch_case_nonconstant_identifier():
    """stmt_switch_case_nonconstant_identifier"""
    source = """
void main() {
    auto a;
    switch (1) {
        case a:
    }
    float b = a;
}
"""
    expected = "TypeMismatchInStatement(SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case Identifier(a): [])]))"
    _assert_checker(source, expected)

def test_067_stmt_void_return_value():
    """stmt_void_return_value"""
    source = """
void main() {
    return 1;
}
"""
    expected = "TypeMismatchInStatement(ReturnStmt(return IntLiteral(1)))"
    _assert_checker(source, expected)

def test_068_stmt_nonvoid_return_empty():
    """stmt_nonvoid_return_empty"""
    source = """
int main() {
    return;
}
"""
    expected = "TypeMismatchInStatement(ReturnStmt(return))"
    _assert_checker(source, expected)

def test_069_stmt_for_auto_init_then_float_use():
    """stmt_for_auto_init_then_float_use"""
    source = """
void main() {
    for (auto a;;) {
        float b = a;
    }
}
"""
    expected = "TypeMismatchInStatement(VarDecl(FloatType(), b = Identifier(a)))"
    _assert_checker(source, expected)

def test_070_stmt_pending_void_then_value():
    """stmt_pending_void_then_value"""
    source = """
foo() {
    return;
    return 1;
}
"""
    expected = "TypeMismatchInStatement(ReturnStmt(return))"
    _assert_checker(source, expected)

def test_071_stmt_typed_initializer_after_float_plus_unknown():
    """stmt_typed_initializer_after_float_plus_unknown"""
    source = """
void main() {
    auto c;
    float a = 1 + c;
}
"""
    expected = "TypeMismatchInStatement(VarDecl(FloatType(), a = BinaryOp(IntLiteral(1), +, Identifier(c))))"
    _assert_checker(source, expected)

def test_072_expr_assignment_type_mismatch():
    """expr_assignment_type_mismatch"""
    source = """
void main() {
    int x = 10;
    string text = "hello";
    x = text;
}
"""
    expected = "TypeMismatchInExpression(AssignExpr(Identifier(x) = Identifier(text)))"
    _assert_checker(source, expected)

def test_073_expr_arithmetic_with_string():
    """expr_arithmetic_with_string"""
    source = """
void main() {
    int x = 1;
    string s = "x";
    x + s;
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(x), +, Identifier(s)))"
    _assert_checker(source, expected)

def test_074_expr_modulus_with_float():
    """expr_modulus_with_float"""
    source = """
void main() {
    float f = 1.0;
    int x = 2;
    f % x;
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(f), %, Identifier(x)))"
    _assert_checker(source, expected)

def test_075_expr_logical_with_float():
    """expr_logical_with_float"""
    source = """
void main() {
    float f = 1.0;
    int x = 1;
    f && x;
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(f), &&, Identifier(x)))"
    _assert_checker(source, expected)

def test_076_expr_not_with_float():
    """expr_not_with_float"""
    source = """
void main() {
    float f = 1.0;
    !f;
}
"""
    expected = "TypeMismatchInExpression(PrefixOp(!Identifier(f)))"
    _assert_checker(source, expected)

def test_077_expr_prefix_inc_string():
    """expr_prefix_inc_string"""
    source = """
void main() {
    string s = "x";
    ++s;
}
"""
    expected = "TypeMismatchInExpression(PrefixOp(++Identifier(s)))"
    _assert_checker(source, expected)

def test_078_expr_postfix_inc_string():
    """expr_postfix_inc_string"""
    source = """
void main() {
    string s = "x";
    s++;
}
"""
    expected = "TypeMismatchInExpression(PostfixOp(Identifier(s)++))"
    _assert_checker(source, expected)

def test_079_expr_member_access_nonstruct():
    """expr_member_access_nonstruct"""
    source = """
void main() {
    int x = 1;
    x.y;
}
"""
    expected = "TypeMismatchInExpression(MemberAccess(Identifier(x).y))"
    _assert_checker(source, expected)

def test_080_expr_member_access_missing_member():
    """expr_member_access_missing_member"""
    source = """
struct Point {
    int x;
};
void main() {
    Point p = {1};
    p.z;
}
"""
    expected = "TypeMismatchInExpression(MemberAccess(Identifier(p).z))"
    _assert_checker(source, expected)

def test_081_expr_function_call_arg_type():
    """expr_function_call_arg_type"""
    source = """
void main() {
    printInt("x");
}
"""
    expected = "TypeMismatchInExpression(FuncCall(printInt, [StringLiteral('x')]))"
    _assert_checker(source, expected)

def test_082_expr_function_call_wrong_arity():
    """expr_function_call_wrong_arity"""
    source = """
int add(int x, int y) {
    return x + y;
}
void main() {
    add(1);
}
"""
    expected = "TypeMismatchInExpression(FuncCall(add, [IntLiteral(1)]))"
    _assert_checker(source, expected)

def test_083_expr_struct_literal_wrong_arity():
    """expr_struct_literal_wrong_arity"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p = {1};
}
"""
    expected = "TypeMismatchInExpression(StructLiteral({IntLiteral(1)}))"
    _assert_checker(source, expected)

def test_084_expr_struct_literal_wrong_field_type():
    """expr_struct_literal_wrong_field_type"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p = {1, "x"};
}
"""
    expected = "TypeMismatchInExpression(StructLiteral({IntLiteral(1), StringLiteral('x')}))"
    _assert_checker(source, expected)

def test_085_expr_struct_assignment_different_types():
    """expr_struct_assignment_different_types"""
    source = """
struct P {
    int x;
};
struct Q {
    int x;
};
void main() {
    P p;
    Q q;
    p = q;
}
"""
    expected = "TypeMismatchInExpression(AssignExpr(Identifier(p) = Identifier(q)))"
    _assert_checker(source, expected)

def test_086_loop_break_outside():
    """loop_break_outside"""
    source = """
void main() {
    break;
}
"""
    expected = "MustInLoop(BreakStmt())"
    _assert_checker(source, expected)

def test_087_loop_continue_outside():
    """loop_continue_outside"""
    source = """
void main() {
    continue;
}
"""
    expected = "MustInLoop(ContinueStmt())"
    _assert_checker(source, expected)

def test_088_loop_continue_in_switch():
    """loop_continue_in_switch"""
    source = """
void main() {
    int x = 1;
    switch (x) {
        case 1:
            break;
            continue;
    }
}
"""
    expected = "MustInLoop(ContinueStmt())"
    _assert_checker(source, expected)

def test_089_valid_else_separate_scope():
    """valid_else_separate_scope"""
    source = """
void main() {
    if (1) int x = 1;
    else int x = 2;
}
"""
    _assert_checker(source)

def test_090_valid_switch_shared_scope_fallthrough_use():
    """valid_switch_shared_scope_fallthrough_use"""
    source = """
void main() {
    switch (1) {
        case 1:
            int x;
        case 2:
            x = 1;
    }
}
"""
    _assert_checker(source)

def test_091_undeclared_initializer_self_reference():
    """undeclared_initializer_self_reference"""
    source = """
void main() {
    int x = x;
}
"""
    expected = "UndeclaredIdentifier(x)"
    _assert_checker(source, expected)

def test_092_undeclared_struct_member_type():
    """undeclared_struct_member_type"""
    source = """
struct Node {
    Next next;
};
"""
    expected = "UndeclaredStruct(Next)"
    _assert_checker(source, expected)

def test_093_infer_binary_with_float_anchor_still_ambiguous():
    """infer_binary_with_float_anchor_still_ambiguous"""
    source = """
void main() {
    auto x;
    int y;
    y = x + 1.0;
}
"""
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(x), +, FloatLiteral(1.0)))"
    _assert_checker(source, expected)

def test_094_stmt_inferred_return_conflict():
    """stmt_inferred_return_conflict"""
    source = """
foo() {
    return 1;
    return "x";
}
"""
    expected = "TypeMismatchInStatement(ReturnStmt(return StringLiteral('x')))"
    _assert_checker(source, expected)

def test_095_stmt_void_call_used_as_int_initializer():
    """stmt_void_call_used_as_int_initializer"""
    source = """
void foo() {}
void main() {
    int x = foo();
}
"""
    expected = "TypeMismatchInStatement(VarDecl(IntType(), x = FuncCall(foo, [])))"
    _assert_checker(source, expected)

def test_096_valid_nested_struct_member_access():
    """valid_nested_struct_member_access"""
    source = """
struct Point {
    int x;
};
struct Box {
    Point p;
};
void main() {
    Box b;
    b.p.x = 1;
}
"""
    _assert_checker(source)

def test_097_loop_break_in_helper_function():
    """loop_break_in_helper_function"""
    source = """
void helper() {
    break;
}
void main() {
    while (1) {
        helper();
    }
}
"""
    expected = "MustInLoop(BreakStmt())"
    _assert_checker(source, expected)

def test_098_stmt_switch_case_nonconstant_binary_identifier():
    """stmt_switch_case_nonconstant_binary_identifier"""
    source = """
void main() {
    int x = 1;
    switch (1) {
        case x + 1:
            break;
    }
}
"""
    expected = "TypeMismatchInStatement(SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case BinaryOp(Identifier(x), +, IntLiteral(1)): [BreakStmt()])]))"
    _assert_checker(source, expected)

def test_099_valid_struct_return_and_member_read():
    """valid_struct_return_and_member_read"""
    source = """
struct Point {
    int x;
    int y;
};
Point makePoint(Point p) {
    return p;
}
void main() {
    Point p = {1, 2};
    int x = makePoint(p).x;
}
"""
    _assert_checker(source)

def test_100_expr_function_call_wrong_arity_builtin():
    """expr_function_call_wrong_arity_builtin"""
    source = """
void main() {
    printInt();
}
"""
    expected = "TypeMismatchInExpression(FuncCall(printInt, []))"
    _assert_checker(source, expected)
