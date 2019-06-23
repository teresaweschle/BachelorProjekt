from Parser import Parser,Term



print(Parser.convert_formula_to_dmacs("And(x,y)"))

parser = Parser()
megaformel1 = "Or(Impl(Not(a),And(b,Not(a))),And(d,Or(e,f)))"
megaformel1AlsTerm = parser.create_term(megaformel1)
megaformel1InCnf = parser.__convert_to_cnf(megaformel1AlsTerm)
print(Parser.convert_formula_to_dmacs("Or(Impl(Not(a),And(b,Not(a))),And(d,Or(e,f)))"))

megaformel2a = "Or(Impl(Not(a),And(b,Not(g))),And(d,Or(e,f)))"
megaformel2 = "Impl(And(g,a)," + megaformel2a + ")"
#megaforme21AlsTerm = parser.create_term(megaformel2)
#megaformel1InCnf = parser.convertToCNF(megaforme21AlsTerm)
print(Parser.convert_formula_to_dmacs(megaformel2))