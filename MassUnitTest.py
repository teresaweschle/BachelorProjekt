from Parser import Parser
from RandomTermGenerator import RandomTermGenerator
from TermComparator import TermComparator

p = Parser()
comparator = TermComparator()
for i in range(0, 100):
    term = RandomTermGenerator.generate_random_term(5, 10)
    termCnf = p.convertToCNF(term)

    assert comparator.compare_terms(term, termCnf)
