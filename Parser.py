import sys
sys.setrecursionlimit(10000)


class Term:
    def __init__(self, operator, parameters=None):
        self.parameters = parameters
        self.operator = operator


class Parser:

    @staticmethod
    def create_term(formula):
        if len(formula) > 3:
            if formula[:2] == "Or":
                formula = formula[3:len(formula) - 1]
                operator = "Or"
            elif formula[:3] == "And":
                formula = formula[4:len(formula) - 1]
                operator = "And"
            elif formula[:3] == "Not":
                formula = formula[4:len(formula) - 1]
                operator = "Not"
            elif formula[:4] == "Impl":
                formula = formula[5:len(formula) - 1]
                operator = "Impl"
            elif formula[:6] == "BiImpl":
                formula = formula[7:len(formula) - 1]
                operator = "BiImpl"
            else:
                assert False, "No valid formula"

            left_parameter = ""
            right_parameter = ""
            parentheses_count = 0
            for i in range(0, len(formula)):
                if formula[i] == "(":
                    parentheses_count += 1
                elif formula[i] == ")":
                    parentheses_count -= 1
                if formula[i] == "," and parentheses_count == 0:
                    right_parameter = formula[i+1:len(formula)]
                    break
                left_parameter += formula[i]

            left_parameter_term = Parser.create_term(left_parameter)  # recursion
            if operator == "Not":
                term = Term(operator, [left_parameter_term])
            else:
                right_parameter_term = Parser.create_term(right_parameter)  # reursion
                term = Term(operator, [left_parameter_term, right_parameter_term])
            return term
        else:
            term = Term(formula, [])
            return term

    @staticmethod
    def replace_implication(term):
        if term.operator is not "Impl":
            return term
        else:
            new_parameters = [Term("Not", [term.parameters[0]])]
            new_parameters += term.parameters[1:]
            replaced = Term("Or", new_parameters)
            return replaced

    @staticmethod
    def replace_biimplication(term):
        if term.operator is not "BiImpl":
            return term
        else:
            subterm1 = Term("Or", [term.parameters[0], Term("Not", [term.parameters[1]])])
            subterm2 = Term("Or", [term.parameters[1], Term("Not", [term.parameters[0]])])
            replaced = Term("And", [subterm1, subterm2])
            return replaced

    @staticmethod
    def de_morgan(term):
        replaced = term
        if term.operator is "Not":
            if term.parameters[0].operator == "Or":
                replaced = Term(
                    "And",
                    [Term("Not", [term.parameters[0].parameters[0]]), Term("Not", [term.parameters[0].parameters[1]])]
                )
            if term.parameters[0].operator == "And":
                replaced = Term(
                    "Or",
                    [Term("Not", [term.parameters[0].parameters[0]]), Term("Not", [term.parameters[0].parameters[1]])]
                )
            if term.parameters[0].operator == "Not":
                replaced = Term(term.parameters[0].parameters[0].operator, term.parameters[0].parameters[0].parameters)
        return replaced

    @staticmethod
    def is_clause(term):
        operators = ("Or", "And", "Not", "Impl", "BiImpl")
        if term.operator not in operators:
            return True
        elif term.operator == "Not":
            if term.parameters[0].operator not in operators:
                return True
            else:
                return False
        elif term.operator == "Or":
            res = (Parser.is_clause(term.parameters[0]) and Parser.is_clause(term.parameters[1]))
            return res
        else:
            return False

    @staticmethod
    def apply_distributive_law(term):
        if term.operator is not "Or":  # hack: in our case we only need Or
            return term
        else:
            if term.parameters[0].operator is not "And" and term.parameters[1].operator is not "And":
                return term
            elif term.parameters[0].operator is "And" and term.parameters[1].operator is "And":
                t1 = Term("Or", [term.parameters[0].parameters[0], term.parameters[1].parameters[0]])
                t2 = Term("Or", [term.parameters[0].parameters[0], term.parameters[1].parameters[1]])
                t3 = Term("Or", [term.parameters[0].parameters[1], term.parameters[1].parameters[0]])
                t4 = Term("Or", [term.parameters[0].parameters[1], term.parameters[1].parameters[1]])
                and1 = Term("And", [t1, t2])
                and2 = Term("And", [t3, t4])
                return Term("And", [and1, and2])
            elif term.parameters[0].operator is "And" and term.parameters[1].operator is not "And":
                t1 = Term("Or", [term.parameters[0].parameters[0], term.parameters[1]])
                t2 = Term("Or", [term.parameters[0].parameters[1], term.parameters[1]])
                return Term("And", [t1, t2])
            elif term.parameters[0].operator is not "And" and term.parameters[1].operator is "And":
                t1 = Term("Or", [term.parameters[1].parameters[0], term.parameters[0]])
                t2 = Term("Or", [term.parameters[1].parameters[1], term.parameters[0]])
                return Term("And", [t1, t2])

    @staticmethod
    def convert_to_cnf(term):
        if term.operator == "Or":
            if Parser.is_clause(term.parameters[0]) and Parser.is_clause(term.parameters[1]):
                return term
            else:
                parameter0 = Parser.convert_to_cnf(term.parameters[0])
                parameter1 = Parser.convert_to_cnf(term.parameters[1])
                result = Term("Or", [parameter0, parameter1])
                result = Parser.apply_distributive_law(result)
                return result
        elif term.operator == "Impl":
            parameter0 = Parser.convert_to_cnf(term.parameters[0])
            parameter1 = Parser.convert_to_cnf(term.parameters[1])
            result = Term("Impl", [parameter0, parameter1])
            result = Parser.replace_implication(result)
            return Parser.convert_to_cnf(result)
        elif term.operator == "BiImpl":
            parameter0 = Parser.convert_to_cnf(term.parameters[0])
            parameter1 = Parser.convert_to_cnf(term.parameters[1])
            result = Term("BiImpl", [parameter0, parameter1])
            result = Parser.replace_biimplication(result)
            return Parser.convert_to_cnf(result)
        elif term.operator == "And":
            if Parser.is_clause(term.parameters[0]) and Parser.is_clause(term.parameters[1]):
                return term
            else:
                parameter0 = Parser.convert_to_cnf(term.parameters[0])
                parameter1 = Parser.convert_to_cnf(term.parameters[1])
                result = Term("And", [parameter0, parameter1])
                return result
        elif term.operator == "Not":
            if term.parameters[0].operator == "And" or term.parameters[0].operator == "Or":
                result = Parser.de_morgan(term)
                result = Parser.convert_to_cnf(result)
                return result
            elif term.parameters[0].operator == "Not":
                return Parser.convert_to_cnf(term.parameters[0].parameters[0])
            elif term.parameters[0].operator == "Impl":
                result = Term(
                    "And",
                    [term.parameters[0].parameters[0], Term("Not", [term.parameters[0].parameters[1]])]
                )
                return Parser.convert_to_cnf(result)
            elif term.parameters[0].operator == "BiImpl":
                rep = Parser.replace_biimplication(term.parameters[0])
                t1 = Term("Not", [rep.parameters[0]])
                t2 = Term("Not", [rep.parameters[1]])
                res = Term("Or", [t1, t2])
                return Parser.convert_to_cnf(res)
            else:
                return term
        else:
            return term

    @staticmethod
    def build_string(term):
        output = ""
        if term.operator == "Or":
            for x in term.parameters:
                if x.operator == "Or":
                    res = Parser.build_string(x)
                    output += res
                elif x.operator == "Not":
                    variable = x.parameters[0].operator
                    res = "-" + variable
                    output += res
                    output += " "
                else:
                    output += x.operator
                    output += " "
        elif term.operator == "And":
            res1 = Parser.build_string(term.parameters[0])
            res2 = Parser.build_string(term.parameters[1])
            output += res1 + "\n"
            output += res2
        else:
            if term.operator == "Not":
                variable = term.parameters[0].operator
                res = "-" + variable
                output += res
            else:
                output += term.operator
        return output

    def create_dmacs(self, term):
        variable_number_by_name = {}
        num_clauses = 1
        num_variables = 0
        current_number = 1
        term = self.build_string(term)
        for x in term:
            if x == "\n":
                num_clauses += 1
            elif x == "-" or x == " ":
                continue
            else:
                if x not in variable_number_by_name:
                    variable_number_by_name[x] = current_number
                    current_number += 1
                    num_variables += 1
        dmacs = "p cnf " + str(num_variables) + " " + str(num_clauses) + "\n"
        for y in term:
            if y in variable_number_by_name:
                y = variable_number_by_name[y]
            dmacs += str(y)
        return dmacs

    @staticmethod
    def convert_formula_to_dmacs(formula):
        parser = Parser()
        formula_term = parser.create_term(formula)
        formula_term_in_cnf = parser.convert_to_cnf(formula_term)
        return parser.create_dmacs(formula_term_in_cnf)
