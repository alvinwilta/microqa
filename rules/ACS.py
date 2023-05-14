def ACS_S(in_service_count: int, out_service_count: int):
    return in_service_count * out_service_count


def ACS(list_services: list, list_in_service_count: dict, list_out_service_count: dict):
    sum_ACS_S = 0
    for service in list_services:
        sum_ACS_S += ACS_S(list_in_service_count[service],
                           list_out_service_count[service])
    return sum_ACS_S / len(list_services)
