from skyfield.api import load, wgs84, Star, utc
from skyfield.framelib import ecliptic_frame
from skyfield import almanac
from skyfield.data import hipparcos
import numpy as np
from datetime import datetime, timedelta
import math
import os
from django.conf import settings
import json
from timezonefinder import TimezoneFinder
import pytz
from .synastry_data import SYNASTRY_DATA, get_generic_text

# PLANET CONSTANTS
PLANETS_LIST = [
    'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 
    'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron'
]

SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 
    'Leo', 'Virgo', 'Libra', 'Scorpio', 
    'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

class AstroEngine:
    _instance = None
    _eph = None
    _ts = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AstroEngine, cls).__new__(cls)
            # Lazy load ephemeris
            print("Loading NASA Ephemeris (DE421)...")
            try:
                base_dir = settings.BASE_DIR
                eph_path = os.path.join(base_dir, 'de421.bsp')
                if not os.path.exists(eph_path):
                     # Fallback to current dir if not in settings base
                     eph_path = 'de421.bsp'
                     
                cls._eph = load(eph_path)
                cls._ts = load.timescale()
            except Exception as e:
                print(f"CRITICAL ERROR loading ephemeris: {e}")
                # Don't crash, but methods will fail
        return cls._instance

    @property
    def eph(self):
        return self._eph

    @property
    def ts(self):
        return self._ts

    def calculate_natal(self, date_str, time_str, lat, lon):
        """
        Full Natal Chart Calculation using NASA data + Precise Timezone.
        """
        # Parse Time Input
        dt_str = f"{date_str} {time_str}"
        dt_str = dt_str.replace('-', '/')
        dt = datetime.strptime(dt_str, "%Y/%m/%d %H:%M")
        
        # TIMEZONE CONVERSION (Precise Political Time)
        # 1. Find Timezone Name from Coordinates
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=lon, lat=lat)
        
        if not tz_name:
            # Fallback (Ocean/Unknown) -> Use approximate LMT
            offset_hours = lon / 15.0
            dt_utc = dt - timedelta(hours=offset_hours)
            t = self.ts.from_datetime(dt_utc.replace(tzinfo=utc))
            tz_display = f"LMT (Approx {offset_hours:.1f}h)"
        else:
            # 2. Localize to that Timezone
            local_tz = pytz.timezone(tz_name)
            
            # localize() handles DST history correctly
            # is_dst=None raises error on ambiguous times, False/True forces. 
            # We use standard mix or 'None' if we are sure, but let's assume standard behavior.
            try:
                local_dt = local_tz.localize(dt, is_dst=None) 
            except pytz.AmbiguousTimeError:
                # Fallback for ambiguous overlap -> Assume standard time (False) or summer (True)? 
                # Usually standard is safer.
                local_dt = local_tz.localize(dt, is_dst=False)
            except pytz.NonExistentTimeError:
                # Clock jumped fwd -> Add 1 hour
                local_dt = local_tz.localize(dt + timedelta(hours=1), is_dst=True)

            # 3. Convert to UTC
            dt_utc = local_dt.astimezone(utc)
            t = self.ts.from_datetime(dt_utc)
            tz_display = tz_name
        
        # Observer
        observer = wgs84.latlon(lat, lon)
        
        # 1. Calculate Planet Positions (Ecliptic Longitude)
        earth = self.eph['earth']
        planets_data = []
        
        # Map Skyfield names
        body_map = {
            'Sun': 'sun', 'Moon': 'moon', 'Mercury': 'mercury', 'Venus': 'venus',
            'Mars': 'mars', 'Jupiter': 'jupiter barycenter', 'Saturn': 'saturn barycenter',
            'Uranus': 'uranus barycenter', 'Neptune': 'neptune barycenter', 
            'Pluto': 'pluto barycenter'
        }
        
        for name, key in body_map.items():
            body = self.eph[key]
            astrometric = earth.at(t).observe(body)
            try:
                # IMPORTANT: Use ecliptic_latlon() for 'Ecliptic of Date' (Tropical Zodiac)
                # frame_latlon(ecliptic_frame) uses J2000 which is fixed/sidereal and causes drift.
                p_lat, p_lon, p_dist = astrometric.apparent().ecliptic_latlon()
                deg = p_lon.degrees
                
                sign_idx = int(deg / 30)
                sign_name = SIGNS[sign_idx]
                sign_deg = deg % 30
                
                # CUSP FIX: Override Sun Sign if it mismatches traditional dates (User Request)
                if name == 'Sun':
                    def get_traditional_sign(m, d):
                        dates = [
                            (1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 21, "Pisces"), (4, 20, "Aries"),
                            (5, 21, "Taurus"), (6, 21, "Gemini"), (7, 23, "Cancer"), (8, 23, "Leo"),
                            (9, 23, "Virgo"), (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"),
                            (12, 32, "Capricorn")
                        ]
                        # Find the matching sign
                        # Logic: if date < cutoff, it's prev sign. Else, check next cutoff.
                        # Simplification:
                        # AQ: Jan 20 - Feb 18. (So if Jan 21 -> AQ. If Jan 19 -> Cap)
                        # Let's use the 'Start' dates.
                        # Aries starts March 21.
                        
                        starts = {
                            1: (20, "Aquarius", "Capricorn"),
                            2: (19, "Pisces", "Aquarius"),
                            3: (21, "Aries", "Pisces"),
                            4: (20, "Taurus", "Aries"),
                            5: (21, "Gemini", "Taurus"),
                            6: (21, "Cancer", "Gemini"),
                            7: (23, "Leo", "Cancer"),
                            8: (23, "Virgo", "Leo"),
                            9: (23, "Libra", "Virgo"),
                            10: (23, "Scorpio", "Libra"),
                            11: (22, "Sagittarius", "Scorpio"),
                            12: (22, "Capricorn", "Sagittarius")
                        }
                        
                        cutoff, current, prev = starts[m]
                        if d >= cutoff:
                            return current
                        else:
                            return prev



                    # Use 'dt' which is already parsed from input (Local Time)
                    # This matches the user's calendar expectation
                    trad_sign = get_traditional_sign(dt.month, dt.day)
                    
                    # If mismatch and within 1.5 degrees (Cusp), enforce traditional
                    if sign_name != trad_sign:
                        # Check distance
                        # If Calc=Aries (0.5), Trad=Pisces. Mismatch!
                        # Verify we are indeed close to border to avoid huge errors
                        is_cusp = (sign_deg < 2.0) or (sign_deg > 28.0)
                        if is_cusp:
                            sign_name = trad_sign
                            # Adjust degree for display?
                            # If we went back to Pisces, we should ideally show 29.9
                            if sign_deg < 2.0: sign_deg = 29.9 # Wrapped back
                            elif sign_deg > 28.0: sign_deg = 0.1 # Wrapped forward
                
                planets_data.append({
                    'name': name,
                    'lon': deg,
                    'sign': sign_name,
                    'sign_lon': sign_deg,
                    'speed': 1.0 # Todo: calculate speed for retro detection
                })
            except Exception as e:
                print(f"Error calc {name}: {e}")

        # 2. Calculate Ascendant (Approximate)
        # AC formula: tan(AC) = cos(LST) / -(sin(LST) * sin(obl) + tan(lat) * cos(obl))
        # This is complex in pure python without proper matrix libs, 
        # So we will use the *Position of the Horizon* relative to Ecliptic.
        # Alternative: Use Whole Sign from Sun if calc fails, but let's try a simple Ascendant logic.
        
        # Simplified Ascendants are notoriously hard. 
        # Strategy: Use local siderial time to find the rising degree.
        # For this demo, we might fallback to Sun=1st House if math fails, 
        # but let's assume we use 'Aries' rising as default if we can't implement the math perfectly here.
        # IMPROVEMENT: Use the 'Sun Rise' method or similar libraries if available.
        # For robustness in this MVP step, we will use a Mock Ascendant based on time-of-day offset from Sun
        # This is a heuristic: Sun is at MC at noon, at AC at sunrise (6am).
        
        # 2. Precise Ascendant Calculation
        # Formula: tan(AC) = -cos(LST) / (sin(LST)*cos(Eps) + tan(Lat)*sin(Eps))
        try:
            # A. Get Sidereal Time
            # Skyfield t includes UT1 if we loaded standard timescale, giving GAST 
            gast = t.gast # Greenwich Apparent Sidereal Time in hours
            
            # Convert to degrees (1 hr = 15 deg)
            gast_deg = gast * 15.0
            
            # Local Sidereal Time = GAST + Longitude
            lst_deg = (gast_deg + lon) % 360
            
            # Convert to Rad
            lst_rad = math.radians(lst_deg)
            lat_rad = math.radians(lat)
            eps_rad = math.radians(23.4392911) # Obliquity of Ecliptic (approx J2000)

            # B. Apply Formula
            # Standard Formula: tan(AC) = cos(LST) / - (sin(LST)*cos(Eps) + tan(Lat)*sin(Eps))
            # y = cos(LST)
            # x = - (sin(LST)*cos(Eps) + tan(Lat)*sin(Eps))
            # AC = atan2(y, x)
            
            num = math.cos(lst_rad)
            den = - ((math.sin(lst_rad) * math.cos(eps_rad)) + (math.tan(lat_rad) * math.sin(eps_rad)))
            
            ac_rad = math.atan2(num, den)
            ac_deg = math.degrees(ac_rad)
            
            # Normalize to 0-360
            ac_deg = ac_deg % 360
            
            # C. Calculate MC (Midheaven)
            # Formula: tan(MC) = tan(LST) / cos(Eps) -> atan2(sin(lst), cos(lst)*cos(eps))
            mc_rad = math.atan2(math.sin(lst_rad), math.cos(lst_rad) * math.cos(eps_rad))
            mc_deg = math.degrees(mc_rad) % 360

            # Determine Sign
            asc_idx = int(ac_deg / 30)
            asc_sign = SIGNS[asc_idx]
            
        except Exception as e:
            print(f"ASC Calculation Failed: {e}")
            asc_sign = "Aries" # Fallback only on math failure
            ac_deg = 0.0
            mc_deg = 0.0

        
        # HOUSES (Whole Sign)
        sign_map = {s: i for i, s in enumerate(SIGNS)}
        asc_idx = sign_map.get(asc_sign, 0)
        
        houses = []
        for i in range(12):
            idx = (asc_idx + i) % 12
            houses.append({
                'house': i + 1,
                'sign': SIGNS[idx],
                'lon': idx * 30.0
            })
            
        # Assign Houses to Planets
        for p in planets_data:
            p_sign_idx = sign_map[p['sign']]
            # Whole Sign House: (PlanetSign - AscSign) + 1
            h = (p_sign_idx - asc_idx) % 12 + 1
            if h <= 0: h += 12
            p['house'] = h
            
        # 2. Node Calc
        node_lon = self.calculate_mean_node(t)
        planets_data.append({
             'name': 'North Node', 'lon': node_lon,
             'sign': SIGNS[int(node_lon/30)], 'sign_lon': node_lon%30, 'house': 1 # approximate
        })
        
        return {
            'planets': planets_data,
            'houses': houses,
            'ascendant': asc_sign,
            'ascendant_deg': ac_deg,
            'midheaven_deg': mc_deg,
            'north_node': node_lon,
            'utc_time': t.utc_strftime('%Y-%m-%d %H:%M:%S'),
            'timezone': tz_display
        }

    def calculate_angles_light(self, t, lat, lon):
        """
        Fast calculation of only Ascendant and MC.
        Bypasses planet calculations for Rectification loops.
        """
        try:
             # A. Get Sidereal Time
            gast = t.gast
            gast_deg = gast * 15.0
            lst_deg = (gast_deg + lon) % 360
            lst_rad = math.radians(lst_deg)
            lat_rad = math.radians(lat)
            eps_rad = math.radians(23.4392911) 

            # B. Ascendant
            num = math.cos(lst_rad)
            den = - ((math.sin(lst_rad) * math.cos(eps_rad)) + (math.tan(lat_rad) * math.sin(eps_rad)))
            ac_rad = math.atan2(num, den)
            ac_deg = math.degrees(ac_rad) % 360
            
            # C. MC
            mc_rad = math.atan2(math.sin(lst_rad), math.cos(lst_rad) * math.cos(eps_rad))
            mc_deg = math.degrees(mc_rad) % 360
            
            # Sign
            asc_idx = int(ac_deg / 30)
            asc_sign = SIGNS[asc_idx]
            
            return {
                'ascendant_deg': ac_deg,
                'midheaven_deg': mc_deg,
                'ascendant': asc_sign
            }
        except Exception as e:
            return {'ascendant_deg': 0, 'midheaven_deg': 0, 'ascendant': 'Aries'}

    def calculate_mean_node(self, t):
        """Calculates Mean North Node Lon."""
        jd = t.tt
        t_cen = (jd - 2451545.0) / 36525.0
        mn = 125.04452 - 1934.136261 * t_cen
        mn = mn % 360.0
        if mn < 0: mn += 360.0
        return mn

    def calculate_draconic(self, natal_planets, node_lon):
        """Draconic = Tropical - Node."""
        draconic = []
        for p in natal_planets:
            if p['name'] == 'North Node': continue
            d_lon = (p['lon'] - node_lon) % 360
            if d_lon < 0: d_lon += 360
            s_idx = int(d_lon / 30)
            draconic.append({
                'name': p['name'], 'lon': d_lon,
                'sign': SIGNS[s_idx], 'sign_lon': d_lon % 30
            })
        return draconic

    def calculate_aspects(self, planets_data):
        aspects = []
        orbs = {'Conjunction': 8, 'Opposition': 8, 'Square': 8, 'Trine': 8, 'Sextile': 6}
        
        for i in range(len(planets_data)):
            for j in range(i + 1, len(planets_data)):
                p1 = planets_data[i]
                p2 = planets_data[j]
                
                diff = abs(p1['lon'] - p2['lon']) % 360
                if diff > 180: diff = 360 - diff
                
                type = None
                if diff <= orbs['Conjunction']: type = 'Conjunction'
                elif abs(diff - 180) <= orbs['Opposition']: type = 'Opposition'
                elif abs(diff - 120) <= orbs['Trine']: type = 'Trine'
                elif abs(diff - 90) <= orbs['Square']: type = 'Square'
                elif abs(diff - 60) <= orbs['Sextile']: type = 'Sextile'
                
                if type:
                    aspects.append({
                        'p1': p1['name'],
                        'p2': p2['name'],
                        'type': type,
                        'orb': round(diff if type=='Conjunction' else abs(diff - {'Opposition':180,'Trine':120,'Square':90,'Sextile':60}[type]), 1)
                    })
        return aspects

    def calculate_synastry(self, p1_list, p2_list, lang='en'):
        score = 50.0 # Base
        aspects_found = []
        
        # Reduced Orbs for Synastry
        orbs = {'Conjunction': 8, 'Opposition': 8, 'Square': 7, 'Trine': 8, 'Sextile': 5}
        weights = {'Conjunction': 10, 'Trine': 8, 'Sextile': 5, 'Opposition': -8, 'Square': -10}
        
        # Romantic Pairs
        romance_pairs = [('Sun', 'Moon'), ('Venus', 'Mars'), ('Moon', 'Moon'), ('Venus', 'Venus'), ('Venus', 'Sun')]
        
        # Deep Analysis Dictionary
        analysis_structure = {
            'Soul Connection': [], # Conjunctions/Trines involving Sun/Moon/Nodes
            'Attraction': [], # Venus/Mars contacts
            'Communication': [], # Mercury contacts
            'Challenges': [] # Saturn/Mars Squares
        }

        for p1 in p1_list:
            for p2 in p2_list:
                # Calculate diff
                diff = abs(p1['lon'] - p2['lon']) % 360
                if diff > 180: diff = 360 - diff
                
                aspect = None
                type_category = "Neutral"
                
                if diff <= orbs['Conjunction']: aspect = 'Conjunction'; type_category = "Harmony"
                elif abs(diff - 120) <= orbs['Trine']: aspect = 'Trine'; type_category = "Harmony"
                elif abs(diff - 60) <= orbs['Sextile']: aspect = 'Sextile'; type_category = "Harmony"
                elif abs(diff - 180) <= orbs['Opposition']: aspect = 'Opposition'; type_category = "Tension"
                elif abs(diff - 90) <= orbs['Square']: aspect = 'Square'; type_category = "Conflict"
                
                if aspect:
                    weight = weights.get(aspect, 0)
                    is_romance = (p1['name'], p2['name']) in romance_pairs or (p2['name'], p1['name']) in romance_pairs
                    
                    if is_romance and weight > 0: weight *= 1.8 # Intense love boost
                    
                    score += weight
                    
                    # Formatting Theme
                    theme = "General"
                    if 'Venus' in [p1['name'], p2['name']] or 'Mars' in [p1['name'], p2['name']]: theme = "Attraction"
                    if 'Mercury' in [p1['name'], p2['name']]: theme = "Communication"
                    if 'Saturn' in [p1['name'], p2['name']] and aspect in ['Square', 'Opposition']: theme = "Karmic Lesson"
                    if 'Jupiter' in [p1['name'], p2['name']] and aspect in ['Trine', 'Conjunction']: theme = "Growth"
                    if 'Moon' in [p1['name'], p2['name']]: theme = "Emotional"
                    
                    # Interpretation Lookup
                    # Sort planets alphabetically to match key format
                    sorted_planets = sorted([p1['name'], p2['name']])
                    key = f"{sorted_planets[0]}_{sorted_planets[1]}_{aspect}"
                    
                    interp_text = ""
                    if lang in SYNASTRY_DATA and key in SYNASTRY_DATA[lang]:
                        interp_text = SYNASTRY_DATA[lang][key]
                    else:
                        interp_text = get_generic_text(p1['name'], p2['name'], aspect, lang)

                    # Store Rich Data
                    aspect_data = {
                        'p1': p1['name'], 'p2': p2['name'],
                        'type': aspect,
                        'category': type_category,
                        'theme': theme,
                        'is_romance': is_romance,
                        'interpretation': interp_text
                    }
                    aspects_found.append(aspect_data)

        # Element Compatibility (Bonus)
        # Simplified: Check Sun Sign Element
        # ... logic skipped for brevity, focused on aspects ...

        # Normalize score 0-100
        score = max(10, min(99, score))
        
        return {
            'score': int(score),
            'aspects': aspects_found
        }

    def calculate_dominants(self, planets):
         # Element counting
         elements = {'Fire': 0, 'Earth': 0, 'Air': 0, 'Water': 0}
         sign_elements = {
             'Aries': 'Fire', 'Leo': 'Fire', 'Sagittarius': 'Fire',
             'Taurus': 'Earth', 'Virgo': 'Earth', 'Capricorn': 'Earth',
             'Gemini': 'Air', 'Libra': 'Air', 'Aquarius': 'Air',
             'Cancer': 'Water', 'Scorpio': 'Water', 'Pisces': 'Water'
         }
         # Weighted: Sun/Moon/Asc get more points
         weights = {'Sun': 3, 'Moon': 3, 'Ascendant': 3, 'Venus': 2, 'Mars': 2}
         
         for p in planets:
             el = sign_elements.get(p['sign'], 'Fire')
             w = weights.get(p['name'], 1)
             elements[el] += w
             
         return elements

    def calculate_planetary_hours(self, date_str, lat, lon):
        try:
            # 1. Parse Date & Location
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            t0 = self._ts.utc(dt.year, dt.month, dt.day, 0, 0, 0)
            t1 = self._ts.utc(dt.year, dt.month, dt.day, 23, 59, 59)
            
            # 2. Calculate Sunrise/Sunset
            location = wgs84.latlon(lat, lon)
            f = almanac.sunrise_sunset(self._eph, location)
            
            # Search window
            search_start = self._ts.utc(dt.year, dt.month, dt.day, 3, 0)
            search_end = self._ts.utc(dt.year, dt.month, dt.day + 1, 12, 0)
            
            t_ev, ev_codes = almanac.find_discrete(search_start, search_end, f)
            
            sr_today = None
            ss_today = None
            sr_tomorrow = None
            
            for t, code in zip(t_ev, ev_codes):
                # Almanac: True(1)=Up (Rise), False(0)=Down (Set)
                if code == 1: 
                    if sr_today is None: sr_today = t
                    else: sr_tomorrow = t; break
                elif code == 0:
                    if ss_today is None: ss_today = t
            
            # Fallback
            if not sr_today or not ss_today or not sr_tomorrow:
                sr_today = self._ts.utc(dt.year, dt.month, dt.day, 6, 0)
                ss_today = self._ts.utc(dt.year, dt.month, dt.day, 18, 0)
                sr_tomorrow = self._ts.utc(dt.year, dt.month, dt.day + 1, 6, 0)

            # 3. Intervals
            day_len = ss_today - sr_today
            night_len = sr_tomorrow - ss_today
            day_step = day_len / 12.0
            night_step = night_len / 12.0
            
            # 4. Rulers (Chaldean Descending: Sat, Jup, Mar, Sun, Ven, Mer, Moo)
            chaldean = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon']
            
            # Day Ruler (0=Mon(Moon)... 6=Sun(Sun))
            # Rulers: Mon:Moon, Tue:Mars, Wed:Merc, Thu:Jup, Fri:Ven, Sat:Sat, Sun:Sun
            weekday_rulers = {0:'Moon', 1:'Mars', 2:'Mercury', 3:'Jupiter', 4:'Venus', 5:'Saturn', 6:'Sun'}
            first_ruler = weekday_rulers[dt.weekday()]
            start_idx = chaldean.index(first_ruler)
            
            hours = []
            
            # Day Hours
            curr = sr_today
            for i in range(12):
                ruler = chaldean[(start_idx + i) % 7]
                nxt = self._ts.tt_jd(curr.tt + day_step)
                
                # Apply UTC+3 for display
                s_local = curr.utc_datetime() + timedelta(hours=3)
                e_local = nxt.utc_datetime() + timedelta(hours=3)
                
                hours.append({
                    'start': s_local.strftime("%H:%M"),
                    'end': e_local.strftime("%H:%M"),
                    'planet': ruler, # Renamed from ruler to planet for frontend consistency
                    'type': 'Day'
                })
                curr = nxt
                
            # Night Hours
            curr = ss_today
            for i in range(12):
                ruler = chaldean[(start_idx + 12 + i) % 7]
                nxt = self._ts.tt_jd(curr.tt + night_step)
                
                s_local = curr.utc_datetime() + timedelta(hours=3)
                e_local = nxt.utc_datetime() + timedelta(hours=3)
                
                hours.append({
                    'start': s_local.strftime("%H:%M"),
                    'end': e_local.strftime("%H:%M"),
                    'planet': ruler, # Renamed from ruler to planet
                    'type': 'Night'
                })
                curr = nxt

            return hours

        except Exception as e:
            print(f"Error calculating hours: {e}")
            return []

    def calculate_career(self, natal_data):
        """
        Generates a detailed career analysis based on MC (10th House), Saturn, and North Node.
        """
        try:
            # Load Data
            base_dir = settings.BASE_DIR
            data_path = os.path.join(base_dir, 'data', 'career_interpretations.json')
            if not os.path.exists(data_path):
                 # Fallback
                 data_path = os.path.join(os.path.dirname(__file__), '../../data/career_interpretations.json')

            with open(data_path, 'r', encoding='utf-8') as f:
                career_db = json.load(f)

            # 1. Identify Key Indicators
            # MC (Midheaven) - logic: Use 10th House Sign
            houses = natal_data.get('houses', [])
            mc_house = next((h for h in houses if h['house'] == 10), None)
            mc_sign = mc_house['sign'] if mc_house else 'Aries'

            # Saturn
            planets = natal_data.get('planets', [])
            saturn = next((p for p in planets if p['name'] == 'Saturn'), None)
            saturn_sign = saturn['sign'] if saturn else 'Capricorn'
            
            # Saturn Element
            elements = {
                'Fire': ['Aries', 'Leo', 'Sagittarius'],
                'Earth': ['Taurus', 'Virgo', 'Capricorn'],
                'Air': ['Gemini', 'Libra', 'Aquarius'],
                'Water': ['Cancer', 'Scorpio', 'Pisces']
            }
            saturn_element = 'earth'
            for elem, signs in elements.items():
                if saturn_sign in signs:
                    saturn_element = elem.lower()
                    break

            # 2. Construct Analysis
            # MC Text
            mc_text = career_db['mc'].get(mc_sign, career_db['mc']['Aries'])

            # Saturn Text
            saturn_text = career_db['saturn'].get(saturn_element, career_db['saturn']['earth'])

            # Monthly Forecast (DYNAMIC TRANSIT LOGIC)
            # We calculate where Jupiter and Saturn are RIGHT NOW and how they impact the user's chart.
            
            # 1. Get Current Date Transits
            now = datetime.now()
            t_now = self.ts.now()
            
            # 2. Get Positions of Transit Jupiter & Saturn
            planets_map = {
                'Jupiter': self.eph['jupiter barycenter'],
                'Saturn': self.eph['saturn barycenter']
            }
            earth = self.eph['earth']
            
            transit_impacts = []
            
            # Natal Points to check against (MC Lon, Saturn Lon)
            # We need MC Longitude. Currently we only have sign. 
            # Let's approximate MC Lon from the House 10 Lon if available, or just use Sign center.
            mc_house_data = next((h for h in houses if h['house'] == 10), None)
            mc_lon = mc_house_data['lon'] if mc_house_data else 0 # Fallback
            
            natal_saturn_lon = saturn['lon'] if saturn else 0
            
            # Check Transits
            for p_name, p_body in planets_map.items():
                astrometric = earth.at(t_now).observe(p_body)
                _, lon, _ = astrometric.apparent().frame_latlon(ecliptic_frame)
                t_lon = lon.degrees
                
                # Check Aspect to Natal MC (Career Point)
                diff_mc = abs(t_lon - mc_lon) % 360
                if diff_mc > 180: diff_mc = 360 - diff_mc
                
                aspect = ""
                if diff_mc < 10: aspect = "Conjunction" # On top of career
                elif abs(diff_mc - 120) < 10: aspect = "Trine" # Good flow
                elif abs(diff_mc - 90) < 10: aspect = "Square" # Tension/Hard work
                elif abs(diff_mc - 180) < 10: aspect = "Opposition" # Full awareness/Balance
                
                if aspect:
                    transit_impacts.append({'planet': p_name, 'target': 'Midheaven', 'aspect': aspect})
                    
                # Check Aspect to Natal Saturn (Discipline)
                diff_sat = abs(t_lon - natal_saturn_lon) % 360
                if diff_sat > 180: diff_sat = 360 - diff_sat
                
                if diff_sat < 10: 
                    transit_impacts.append({'planet': p_name, 'target': 'Natal Saturn', 'aspect': 'Conjunction'})

            # 3. Generate Dynamic Text from Impacts
            forecast_en = ""
            forecast_tr = ""
            
            if not transit_impacts:
                # No major heavy transit -> Standard Phase
                forecast_en = f"The heavy planets are currently moving through neutral territory in relation to your career chart. This is a time of 'Business as Usual', ideal for maintaining steady progress and sticking to your long-term plans without major disruptions."
                forecast_tr = f"Ağır gezegenler şu anda kariyer haritanızla ilgili nötr bir bölgeden geçiyor. Bu, 'Her Şey Yolunda' dönemidir; büyük aksamalar olmadan istikrarlı ilerlemeyi sürdürmek ve uzun vadeli planlarınıza sadık kalmak için idealdir."
            else:
                # Generate sentence based on first major impact
                imp = transit_impacts[0]
                p = imp['planet']
                a = imp['aspect']
                t = imp['target']
                
                # Logic text generator
                if p == 'Jupiter':
                    if a in ['Conjunction', 'Trine']:
                        forecast_en = "Jupiter is blessing your career sector! Expect growth, promotions, or new opportunities. It's time to expand."
                        forecast_tr = "Jüpiter kariyer sektörünüzü kutsuyor! Büyüme, terfi veya yeni fırsatlar bekleyin. Genişleme zamanı."
                    else:
                        forecast_en = "Jupiter is challenging your career path. You may want to overexpand or take risks. Be optimistic but careful."
                        forecast_tr = "Jüpiter kariyer yolunuzu zorluyor. Aşırı büyümek veya risk almak isteyebilirsiniz. İyimser ama dikkatli olun."
                elif p == 'Saturn':
                     if a in ['Conjunction', 'Trine']:
                        forecast_en = "Saturn is solidifying your position. Hard work brings tangible, long-lasting rewards now. Responsibility increases."
                        forecast_tr = "Satürn pozisyonunuzu sağlamlaştırıyor. Sıkı çalışma şimdi somut, uzun vadeli ödüller getiriyor. Sorumluluk artıyor."
                     else:
                        forecast_en = "Saturn is testing your foundations. You may feel restricted or overworked. It's a test of endurance; do not give up."
                        forecast_tr = "Satürn temellerinizi sınıyor. Kısıtlanmış veya çok çalışmış hissedebilirsiniz. Bu bir dayanıklılık testi; pes etmeyin."

            return {
                'mc_sign': mc_sign,
                'saturn_sign': saturn_sign,
                'analysis': {
                    'en': f"<h3>The Pillar of Public Status: Midheaven in {mc_sign}</h3><p>{mc_text['en']}</p><br><h3>The Discipline of Saturn</h3><p>{saturn_text['en']}</p><br><h3>Dynamic Cosmic Forecast ({now.strftime('%B %Y')})</h3><p>{forecast_en}</p>",
                    'tr': f"<h3>Kamu Statüsünün Sütunu: {mc_sign} Burcundaki Tepe Noktası</h3><p>{mc_text['tr']}</p><br><h3>Satürn Disiplini</h3><p>{saturn_text['tr']}</p><br><h3>Dinamik Kozmik Tahmin ({now.strftime('%B %Y')})</h3><p>{forecast_tr}</p>"
                }
            }

        except Exception as e:
            print(f"Career Calc Error: {e}")
            return {'analysis': {'en': "Data unavailable.", 'tr': "Veri mevcut değil."}}

