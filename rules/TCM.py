from rule import Rule


class TCM(Rule):
    def calculate(self):
        tcm = 0
        for service in self.param.list_services:
            copf = self.COPF(
                self.param.list_indirect_call[service], self.param.list_total_service_ops[service], self.param.total_services)
            cohf = self.COHF(
                self.param.list_total_one_service_edges[service], self.param.list_total_service_ops[service], self.param.total_services)
            comf = self.COMF(copf, cohf)
            tcm_s = self.TCM_S(self.param.list_indirect_call[service], self.param.list_total_one_service_edges[service],
                               self.param.list_total_service_ops[service], self.param.total_services)
            tcm += tcm_s * comf
        return tcm

    def setup_param(self):
        self.rule_name = 'TCM'
        self.max_value = '+'
        self.param_min = 'Low Complexity'
        self.param_max = 'High Complexity'
        self.best = 'left'

    def f_val(self, total_service_ops, total_service):
        return total_service_ops + total_service

    def COPF(self, indirect_call, total_service_ops, total_service):
        f = self.f_val(total_service_ops, total_service)
        return (indirect_call / ((f * f) - f))

    def COHF(self, total_one_service_edges, total_service_ops, total_service):
        f = self.f_val(total_service_ops, total_service)
        return (total_one_service_edges / ((f * f) - f))

    def COMF(self, copf, cohf):
        return copf / cohf

    def TCM_S(self, indirect_call, total_one_service_edges, total_service_ops, total_service):
        return ((indirect_call + total_service + total_service_ops) / total_one_service_edges)
