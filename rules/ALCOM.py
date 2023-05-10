def LCOM(total_param, total_unique_param, total_service_ops):
    denom = total_unique_param * \
        (1 if total_service_ops == 0 else total_service_ops)
    return 1 - (total_param / (1 if denom == 0 else denom))


def ALCOM(list_services, list_total_param, list_total_unique_param, list_total_service_ops):
    sum_lcom = 0
    for service in list_services:
        sum_lcom += LCOM(list_total_param[service],
                         list_total_unique_param[service], list_total_service_ops[service])
    return sum_lcom / len(list_services)