import typing as t
import pydash as pyd


DataObj = t.TypeVar('DataObj')
Metric = t.TypeVar('Metric')  # Must be comparable and have a natural order, eg int or float


def parameter_maximizing_bisection(
        parameters_to_data: t.Dict[float, DataObj],
        data_to_metric: t.Callable[[DataObj], Metric],
) -> float:
    """
    Figures out the next parameter value to try by bisecting the parameter of the max metric
    with its largest adjacent parameter.
    :param parameters_to_data: Mapping of parameters to their corresponding data objects
    :param data_to_metric: Function that derives a Metric from the DataObj. Should be memoizing for multi-step
        performance.
    :return: Next parameter value to try
    """
    # First, derive metrics for each of the parameters
    params_and_metrics: t.List[t.Tuple[float, Metric]] = [
        (param, data_to_metric(data_obj))
        for param, data_obj in parameters_to_data.items()
    ]

    assert len(params_and_metrics) >= 2, 'Must have at least two parameters to start bisecting sweep'

    # Order the params
    params_and_metrics = pyd.sort_by(params_and_metrics, lambda tup: tup[0])

    # Find the max
    max_param_and_metric = params_and_metrics[0]
    max_param_i = 0
    for i, pm in enumerate(params_and_metrics):
        if max_param_and_metric[1] < pm[1]:
            max_param_and_metric = pm
            max_param_i = i


    adjacent_params = [
        params_and_metrics[i] for i in (max_param_i - 1, max_param_i + 1)
        if 0 <= i < len(params_and_metrics)
    ]

    max_adjacent_param = pyd.max_by(adjacent_params, lambda tup: tup[1])

    # Now bisect the param
    return max_param_and_metric[0] + (max_adjacent_param[0] - max_param_and_metric[0]) / 2





