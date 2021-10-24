import typing as t
import os

import requests
import pandas as pd


def assert_pvwatts_ready():
    assert os.environ.get('PVWATTS_API_KEY') is not None, 'Missing PVWATTS_API_KEY envvar! Set it as envvar or into ' \
                                                          'os.environ["PVWATTS_API_KEY"]!'


def v6_1_kw_solar_ac_production(
        lat: float,
        lon: float,
        losses: float = 10,
        system_capacity_kw: float = 1,
        country_code: str = 'US',
        tilt: t.Optional[float] = None,
        azimuth: float = 180,
        module_type: int = 0,
        pvwatts_params: t.Optional[dict] = None,
):
    """
    Makes a call to PVWatts v6

    Most params defined as per https://developer.nrel.gov/docs/solar/pvwatts/v6/

    :param lat:
    :param lon:
    :param losses: System losses as a percent (default 10, or 10% losses)
    :param system_capacity_kw: Defaults to 1kW for easy scaling
    :param country_code:
    :param tilt: 0 is facing up (horizontal), 90 is facing the horizon (vertical)
    :param azimuth: 0 is North-facing, 180 is south-facing
    :param module_type: 0 = Standard, 1 = Premium, 2 = Thin film
    :param pvwatts_params: Key-values of any other pvwatts params to use/override
        Other params to consider using:
        - dc_ac_ratio: DC to AC ratio (default 1.2)
        - inv_eff: Inverter efficiency at rated power (default 96)
        - gcr: Ground coverage ratio, a measure of solar panel overlap (default 0.4)
    :return:
    """
    if tilt is not None:
        assert 0 <= tilt <= 90, 'invalid tilt'
    else:
        tilt = lat  # Good rule of thumb is panels should be angled at latitude

    assert 0 <= azimuth < 360, 'invalid azimuth'

    params = {
        'lat': lat,
        'lon': lon,
        'losses': losses,
        'system_capacity': system_capacity_kw,
        'country_code': country_code,
        'tilt': tilt,
        'azimuth': azimuth,
        'dataset': 'nsrdb' if country_code == 'US' else 'intl',
        'radius': 0,  # Pass in radius=0 to use the closest station regardless of the distance.
        'timeframe': 'hourly',
        'module_type': module_type,
        'array_type': 0,  # Fixed - Open Rack
        'api_key': os.environ["PVWATTS_API_KEY"],
        **(pvwatts_params or {}),
    }
    resp = requests.get(
        url='https://developer.nrel.gov/api/pvwatts/v6.json',
        params=params,
    )

    if not resp.ok:
        raise RuntimeError(f'PVWatts API call failed with {resp.status_code}: {resp.text}')

    return resp


def resp_to_df(json):
    return pd.DataFrame(
        {
            'ac': json['outputs']['dc'],  # AC system output, Wac
            'dc': json['outputs']['dc'],  # DC array output, Wdc

            'temp_amb': json['outputs']['tamb'],  # Ambient temperature, deg C
            'temp_cell': json['outputs']['tcell'],  # Module temperature, deg C

            'irr_diffuse': json['outputs']['df'],  # Diffuse irradiance (W/m2)
            'irr_poa': json['outputs']['poa'],  # Plane-of-array irradiance (W/m2)
            'irr_normal': json['outputs']['dn'],  # Beam normal irradiance (W/m2)
        },
        index=pd.date_range(
            start='2021-01-01',
            end='2022-01-01',  # Normally end date is inclusive, but see 'closed' kwarg
            closed='left',  # start date inclusive, end date exclusive
            # tz=json['station_info']['tz'],  # TODO: This is a constant offset like -08, param needs a str
            freq='H',
        )
    )
