# Generated from c:/HK252/PPL/BTL/tyc-compiler/src/grammar/TyC.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .TyCParser import TyCParser
else:
    from TyCParser import TyCParser

# This class defines a complete listener for a parse tree produced by TyCParser.
class TyCListener(ParseTreeListener):

    # Enter a parse tree produced by TyCParser#program.
    def enterProgram(self, ctx:TyCParser.ProgramContext):
        pass

    # Exit a parse tree produced by TyCParser#program.
    def exitProgram(self, ctx:TyCParser.ProgramContext):
        pass


    # Enter a parse tree produced by TyCParser#structDecl.
    def enterStructDecl(self, ctx:TyCParser.StructDeclContext):
        pass

    # Exit a parse tree produced by TyCParser#structDecl.
    def exitStructDecl(self, ctx:TyCParser.StructDeclContext):
        pass


    # Enter a parse tree produced by TyCParser#structMember.
    def enterStructMember(self, ctx:TyCParser.StructMemberContext):
        pass

    # Exit a parse tree produced by TyCParser#structMember.
    def exitStructMember(self, ctx:TyCParser.StructMemberContext):
        pass


    # Enter a parse tree produced by TyCParser#funcDecl.
    def enterFuncDecl(self, ctx:TyCParser.FuncDeclContext):
        pass

    # Exit a parse tree produced by TyCParser#funcDecl.
    def exitFuncDecl(self, ctx:TyCParser.FuncDeclContext):
        pass


    # Enter a parse tree produced by TyCParser#returnType.
    def enterReturnType(self, ctx:TyCParser.ReturnTypeContext):
        pass

    # Exit a parse tree produced by TyCParser#returnType.
    def exitReturnType(self, ctx:TyCParser.ReturnTypeContext):
        pass


    # Enter a parse tree produced by TyCParser#primitiveType.
    def enterPrimitiveType(self, ctx:TyCParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by TyCParser#primitiveType.
    def exitPrimitiveType(self, ctx:TyCParser.PrimitiveTypeContext):
        pass


    # Enter a parse tree produced by TyCParser#paramList.
    def enterParamList(self, ctx:TyCParser.ParamListContext):
        pass

    # Exit a parse tree produced by TyCParser#paramList.
    def exitParamList(self, ctx:TyCParser.ParamListContext):
        pass


    # Enter a parse tree produced by TyCParser#param.
    def enterParam(self, ctx:TyCParser.ParamContext):
        pass

    # Exit a parse tree produced by TyCParser#param.
    def exitParam(self, ctx:TyCParser.ParamContext):
        pass


    # Enter a parse tree produced by TyCParser#typeSpec.
    def enterTypeSpec(self, ctx:TyCParser.TypeSpecContext):
        pass

    # Exit a parse tree produced by TyCParser#typeSpec.
    def exitTypeSpec(self, ctx:TyCParser.TypeSpecContext):
        pass


    # Enter a parse tree produced by TyCParser#stmt.
    def enterStmt(self, ctx:TyCParser.StmtContext):
        pass

    # Exit a parse tree produced by TyCParser#stmt.
    def exitStmt(self, ctx:TyCParser.StmtContext):
        pass


    # Enter a parse tree produced by TyCParser#varDecl.
    def enterVarDecl(self, ctx:TyCParser.VarDeclContext):
        pass

    # Exit a parse tree produced by TyCParser#varDecl.
    def exitVarDecl(self, ctx:TyCParser.VarDeclContext):
        pass


    # Enter a parse tree produced by TyCParser#exprList.
    def enterExprList(self, ctx:TyCParser.ExprListContext):
        pass

    # Exit a parse tree produced by TyCParser#exprList.
    def exitExprList(self, ctx:TyCParser.ExprListContext):
        pass


    # Enter a parse tree produced by TyCParser#blockStmt.
    def enterBlockStmt(self, ctx:TyCParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by TyCParser#blockStmt.
    def exitBlockStmt(self, ctx:TyCParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by TyCParser#ifStmt.
    def enterIfStmt(self, ctx:TyCParser.IfStmtContext):
        pass

    # Exit a parse tree produced by TyCParser#ifStmt.
    def exitIfStmt(self, ctx:TyCParser.IfStmtContext):
        pass


    # Enter a parse tree produced by TyCParser#whileStmt.
    def enterWhileStmt(self, ctx:TyCParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by TyCParser#whileStmt.
    def exitWhileStmt(self, ctx:TyCParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by TyCParser#forStmt.
    def enterForStmt(self, ctx:TyCParser.ForStmtContext):
        pass

    # Exit a parse tree produced by TyCParser#forStmt.
    def exitForStmt(self, ctx:TyCParser.ForStmtContext):
        pass


    # Enter a parse tree produced by TyCParser#forInit.
    def enterForInit(self, ctx:TyCParser.ForInitContext):
        pass

    # Exit a parse tree produced by TyCParser#forInit.
    def exitForInit(self, ctx:TyCParser.ForInitContext):
        pass


    # Enter a parse tree produced by TyCParser#forCondition.
    def enterForCondition(self, ctx:TyCParser.ForConditionContext):
        pass

    # Exit a parse tree produced by TyCParser#forCondition.
    def exitForCondition(self, ctx:TyCParser.ForConditionContext):
        pass


    # Enter a parse tree produced by TyCParser#forUpdate.
    def enterForUpdate(self, ctx:TyCParser.ForUpdateContext):
        pass

    # Exit a parse tree produced by TyCParser#forUpdate.
    def exitForUpdate(self, ctx:TyCParser.ForUpdateContext):
        pass


    # Enter a parse tree produced by TyCParser#switchStmt.
    def enterSwitchStmt(self, ctx:TyCParser.SwitchStmtContext):
        pass

    # Exit a parse tree produced by TyCParser#switchStmt.
    def exitSwitchStmt(self, ctx:TyCParser.SwitchStmtContext):
        pass


    # Enter a parse tree produced by TyCParser#caseClause.
    def enterCaseClause(self, ctx:TyCParser.CaseClauseContext):
        pass

    # Exit a parse tree produced by TyCParser#caseClause.
    def exitCaseClause(self, ctx:TyCParser.CaseClauseContext):
        pass


    # Enter a parse tree produced by TyCParser#breakStmt.
    def enterBreakStmt(self, ctx:TyCParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by TyCParser#breakStmt.
    def exitBreakStmt(self, ctx:TyCParser.BreakStmtContext):
        pass


    # Enter a parse tree produced by TyCParser#continueStmt.
    def enterContinueStmt(self, ctx:TyCParser.ContinueStmtContext):
        pass

    # Exit a parse tree produced by TyCParser#continueStmt.
    def exitContinueStmt(self, ctx:TyCParser.ContinueStmtContext):
        pass


    # Enter a parse tree produced by TyCParser#returnStmt.
    def enterReturnStmt(self, ctx:TyCParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by TyCParser#returnStmt.
    def exitReturnStmt(self, ctx:TyCParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by TyCParser#exprStmt.
    def enterExprStmt(self, ctx:TyCParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by TyCParser#exprStmt.
    def exitExprStmt(self, ctx:TyCParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by TyCParser#expr.
    def enterExpr(self, ctx:TyCParser.ExprContext):
        pass

    # Exit a parse tree produced by TyCParser#expr.
    def exitExpr(self, ctx:TyCParser.ExprContext):
        pass


    # Enter a parse tree produced by TyCParser#assignExpr.
    def enterAssignExpr(self, ctx:TyCParser.AssignExprContext):
        pass

    # Exit a parse tree produced by TyCParser#assignExpr.
    def exitAssignExpr(self, ctx:TyCParser.AssignExprContext):
        pass


    # Enter a parse tree produced by TyCParser#logicalOrExpr.
    def enterLogicalOrExpr(self, ctx:TyCParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by TyCParser#logicalOrExpr.
    def exitLogicalOrExpr(self, ctx:TyCParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by TyCParser#logicalAndExpr.
    def enterLogicalAndExpr(self, ctx:TyCParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by TyCParser#logicalAndExpr.
    def exitLogicalAndExpr(self, ctx:TyCParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by TyCParser#equalityExpr.
    def enterEqualityExpr(self, ctx:TyCParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by TyCParser#equalityExpr.
    def exitEqualityExpr(self, ctx:TyCParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by TyCParser#relationalExpr.
    def enterRelationalExpr(self, ctx:TyCParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by TyCParser#relationalExpr.
    def exitRelationalExpr(self, ctx:TyCParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by TyCParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:TyCParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by TyCParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:TyCParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by TyCParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:TyCParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by TyCParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:TyCParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by TyCParser#unaryExpr.
    def enterUnaryExpr(self, ctx:TyCParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by TyCParser#unaryExpr.
    def exitUnaryExpr(self, ctx:TyCParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by TyCParser#postfixExpr.
    def enterPostfixExpr(self, ctx:TyCParser.PostfixExprContext):
        pass

    # Exit a parse tree produced by TyCParser#postfixExpr.
    def exitPostfixExpr(self, ctx:TyCParser.PostfixExprContext):
        pass


    # Enter a parse tree produced by TyCParser#primaryExpr.
    def enterPrimaryExpr(self, ctx:TyCParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by TyCParser#primaryExpr.
    def exitPrimaryExpr(self, ctx:TyCParser.PrimaryExprContext):
        pass



del TyCParser