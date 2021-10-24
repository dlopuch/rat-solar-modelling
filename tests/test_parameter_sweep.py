from rat import parameter_sweep


def test_param_bisection__base():
    next_param = parameter_sweep.parameter_maximizing_bisection(
        parameters_to_data={
            0: 11,
            90: 11,
        },
        data_to_metric=lambda x: x,
    )

    assert next_param == 90/2


def test_param_bisection__from_a_max_left():
    next_param = parameter_sweep.parameter_maximizing_bisection(
        parameters_to_data={
            0: 22,
            45: 99,
            90: 11,
        },
        data_to_metric=lambda x: x,
    )

    assert next_param == 45/2


def test_param_bisection__from_a_max_right():
    next_param = parameter_sweep.parameter_maximizing_bisection(
        parameters_to_data={
            0: 11,
            45: 99,
            90: 22,
        },
        data_to_metric=lambda x: x,
    )

    assert next_param == 45 + (90 - 45)/2


def test_param_bisection__from_a_max_right__out_of_order():
    next_param = parameter_sweep.parameter_maximizing_bisection(
        parameters_to_data={
            90: 22,
            0: 11,
            45: 99,
        },
        data_to_metric=lambda x: x,
    )

    assert next_param == 45 + (90 - 45)/2


def test_param_bisection__equal_adjacents():
    # TODO: When the adjacents are equal, we choose only one. Really should spit out both to do.
    next_param = parameter_sweep.parameter_maximizing_bisection(
        parameters_to_data={
            0: 11,
            45: 99,
            90: 11,
        },
        data_to_metric=lambda x: x,
    )

    assert next_param == 45 - 45/2


def test_param_bisection__multiple_maxes():
    # TODO: When multiple maxes, really should suggest multiple bisections
    next_param = parameter_sweep.parameter_maximizing_bisection(
        parameters_to_data={
            0: 55,
            20: 99,
            30: 11,
            40: 99,
            50: 55,
        },
        data_to_metric=lambda x: x,
    )

    assert next_param == 20 - 20/2


def test_param_bisection__data_to_metric_function():
    next_param = parameter_sweep.parameter_maximizing_bisection(
        parameters_to_data={
            0: 22,
            20: 55,
            100: -99,
            120: -30,
        },
        data_to_metric=lambda x: -x,  # Make sure "highest" metrics are the inverted results of fn
    )

    assert next_param == 110

