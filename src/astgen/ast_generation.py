"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language."""

    # ========================================================================
    # Program and Top-level Declarations
    # ========================================================================

    def visitProgram(self, ctx: TyCParser.ProgramContext):
        """program: (structDecl | funcDecl)* EOF"""
        decls = []
        for child in ctx.children:
            if isinstance(child, TyCParser.StructDeclContext):
                decls.append(self.visit(child))
            elif isinstance(child, TyCParser.FuncDeclContext):
                decls.append(self.visit(child))
        return Program(decls)

    def visitStructDecl(self, ctx: TyCParser.StructDeclContext):
        """structDecl: STRUCT IDENTIFIER LEFT_BRACE structMember* RIGHT_BRACE SEMICOLON"""
        name = ctx.IDENTIFIER().getText()
        members = [self.visit(m) for m in ctx.structMember()]
        return StructDecl(name, members)

    def visitStructMember(self, ctx: TyCParser.StructMemberContext):
        """structMember: typeSpec IDENTIFIER SEMICOLON"""
        member_type = self.visit(ctx.typeSpec())
        name = ctx.IDENTIFIER().getText()
        return MemberDecl(member_type, name)

    def visitFuncDecl(self, ctx: TyCParser.FuncDeclContext):
        """funcDecl: returnType? IDENTIFIER LEFT_PAREN paramList? RIGHT_PAREN blockStmt"""
        return_type = self.visit(ctx.returnType()) if ctx.returnType() else None
        name = ctx.IDENTIFIER().getText()
        params = self.visit(ctx.paramList()) if ctx.paramList() else []
        body = self.visit(ctx.blockStmt())
        return FuncDecl(return_type, name, params, body)

    def visitReturnType(self, ctx: TyCParser.ReturnTypeContext):
        """returnType: primitiveType | IDENTIFIER"""
        if ctx.primitiveType():
            return self.visit(ctx.primitiveType())
        return StructType(ctx.IDENTIFIER().getText())

    def visitPrimitiveType(self, ctx: TyCParser.PrimitiveTypeContext):
        """primitiveType: INT_TYPE | FLOAT_TYPE | STRING_TYPE | VOID"""
        token_type = ctx.start.type
        if token_type == TyCParser.INT_TYPE:
            return IntType()
        elif token_type == TyCParser.FLOAT_TYPE:
            return FloatType()
        elif token_type == TyCParser.STRING_TYPE:
            return StringType()
        else:  # VOID
            return VoidType()

    def visitParamList(self, ctx: TyCParser.ParamListContext):
        """paramList: param (COMMA param)*"""
        return [self.visit(p) for p in ctx.param()]

    def visitParam(self, ctx: TyCParser.ParamContext):
        """param: typeSpec IDENTIFIER"""
        param_type = self.visit(ctx.typeSpec())
        name = ctx.IDENTIFIER().getText()
        return Param(param_type, name)

    def visitTypeSpec(self, ctx: TyCParser.TypeSpecContext):
        """typeSpec: primitiveType | IDENTIFIER"""
        if ctx.primitiveType():
            return self.visit(ctx.primitiveType())
        return StructType(ctx.IDENTIFIER().getText())

    # ========================================================================
    # Statements
    # ========================================================================

    def visitBlockStmt(self, ctx: TyCParser.BlockStmtContext):
        """blockStmt: LEFT_BRACE (varDecl | stmt)* RIGHT_BRACE"""
        statements = []
        for child in ctx.children:
            if isinstance(child, TyCParser.VarDeclContext):
                statements.append(self.visit(child))
            elif isinstance(child, TyCParser.StmtContext):
                statements.append(self.visit(child))
        return BlockStmt(statements)

    def visitStmt(self, ctx: TyCParser.StmtContext):
        """stmt: varDecl | blockStmt | ifStmt | ... — delegate to child"""
        return self.visit(ctx.getChild(0))

    def visitVarDecl(self, ctx: TyCParser.VarDeclContext):
        """varDecl:
            AUTO IDENTIFIER (ASSIGN expr)? SEMICOLON
          | typeSpec IDENTIFIER (ASSIGN expr)? SEMICOLON
          | typeSpec IDENTIFIER ASSIGN LEFT_BRACE exprList? RIGHT_BRACE SEMICOLON
        """
        if ctx.AUTO():
            name = ctx.IDENTIFIER().getText()
            init_value = self.visit(ctx.expr()) if ctx.expr() else None
            return VarDecl(None, name, init_value)
        elif ctx.LEFT_BRACE():
            var_type = self.visit(ctx.typeSpec())
            name = ctx.IDENTIFIER().getText()
            values = self.visit(ctx.exprList()) if ctx.exprList() else []
            return VarDecl(var_type, name, StructLiteral(values))
        else:
            var_type = self.visit(ctx.typeSpec())
            name = ctx.IDENTIFIER().getText()
            init_value = self.visit(ctx.expr()) if ctx.expr() else None
            return VarDecl(var_type, name, init_value)

    def visitExprList(self, ctx: TyCParser.ExprListContext):
        """exprList: expr (COMMA expr)*"""
        return [self.visit(e) for e in ctx.expr()]

    def visitIfStmt(self, ctx: TyCParser.IfStmtContext):
        """ifStmt: IF LEFT_PAREN expr RIGHT_PAREN stmt (ELSE stmt)?"""
        condition = self.visit(ctx.expr())
        then_stmt = self.visit(ctx.stmt(0))
        else_stmt = self.visit(ctx.stmt(1)) if len(ctx.stmt()) > 1 else None
        return IfStmt(condition, then_stmt, else_stmt)

    def visitWhileStmt(self, ctx: TyCParser.WhileStmtContext):
        """whileStmt: WHILE LEFT_PAREN expr RIGHT_PAREN stmt"""
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.stmt())
        return WhileStmt(condition, body)

    def visitForStmt(self, ctx: TyCParser.ForStmtContext):
        """forStmt: FOR LEFT_PAREN forInit? SEMICOLON forCondition? SEMICOLON forUpdate? RIGHT_PAREN stmt"""
        init = self.visit(ctx.forInit()) if ctx.forInit() else None
        condition = self.visit(ctx.forCondition()) if ctx.forCondition() else None
        update = self.visit(ctx.forUpdate()) if ctx.forUpdate() else None
        body = self.visit(ctx.stmt())
        return ForStmt(init, condition, update, body)

    def visitForInit(self, ctx: TyCParser.ForInitContext):
        """forInit:
            AUTO IDENTIFIER (ASSIGN expr)?
          | typeSpec IDENTIFIER (ASSIGN expr)?
          | assignExpr
        """
        if ctx.AUTO():
            name = ctx.IDENTIFIER().getText()
            init_value = self.visit(ctx.expr()) if ctx.expr() else None
            return VarDecl(None, name, init_value)
        elif ctx.typeSpec():
            var_type = self.visit(ctx.typeSpec())
            name = ctx.IDENTIFIER().getText()
            init_value = self.visit(ctx.expr()) if ctx.expr() else None
            return VarDecl(var_type, name, init_value)
        else:
            return ExprStmt(self.visit(ctx.assignExpr()))

    def visitForCondition(self, ctx: TyCParser.ForConditionContext):
        """forCondition: expr"""
        return self.visit(ctx.expr())

    def visitForUpdate(self, ctx: TyCParser.ForUpdateContext):
        """forUpdate: assignExpr | postfixExpr"""
        if ctx.assignExpr():
            return self.visit(ctx.assignExpr())
        return self.visit(ctx.postfixExpr())

    def visitSwitchStmt(self, ctx: TyCParser.SwitchStmtContext):
        """switchStmt: SWITCH LEFT_PAREN expr RIGHT_PAREN LEFT_BRACE caseClause* RIGHT_BRACE"""
        expr = self.visit(ctx.expr())
        cases = []
        default_case = None
        for clause in ctx.caseClause():
            result = self.visit(clause)
            if isinstance(result, CaseStmt):
                cases.append(result)
            else:  # DefaultStmt
                default_case = result
        return SwitchStmt(expr, cases, default_case)

    def visitCaseClause(self, ctx: TyCParser.CaseClauseContext):
        """caseClause: CASE expr COLON stmt* | DEFAULT COLON stmt*"""
        stmts = [self.visit(s) for s in ctx.stmt()]
        if ctx.CASE():
            expr = self.visit(ctx.expr())
            return CaseStmt(expr, stmts)
        else:
            return DefaultStmt(stmts)

    def visitBreakStmt(self, ctx: TyCParser.BreakStmtContext):
        return BreakStmt()

    def visitContinueStmt(self, ctx: TyCParser.ContinueStmtContext):
        return ContinueStmt()

    def visitReturnStmt(self, ctx: TyCParser.ReturnStmtContext):
        """returnStmt: RETURN expr? SEMICOLON"""
        expr = self.visit(ctx.expr()) if ctx.expr() else None
        return ReturnStmt(expr)

    def visitExprStmt(self, ctx: TyCParser.ExprStmtContext):
        """exprStmt: expr SEMICOLON"""
        return ExprStmt(self.visit(ctx.expr()))

    # ========================================================================
    # Expressions
    # ========================================================================

    def visitExpr(self, ctx: TyCParser.ExprContext):
        """expr: assignExpr"""
        return self.visit(ctx.assignExpr())

    def visitAssignExpr(self, ctx: TyCParser.AssignExprContext):
        """assignExpr: logicalOrExpr (ASSIGN assignExpr)?"""
        lhs = self.visit(ctx.logicalOrExpr())
        if ctx.assignExpr():
            rhs = self.visit(ctx.assignExpr())
            return AssignExpr(lhs, rhs)
        return lhs

    def visitLogicalOrExpr(self, ctx: TyCParser.LogicalOrExprContext):
        """logicalOrExpr: logicalAndExpr (LOGICAL_OR logicalAndExpr)*"""
        children = [self.visit(c) for c in ctx.logicalAndExpr()]
        if len(children) == 1:
            return children[0]
        result = children[0]
        for i in range(1, len(children)):
            op = ctx.getChild(2 * i - 1).getText()
            result = BinaryOp(result, op, children[i])
        return result

    def visitLogicalAndExpr(self, ctx: TyCParser.LogicalAndExprContext):
        """logicalAndExpr: equalityExpr (LOGICAL_AND equalityExpr)*"""
        children = [self.visit(c) for c in ctx.equalityExpr()]
        if len(children) == 1:
            return children[0]
        result = children[0]
        for i in range(1, len(children)):
            op = ctx.getChild(2 * i - 1).getText()
            result = BinaryOp(result, op, children[i])
        return result

    def visitEqualityExpr(self, ctx: TyCParser.EqualityExprContext):
        """equalityExpr: relationalExpr ((EQUAL | NOT_EQUAL) relationalExpr)*"""
        children = [self.visit(c) for c in ctx.relationalExpr()]
        if len(children) == 1:
            return children[0]
        result = children[0]
        for i in range(1, len(children)):
            op = ctx.getChild(2 * i - 1).getText()
            result = BinaryOp(result, op, children[i])
        return result

    def visitRelationalExpr(self, ctx: TyCParser.RelationalExprContext):
        """relationalExpr: additiveExpr ((LESS_THAN | ...) additiveExpr)*"""
        children = [self.visit(c) for c in ctx.additiveExpr()]
        if len(children) == 1:
            return children[0]
        result = children[0]
        for i in range(1, len(children)):
            op = ctx.getChild(2 * i - 1).getText()
            result = BinaryOp(result, op, children[i])
        return result

    def visitAdditiveExpr(self, ctx: TyCParser.AdditiveExprContext):
        """additiveExpr: multiplicativeExpr ((PLUS | MINUS) multiplicativeExpr)*"""
        children = [self.visit(c) for c in ctx.multiplicativeExpr()]
        if len(children) == 1:
            return children[0]
        result = children[0]
        for i in range(1, len(children)):
            op = ctx.getChild(2 * i - 1).getText()
            result = BinaryOp(result, op, children[i])
        return result

    def visitMultiplicativeExpr(self, ctx: TyCParser.MultiplicativeExprContext):
        """multiplicativeExpr: unaryExpr ((MULTIPLY | DIVIDE | MODULUS) unaryExpr)*"""
        children = [self.visit(c) for c in ctx.unaryExpr()]
        if len(children) == 1:
            return children[0]
        result = children[0]
        for i in range(1, len(children)):
            op = ctx.getChild(2 * i - 1).getText()
            result = BinaryOp(result, op, children[i])
        return result

    def visitUnaryExpr(self, ctx: TyCParser.UnaryExprContext):
        """unaryExpr:
            (PLUS | MINUS | LOGICAL_NOT) unaryExpr
          | (INCREMENT | DECREMENT) unaryExpr
          | postfixExpr
        """
        if ctx.postfixExpr():
            return self.visit(ctx.postfixExpr())
        op = ctx.getChild(0).getText()
        operand = self.visit(ctx.unaryExpr())
        return PrefixOp(op, operand)

    def visitPostfixExpr(self, ctx: TyCParser.PostfixExprContext):
        """postfixExpr: primaryExpr (DOT IDENTIFIER | LEFT_PAREN exprList? RIGHT_PAREN | INCREMENT | DECREMENT)*

        The children after primaryExpr form postfix chains:
        - DOT IDENTIFIER  (2 tokens)
        - LEFT_PAREN exprList? RIGHT_PAREN  (2 or 3 tokens)
        - INCREMENT  (1 token)
        - DECREMENT  (1 token)
        """
        result = self.visit(ctx.primaryExpr())


        children = list(ctx.children)
        i = 1  
        while i < len(children):
            token = children[i]
            token_type = token.symbol.type if hasattr(token, 'symbol') else None

            if token_type == TyCParser.DOT:
                member_name = children[i + 1].getText()
                result = MemberAccess(result, member_name)
                i += 2
            elif token_type == TyCParser.LEFT_PAREN:

                args = []
                i += 1
                if i < len(children):
                    cur = children[i]
                    cur_type = cur.symbol.type if hasattr(cur, 'symbol') else None
                    if isinstance(cur, TyCParser.ExprListContext):
                        args = self.visit(cur)
                        i += 1

                    i += 1 

                if isinstance(result, Identifier):
                    result = FuncCall(result.name, args)
                else:

                    result = FuncCall(str(result), args)
            elif token_type == TyCParser.INCREMENT:
                result = PostfixOp('++', result)
                i += 1
            elif token_type == TyCParser.DECREMENT:
                result = PostfixOp('--', result)
                i += 1
            else:
                i += 1

        return result

    def visitPrimaryExpr(self, ctx: TyCParser.PrimaryExprContext):
        """primaryExpr:
            INTEGER_LITERAL
          | FLOAT_LITERAL
          | STRING_LITERAL
          | IDENTIFIER
          | LEFT_PAREN expr RIGHT_PAREN
          | LEFT_BRACE exprList? RIGHT_BRACE
        """
        if ctx.INTEGER_LITERAL():
            raw = ctx.INTEGER_LITERAL().getText()
            return IntLiteral(int(raw))
        elif ctx.FLOAT_LITERAL():
            raw = ctx.FLOAT_LITERAL().getText()
            return FloatLiteral(float(raw))
        elif ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText())
        elif ctx.IDENTIFIER():
            return Identifier(ctx.IDENTIFIER().getText())
        elif ctx.expr():
            return self.visit(ctx.expr())
        else:
            values = self.visit(ctx.exprList()) if ctx.exprList() else []
            return StructLiteral(values)
