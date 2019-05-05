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

