import json
import argparse
from datetime import datetime, timedelta
from typing import Iterable

import requests_cache
import openmeteo_requests
import pandas as pd
from retry_requests import retry

team_name = "Декада"


def call_api(lat: float, lng: float, date: str):
    # Extraction of start_date and end_date from input parameter
    start_date = date
    end_date = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=60)).date()

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lng,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation",
                   "rain", "snowfall", "snow_depth", "weather_code", "pressure_msl", "surface_pressure", "cloud_cover",
                   "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "et0_fao_evapotranspiration",
                   "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_100m", "wind_direction_10m",
                   "wind_direction_100m", "wind_gusts_10m", "soil_temperature_0_to_7cm", "soil_temperature_7_to_28cm",
                   "soil_temperature_28_to_100cm", "soil_temperature_100_to_255cm", "soil_moisture_0_to_7cm",
                   "soil_moisture_7_to_28cm", "soil_moisture_28_to_100cm", "soil_moisture_100_to_255cm", "is_day",
                   "sunshine_duration", "shortwave_radiation", "direct_radiation", "diffuse_radiation",
                   "direct_normal_irradiance", "global_tilted_irradiance", "terrestrial_radiation",
                   "shortwave_radiation_instant", "direct_radiation_instant", "diffuse_radiation_instant",
                   "direct_normal_irradiance_instant", "global_tilted_irradiance_instant",
                   "terrestrial_radiation_instant"],
        "wind_speed_unit": "ms",
        "models": ["best_match", "ecmwf_ifs", "era5_seamless", "era5", "era5_land", "cerra"]
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()
    hourly_rain = hourly.Variables(5).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(6).ValuesAsNumpy()
    hourly_snow_depth = hourly.Variables(7).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(8).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(9).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(10).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(11).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(12).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(13).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(14).ValuesAsNumpy()
    hourly_et0_fao_evapotranspiration = hourly.Variables(15).ValuesAsNumpy()
    hourly_vapour_pressure_deficit = hourly.Variables(16).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(17).ValuesAsNumpy()
    hourly_wind_speed_100m = hourly.Variables(18).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(19).ValuesAsNumpy()
    hourly_wind_direction_100m = hourly.Variables(20).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(21).ValuesAsNumpy()
    hourly_soil_temperature_0_to_7cm = hourly.Variables(22).ValuesAsNumpy()
    hourly_soil_temperature_7_to_28cm = hourly.Variables(23).ValuesAsNumpy()
    hourly_soil_temperature_28_to_100cm = hourly.Variables(24).ValuesAsNumpy()
    hourly_soil_temperature_100_to_255cm = hourly.Variables(25).ValuesAsNumpy()
    hourly_soil_moisture_0_to_7cm = hourly.Variables(26).ValuesAsNumpy()
    hourly_soil_moisture_7_to_28cm = hourly.Variables(27).ValuesAsNumpy()
    hourly_soil_moisture_28_to_100cm = hourly.Variables(28).ValuesAsNumpy()
    hourly_soil_moisture_100_to_255cm = hourly.Variables(29).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(30).ValuesAsNumpy()
    hourly_sunshine_duration = hourly.Variables(31).ValuesAsNumpy()
    hourly_shortwave_radiation = hourly.Variables(32).ValuesAsNumpy()
    hourly_direct_radiation = hourly.Variables(33).ValuesAsNumpy()
    hourly_diffuse_radiation = hourly.Variables(34).ValuesAsNumpy()
    hourly_direct_normal_irradiance = hourly.Variables(35).ValuesAsNumpy()
    hourly_global_tilted_irradiance = hourly.Variables(36).ValuesAsNumpy()
    hourly_terrestrial_radiation = hourly.Variables(37).ValuesAsNumpy()
    hourly_shortwave_radiation_instant = hourly.Variables(38).ValuesAsNumpy()
    hourly_direct_radiation_instant = hourly.Variables(39).ValuesAsNumpy()
    hourly_diffuse_radiation_instant = hourly.Variables(40).ValuesAsNumpy()
    hourly_direct_normal_irradiance_instant = hourly.Variables(41).ValuesAsNumpy()
    hourly_global_tilted_irradiance_instant = hourly.Variables(42).ValuesAsNumpy()
    hourly_terrestrial_radiation_instant = hourly.Variables(43).ValuesAsNumpy()

    def to_float_list(array: Iterable):
        return [float(i) for i in array]

    results_dict = {"date": [str(i) for i in pd.date_range(start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                                                           end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                                                           freq=pd.Timedelta(seconds=hourly.Interval()),
                                                           inclusive="left")],
                    "temperature_2m": to_float_list(hourly_temperature_2m),
                    "relative_humidity_2m": to_float_list(hourly_relative_humidity_2m),
                    "dew_point_2m": to_float_list(hourly_dew_point_2m),
                    "apparent_temperature": to_float_list(hourly_apparent_temperature),
                    "precipitation": to_float_list(hourly_precipitation),
                    "rain": to_float_list(hourly_rain),
                    "snowfall": to_float_list(hourly_snowfall),
                    "snow_depth": to_float_list(hourly_snow_depth),
                    "weather_code": to_float_list(hourly_weather_code),
                    "pressure_msl": to_float_list(hourly_pressure_msl),
                    "surface_pressure": to_float_list(hourly_surface_pressure),
                    "cloud_cover": to_float_list(hourly_cloud_cover),
                    "cloud_cover_low": to_float_list(hourly_cloud_cover_low),
                    "cloud_cover_mid": to_float_list(hourly_cloud_cover_mid),
                    "cloud_cover_high": to_float_list(hourly_cloud_cover_high),
                    "et0_fao_evapotranspiration": to_float_list(hourly_et0_fao_evapotranspiration),
                    "vapour_pressure_deficit": to_float_list(hourly_vapour_pressure_deficit),
                    "wind_speed_10m": to_float_list(hourly_wind_speed_10m),
                    "wind_speed_100m": to_float_list(hourly_wind_speed_100m),
                    "wind_direction_10m": to_float_list(hourly_wind_direction_10m),
                    "wind_direction_100m": to_float_list(hourly_wind_direction_100m),
                    "wind_gusts_10m": to_float_list(hourly_wind_gusts_10m),
                    "soil_temperature_0_to_7cm": to_float_list(hourly_soil_temperature_0_to_7cm),
                    "soil_temperature_7_to_28cm": to_float_list(hourly_soil_temperature_7_to_28cm),
                    "soil_temperature_28_to_100cm": to_float_list(hourly_soil_temperature_28_to_100cm),
                    "soil_temperature_100_to_255cm": to_float_list(hourly_soil_temperature_100_to_255cm),
                    "soil_moisture_0_to_7cm": to_float_list(hourly_soil_moisture_0_to_7cm),
                    "soil_moisture_7_to_28cm": to_float_list(hourly_soil_moisture_7_to_28cm),
                    "soil_moisture_28_to_100cm": to_float_list(hourly_soil_moisture_28_to_100cm),
                    "soil_moisture_100_to_255cm": to_float_list(hourly_soil_moisture_100_to_255cm),
                    "is_day": to_float_list(hourly_is_day),
                    "sunshine_duration": to_float_list(hourly_sunshine_duration),
                    "shortwave_radiation": to_float_list(hourly_shortwave_radiation),
                    "direct_radiation": to_float_list(hourly_direct_radiation),
                    "diffuse_radiation": to_float_list(hourly_diffuse_radiation),
                    "direct_normal_irradiance": to_float_list(hourly_direct_normal_irradiance),
                    "global_tilted_irradiance": to_float_list(hourly_global_tilted_irradiance),
                    "terrestrial_radiation": to_float_list(hourly_terrestrial_radiation),
                    "shortwave_radiation_instant": to_float_list(hourly_shortwave_radiation_instant),
                    "direct_radiation_instant": to_float_list(hourly_direct_radiation_instant),
                    "diffuse_radiation_instant": to_float_list(hourly_diffuse_radiation_instant),
                    "direct_normal_irradiance_instant": to_float_list(hourly_direct_normal_irradiance_instant),
                    "global_tilted_irradiance_instant": to_float_list(hourly_global_tilted_irradiance_instant),
                    "terrestrial_radiation_instant": to_float_list(hourly_terrestrial_radiation_instant)}

    return results_dict


# Функция для сохранения результатов в JSON файл
def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, help="Широта")
    parser.add_argument("--lng", type=float, help="Долгота")
    parser.add_argument("--date", type=str, help="Дата в формате YYYY-MM-DD")
    args = parser.parse_args()

    if not all([args.lat, args.lng, args.date]):
        print("Не все обязательные аргументы предоставлены.")
        parser.print_help()
        exit(1)

    results = call_api(args.lat, args.lng, args.date)
    save_json(results, f'{team_name}.json')
