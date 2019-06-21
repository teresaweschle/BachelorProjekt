from Parser import Parser,Term



print(Parser.ConvertFormulaToDMACS("And(x,y)"))

parser = Parser()
megaformel1 = "Or(Impl(Not(a),And(b,Not(a))),And(d,Or(e,f)))"
megaformel1AlsTerm = parser.create_term(megaformel1)
megaformel1InCnf = parser.convertToCNF(megaformel1AlsTerm)

print(Parser.ConvertFormulaToDMACS("Or(Impl(Not(a),And(b,Not(a))),And(d,Or(e,f)))"))