from Parser import Parser,Term

def test_create_term():
    p = Parser()
    x = "Or(a,b)"
    x = p.create_term(x)
    assert x.operator == "Or"
    assert len(x.parameters) == 2
    assert x.parameters[0].operator == "a"
    assert x.parameters[1].operator == "b"
    n = "Not(f)"
    n = p.create_term(n)
    assert n.operator == "Not"
    assert len(n.parameters) == 1
    assert n.parameters[0].operator == "f"
    phi = "And(Or(x,b),y)"
    phi = p.create_term(phi)
    assert phi.operator == "And"
    assert len(phi.parameters) == 2
    assert phi.parameters[0].operator == "Or"
    assert phi.parameters[1].operator == "y"
    psi = "BiImpl(Or(x,b),y)"
    psi = p.create_term(psi)
    assert psi.operator == "BiImpl"
    assert len(psi.parameters) == 2
    assert psi.parameters[0].operator == "Or"
    assert psi.parameters[1].operator == "y"
    x = "Impl(Or(a,b),n)"
    x = p.create_term(x)
    assert x.operator == "Impl"
    assert len(x.parameters) == 2
    assert x.parameters[0].operator == "Or"
    assert x.parameters[1].operator == "n"
    x = "Impl(And(a,b),n)"
    x = p.create_term(x)
    assert len(x.parameters) == 2
    assert x.parameters[0].operator == "And"
    assert x.parameters[1].operator == "n"
    x = "Impl(Not(a),n)"
    x = p.create_term(x)
    assert len(x.parameters) == 2
    assert x.parameters[0].operator == "Not"
    assert x.parameters[1].operator == "n"
    assert len(x.parameters[0].parameters) == 1

def test_replace_implication ():
    x = "Impl(a,b)"
    y= Parser()
    x = y.create_term(x)
    x = y.replace_implication(x)
    assert x.operator == "Or"
    assert x.parameters[0].operator == "Not"
    assert x.parameters[0].parameters[0].operator == "a"
    assert x.parameters[1].operator == "b"

def test_replace_biimplication ():
    x = "BiImpl(a,b)"
    y= Parser()
    x = y.create_term(x)
    x = y.replace_biimplication(x)
    assert x.operator == "And"
    assert x.parameters[0].operator == "Or"
    assert x.parameters[1].operator == "Or"
    assert x.parameters[0].parameters[0].operator == "a"
    assert x.parameters[0].parameters[1].operator == "Not"
    assert x.parameters[0].parameters[1].parameters[0].operator == "b"
    assert x.parameters[1].parameters[0].operator == "b"
    assert x.parameters[1].parameters[1].operator == "Not"
    assert x.parameters[1].parameters[1].parameters[0].operator == "a"

def test_de_Morgan():
    x=("Not(Or(a,b))")
    y =Parser()
    x = y.create_term(x)
    x = y.de_Morgan(x)
    assert x.operator == "And"
    assert x.parameters[0].operator == "Not"
    assert x.parameters[1].operator == "Not"
    assert x.parameters[0].parameters[0].operator == "a"
    assert x.parameters[1].parameters[0].operator == "b"
    x = "Not(Not(a))"
    x = y.create_term(x)
    x = y.de_Morgan(x)
    assert x.operator == "a"
    x = ("Not(And(a,b))")
    x = y.create_term(x)
    x = y.de_Morgan(x)
    assert x.operator == "Or"
    assert x.parameters[0].operator == "Not"
    assert x.parameters[1].operator == "Not"
    assert x.parameters[0].parameters[0].operator == "a"
    assert x.parameters[1].parameters[0].operator == "b"
    x = ("Not(Impl(a,b))")
    x = y.create_term(x)
    x = y.de_Morgan(x)
    assert x.operator == "Not"
    assert x.parameters[0].operator == "Impl"

