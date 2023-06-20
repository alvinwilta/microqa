from . import rule


class TRS(rule.Rule):
    def calculate(self):
        sum_trs = 0
        for service in self.param.list_services:
            sum_trs = sum_trs + self.param.list_total_one_service_edges[service]
        return sum_trs / len(self.param.list_services)

    def setup_param(self):
        self.rule_name = 'TRS'
        self.max_value = '+'
        self.param_min = 'Low Complexity'
        self.param_max = 'High Complexity'
        self.best = 'left'