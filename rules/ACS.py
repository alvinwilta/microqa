def ACS_S(in_service_count, out_service_count):
    return in_service_count * out_service_count


def ACS(list_services, list_in_service_count, list_out_service_count):
    sum_ACS_S = 0
    for service in list_services:
        sum_ACS_S += ACS_S(list_in_service_count[service],
                           list_out_service_count[service])
    return sum_ACS_S / len(list_services)
