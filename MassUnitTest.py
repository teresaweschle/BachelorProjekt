from Parser import Parser
from RandomTermGenerator import RandomTermGenerator
from TermComparator import TermComparator


def test_parser_hardcore():
    p = Parser()
    comparator = TermComparator()
    for i in range(0, 100):
        term = RandomTermGenerator.generate_random_term(6, 10)
        term_cnf = p.convert_to_cnf(term)

        assert comparator.compare_terms(term, term_cnf)
