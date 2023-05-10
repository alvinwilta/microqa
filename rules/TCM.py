
def f_val(total_service_ops, total_service):
    return total_service_ops + total_service


def COPF(indirect_call, total_service_ops, total_service):
    f = f_val(total_service_ops, total_service)
    return (indirect_call / ((f * f) - f))


def COHF(total_one_service_edges, total_service_ops, total_service):
    f = f_val(total_service_ops, total_service)
    return (total_one_service_edges / ((f * f) - f))


def COMF(copf, cohf):
    return copf / cohf


def TCM_S(indirect_call, total_one_service_edges, total_service_ops, total_service):
    return ((indirect_call + total_service + total_service_ops) / total_one_service_edges)


def TCM(list_services, total_service, list_total_service_ops, list_total_one_service_edges, list_indirect_call):
    tcm = 0
    for service in list_services:
        copf = COPF(
            list_indirect_call[service], list_total_service_ops[service], total_service)
        cohf = COHF(
            list_total_one_service_edges[service], list_total_service_ops[service], total_service)
        comf = COMF(copf, cohf)
        tcm_s = TCM_S(list_indirect_call[service], list_total_one_service_edges[service],
                      list_total_service_ops[service], total_service)
        tcm += tcm_s * comf
    return tcm
