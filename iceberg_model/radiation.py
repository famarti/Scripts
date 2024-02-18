# -*- coding: utf-8 -*-
"""
Script para cálculos relacionados con la radiación solar y la posición del sol.
"""

import numpy as np
import datetime


def get_julian_datetime(date):
    """
    Convierte un objeto datetime en un número flotante juliano.
    Args:
        date: objeto datetime de la fecha en cuestión

    Returns: float - Fecha juliana calculada (Día del año).
    Raises:
        TypeError : Tipo de parámetro incorrecto
        ValueError: Fecha fuera del rango de la ecuación
    """

    # Asegurar el formato correcto
    if not isinstance(date, datetime.datetime):
        raise TypeError('Tipo de parámetro "date" inválido - se espera datetime')
    elif date.year < 1801 or date.year > 2099:
        raise ValueError("La fecha debe estar entre los años 1801 y 2099")

    # Realizar el cálculo
    julian_datetime = date.timetuple().tm_yday

    return julian_datetime


def f_param(julian_day):
    return (np.pi / 180) * (279.5 + 0.9856 * julian_day)


def delta_param(julian_day):
    return -(np.pi / 180) * 23.45 * np.cos((2 * np.pi * (julian_day + 10)) / 365)


def et_param(f):
    return (
        -104.7 * np.sin(f)
        + 596.2 * np.sin(2 * f)
        + 4.3 * np.sin(3 * f)
        - 12.7 * np.sin(4 * f)
        - 429.3 * np.cos(f)
        - 2 * np.cos(2 * f)
        + 19.3 * np.cos(3 * f)
    ) / 3600


def lc_param(longitude):
    if longitude < 0:
        lon = np.deg2rad(longitude)
        return (-4 / 60) * (np.deg2rad(45) - lon)  # revisar
    else:
        lon = np.deg2rad(longitude)
        return (4 / 60) * (np.deg2rad(45) - lon)


def hour_angle(hour, lc, et):
    t0 = 12 - lc - et
    return (np.pi / 12) * (hour - t0)


def solar_zenith_angle(latitude, hour_angle, delta):
    """
    El ángulo entre los rayos del sol y la dirección vertical.

    Retorna el coseno del ángulo cenital solar.

    La latitud debe estar en grados.
    """
    lat = np.deg2rad(latitude)
    h = hour_angle
    d = delta
    return (np.sin(lat) * np.sin(d)) + (np.cos(lat) * np.cos(d) * np.cos(h))


def solar_irradiance(cos_zenith_angle, julian_day):
    """
    Parámetros
    ----------
    Coseno del ángulo cenital solar.

    Retorna
    -------
    La irradiación solar en W/m^2 día

    -------
    La fórmula de la distancia real Tierra-Sol (R):
    https://physics.stackexchange.com/questions/177949/earth-sun-distance-on-a-given-day-of-the-year

    """
    Rm = 1.49597870e11  # Distancia media Tierra-Sol (m)
    R = (1 - 0.01672 * np.cos(0.9856 * (julian_day - 4))) * (1.496e11)  # (m)
    return 1380 * cos_zenith_angle * (R / Rm) ** (-2)


def irradiance(latitude, longitude, date, hour):
    lat = np.deg2rad(latitude)
    lon = np.deg2rad(longitude)

    # Asegurar el formato correcto
    if not isinstance(date, datetime.datetime) and not isinstance(date, datetime.date):
        raise TypeError('Tipo de parámetro "date" inválido - se espera datetime')
    elif date.year < 1801 or date.year > 2099:
        raise ValueError("La fecha debe estar entre los años 1801 y 2099")

    # Realizar el cálculo
    julian_day = date.timetuple().tm_yday

    f = (np.pi / 180) * (279.5 + 0.9856 * julian_day)

    d = -(np.pi / 180) * 23.45 * np.cos((2 * np.pi * (julian_day + 10)) / 365)

    et = (
        -104.7 * np.sin(f)
        + 596.2 * np.sin(2 * f)
        + 4.3 * np.sin(3 * f)
        - 12.7 * np.sin(4 * f)
        - 429.3 * np.cos(f)
        - 2 * np.cos(2 * f)
        + 19.3 * np.cos(3 * f)
    ) / 3600

    if lon < 0:
        lc = (-4 / 60) * (np.deg2rad(45) - lon)
    else:
        lc = (4 / 60) * (np.deg2rad(45) - lon)

    t0 = 12 - lc - et

    h = (np.pi / 12) * (hour - t0)

    cos_zenith_angle = (np.sin(lat) * np.sin(d)) + (np.cos(lat) * np.cos(d) * np.cos(h))

    Rm = 1.49597870e11  # Distancia media Tierra-Sol (m)
    R = (1 - 0.01672 * np.cos(0.9856 * (julian_day - 4))) * (1.496e11)  # (m)

    I = 1367 * cos_zenith_angle * (R / Rm) ** (-2)  # W/m2

    if I > 0:
        return I
    else:
        return 0


def quick_irradiance(date):
    # Asegurar el formato correcto
    if not isinstance(date, datetime.datetime) and not isinstance(date, datetime.date):
        raise TypeError('Tipo de parámetro "date" inválido - se espera datetime')
    elif date.year < 1801 or date.year > 2099:
        raise ValueError("La fecha debe estar entre los años 1801 y 2099")

    # Realizar el cálculo
    julian_day = date.timetuple().tm_yday

    return 1367 * (1 + 0.034 * np.cos((2 * np.pi) * (julian_day / 265.25)))


# fecha = datetime.datetime.today()
fecha = datetime.date(2021, 6, 21)
hora = 12
irr = irradiance(60.6838, -56.6127, fecha, hora)
# quick_irr = quick_irradiance(fecha)
