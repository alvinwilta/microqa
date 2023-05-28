from rule import Rule
from interface import RuleInterface


class ALCOM(Rule):
    def calculate(self):
        sum_lcom = 0
        for service in self.param.list_services:
            sum_lcom += self.LCOM(self.param.list_total_param[service],
                                  self.param.list_total_unique_param[service], self.param.list_total_service_ops[service])
        return sum_lcom / len(self.param.list_services)

    def setup_param(self):
        self.rule_name = 'ALCOM'
        self.max_value = 1
        self.param_min = 'Less Cohesive'
        self.param_max = 'Highy Cohesive'
        self.best = 'right'

    def LCOM(self, total_param: int, total_unique_param: int, total_service_ops: int):
        denom = total_unique_param * \
            (1 if total_service_ops == 0 else total_service_ops)
        return 1 - (total_param / (1 if denom == 0 else denom))
