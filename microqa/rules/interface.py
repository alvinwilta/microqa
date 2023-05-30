class RuleInterface:
    """
    The interface for the modules to work together
    """

    def __init__(self,
                 total_service: int,
                 list_services: list,
                 list_total_param: dict,
                 list_total_unique_param: dict,
                 list_total_service_ops: dict,
                 list_total_one_service_edges: dict,
                 list_in_service_count: dict,
                 list_out_service_count: dict,
                 list_indirect_call: dict):
        self.list_services = list_services
        self.total_services = total_service
        self.list_total_param = list_total_param
        self.list_total_unique_param = list_total_unique_param
        self.list_total_service_ops = list_total_service_ops
        self.list_total_one_service_edges = list_total_one_service_edges
        self.list_in_service_count = list_in_service_count
        self.list_out_service_count = list_out_service_count
        self.list_indirect_call = list_indirect_call
