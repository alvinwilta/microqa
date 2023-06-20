from . import rule


class ACS(rule.Rule):
    def calculate(self):
        sum_ACS_S = 0
        for service in self.param.list_services:
            sum_ACS_S += self.ACS_S(self.param.list_in_service_count[service],
                                    self.param.list_out_service_count[service])
        return sum_ACS_S / len(self.param.list_services)

    def setup_param(self):
        self.rule_name = 'ACS'
        self.max_value = 1
        self.param_min = 'Loosely Coupled'
        self.param_max = 'Tightly Coupled'
        self.best = 'left'

    def ACS_S(self, in_service_count: int, out_service_count: int):
        return in_service_count * out_service_count
