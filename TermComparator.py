# TODO_Teresa: um Biimpl, TOP und BOT erweitern


class TermComparator:

    def __init__(self):
        self.known_interpretations = {}

    def get_interpretations(self, num_variables):
        if num_variables in self.known_interpretations:
            return self.known_interpretations[num_variables]

        result = self.compute_interpretations(num_variables)
        self.known_interpretations[num_variables] = result
        return result

    def compute_interpretations(self, num_variables):
        # Abbruchbedingung für Rekursion
        if num_variables == 0:
            return []
        if num_variables == 1:
            return [[0], [1]]

        # num_variables > 1:
        result = []
        # Berechne alle Interpretationen für eine Variable weniger
        result_one_less = self.get_interpretations(num_variables - 1)  # Recursion
        # Kombiniere alle Interpretationen mit einer Variable weniger mit v0 = 0 und v0 = 1
        for interpretation in result_one_less:
            interpretation0 = [0]
            for i in range(0, len(interpretation)):
                interpretation0.append(interpretation[i])
            interpretation1 = [1]
            for i in range(0, len(interpretation)):
                interpretation1.append(interpretation[i])
            result.append(interpretation0)
            result.append(interpretation1)
        return result

    @staticmethod
    def collect_variables(result, term):
        if term.parameters is None or term.parameters == 0:
            if term.operator not in result:
                result.append(term.operator)
        elif len(term.parameters) == 1:
            TermComparator.collect_variables(result, term.parameters[0])
        elif len(term.parameters) == 2:
            TermComparator.collect_variables(result, term.parameters[0])
            TermComparator.collect_variables(result, term.parameters[1])

    @staticmethod
    def compute_truth(variables, term, interpretation):
        if term.parameters is None or term.parameters == 0:
            return interpretation[variables.index(term.operator)]
        elif term.operator == "Not":
            return 1 - TermComparator.compute_truth(variables, term.parameters[0], interpretation)
        elif term.operator == "Or":
            result0 = TermComparator.compute_truth(variables, term.parameters[0], interpretation)
            if result0 == 1:
                return 1
            return TermComparator.compute_truth(variables, term.parameters[1], interpretation)
        elif term.operator == "And":
            result0 = TermComparator.compute_truth(variables, term.parameters[0], interpretation)
            if result0 == 0:
                return 0
            return TermComparator.compute_truth(variables, term.parameters[1], interpretation)
        elif term.operator == "Impl":  # Impl(a,b) gdw Or(-a,b)
            result0 = TermComparator.compute_truth(variables, term.parameters[0], interpretation)
            if result0 == 0:
                return 1
            return TermComparator.compute_truth(variables, term.parameters[1], interpretation)

    def compare_terms(self, term_1, term_2):
        variables = []
        self.collect_variables(variables, term_1)
        self.collect_variables(variables, term_2)

        interpretations = self.get_interpretations(len(variables))
        for interpretation in interpretations:
            result1 = self.compute_truth(variables, term_1, interpretation)
            result2 = self.compute_truth(variables, term_2, interpretation)
            if result1 != result2:
                print("Wrong for interpretation: ")
                print(interpretation)
                return False

        return True


# parser = Parser()
# term1 = parser.create_term("Not(And(a,b))")
# term2 = parser.create_term("Or(Not(a),Not(b))")
# term3 = parser.create_term("Or(a,Not(b))")
#
# comparator = TermComparator()
# print(comparator.compare_terms(term1, term2))
# print(comparator.compare_terms(term1, term3))
