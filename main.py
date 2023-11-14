import ephem
import time
import datetime
import mpmath
import sxtwl
mpmath.mp.dps = 10
now = datetime.datetime.utcnow()
time_now = time.gmtime(time.time())
utc_time = f"{time.strftime('%Y-%m-%d', time_now)} 00:00:00"
local_time = datetime.datetime.now().strftime("%Y-%m-%d")
# utc_time = "9999-04-30 00:00:00"
date = sxtwl.fromSolar(int(local_time.split("-")[0]), int(local_time.split("-")[1]), int(local_time.split("-")[2]))
lunar_date_day = date.getLunarDay()
hangzhou = ephem.Observer()
hangzhou.pressure = 0
hangzhou.lat, hangzhou.lon = "30.2901", "120.1277"
def format_time(time):
    return ephem.localtime(ephem.Date(time) + 8 * ephem.hour)
def get_azimuth(azimuth):
    body_azimuth = f"{str(azimuth).split(':')[0]}°{str(azimuth).split(':')[1]}′{str(azimuth).split(':')[2]}″"
    if ephem.degrees("0") <= azimuth < ephem.degrees("22.5"):
        body_azimuth = f"{body_azimuth}（北）"
    elif ephem.degrees("22.5") <= azimuth < ephem.degrees("45"):
        body_azimuth = f"{body_azimuth}（东北偏北）"
    elif ephem.degrees("45") <= azimuth < ephem.degrees("67.5"):
        body_azimuth = f"{body_azimuth}（东北）"
    elif ephem.degrees("67.5") <= azimuth < ephem.degrees("90"):
        body_azimuth = f"{body_azimuth}（东北偏东）"
    elif ephem.degrees("90") <= azimuth < ephem.degrees("112.5"):
        body_azimuth = f"{body_azimuth}（东）"
    elif ephem.degrees("112.5") <= azimuth < ephem.degrees("135"):
        body_azimuth = f"{body_azimuth}（东南偏东）"
    elif ephem.degrees("135") <= azimuth < ephem.degrees("157.5"):
        body_azimuth = f"{body_azimuth}（东南）"
    elif ephem.degrees("157.5") <= azimuth < ephem.degrees("180"):
        body_azimuth = f"{body_azimuth}（东南偏南）"
    elif ephem.degrees("180") <= azimuth < ephem.degrees("202.5"):
        body_azimuth = f"{body_azimuth}（南）"
    elif ephem.degrees("202.5") <= azimuth < ephem.degrees("225"):
        body_azimuth = f"{body_azimuth}（西南偏南）"
    elif ephem.degrees("225") <= azimuth < ephem.degrees("247.5"):
        body_azimuth = f"{body_azimuth}（西南）"
    elif ephem.degrees("247.5") <= azimuth < ephem.degrees("270"):
        body_azimuth = f"{body_azimuth}（西南偏西）"
    elif ephem.degrees("270") <= azimuth < ephem.degrees("292.5"):
        body_azimuth = f"{body_azimuth}（西）"
    elif ephem.degrees("292.5") <= azimuth < ephem.degrees("315"):
        body_azimuth = f"{body_azimuth}（西北偏西）"
    elif ephem.degrees("315") <= azimuth < ephem.degrees("337.5"):
        body_azimuth = f"{body_azimuth}（西北）"
    elif ephem.degrees("337.5") <= azimuth < ephem.degrees("360"):
        body_azimuth = f"{body_azimuth}（西北偏北）"
    return body_azimuth
def moon_phase_name(day):
    if day == 1:
        return "新月"
    elif 2 <= day <= 6:
        return "蛾眉月"
    elif 7 <= day <= 8:
        return "上弦月"
    elif 9 <= day <= 14:
        return "盈凸月"
    elif day == 15:
        return "满月"
    elif 16 <= day <= 21:
        return "亏凸月"
    elif 22 <= day <= 23:
        return "下弦月"
    elif 24 <= day <= 30:
        return "残月"
def get_sun_azimuth(time):
    hangzhou.date = ephem.Date(time) - 8 * ephem.hour
    sun = ephem.Sun()
    sun.compute(hangzhou)
    azimuth = sun.az
    return get_azimuth(azimuth)
def get_moon_azimuth(time):
    hangzhou.date = ephem.Date(time) - 8 * ephem.hour
    moon = ephem.Moon()
    moon.compute(hangzhou)
    azimuth = moon.az
    return get_azimuth(azimuth)
def get_planet_azimuth(time, planet_name):
    hangzhou.date = ephem.Date(time) - 8 * ephem.hour
    planet = eval(f"ephem.{planet_name.capitalize()}()")
    planet.compute(hangzhou)
    azimuth = planet.az
    return get_azimuth(azimuth)
def get_sun_altitude(time):
    hangzhou.date = ephem.Date(time) - 8 * ephem.hour
    sun = ephem.Sun()
    sun.compute(hangzhou)
    altitude = sun.alt
    return format_degrees(altitude)
def get_moon_altitude(time):
    hangzhou.date = ephem.Date(time) - 8 * ephem.hour
    moon = ephem.Moon()
    moon.compute(hangzhou)
    altitude = moon.alt
    return format_degrees(altitude)
def get_planet_altitude(time, planet_name):
    hangzhou.date = ephem.Date(time) - 8 * ephem.hour
    planet = eval(f"ephem.{planet_name.capitalize()}()")
    planet.compute(hangzhou)
    altitude = planet.alt
    return format_degrees(altitude)
def get_infomation(type, time, body_name, mode=None, coordinate=None):
    hangzhou.date = ephem.Date(time)
    body = eval(f"ephem.{body_name.capitalize()}()")
    body.compute(hangzhou)
    if mode:
        declination = eval(f"body.{mode}_dec")
        right_ascension = eval(f"body.{mode}_ra")
    else:
        declination = body.dec
        right_ascension = body.ra
    if coordinate:
        b = eval(f"ephem.{coordinate.capitalize()}(ephem.Equatorial(declination, right_ascension))")
        declination = b.lat
        right_ascension = b.lon
    if type == "declination":
        return format_degrees(declination)
    elif type == "right_ascension":
        return format_degrees(right_ascension)
def get_distance_infomation(planet_sun_distance, english_planet_name, chinese_planet_name):
    mean_sun_distance = {"Mercury": 57909227000, "Venus": 108209475000, "Mars": 227943824000, "Jupiter": 778340821000, "Saturn": 1426666000000, "Uranus": 2870658000000, "Neptune": 4498396000000}
    infomation = f"（{planet_sun_distance * 149597870700 / mean_sun_distance[english_planet_name]}倍{chinese_planet_name}与太阳的平均距离）"
    return infomation
def format_degrees(degree):
    return f"{str(degree).split(':')[0]}°{str(degree).split(':')[1]}′{str(degree).split(':')[2]}″"
sun = ephem.Sun()
sun.compute()
sun_radius = sun.size / 120
hangzhou.horizon = f"-0:{sun_radius}"
now_time = ephem.Date(time.strftime('%Y-%m-%d %H:%M:%S', time_now)) + 8 * ephem.hour
sun_azimuth = get_sun_azimuth(now_time)
sun_altitude = get_sun_altitude(now_time)
sun_declination = get_infomation("declination", now, "Sun")
sun_right_ascension = get_infomation("right_ascension", now, "Sun")
sun_astrometric_declination = get_infomation("declination", now, "Sun", "a")
sun_astrometric_right_ascension = get_infomation("right_ascension", now, "Sun", "a")
sun_apparent_declination = get_infomation("declination", now, "Sun", "g")
sun_apparent_right_ascension = get_infomation("right_ascension", now, "Sun", "g")
ecliptic_sun_declination = get_infomation("declination", now, "Sun", coordinate="ecliptic")
ecliptic_sun_right_ascension = get_infomation("right_ascension", now, "Sun", coordinate="ecliptic")
ecliptic_sun_astrometric_declination = get_infomation("declination", now, "Sun", "a", "ecliptic")
ecliptic_sun_astrometric_right_ascension = get_infomation("right_ascension", now, "Sun", "a", "ecliptic")
ecliptic_sun_apparent_declination = get_infomation("declination", now, "Sun", "g", "ecliptic")
ecliptic_sun_apparent_right_ascension = get_infomation("right_ascension", now, "Sun", "g", "ecliptic")
galactic_sun_declination = get_infomation("declination", now, "Sun", coordinate="galactic")
galactic_sun_right_ascension = get_infomation("right_ascension", now, "Sun", coordinate="galactic")
galactic_sun_astrometric_declination = get_infomation("declination", now, "Sun", "a", "galactic")
galactic_sun_astrometric_right_ascension = get_infomation("right_ascension", now, "Sun", "a", "galactic")
galactic_sun_apparent_declination = get_infomation("declination", now, "Sun", "g", "galactic")
galactic_sun_apparent_right_ascension = get_infomation("right_ascension", now, "Sun", "g", "galactic")
sun_angular_diameter = format_degrees(ephem.hours(f"0:00:{sun.size}"))
sun_magnitude = sun.mag
earth_heliocentric_longitude = sun.hlon
earth_heliocentric_latitude = sun.hlat
def get_shadow_ratio(time):
    hangzhou.date = ephem.Date(time) - 8 * ephem.hour
    sun = ephem.Sun()
    sun.compute(hangzhou)
    a = repr(sun.alt)
    if float(a) > 0:
        shadow_ratio = 1 / mpmath.tan(a)
        return f"1:{shadow_ratio}"
    else:
        return "太阳在地平线以下"
shadow_ratio = get_shadow_ratio(now_time)
sun_earth_distance = f"{sun.earth_distance * 149597870700}米（{sun.earth_distance}倍日地平均距离）"
sun_hour_angle = sun.ha
sunrise_begin = format_time(hangzhou.previous_rising(ephem.Sun(), start=utc_time, use_center=True))
sunrise_begin_azimuth = get_sun_azimuth(sunrise_begin)
sunset_end = format_time(hangzhou.next_setting(ephem.Sun(), start=utc_time, use_center=True))
sunset_end_azimuth = get_sun_azimuth(sunset_end)
hangzhou.horizon = f"0:{sun_radius}"
sunrise_end = format_time(hangzhou.previous_rising(ephem.Sun(), start=utc_time, use_center=True))
sunrise_end_azimuth = get_sun_azimuth(sunrise_end)
sunset_begin = format_time(hangzhou.next_setting(ephem.Sun(), start=utc_time, use_center=True))
sunset_begin_azimuth = get_sun_azimuth(sunset_begin)
sunrise_duration = sunrise_end - sunrise_begin
sunset_duration = sunset_end - sunset_begin
hangzhou.horizon = f"-0:{sun_radius + 34}"
false_sunrise_begin = format_time(hangzhou.previous_rising(ephem.Sun(), start=utc_time, use_center=True))
false_sunrise_begin_azimuth = get_sun_azimuth(false_sunrise_begin)
false_sunset_end = format_time(hangzhou.next_setting(ephem.Sun(), start=utc_time, use_center=True))
false_sunset_end_azimuth = get_sun_azimuth(false_sunset_end)
hangzhou.horizon = f"-0:{34 - sun_radius}"
false_sunrise_end = format_time(hangzhou.previous_rising(ephem.Sun(), start=utc_time, use_center=True))
false_sunrise_end_azimuth = get_sun_azimuth(false_sunrise_end)
false_sunset_begin = format_time(hangzhou.next_setting(ephem.Sun(), start=utc_time, use_center=True))
false_sunset_begin_azimuth = get_sun_azimuth(false_sunset_begin)
false_sunrise_duration = false_sunrise_end - false_sunrise_begin
false_sunset_duration = false_sunset_end - false_sunset_begin
hangzhou.horizon = "-6"
civil_twilight_begin = format_time(hangzhou.previous_rising(ephem.Sun(), start=utc_time, use_center=True))
civil_twilight_end = format_time(hangzhou.next_setting(ephem.Sun(), start=utc_time, use_center=True))
hangzhou.horizon = "-12"
nautical_twilight_begin = format_time(hangzhou.previous_rising(ephem.Sun(), start=utc_time, use_center=True))
nautical_twilight_end = format_time(hangzhou.next_setting(ephem.Sun(), start=utc_time, use_center=True))
hangzhou.horizon = "-18"
astronomical_twilight_begin = format_time(hangzhou.previous_rising(ephem.Sun(), start=utc_time, use_center=True))
astronomical_twilight_end = format_time(hangzhou.next_setting(ephem.Sun(), start=utc_time, use_center=True))
morning_civil_twilight_duration = sunrise_begin - civil_twilight_begin
evening_civil_twilight_duration = civil_twilight_end - sunset_end
morning_nautical_twilight_duration = civil_twilight_begin - nautical_twilight_begin
evening_nautical_twilight_duration = nautical_twilight_end - civil_twilight_end
morning_astronomical_twilight_duration = nautical_twilight_begin - astronomical_twilight_begin
evening_astronomical_twilight_duration = astronomical_twilight_end - nautical_twilight_end
hangzhou.horizon = "6"
sunrise_golden_hour_end = format_time(hangzhou.previous_rising(ephem.Sun(), start=utc_time, use_center=True))
sunrise_golden_hour_end_azimuth = get_sun_azimuth(sunrise_golden_hour_end)
sunset_golden_hour_begin = format_time(hangzhou.next_setting(ephem.Sun(), start=utc_time, use_center=True))
sunset_golden_hour_begin_azimuth = get_sun_azimuth(sunset_golden_hour_begin)
sunrise_golden_hour_begin = false_sunrise_begin
sunrise_golden_hour_begin_azimuth = false_sunrise_begin_azimuth
sunset_golden_hour_end = false_sunset_end
sunset_golden_hour_end_azimuth = false_sunset_end_azimuth
sunrise_golden_hour_duration = sunrise_golden_hour_end - sunrise_golden_hour_begin
sunset_golden_hour_duration = sunset_golden_hour_end - sunset_golden_hour_begin
hangzhou.horizon = "-8"
sunrise_blue_hour_begin = format_time(hangzhou.previous_rising(ephem.Sun(), start=utc_time, use_center=True))
sunset_blue_hour_end = format_time(hangzhou.next_setting(ephem.Sun(), start=utc_time, use_center=True))
hangzhou.horizon = "-4"
sunrise_blue_hour_end = format_time(hangzhou.previous_rising(ephem.Sun(), start=utc_time, use_center=True))
sunset_blue_hour_begin = format_time(hangzhou.next_setting(ephem.Sun(), start=utc_time, use_center=True))
sunrise_blue_hour_duration = sunrise_blue_hour_end - sunrise_blue_hour_begin
sunset_blue_hour_duration = sunset_blue_hour_end - sunset_blue_hour_begin
sun_upper_culmination = format_time(hangzhou.next_transit(ephem.Sun(), start=utc_time))
sun_upper_culmination_altitude = get_sun_altitude(sun_upper_culmination)
sun_lower_culmination = format_time(hangzhou.next_antitransit(ephem.Sun(), start=utc_time))
sun_lower_culmination_altitude = get_sun_altitude(sun_lower_culmination)
day_duration = sunset_end - sunrise_begin
dawn_duration = sunrise_begin - astronomical_twilight_begin
dusk_duration = astronomical_twilight_end - sunset_end
a = format_time(ephem.Date(f"{time.strftime('%Y-%m-%d', time_now)} 16:00:00"))
night_duration = str(a - astronomical_twilight_end + astronomical_twilight_begin).split(" ")[1]
moon = ephem.Moon()
moon.compute()
radius = moon.size / 120
moon_azimuth = get_moon_azimuth(now_time)
moon_altitude = get_moon_altitude(now_time)
moon_declination = get_infomation("declination", now, "Moon")
moon_right_ascension = get_infomation("right_ascension", now, "Moon")
moon_astrometric_declination = get_infomation("declination", now, "Moon", "a")
moon_astrometric_right_ascension = get_infomation("right_ascension", now, "Moon", "a")
moon_apparent_declination = get_infomation("declination", now, "Moon", "g")
moon_apparent_right_ascension = get_infomation("right_ascension", now, "Moon", "g")
ecliptic_moon_declination = get_infomation("declination", now, "Moon", coordinate="ecliptic")
ecliptic_moon_right_ascension = get_infomation("right_ascension", now, "Moon", coordinate="ecliptic")
ecliptic_moon_astrometric_declination = get_infomation("declination", now, "Moon", "a", "ecliptic")
ecliptic_moon_astrometric_right_ascension = get_infomation("right_ascension", now, "Moon", "a", "ecliptic")
ecliptic_moon_apparent_declination = get_infomation("declination", now, "Moon", "g", "ecliptic")
ecliptic_moon_apparent_right_ascension = get_infomation("right_ascension", now, "Moon", "g", "ecliptic")
galactic_moon_declination = get_infomation("declination", now, "Moon", coordinate="galactic")
galactic_moon_right_ascension = get_infomation("right_ascension", now, "Moon", coordinate="galactic")
galactic_moon_astrometric_declination = get_infomation("declination", now, "Moon", "a", "galactic")
galactic_moon_astrometric_right_ascension = get_infomation("right_ascension", now, "Moon", "a", "galactic")
galactic_moon_apparent_declination = get_infomation("declination", now, "Moon", "g", "galactic")
galactic_moon_apparent_right_ascension = get_infomation("right_ascension", now, "Moon", "g", "galactic")
moon_angular_diameter = format_degrees(ephem.hours(f"0:00:{moon.size}"))
moon_magnitude = moon.mag
moon_earth_distance = f"{moon.earth_distance * 149597870700}米（{moon.earth_distance}天文单位）（{moon.earth_distance * 149597870700 / 384400000}倍地月平均距离）"
moon_sun_distance = f"{moon.sun_distance * 149597870700}米（{moon.sun_distance}天文单位）"
moon_hour_angle = moon.ha
moon_phase = f"{moon.moon_phase * 100}%（{moon_phase_name(lunar_date_day)}）"
previous_new_moon_time = format_time(ephem.previous_new_moon(utc_time))
next_new_moon_time = format_time(ephem.next_new_moon(utc_time))
previous_first_quarter_moon_time = format_time(ephem.previous_first_quarter_moon(utc_time))
next_first_quarter_moon_time = format_time(ephem.next_first_quarter_moon(utc_time))
previous_full_moon_time = format_time(ephem.previous_full_moon(utc_time))
next_full_moon_time = format_time(ephem.next_full_moon(utc_time))
previous_last_quarter_moon_time = format_time(ephem.previous_last_quarter_moon(utc_time))
next_last_quarter_moon_time = format_time(ephem.next_last_quarter_moon(utc_time))
moon_age = f"{str(format_time(now) - previous_new_moon_time).split(' days, ')[0]}天{str(format_time(now) - previous_new_moon_time).split(' days, ')[1]}"
moon_elongation = moon.elong
hangzhou.horizon = f"-0:{radius}:00"
moonrise_begin_a = format_time(hangzhou.previous_rising(ephem.Moon(), start=utc_time, use_center=True))
moonrise_begin_b = format_time(hangzhou.next_rising(ephem.Moon(), start=utc_time, use_center=True))
moonset_end_a = format_time(hangzhou.previous_setting(ephem.Moon(), start=utc_time, use_center=True))
moonset_end_b = format_time(hangzhou.next_setting(ephem.Moon(), start=utc_time, use_center=True))
hangzhou.horizon = f"0:{radius}:00"
moonrise_end_a = format_time(hangzhou.previous_rising(ephem.Moon(), start=utc_time, use_center=True))
moonrise_end_b = format_time(hangzhou.next_rising(ephem.Moon(), start=utc_time, use_center=True))
moonset_begin_a = format_time(hangzhou.previous_setting(ephem.Moon(), start=utc_time, use_center=True))
moonset_begin_b = format_time(hangzhou.next_setting(ephem.Moon(), start=utc_time, use_center=True))
hangzhou.horizon = f"-0:{34 + radius}:00"
false_moonrise_begin_a = format_time(hangzhou.previous_rising(ephem.Moon(), start=utc_time, use_center=True))
false_moonrise_begin_b = format_time(hangzhou.next_rising(ephem.Moon(), start=utc_time, use_center=True))
false_moonset_end_a = format_time(hangzhou.previous_setting(ephem.Moon(), start=utc_time, use_center=True))
false_moonset_end_b = format_time(hangzhou.next_setting(ephem.Moon(), start=utc_time, use_center=True))
hangzhou.horizon = f"-0:{34 - radius}:00"
false_moonrise_end_a = format_time(hangzhou.previous_rising(ephem.Moon(), start=utc_time, use_center=True))
false_moonrise_end_b = format_time(hangzhou.next_rising(ephem.Moon(), start=utc_time, use_center=True))
false_moonset_begin_a = format_time(hangzhou.previous_setting(ephem.Moon(), start=utc_time, use_center=True))
false_moonset_begin_b = format_time(hangzhou.next_setting(ephem.Moon(), start=utc_time, use_center=True))
def screen_time(now):
    if now == "":
        return False
    a = utc_time.split("-")[2].split(" ")[0]
    b = str(now).split("-")[2].split(" ")[0]
    if a == b:
        return True
    else:
        return False
moonrise_begin = None
moonrise_end = None
moonset_begin = None
moonset_end = None
if screen_time(moonrise_begin_a):
    moonrise_begin = moonrise_begin_a
elif screen_time(moonrise_begin_b):
    moonrise_begin = moonrise_begin_b
if screen_time(moonset_end_a):
    moonset_end = moonset_end_a
elif screen_time(moonset_end_b):
    moonset_end = moonset_end_b
if screen_time(moonrise_end_a):
    moonrise_end = moonrise_end_a
elif screen_time(moonrise_end_b):
    moonrise_end = moonrise_end_b
if screen_time(moonset_begin_a):
    moonset_begin = moonset_begin_a
elif screen_time(moonset_begin_b):
    moonset_begin = moonset_begin_b
if moonrise_begin != None and moonrise_end != None:
    moonrise_duration = moonrise_end - moonrise_begin
    moonrise_end_azimuth = get_moon_azimuth(moonrise_end)
    moonrise_begin_azimuth = get_moon_azimuth(moonrise_begin)
if moonrise_begin == None or moonrise_end == None:
    moonrise_begin, moonrise_end, moonrise_duration = "无月出", "无月出", "无月出"
    moonrise_begin_azimuth, moonrise_end_azimuth = "无月出", "无月出"
if moonset_begin != None and moonset_end != None:
    moonset_duration = moonset_end - moonset_begin
    moonset_end_azimuth = get_moon_azimuth(moonset_end)
    moonset_begin_azimuth = get_moon_azimuth(moonset_begin)
if moonset_begin == None or moonset_end == None:
    moonset_begin, moonset_end, moonset_duration = "无月落", "无月落", "无月落"
    moonset_begin_azimuth, moonset_end_azimuth = "无月落", "无月落"
false_moonrise_begin = None
false_moonrise_end = None
false_moonset_begin = None
false_moonset_end = None
if screen_time(false_moonrise_begin_a):
    false_moonrise_begin = false_moonrise_begin_a
elif screen_time(false_moonrise_begin_b):
    false_moonrise_begin = false_moonrise_begin_b
if screen_time(false_moonset_end_a):
    false_moonset_end = false_moonset_end_a
elif screen_time(false_moonset_end_b):
    false_moonset_end = false_moonset_end_b
if screen_time(false_moonrise_end_a):
    false_moonrise_end = false_moonrise_end_a
elif screen_time(false_moonrise_end_b):
    false_moonrise_end = false_moonrise_end_b
if screen_time(false_moonset_begin_a):
    false_moonset_begin = false_moonset_begin_a
elif screen_time(false_moonset_begin_b):
    false_moonset_begin = false_moonset_begin_b
if false_moonrise_begin != None and false_moonrise_end != None:
    false_moonrise_duration = false_moonrise_end - false_moonrise_begin
    false_moonrise_end_azimuth = get_moon_azimuth(false_moonrise_end)
    false_moonrise_begin_azimuth = get_moon_azimuth(false_moonrise_begin)
if false_moonrise_begin == None or false_moonrise_end == None:
    false_moonrise_begin, false_moonrise_end, false_moonrise_duration = "无假月出", "无假月出", "无假月出"
    false_moonrise_begin_azimuth, false_moonrise_end_azimuth = "无假月出", "无假月出"
if false_moonset_begin != None and false_moonset_end != None:
    false_moonset_duration = false_moonset_end - false_moonset_begin
    false_moonset_end_azimuth = get_moon_azimuth(false_moonset_end)
    false_moonset_begin_azimuth = get_moon_azimuth(false_moonset_begin)
if false_moonset_begin == None or false_moonset_end == None:
    false_moonset_begin, false_moonset_end, false_moonset_duration = "无假月落", "无假月落", "无假月落"
    false_moonset_begin_azimuth, false_moonset_end_azimuth = "无假月落", "无假月落"
upper_culmination_a = format_time(hangzhou.previous_transit(ephem.Moon(), start=utc_time))
upper_culmination_b = format_time(hangzhou.next_transit(ephem.Moon(), start=utc_time))
lower_culmination_a = format_time(hangzhou.previous_antitransit(ephem.Moon(), start=utc_time))
lower_culmination_b = format_time(hangzhou.next_antitransit(ephem.Moon(), start=utc_time))
moon_upper_culmination = None
moon_lower_culmination = None
if screen_time(upper_culmination_a):
    moon_upper_culmination = upper_culmination_a
elif screen_time(upper_culmination_b):
    moon_upper_culmination = upper_culmination_b
if screen_time(lower_culmination_a):
    moon_lower_culmination = lower_culmination_a
elif screen_time(lower_culmination_b):
    moon_lower_culmination = lower_culmination_b
if moon_upper_culmination == None:
    moon_upper_culmination = "无月上中天"
    moon_upper_culmination_altitude = "无月上中天"
else:
    moon_upper_culmination_altitude = get_moon_altitude(moon_upper_culmination)
if moon_lower_culmination == None:
    moon_lower_culmination = "无月下中天"
    moon_upper_culmination_altitude = "无月下中天"
else:
    moon_lower_culmination_altitude = get_moon_altitude(moon_lower_culmination)

def get_planet_infomation(english_planet_name, chinese_planet_name):
    planet = eval(f"ephem.{english_planet_name.capitalize()}()")
    planet.compute()
    radius = planet.size / 120
    planet_azimuth = get_planet_azimuth(now_time, english_planet_name)
    planet_altitude = get_planet_altitude(now_time, english_planet_name)
    planet_declination = get_infomation("declination", now, english_planet_name)
    planet_right_ascension = get_infomation("right_ascension", now, english_planet_name)
    planet_astrometric_declination = get_infomation("declination", now, english_planet_name, "a")
    planet_astrometric_right_ascension = get_infomation("right_ascension", now, english_planet_name, "a")
    planet_apparent_declination = get_infomation("declination", now, english_planet_name, "g")
    planet_apparent_right_ascension = get_infomation("right_ascension", now, english_planet_name, "g")
    ecliptic_planet_declination = get_infomation("declination", now, english_planet_name, coordinate="ecliptic")
    ecliptic_planet_right_ascension = get_infomation("right_ascension", now, english_planet_name, coordinate="ecliptic")
    ecliptic_planet_astrometric_declination = get_infomation("declination", now, english_planet_name, "a", "ecliptic")
    ecliptic_planet_astrometric_right_ascension = get_infomation("right_ascension", now, english_planet_name, "a", "ecliptic")
    ecliptic_planet_apparent_declination = get_infomation("declination", now, english_planet_name, "g", "ecliptic")
    ecliptic_planet_apparent_right_ascension = get_infomation("right_ascension", now, english_planet_name, "g", "ecliptic")
    galactic_planet_declination = get_infomation("declination", now, english_planet_name, coordinate="galactic")
    galactic_planet_right_ascension = get_infomation("right_ascension", now, english_planet_name, coordinate="galactic")
    galactic_planet_astrometric_declination = get_infomation("declination", now, english_planet_name, "a", "galactic")
    galactic_planet_astrometric_right_ascension = get_infomation("right_ascension", now, english_planet_name, "a", "galactic")
    galactic_planet_apparent_declination = get_infomation("declination", now, english_planet_name, "g", "galactic")
    galactic_planet_apparent_right_ascension = get_infomation("right_ascension", now, english_planet_name, "g", "galactic")
    planet_angular_diameter = format_degrees(ephem.hours(f"0:00:{planet.size}"))
    planet_magnitude = planet.mag
    planet_earth_distance = f"{planet.earth_distance * 149597870700}米（{planet.earth_distance}天文单位）"
    planet_sun_distance = f"{planet.sun_distance * 149597870700}米（{planet.sun_distance}天文单位）{get_distance_infomation(planet.sun_distance, english_planet_name, chinese_planet_name)}"
    planet_hour_angle = planet.ha
    planet_phase = f"{planet.phase}%"
    planet_elongation = planet.elong
    hangzhou.horizon = f"-0:{radius}:00"
    planet_rise_begin_a = format_time(hangzhou.previous_rising(planet, start=utc_time, use_center=True))
    planet_rise_begin_b = format_time(hangzhou.next_rising(planet, start=utc_time, use_center=True))
    planet_set_end_a = format_time(hangzhou.previous_setting(planet, start=utc_time, use_center=True))
    planet_set_end_b = format_time(hangzhou.next_setting(planet, start=utc_time, use_center=True))
    hangzhou.horizon = f"0:{radius}:00"
    planet_rise_end_a = format_time(hangzhou.previous_rising(planet, start=utc_time, use_center=True))
    planet_rise_end_b = format_time(hangzhou.next_rising(planet, start=utc_time, use_center=True))
    planet_set_begin_a = format_time(hangzhou.previous_setting(planet, start=utc_time, use_center=True))
    planet_set_begin_b = format_time(hangzhou.next_setting(planet, start=utc_time, use_center=True))
    hangzhou.horizon = f"-0:{34 + radius}:00"
    false_planet_rise_begin_a = format_time(hangzhou.previous_rising(planet, start=utc_time, use_center=True))
    false_planet_rise_begin_b = format_time(hangzhou.next_rising(planet, start=utc_time, use_center=True))
    false_planet_set_end_a = format_time(hangzhou.previous_setting(planet, start=utc_time, use_center=True))
    false_planet_set_end_b = format_time(hangzhou.next_setting(planet, start=utc_time, use_center=True))
    hangzhou.horizon = f"-0:{34 - radius}:00"
    false_planet_rise_end_a = format_time(hangzhou.previous_rising(planet, start=utc_time, use_center=True))
    false_planet_rise_end_b = format_time(hangzhou.next_rising(planet, start=utc_time, use_center=True))
    false_planet_set_begin_a = format_time(hangzhou.previous_setting(planet, start=utc_time, use_center=True))
    false_planet_set_begin_b = format_time(hangzhou.next_setting(planet, start=utc_time, use_center=True))
    def screen_time(now):
        if now == "":
            return False
        a = utc_time.split("-")[2].split(" ")[0]
        b = str(now).split("-")[2].split(" ")[0]
        if a == b:
            return True
        else:
            return False
    planet_rise_begin = None
    planet_rise_end = None
    planet_set_begin = None
    planet_set_end = None
    if screen_time(planet_rise_begin_a):
        planet_rise_begin = planet_rise_begin_a
    elif screen_time(planet_rise_begin_b):
        planet_rise_begin = planet_rise_begin_b
    if screen_time(planet_set_end_a):
        planet_set_end = planet_set_end_a
    elif screen_time(planet_set_end_b):
        planet_set_end = planet_set_end_b
    if screen_time(planet_rise_end_a):
        planet_rise_end = planet_rise_end_a
    elif screen_time(planet_rise_end_b):
        planet_rise_end = planet_rise_end_b
    if screen_time(planet_set_begin_a):
        planet_set_begin = planet_set_begin_a
    elif screen_time(planet_set_begin_b):
        planet_set_begin = planet_set_begin_b
    if planet_rise_begin != None and planet_rise_end != None:
        planet_rise_duration = planet_rise_end - planet_rise_begin
        planet_rise_end_azimuth = get_planet_azimuth(planet_rise_end, english_planet_name)
        planet_rise_begin_azimuth = get_planet_azimuth(planet_rise_begin, english_planet_name)
    if planet_rise_begin == None or planet_rise_end == None:
        planet_rise_begin, planet_rise_end, planet_rise_duration = f"{english_planet_name}未升起", f"{english_planet_name}未升起", f"{english_planet_name}未升起"
        planet_rise_begin_azimuth, planet_rise_end_azimuth = f"{english_planet_name}未升起", f"{english_planet_name}未升起"
    if planet_set_begin != None and planet_set_end != None:
        planet_set_duration = planet_set_end - planet_set_begin
        planet_set_end_azimuth = get_planet_azimuth(planet_set_end, english_planet_name)
        planet_set_begin_azimuth = get_planet_azimuth(planet_set_begin, english_planet_name)
    if planet_set_begin == None or planet_set_end == None:
        planet_set_begin, planet_set_end, planet_set_duration = f"{english_planet_name}未落下", f"{english_planet_name}未落下", f"{english_planet_name}未落下"
        planet_set_begin_azimuth, planet_set_end_azimuth = f"{english_planet_name}未落下", f"{english_planet_name}未落下"
    false_planet_rise_begin = None
    false_planet_rise_end = None
    false_planet_set_begin = None
    false_planet_set_end = None
    if screen_time(false_planet_rise_begin_a):
        false_planet_rise_begin = false_planet_rise_begin_a
    elif screen_time(false_planet_rise_begin_b):
        false_planet_rise_begin = false_planet_rise_begin_b
    if screen_time(false_planet_set_end_a):
        false_planet_set_end = false_planet_set_end_a
    elif screen_time(false_planet_set_end_b):
        false_planet_set_end = false_planet_set_end_b
    if screen_time(false_planet_rise_end_a):
        false_planet_rise_end = false_planet_rise_end_a
    elif screen_time(false_planet_rise_end_b):
        false_planet_rise_end = false_planet_rise_end_b
    if screen_time(false_planet_set_begin_a):
        false_planet_set_begin = false_planet_set_begin_a
    elif screen_time(false_planet_set_begin_b):
        false_planet_set_begin = false_planet_set_begin_b
    if false_planet_rise_begin != None and false_planet_rise_end != None:
        false_planet_rise_duration = false_planet_rise_end - false_planet_rise_begin
        false_planet_rise_end_azimuth = get_planet_azimuth(false_planet_rise_end, english_planet_name)
        false_planet_rise_begin_azimuth = get_planet_azimuth(false_planet_rise_begin, english_planet_name)
    if false_planet_rise_begin == None or false_planet_rise_end == None:
        false_planet_rise_begin, false_planet_rise_end, false_planet_rise_duration = f"大气折射中的{english_planet_name}未升起", f"大气折射中的{english_planet_name}未升起", f"大气折射中的{english_planet_name}未升起"
        false_planet_rise_begin_azimuth, false_planet_rise_end_azimuth = f"大气折射中的{english_planet_name}未升起", f"大气折射中的{english_planet_name}未升起"
    if false_planet_set_begin != None and false_planet_set_end != None:
        false_planet_set_duration = false_planet_set_end - false_planet_set_begin
        false_planet_set_end_azimuth = get_planet_azimuth(false_planet_set_end, english_planet_name)
        false_planet_set_begin_azimuth = get_planet_azimuth(false_planet_set_begin, english_planet_name)
    if false_planet_set_begin == None or false_planet_set_end == None:
        false_planet_set_begin, false_planet_set_end, false_planet_set_duration = f"大气折射中的{english_planet_name}未落下", f"大气折射中的{english_planet_name}未落下", f"大气折射中的{english_planet_name}未落下"
        false_planet_set_begin_azimuth, false_planet_set_end_azimuth = f"大气折射中的{english_planet_name}未落下", f"大气折射中的{english_planet_name}未落下"
    upper_culmination_a = format_time(hangzhou.previous_transit(planet, start=utc_time))
    upper_culmination_b = format_time(hangzhou.next_transit(planet, start=utc_time))
    lower_culmination_a = format_time(hangzhou.previous_antitransit(planet, start=utc_time))
    lower_culmination_b = format_time(hangzhou.next_antitransit(planet, start=utc_time))
    planet_upper_culmination = None
    planet_lower_culmination = None
    if screen_time(upper_culmination_a):
        planet_upper_culmination = upper_culmination_a
    elif screen_time(upper_culmination_b):
        planet_upper_culmination = upper_culmination_b
    if screen_time(lower_culmination_a):
        planet_lower_culmination = lower_culmination_a
    elif screen_time(lower_culmination_b):
        planet_lower_culmination = lower_culmination_b
    if planet_upper_culmination == None:
        planet_upper_culmination = f"{english_planet_name}未落下"
        planet_upper_culmination_altitude = f"{english_planet_name}未落下"
    else:
        planet_upper_culmination_altitude = get_planet_altitude(planet_upper_culmination, english_planet_name)
    if planet_lower_culmination == None:
        planet_lower_culmination = f"{english_planet_name}未下中天"
        planet_upper_culmination_altitude = f"{english_planet_name}未下中天"
    else:
        planet_lower_culmination_altitude = get_planet_altitude(planet_lower_culmination, english_planet_name)
    infomation = f"""{chinese_planet_name}方位角：{planet_azimuth}
{chinese_planet_name}高度角：{planet_altitude}
{chinese_planet_name}赤纬：{planet_declination}
{chinese_planet_name}赤经：{planet_right_ascension}
{chinese_planet_name}实际赤纬：{planet_astrometric_declination}
{chinese_planet_name}实际赤经：{planet_astrometric_right_ascension}
{chinese_planet_name}地心赤纬：{planet_apparent_declination}
{chinese_planet_name}地心赤经：{planet_apparent_right_ascension}
{chinese_planet_name}黄纬：{ecliptic_planet_declination}
{chinese_planet_name}黄经：{ecliptic_planet_right_ascension}
{chinese_planet_name}实际黄纬：{ecliptic_planet_astrometric_declination}
{chinese_planet_name}实际黄经：{ecliptic_planet_astrometric_right_ascension}
{chinese_planet_name}地心黄纬：{ecliptic_planet_apparent_declination}
{chinese_planet_name}地心黄经：{ecliptic_planet_apparent_right_ascension}
{chinese_planet_name}银纬：{galactic_planet_declination}
{chinese_planet_name}银经：{galactic_planet_right_ascension}
{chinese_planet_name}实际银纬：{galactic_planet_astrometric_declination}
{chinese_planet_name}实际银经：{galactic_planet_astrometric_right_ascension}
{chinese_planet_name}地心银纬：{galactic_planet_apparent_declination}
{chinese_planet_name}地心银经：{galactic_planet_apparent_right_ascension}
{chinese_planet_name}视直径：{planet_angular_diameter}
{chinese_planet_name}视星等：{planet_magnitude}
地球与{chinese_planet_name}距离：{planet_earth_distance}
太阳与{chinese_planet_name}距离：{planet_sun_distance}
{chinese_planet_name}时角：{planet_hour_angle}
{chinese_planet_name}照射范围：{planet_phase}
{chinese_planet_name}距角：{planet_elongation}
{chinese_planet_name}升起开始：{planet_rise_begin}
{chinese_planet_name}升起开始方位角：{planet_rise_begin_azimuth}
{chinese_planet_name}升起结束：{planet_rise_end}
{chinese_planet_name}升起结束方位角：{planet_rise_end_azimuth}
{chinese_planet_name}升起持续时间：{planet_rise_duration}
{chinese_planet_name}落下开始：{planet_set_begin}
{chinese_planet_name}落下开始方位角：{planet_set_begin_azimuth}
{chinese_planet_name}落下结束：{planet_set_end}
{chinese_planet_name}落下结束方位角：{planet_set_end_azimuth}
{chinese_planet_name}落下持续时间：{planet_set_duration}
大气折射中{chinese_planet_name}升起开始：{false_planet_rise_begin}
大气折射中{chinese_planet_name}升起开始方位角：{false_planet_rise_begin_azimuth}
大气折射中{chinese_planet_name}升起结束：{false_planet_rise_end}
大气折射中{chinese_planet_name}升起结束方位角：{false_planet_rise_end_azimuth}
大气折射中{chinese_planet_name}升起持续时间：{false_planet_rise_duration}
大气折射中{chinese_planet_name}落下开始：{false_planet_set_begin}
大气折射中{chinese_planet_name}落下开始方位角：{false_planet_set_begin_azimuth}
大气折射中{chinese_planet_name}落下结束：{false_planet_set_end}
大气折射中{chinese_planet_name}落下结束方位角：{false_planet_set_end_azimuth}
大气折射中{chinese_planet_name}落下持续时间：{false_planet_set_duration}
{chinese_planet_name}上中天：{planet_upper_culmination}
{chinese_planet_name}上中天高度角：{planet_upper_culmination_altitude}
{chinese_planet_name}下中天：{planet_lower_culmination}
{chinese_planet_name}下中天高度角：{planet_lower_culmination_altitude}"""
    return infomation
text = f"""太阳：
太阳方位角：{sun_azimuth}
太阳高度角：{sun_altitude}
太阳赤纬：{sun_declination}
太阳赤经：{sun_right_ascension}
太阳实际赤纬：{sun_astrometric_declination}
太阳实际赤经：{sun_astrometric_right_ascension}
太阳地心赤纬：{sun_apparent_declination}
太阳地心赤经：{sun_apparent_right_ascension}
太阳黄纬：{ecliptic_sun_declination}
太阳黄经：{ecliptic_sun_right_ascension}
太阳实际黄纬：{ecliptic_sun_astrometric_declination}
太阳实际黄经：{ecliptic_sun_astrometric_right_ascension}
太阳地心黄纬：{ecliptic_sun_apparent_declination}
太阳地心黄经：{ecliptic_sun_apparent_right_ascension}
太阳银纬：{galactic_sun_declination}
太阳银经：{galactic_sun_right_ascension}
太阳实际银纬：{galactic_sun_astrometric_declination}
太阳实际银经：{galactic_sun_astrometric_right_ascension}
太阳地心银纬：{galactic_sun_apparent_declination}
太阳地心银经：{galactic_sun_apparent_right_ascension}
太阳视直径：{sun_angular_diameter}
太阳视星等：{sun_magnitude}
影子倍率：{shadow_ratio}
日地距离：{sun_earth_distance}
太阳时角：{sun_hour_angle}
日出开始：{sunrise_begin}
日出开始方位角：{sunrise_begin_azimuth}
日出结束：{sunrise_end}
日出结束方位角：{sunrise_end_azimuth}
日出持续时间：{sunrise_duration}
日落开始：{sunset_begin}
日落开始方位角：{sunset_begin_azimuth}
日落结束：{sunset_end}
日落结束方位角：{sunset_end_azimuth}
日落持续时间：{sunset_duration}
假日出开始：{false_sunrise_begin}
假日出开始方位角：{false_sunrise_begin_azimuth}
假日出结束：{false_sunrise_end}
假日出结束方位角：{false_sunrise_end_azimuth}
假日出持续时间：{false_sunrise_duration}
假日落开始：{false_sunset_begin}
假日落开始方位角：{false_sunset_begin_azimuth}
假日落结束：{false_sunset_end}
假日落结束方位角：{false_sunset_end_azimuth}
假日落持续时间：{false_sunset_duration}
日出黄金时刻开始：{sunrise_golden_hour_begin}
日出黄金时刻开始方位角：{sunrise_golden_hour_begin_azimuth}
日出黄金时刻结束：{sunrise_golden_hour_end}
日出黄金时刻结束方位角：{sunrise_golden_hour_end_azimuth}
日出黄金时刻持续时间：{sunrise_golden_hour_duration}
日落黄金时刻开始：{sunset_golden_hour_begin}
日落黄金时刻开始方位角：{sunset_golden_hour_begin_azimuth}
日落黄金时刻结束：{sunset_golden_hour_end}
日落黄金时刻结束方位角：{sunset_golden_hour_end_azimuth}
日落黄金时刻持续时间：{sunset_golden_hour_duration}
日出蓝调时刻开始：{sunrise_blue_hour_begin}
日出蓝调时刻结束：{sunrise_blue_hour_end}
日出蓝调时刻持续时间：{sunrise_blue_hour_duration}
日落蓝调时刻开始：{sunset_blue_hour_begin}
日落蓝调时刻结束：{sunset_blue_hour_end}
日落蓝调时刻持续时间：{sunset_blue_hour_duration}
日上中天：{sun_upper_culmination}
日上中天高度角：{sun_upper_culmination_altitude}
日下中天：{sun_lower_culmination}
日下中天高度角：{sun_lower_culmination_altitude}
天文晨光始：{astronomical_twilight_begin}
天文晨光持续时间：{morning_astronomical_twilight_duration}
航海晨光始：{nautical_twilight_begin}
航海晨光持续时间：{morning_nautical_twilight_duration}
民用晨光始：{civil_twilight_begin}
民用晨光持续时间：{morning_civil_twilight_duration}
民用昏影终：{civil_twilight_end}
民用昏影持续时间：{evening_civil_twilight_duration}
航海昏影终：{nautical_twilight_end}
航海昏影持续时间：{evening_civil_twilight_duration}
天文昏影终：{astronomical_twilight_end}
天文昏影持续时间：{evening_civil_twilight_duration}
白天长度：{day_duration}
夜晚长度：{night_duration}
黎明长度：{dawn_duration}
黄昏长度：{dusk_duration}

月球：
月球方位角：{moon_azimuth}
月球高度角：{moon_altitude}
月球赤纬：{moon_declination}
月球赤经：{moon_right_ascension}
月球实际赤纬：{moon_astrometric_declination}
月球实际赤经：{moon_astrometric_right_ascension}
月球地心赤纬：{moon_apparent_declination}
月球地心赤经：{moon_apparent_right_ascension}
月球黄纬：{ecliptic_moon_declination}
月球黄经：{ecliptic_moon_right_ascension}
月球实际黄纬：{ecliptic_moon_astrometric_declination}
月球实际黄经：{ecliptic_moon_astrometric_right_ascension}
月球地心黄纬：{ecliptic_moon_apparent_declination}
月球地心黄经：{ecliptic_moon_apparent_right_ascension}
月球银纬：{galactic_moon_declination}
月球银经：{galactic_moon_right_ascension}
月球实际银纬：{galactic_moon_astrometric_declination}
月球实际银经：{galactic_moon_astrometric_right_ascension}
月球地心银纬：{galactic_moon_apparent_declination}
月球地心银经：{galactic_moon_apparent_right_ascension}
月球视直径：{moon_angular_diameter}
月球视星等：{moon_magnitude}
地月距离：{moon_earth_distance}
日月距离：{moon_sun_distance}
月球时角：{moon_hour_angle}
月龄：{moon_age}
月球照射范围：{moon_phase}
月球距角：{moon_elongation}
月出开始：{moonrise_begin}
月出开始方位角：{moonrise_begin_azimuth}
月出结束：{moonrise_end}
月出结束方位角：{moonrise_end_azimuth}
月出持续时间：{moonrise_duration}
月落开始：{moonset_begin}
月落开始方位角：{moonset_begin_azimuth}
月落结束：{moonset_end}
月落结束方位角：{moonset_end_azimuth}
月落持续时间：{moonset_duration}
假月出开始：{false_moonrise_begin}
假月出开始方位角：{false_moonrise_begin_azimuth}
假月出结束：{false_moonrise_end}
假月出结束方位角：{false_moonrise_end_azimuth}
假月出持续时间：{false_moonrise_duration}
假月落开始：{false_moonset_begin}
假月落开始方位角：{false_moonset_begin_azimuth}
假月落结束：{false_moonset_end}
假月落结束方位角：{false_moonset_end_azimuth}
假月落持续时间：{false_moonset_duration}
月上中天：{moon_upper_culmination}
月上中天高度角：{moon_upper_culmination_altitude}
月下中天：{moon_lower_culmination}
月下中天高度角：{moon_lower_culmination_altitude}
上一次新月：{previous_new_moon_time}
下一次新月：{next_new_moon_time}
上一次满月：{previous_full_moon_time}
下一次满月：{next_full_moon_time}
上一次上弦月：{previous_first_quarter_moon_time}
下一次上弦月：{next_first_quarter_moon_time}
上一次下弦月：{previous_last_quarter_moon_time}
下一次下弦月：{next_last_quarter_moon_time}

水星：
{get_planet_infomation("Mercury", "水星")}

金星：
{get_planet_infomation("Venus", "金星")}

火星：
{get_planet_infomation("Mars", "火星")}

木星：
{get_planet_infomation("Jupiter", "木星")}

土星：
{get_planet_infomation("Saturn", "土星")}

天王星：
{get_planet_infomation("Uranus", "天王星")}

海王星：
{get_planet_infomation("Neptune", "海王星")}"""
print(text)
