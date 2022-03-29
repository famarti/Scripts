# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 10:29:24 2021

@author: Usuario
"""

import numpy as np
import datetime

# date = datetime.datetime.strptime(run_options.StartTime, "%Y%m%d%H%M%S")

def get_julian_datetime(date):
    """
    Convert a datetime object into julian float.
    Args:
        date: datetime-object of date in question

    Returns: float - Julian calculated datetime (Day of year).
    Raises: 
        TypeError : Incorrect parameter type
        ValueError: Date out of range of equation
    """

    # Ensure correct format
    if not isinstance(date, datetime.datetime):
        raise TypeError('Invalid type for parameter "date" - expecting datetime')
    elif date.year < 1801 or date.year > 2099:
        raise ValueError('Datetime must be between year 1801 and 2099')

    # Perform the calculation
    julian_datetime = date.timetuple().tm_yday 

    return julian_datetime

def f_param(julian_day):
    return (np.pi/180)*(279.5 + 0.9856*julian_day)

def delta_param(julian_day):
    return -(np.pi/180)*23.45*np.cos((2*np.pi*(julian_day+10))/365)

def et_param(f):
    return (-104.7*np.sin(f) + 596.2*np.sin(2*f) + 4.3*np.sin(3*f) - 12.7*np.sin(4*f) - 429.3*np.cos(f) - 2*np.cos(2*f) + 19.3*np.cos(3*f))/3600

def lc_param(longitude):
    if longitude < 0:
        lon = np.deg2rad(longitude)
        return (-4/60)*(np.deg2rad(45) - lon) # revisar
    else:
        lon = np.deg2rad(longitude)
        return (4/60)*(np.deg2rad(45) - lon)
        
def hour_angle(hour, lc, et):
    t0 = 12 - lc - et
    return (np.pi/12)*(hour - t0)

def solar_zenith_angle(latitude, hour_angle, delta):
    """
    The angle between the sun's rays and the vertical direction.
    
    Returns the cosine of the solar zenith angle 
    
    latitude must be on degrees.
    """
    lat = np.deg2rad(latitude)
    h = hour_angle
    d = delta
    return (np.sin(lat)*np.sin(d))+(np.cos(lat)*np.cos(d)*np.cos(h))

def solar_irradiance(cos_zenith_angle, julian_day):
    """

    Parameters
    ----------
    Cosine of solar zenith angle.

    Returns
    -------
    The solar irradiance in W/m^2 day
    
    -------
    The earth-sun real distance (R) formula:
    https://physics.stackexchange.com/questions/177949/earth-sun-distance-on-a-given-day-of-the-year
    
    """
    Rm = 1.49597870E11 # Earth-Sun mean distance (m)
    R = (1 - 0.01672 * np.cos(0.9856 * (julian_day - 4))) * (1.496E11) # (m)
    return 1380*cos_zenith_angle*(R/Rm)**(-2)

def irradiance(latitude, longitude, date, hour):
    lat = np.deg2rad(latitude)
    lon = np.deg2rad(longitude)
    
    # Ensure correct format
    if not isinstance(date, datetime.datetime) and not isinstance(date, datetime.date):
        raise TypeError('Invalid type for parameter "date" - expecting datetime')
    elif date.year < 1801 or date.year > 2099:
        raise ValueError('Datetime must be between year 1801 and 2099')

    # Perform the calculation
    julian_day = date.timetuple().tm_yday 

    f = (np.pi/180)*(279.5 + 0.9856*julian_day)
    
    d = -(np.pi/180)*23.45*np.cos((2*np.pi*(julian_day+10))/365)

    et = (-104.7*np.sin(f) + 596.2*np.sin(2*f) + 4.3*np.sin(3*f) - 12.7*np.sin(4*f) - 429.3*np.cos(f) - 2*np.cos(2*f) + 19.3*np.cos(3*f))/3600

    if lon < 0:
        lc = (-4/60)*(np.deg2rad(45) - lon)
    else:
        lc = (4/60)*(np.deg2rad(45) - lon)

    t0 = 12 - lc - et

    h = (np.pi/12)*(hour - t0)

    cos_zenith_angle = (np.sin(lat)*np.sin(d))+(np.cos(lat)*np.cos(d)*np.cos(h))

    Rm = 1.49597870E11 # Earth-Sun mean distance (m)
    R = (1 - 0.01672 * np.cos(0.9856 * (julian_day - 4))) * (1.496E11) # (m)
    
    I = 1367*cos_zenith_angle*(R/Rm)**(-2) # W/m2

    if I > 0:
        return I
    else:
        return 0

def quick_irradiance(date):
    # Ensure correct format
    if not isinstance(date, datetime.datetime) and not isinstance(date, datetime.date):
        raise TypeError('Invalid type for parameter "date" - expecting datetime')
    elif date.year < 1801 or date.year > 2099:
        raise ValueError('Datetime must be between year 1801 and 2099')

    # Perform the calculation
    julian_day = date.timetuple().tm_yday 
    
    return 1367*(1 + 0.034 * np.cos((2*np.pi)*(julian_day/265.25)))

#fecha = datetime.datetime.today()
fecha = datetime.date(2021,6,21)
hora = 12
irr = irradiance(60.6838, -56.6127, fecha, hora )
#quick_irr = quick_irradiance(fecha)
