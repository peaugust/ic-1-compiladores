from .parser.cmmParser import cmmParser
from .parser.cmmVisitor import cmmVisitor
from typing import List, Dict, Callable

class FuncDef:
    def __init__(self, name : str, args : List[str], body : List[Callable] ):
        self.name = name
        self.args = args
        self.body = body
    
    def __call__(self, *args, **kwargs):
        glob = kwargs['glob']

        loc = {}
        for arg, value in zip(self.args, args):
            loc[arg] = value
        
        for stmt in self.body:
            stmt(glob, loc)
            if '__return__' in loc:
                break
        
        return loc['__return__']

class globVisitor(cmmVisitor):
    def __init__(self, file_name):
        self.file_name = file_name
        self.func_table = set()

    def visitStart(self, ctx:cmmParser.StartContext) -> Dict[str, FuncDef]:
        glob = {}
        for func in ctx.func():
            func_def = self.visit(func)
            glob[func_def.name] = func_def

        return glob
    
    def visitFunc(self, ctx:cmmParser.FuncContext):
        name = ctx.name.text
        args = self.visit(ctx.args()) if ctx.args() else [] # List or arguments
        
        self.id_table = set() # Function id table
        for arg in args:
            self.id_table.add(arg)

        self.func_table.add(name)

        body = self.visit(ctx.statms())

        return FuncDef(
            name=name,
            args=args,
            body=body
        )

    def visitStatms(self, ctx:cmmParser.StatmsContext):
        return [self.visit(stmt) for stmt in ctx.statm()]

    def visitWhile(self, ctx:cmmParser.WhileContext):
        test = self.visit(ctx.cond)
        body = self.visit(ctx.statms())

        def __while__(glob, loc):
            while test(glob, loc):
                for stmt in body:
                    stmt(glob, loc)

        return __while__

    def visitIf(self, ctx:cmmParser.IfContext):
        test = self.visit(ctx.cond)
        body = self.visit(ctx.then)
        orelse = self.visit(ctx.otherwise) if ctx.ELSE() else None
        
        def __if__(glob, loc):
            if test(glob, loc):
                for stmt in body:
                    stmt(glob, loc)
            elif orelse is not None:
                for stmt in orelse:
                    stmt(glob, loc)

        return __if__
        
    def visitArgs(self, ctx:cmmParser.ArgsContext):
        return [str(id) for id in ctx.ID()]

    def visitCall(self, ctx:cmmParser.CallContext):
        id = ctx.name.text
        if id not in self.func_table:
            raise KeyError(self.file_name+':'+str(ctx.name.line)+':'+str(ctx.name.column)+' function '+id+' is not defined')
        
        args = self.visit(ctx.exprs())

        return lambda glob, loc : glob[id](*[exp(glob, loc) for exp in args], glob=glob)

    def visitExprs(self, ctx:cmmParser.ExprsContext):
        return [self.visit(x) for x in ctx.expr()]

    def visitAssign(self, ctx:cmmParser.AssignContext):
        expr = self.visit(ctx.expr())
        id = str(ctx.ID())
        if id not in self.id_table: # Create table entry if variable is not defined
            self.id_table.add(id)
        
        def __assign__(glob, loc):
            loc[id] = expr(glob, loc)
            
        return __assign__

    def visitReturn(self, ctx:cmmParser.ReturnContext):
        expr = self.visit(ctx.expr())
        def __return__(glob, loc):
            loc['__return__'] = expr(glob, loc) 
        return __return__

    def visitAtom(self, ctx:cmmParser.AtomContext):
        if ctx.expr():
            return self.visit(ctx.expr())
        elif ctx.ID():
            id = str(ctx.ID())
            if id not in self.id_table:
                symbol = ctx.ID().getSymbol()
                raise KeyError(self.file_name+':'+str(symbol.line)+':'+str(symbol.column)+' variable '+id+' is not defined')
            return lambda glob, loc : loc[id]
        elif ctx.INT():
            value = int(str(ctx.INT()))
            return lambda glob, loc : value
        elif ctx.call():
            return self.visit(ctx.call())
        elif ctx.INPUT():
            return lambda glob, loc : int(input('>>> '))

    op_map = {
        '<' : lambda a, b : a <  b,
        '>' : lambda a, b : a >  b,
        '>=': lambda a, b : a >= b,
        '<=': lambda a, b : a <= b,
        '==': lambda a, b : a == b,
        '!=': lambda a, b : a != b,
        '+' : lambda a, b : a +  b,
        '-' : lambda a, b : a -  b,
        '*' : lambda a, b : a *  b,
        '/' : lambda a, b : a // b,
    }

    def visitExpr(self, ctx:cmmParser.ExprContext):
        left = self.visit(ctx.left)
        if ctx.right: # >, <, >=, <=, ==, != 
            right = self.visit(ctx.right)
            op = self.op_map[ctx.op.text]

            return lambda glob, loc : op(left(glob, loc), right(glob, loc))
        else: # higher priority expsetion 
             return left 

    def visitSumm(self, ctx:cmmParser.SummContext):
        left = self.visit(ctx.left)
        if ctx.right:
            right = self.visit(ctx.right)
            op = self.op_map[ctx.op.text]

            return lambda glob, loc : op(left(glob, loc), right(glob, loc))
        return left

    def visitMult(self, ctx:cmmParser.MultContext):
        left = self.visit(ctx.left)
        if ctx.right:
            right = self.visit(ctx.right)
            op = self.op_map[ctx.op.text]

            return lambda glob, loc : op(left(glob, loc), right(glob, loc))
        return left

    def visitPrint(self, ctx:cmmParser.PrintContext):
        arg = self.visit(ctx.expr())
        return lambda glob, loc : print(arg(glob, loc))

