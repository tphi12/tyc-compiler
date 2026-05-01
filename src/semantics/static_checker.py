"""
Static Semantic Checker for TyC Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the TyC procedural programming language. It performs type checking,
scope management, type inference, and detects all semantic errors as
specified in the TyC language specification.
"""

from functools import reduce
from typing import (
    Dict,
    List,
    Set,
    Optional,
    Any,
    Tuple,
    NamedTuple,
    Union,
    TYPE_CHECKING,
)
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode,
    Program,
    StructDecl,
    MemberDecl,
    FuncDecl,
    Param,
    VarDecl,
    IfStmt,
    WhileStmt,
    ForStmt,
    BreakStmt,
    ContinueStmt,
    ReturnStmt,
    BlockStmt,
    SwitchStmt,
    CaseStmt,
    DefaultStmt,
    Type,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    BinaryOp,
    PrefixOp,
    PostfixOp,
    AssignExpr,
    MemberAccess,
    FuncCall,
    Identifier,
    StructLiteral,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    ExprStmt,
    Expr,
    Stmt,
    Decl,
)
from .static_error import (
    StaticError,
    Redeclared,
    UndeclaredIdentifier,
    UndeclaredFunction,
    UndeclaredStruct,
    TypeCannotBeInferred,
    TypeMismatchInStatement,
    TypeMismatchInExpression,
    MustInLoop,
)

class SymbolType:
    VAR = "Variable"
    FUNC = "Function"
    STRUCT = "Struct"
    PARAM = "Parameter"
    MEMBER = "Member"

class Symbol:
    def __init__(self, name: str, kind: str, type_val: Optional[Type] = None):
        self.name = name
        self.kind = kind
        self.type_val = type_val

class FuncSymbol(Symbol):
    def __init__(self, name: str, return_type: Optional[Type], param_types: List[Optional[Type]]):
        super().__init__(name, SymbolType.FUNC, return_type)
        self.param_types = param_types

class StructSymbol(Symbol):
    def __init__(self, name: str, members: Dict[str, Type]):
        super().__init__(name, SymbolType.STRUCT, StructType(name))
        self.members = members

class Environment:
    def __init__(self):
        self.scopes: List[Dict[Tuple[str, bool], Symbol]] = [{}]
        
    def enter_scope(self):
        self.scopes.append({})
        
    def exit_scope(self):
        self.scopes.pop()
        
    def put(self, symbol: Symbol) -> bool:
        key = (symbol.name, symbol.kind == SymbolType.STRUCT)
        if key in self.scopes[-1]:
            return False
        self.scopes[-1][key] = symbol
        return True
        
    def current_has(self, name: str, is_struct: bool = False) -> bool:
        key = (name, is_struct)
        return key in self.scopes[-1]

    def get(self, name: str, is_struct: bool = False) -> Optional[Symbol]:
        key = (name, is_struct)
        for scope in reversed(self.scopes):
            if key in scope:
                return scope[key]
        return None

class DummyForNameBypass:
    def __init__(self, node):
        self.node = node
    def __str__(self):
        return str(self.node)

class StaticChecker(ASTVisitor):
    def __init__(self):
        self.env = Environment()

    def check_unresolved_autos(self, node: ASTNode):
        for sym in self.env.scopes[-1].values():
            if sym.type_val is None:
                raise TypeCannotBeInferred(node)

    def is_constant_expr(self, node: ASTNode) -> bool:
        if isinstance(node, IntLiteral):
            return True
        if isinstance(node, PrefixOp) and node.operator in ('+', '-'):
            return self.is_constant_expr(node.operand)
        if isinstance(node, BinaryOp) and node.operator in ('+', '-', '*', '/', '%'):
            return self.is_constant_expr(node.left) and self.is_constant_expr(node.right)
        return False

    def is_same_type(self, t1: Optional[Type], t2: Optional[Type]) -> bool:
        if t1 is None or t2 is None:
            return False
        if type(t1) != type(t2):
            return False
        if isinstance(t1, StructType) and isinstance(t2, StructType):
            return t1.struct_name == t2.struct_name
        return True

    def find_auto_var(self, node: ASTNode) -> ASTNode:
        if isinstance(node, Identifier):
            return node
        if hasattr(node, 'left'):
            return self.find_auto_var(node.left) or self.find_auto_var(node.right)
        if hasattr(node, 'lhs'):
            return self.find_auto_var(node.lhs) or self.find_auto_var(node.rhs)
        if hasattr(node, 'operand'):
            return self.find_auto_var(node.operand)
        return node

    def is_unknown(self, t: Any) -> bool:
        return t is None

    def check_program(self, ast):
        return self.visit(ast, None)

    def visit_program(self, node: "Program", o: Any = None):
        self.env = Environment()
        self.env.put(FuncSymbol("readInt", IntType(), []))
        self.env.put(FuncSymbol("readFloat", FloatType(), []))
        self.env.put(FuncSymbol("readString", StringType(), []))
        self.env.put(FuncSymbol("printInt", VoidType(), [IntType()]))
        self.env.put(FuncSymbol("printFloat", VoidType(), [FloatType()]))
        self.env.put(FuncSymbol("printString", VoidType(), [StringType()]))
        
        for decl in node.decls:
            self.visit(decl)

    def visit_struct_decl(self, node: "StructDecl", o: Any = None):
        if self.env.current_has(node.name, True):
            raise Redeclared(SymbolType.STRUCT, node.name)
            
        members = {}
        for member in node.members:
            if isinstance(member.member_type, StructType):
                sym = self.env.get(member.member_type.struct_name, True)
                if not isinstance(sym, StructSymbol):
                    raise UndeclaredStruct(member.member_type.struct_name)
            if member.name in members:
                raise Redeclared(SymbolType.MEMBER, member.name)
            members[member.name] = member.member_type
            
        self.env.put(StructSymbol(node.name, members))

    def visit_member_decl(self, node: "MemberDecl", o: Any = None):
        pass 

    def visit_func_decl(self, node: "FuncDecl", o: Any = None):
        if self.env.current_has(node.name, False):
            raise Redeclared(SymbolType.FUNC, node.name)
            
        param_types = []
        for p in node.params:
            if isinstance(p.param_type, StructType):
                sym = self.env.get(p.param_type.struct_name, True)
                if not isinstance(sym, StructSymbol):
                    raise UndeclaredStruct(p.param_type.struct_name)
            param_types.append(p.param_type)
            
        func_sym = FuncSymbol(node.name, node.return_type, param_types)
        self.env.put(func_sym)
        
        self.env.enter_scope()
        
        for p in node.params:
            if self.env.current_has(p.name, False):
                raise Redeclared(SymbolType.PARAM, p.name)
            self.env.put(Symbol(p.name, SymbolType.PARAM, p.param_type))
            
        ctx = dict(o) if o else {}
        ctx['func'] = func_sym
        self.visit(node.body, ctx)
        
        if func_sym.type_val is None:
            func_sym.type_val = VoidType()
            
        self.check_unresolved_autos(node)
        self.env.exit_scope()

    def visit_param(self, node: "Param", o: Any = None):
        pass

    def visit_int_type(self, node: "IntType", o: Any = None):
        return IntType()
    def visit_float_type(self, node: "FloatType", o: Any = None):
        return FloatType()
    def visit_string_type(self, node: "StringType", o: Any = None):
        return StringType()
    def visit_void_type(self, node: "VoidType", o: Any = None):
        return VoidType()
    def visit_struct_type(self, node: "StructType", o: Any = None):
        return node

    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        self.env.enter_scope()
        for stmt in node.statements:
            self.visit(stmt, o)
        self.check_unresolved_autos(node)
        self.env.exit_scope()

    def visit_var_decl(self, node: "VarDecl", o: Any = None):
        var_type = node.var_type
        
        if isinstance(var_type, StructType):
            sym = self.env.get(var_type.struct_name, True)
            if not isinstance(sym, StructSymbol):
                raise UndeclaredStruct(var_type.struct_name)

        if node.init_value:
            ctx = dict(o) if o else {}
            ctx['hint'] = var_type
            init_type = self.visit(node.init_value, ctx)
            
            if self.is_unknown(var_type):
                var_type = init_type
            elif not self.is_unknown(init_type):
                if not self.is_same_type(var_type, init_type):
                    raise TypeMismatchInStatement(node)
                    
        if self.env.current_has(node.name, False):
            raise Redeclared(SymbolType.VAR, node.name)
            
        if len(self.env.scopes) > 1:
            param_sym = self.env.scopes[1].get((node.name, False))
            if param_sym and param_sym.kind == SymbolType.PARAM:
                raise Redeclared(SymbolType.VAR, node.name)
            
        self.env.put(Symbol(node.name, SymbolType.VAR, var_type))
        return var_type

    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        ctx = dict(o) if o else {}
        ctx['hint'] = IntType()
        cond_type = self.visit(node.condition, ctx)
        
        if self.is_unknown(cond_type):
            raise TypeCannotBeInferred(node.condition)
        if not isinstance(cond_type, IntType):
            raise TypeMismatchInStatement(node)
            
        self.env.enter_scope()
        self.visit(node.then_stmt, o)
        self.check_unresolved_autos(node.then_stmt)
        self.env.exit_scope()
        
        if node.else_stmt:
            self.env.enter_scope()
            self.visit(node.else_stmt, o)
            self.check_unresolved_autos(node.else_stmt)
            self.env.exit_scope()

    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        ctx = dict(o) if o else {}
        ctx['hint'] = IntType()
        cond_type = self.visit(node.condition, ctx)
        
        if self.is_unknown(cond_type):
            raise TypeCannotBeInferred(node.condition)
        if not isinstance(cond_type, IntType):
            raise TypeMismatchInStatement(node)
            
        loop_ctx = dict(o) if o else {}
        loop_ctx['in_loop'] = True
        self.env.enter_scope()
        self.visit(node.body, loop_ctx)
        self.check_unresolved_autos(node.body)
        self.env.exit_scope()

    def visit_for_stmt(self, node: "ForStmt", o: Any = None):
        if node.init:
            self.visit(node.init, o)
            if isinstance(node.init, VarDecl):
                sym = self.env.get(node.init.name, False)
                if sym and sym.type_val is None:
                    sym.type_val = IntType()
            elif isinstance(node.init, ExprStmt) and isinstance(node.init.expr, AssignExpr) and isinstance(node.init.expr.lhs, Identifier):
                sym = self.env.get(node.init.expr.lhs.name, False)
                if sym and sym.type_val is None:
                    sym.type_val = IntType()
            
        if node.condition:
            ctx = dict(o) if o else {}
            ctx['hint'] = IntType()
            self.visit(node.condition, ctx)
                
        if node.update:
            self.visit(node.update, o)
            
        loop_ctx = dict(o) if o else {}
        loop_ctx['in_loop'] = True
        
        self.env.enter_scope()
        self.visit(node.body, loop_ctx)
        
        if node.init:
            if isinstance(node.init, VarDecl):
                sym = self.env.get(node.init.name, False)
                init_t = sym.type_val if sym else None
            elif isinstance(node.init, ExprStmt) and isinstance(node.init.expr, AssignExpr) and isinstance(node.init.expr.lhs, Identifier):
                sym = self.env.get(node.init.expr.lhs.name, False)
                init_t = sym.type_val if sym else None
            else:
                init_t = None
            if self.is_unknown(init_t):
                raise TypeCannotBeInferred(node)
            if not isinstance(init_t, IntType):
                raise TypeMismatchInStatement(node)
                
        if node.condition:
            cond_t = self.visit(node.condition, o)
            if self.is_unknown(cond_t):
                raise TypeCannotBeInferred(node)
            if not isinstance(cond_t, IntType):
                raise TypeMismatchInStatement(node)
                
        if node.update:
            upd_t = self.visit(node.update, o)
            if self.is_unknown(upd_t):
                raise TypeCannotBeInferred(node)
            if not isinstance(upd_t, IntType):
                raise TypeMismatchInStatement(node)
                
        self.check_unresolved_autos(node)
        self.env.exit_scope()

    def visit_switch_stmt(self, node: "SwitchStmt", o: Any = None):
        ctx = dict(o) if o else {}
        ctx['hint'] = IntType()
        expr_type = self.visit(node.expr, ctx)
        
        if self.is_unknown(expr_type):
            raise TypeCannotBeInferred(node.expr)
        if not isinstance(expr_type, IntType):
            raise TypeMismatchInStatement(node)
            
        sw_ctx = dict(o) if o else {}
        sw_ctx['in_switch'] = True
        
        self.env.enter_scope()
        for case_st in node.cases:
            self.visit(case_st, sw_ctx)
        if node.default_case:
            self.visit(node.default_case, sw_ctx)
        self.check_unresolved_autos(node)
        self.env.exit_scope()
        
        for case_st in node.cases:
            if not self.is_constant_expr(case_st.expr):
                raise TypeMismatchInStatement(node)

    def visit_case_stmt(self, node: "CaseStmt", o: Any = None):
        ctx = dict(o) if o else {}
        ctx['hint'] = IntType()
        case_val_type = self.visit(node.expr, ctx)
        for stmt in node.statements:
            self.visit(stmt, o)

    def visit_default_stmt(self, node: "DefaultStmt", o: Any = None):
        for stmt in node.statements:
            self.visit(stmt, o)

    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        ol = o or {}
        if not ol.get('in_loop') and not ol.get('in_switch'):
            raise MustInLoop(node)

    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        ol = o or {}
        if not ol.get('in_loop'):
            raise MustInLoop(node)

    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        func_sym = (o.get('func') if o else None)
        
        if func_sym and func_sym.type_val is None:
            if node.expr is None:
                if not hasattr(func_sym, 'pending_void_returns'):
                    func_sym.pending_void_returns = []
                func_sym.pending_void_returns.append(node)
            else:
                ctx = dict(o) if o else {}
                expr_type = self.visit(node.expr, ctx)
                if self.is_unknown(expr_type):
                    raise TypeCannotBeInferred(node)
                    
                func_sym.type_val = expr_type
                if hasattr(func_sym, 'pending_void_returns') and len(func_sym.pending_void_returns) > 0:
                    raise TypeMismatchInStatement(func_sym.pending_void_returns[0])
        elif func_sym:
            if node.expr is None:
                if not isinstance(func_sym.type_val, VoidType):
                    raise TypeMismatchInStatement(node)
            else:
                if isinstance(func_sym.type_val, VoidType):
                    raise TypeMismatchInStatement(node)
                    
                ctx = dict(o) if o else {}
                ctx['hint'] = func_sym.type_val
                expr_type = self.visit(node.expr, ctx)
                    
                if not self.is_same_type(func_sym.type_val, expr_type):
                    raise TypeMismatchInStatement(node)

    def visit_expr_stmt(self, node: "ExprStmt", o: Any = None):
        ctx = dict(o) if o else {}
        ctx['is_stmt'] = node
        return self.visit(node.expr, ctx)


    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        arithmetic = ('+', '-', '*', '/')
        modulus = ('%',)
        relational = ('==', '!=', '<', '<=', '>', '>=')
        logical = ('&&', '||')
        
        hint_left = None
        hint_right = None
        
        if node.operator in logical or node.operator in modulus:
            hint_left = IntType()
            hint_right = IntType()
            
        ctx = dict(o) if o else {}
        
        left_type = self.visit(node.left, {**ctx, 'hint': hint_left})
        right_type = self.visit(node.right, {**ctx, 'hint': hint_right})
        
        if self.is_unknown(left_type) and not self.is_unknown(right_type):
            if isinstance(right_type, IntType) and node.operator not in relational:
                left_type = self.visit(node.left, {**ctx, 'hint': right_type})
        if self.is_unknown(right_type) and not self.is_unknown(left_type):
            if isinstance(left_type, IntType) and node.operator not in relational:
                right_type = self.visit(node.right, {**ctx, 'hint': left_type})
            
        if self.is_unknown(left_type) or self.is_unknown(right_type):
            raise TypeCannotBeInferred(node)
            
        if node.operator in arithmetic or node.operator in relational:
            if isinstance(left_type, FloatType) and self.is_unknown(right_type):
                raise TypeCannotBeInferred(node)
            if isinstance(right_type, FloatType) and self.is_unknown(left_type):
                raise TypeCannotBeInferred(node)
                
        if node.operator in modulus or node.operator in logical:
            if not isinstance(left_type, IntType) or not isinstance(right_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()
            
        elif node.operator in arithmetic or node.operator in relational:
            if not isinstance(left_type, (IntType, FloatType)) or not isinstance(right_type, (IntType, FloatType)):
                raise TypeMismatchInExpression(node)
                
            if node.operator in relational:
                return IntType()
            else:
                if isinstance(left_type, FloatType) or isinstance(right_type, FloatType):
                    return FloatType()
                return IntType()

    def visit_prefix_op(self, node: "PrefixOp", o: Any = None):
        ctx = dict(o) if o else {}
        if node.operator in ('++', '--'):
            if not isinstance(node.operand, (Identifier, MemberAccess)):
                raise TypeMismatchInExpression(node)
            op_type = self.visit(node.operand, {**ctx, 'hint': IntType()})
            if self.is_unknown(op_type):
                raise TypeCannotBeInferred(node)
            if not isinstance(op_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()
        elif node.operator == '!':
            op_type = self.visit(node.operand, {**ctx, 'hint': IntType()})
            if self.is_unknown(op_type):
                raise TypeCannotBeInferred(node)
            if not isinstance(op_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()
        elif node.operator in ('+', '-'):
            op_type = self.visit(node.operand, ctx)
            if self.is_unknown(op_type):
                raise TypeCannotBeInferred(node)
            if not isinstance(op_type, (IntType, FloatType)):
                raise TypeMismatchInExpression(node)
            return op_type

    def visit_postfix_op(self, node: "PostfixOp", o: Any = None):
        ctx = dict(o) if o else {}
        if not isinstance(node.operand, (Identifier, MemberAccess)):
            raise TypeMismatchInExpression(node)
        op_type = self.visit(node.operand, {**ctx, 'hint': IntType()})
        if self.is_unknown(op_type):
            raise TypeCannotBeInferred(node)
        if not isinstance(op_type, IntType):
            raise TypeMismatchInExpression(node)
        return IntType()

    def visit_assign_expr(self, node: "AssignExpr", o: Any = None):
        ol = o or {}
        lhs_type = self.visit(node.lhs, o)
        rhs_type = self.visit(node.rhs, {**ol, 'hint': lhs_type})
        
        if self.is_unknown(lhs_type) and not self.is_unknown(rhs_type):
            if isinstance(rhs_type, IntType):
                lhs_type = self.visit(node.lhs, {**ol, 'hint': rhs_type})
            
        if self.is_unknown(lhs_type) or self.is_unknown(rhs_type):
            raise TypeCannotBeInferred(node)
            
        if not self.is_same_type(lhs_type, rhs_type):
            raise TypeMismatchInExpression(node)
                
        if not isinstance(node.lhs, (Identifier, MemberAccess)):
            raise TypeMismatchInExpression(node)
            
        return lhs_type

    def visit_member_access(self, node: "MemberAccess", o: Any = None):
        obj_type = self.visit(node.obj, o)
        if self.is_unknown(obj_type):
            raise TypeCannotBeInferred(node)
        if not isinstance(obj_type, StructType):
            raise TypeMismatchInExpression(node)
            
        sym = self.env.get(obj_type.struct_name, True)
        if not isinstance(sym, StructSymbol):
            raise UndeclaredStruct(obj_type.struct_name)
            
        if node.member not in sym.members:
            raise TypeMismatchInExpression(node)
            
        return sym.members[node.member]

    def visit_func_call(self, node: "FuncCall", o: Any = None):
        sym = self.env.get(node.name, False)
        if not isinstance(sym, FuncSymbol):
            raise UndeclaredFunction(node.name)
            
        if len(node.args) != len(sym.param_types):
            raise TypeMismatchInExpression(node)
            
        for i, arg in enumerate(node.args):
            ctx = dict(o) if o else {}
            ctx['hint'] = sym.param_types[i]
            arg_type = self.visit(arg, ctx)
            
            if self.is_unknown(arg_type):
                raise TypeCannotBeInferred(node)
                
            if not self.is_same_type(arg_type, sym.param_types[i]):
                raise TypeMismatchInExpression(node)
                
        if sym.type_val is None:
            raise TypeCannotBeInferred(DummyForNameBypass(node))
        return sym.type_val

    def visit_identifier(self, node: "Identifier", o: Any = None):
        sym = self.env.get(node.name, False)
        if not sym:
            raise UndeclaredIdentifier(node.name)
            
        if sym.type_val is None:
            ol = o or {}
            hint = ol.get('hint')
            if hint is not None:
                sym.type_val = hint
                return hint
            return None
        return sym.type_val

    def visit_struct_literal(self, node: "StructLiteral", o: Any = None):
        ol = o or {}
        hint = ol.get('hint')
        
        if hint is None or not isinstance(hint, StructType):
            raise TypeCannotBeInferred(node)
            
        sym = self.env.get(hint.struct_name, True)
        if not isinstance(sym, StructSymbol):
            raise UndeclaredStruct(hint.struct_name)
            
        if len(node.values) != len(sym.members):
            raise TypeMismatchInExpression(node)
            
        for i, (m_id, m_type) in enumerate(sym.members.items()):
            val_type = self.visit(node.values[i], {**ol, 'hint': m_type})
            if self.is_unknown(val_type):
                raise TypeCannotBeInferred(node)
            if not self.is_same_type(val_type, m_type):
                raise TypeMismatchInExpression(node)
                
        return hint

    def visit_int_literal(self, node: "IntLiteral", o: Any = None):
        return IntType()

    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        return FloatType()

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        return StringType()
