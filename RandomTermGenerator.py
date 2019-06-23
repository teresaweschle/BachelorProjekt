import random
from Parser import Term, Parser

# TODO_Teresa: um Biimpl, TOP und BOT erweitern


class RandomTermGenerator:

    @staticmethod
    def generate_random_term(max_complexity, max_num_variables):
        complexity = random.randint(1, max_complexity)
        return RandomTermGenerator.__generate_random_term_internal(complexity, max_num_variables)

    @staticmethod
    def __generate_random_term_internal(complexity, max_num_variables):
        operator = 0
        if complexity > 0:
            operator = random.randint(0, 4)

        if operator == 0:
            variable = random.randint(0, max_num_variables)
            return Term(str(variable))
        elif operator == 1:
            term1 = RandomTermGenerator.__generate_random_term_internal(complexity - 1, max_num_variables)
            return Term("Not", [term1])
        elif operator == 2:
            term1 = RandomTermGenerator.__generate_random_term_internal(complexity-1, max_num_variables)
            term2 = RandomTermGenerator.__generate_random_term_internal(complexity-1, max_num_variables)
            return Term("And", [term1, term2])
        elif operator == 3:
            term1 = RandomTermGenerator.__generate_random_term_internal(complexity - 1, max_num_variables)
            term2 = RandomTermGenerator.__generate_random_term_internal(complexity - 1, max_num_variables)
            return Term("Or", [term1, term2])
        elif operator == 4:
            term1 = RandomTermGenerator.__generate_random_term_internal(complexity - 1, max_num_variables)
            term2 = RandomTermGenerator.__generate_random_term_internal(complexity - 1, max_num_variables)
            return Term("Impl", [term1, term2])

# p = Parser()
# for i in range(0, 10):
#     term = RandomTermGenerator.generate_random_term(2, 3)
#     termCnf = p.convertToCNF(term)
#     termOutput = p.createDMACS(term)
#     print(termOutput)
