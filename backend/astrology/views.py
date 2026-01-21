from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import random
from .engine import AstroEngine
import datetime
from datetime import datetime as dt
import geonamescache
from .tarot_data import tarot_deck
from .horoscope_data import SENTENCES, SIGNS_TR, SIGNS_EN
from django.db.models import Q
from .models import PlanetInterpretation, AspectInterpretation, DailyTip, DailyHoroscope, UserProfile, UserActivityLog
from django.db.models import Count, Max, Min
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Try to import flatlib, handle error if not installed
try:
    from flatlib.datetime import Datetime
    from flatlib.geopos import GeoPos
    from flatlib.chart import Chart
    from flatlib import const
    FLATLIB_AVAILABLE = True
except ImportError:
    FLATLIB_AVAILABLE = False

@csrf_exempt
def calculate_chart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=405)

    try:
        data = json.loads(request.body)
        date_str = data.get('date').replace('-', '/') if data.get('date') else None 
        time_str = data.get('time') 
        lat = float(data.get('lat', 41.0))
        lon = float(data.get('lon', 28.0))
        lang = data.get('lang', 'en') 
        
        # Initialize NASA Engine
        engine = AstroEngine()
        
        # 1. Main Calculation (Skyfield)
        natal_data = engine.calculate_natal(date_str, time_str, lat, lon)
        
        # 2. Enrich with Interpretations (Smart Generator)
        # We use a generative approach to ensure rich, long descriptions without massive DB seeding
        
        # Archetypes (Data could be moved to a separate file, but kept here for stability)
        ARCHETYPES = {
            'en': {
                'Sun': "The Sun represents your ego, core identity, and life force. It is the 'Hero' within you.",
                'Moon': "The Moon governs your emotions, instincts, and the subconscious. It represents your inner world.",
                'Mercury': "Mercury rules communication, intellect, and how you process information.",
                'Venus': "Venus is the planet of love, beauty, values, and how you attract relationships.",
                'Mars': "Mars represents your drive, action, passion, and how you assert yourself.",
                'Jupiter': "Jupiter is the seeker of expansion, luck, philosophy, and abundance.",
                'Saturn': "Saturn represents discipline, structure, karma, and life's hard lessons.",
                'Uranus': "Uranus acts as the awakener, ruling innovation, rebellion, and sudden change.",
                'Neptune': "Neptune involves dreams, intuition, illusion, and spiritual transcendence.",
                'Pluto': "Pluto governs transformation, power, regeneration, and the cycle of rebirth.",
                'North Node': "The North Node points to your karmic destiny and the qualities you must develop."
            },
            'tr': {
                'Sun': "Güneş, egonuzu, temel kimliğinizi ve yaşam gücünüzü temsil eder. O, içinizdeki 'Kahraman'dır.",
                'Moon': "Ay, duygularınızı, içgüdülerinizi ve bilinçaltınızı yönetir. İç dünyanızın aynasıdır.",
                'Mercury': "Merkür, iletişimi, zekayı ve bilgiyi nasıl işlediğinizi yönetir.",
                'Venus': "Venüs aşkın, güzelliğin, değerlerin ve ilişkileri nasıl çektiğinizin gezegenidir.",
                'Mars': "Mars, dürtülerinizi, eylemlerinizi, tutkunuzu ve kendinizi nasıl ortaya koyduğunuzu temsil eder.",
                'Jupiter': "Jüpiter, genişlemenin, şansın, felsefenin ve bolluğun arayıcısıdır.",
                'Saturn': "Satürn, disiplini, yapıyı, karmayı ve hayatın zorlu derslerini temsil eder.",
                'Uranus': "Uranüs, yeniliği, isyanı ve ani değişimleri yöneten uyanışçıdır.",
                'Neptune': "Neptün hayalleri, sezgiyi, illüzyonu ve ruhsal aşkınlığı içerir.",
                'Pluto': "Plüton, dönüşümü, gücü, yenilenmeyi ve yeniden doğuş döngüsünü yönetir.",
                'North Node': "Kuzey Ay Düğümü, karmik kaderinizi ve bu hayatta geliştirmeniz gereken nitelikleri işaret eder."
            }
        }

        SIGNS_MEANING = {
            'en': {
                'Aries': "In Aries, this energy is expressed impulsively, dynamically, and with great courage. You take initiative and lead with fire.",
                'Taurus': "In Taurus, this energy is grounded, seeking stability, comfort, and tangible results. You move with deliberate patience.",
                'Gemini': "In Gemini, this energy manifests through curiosity, adaptability, and social connection. You thrive on variety and intellect.",
                'Cancer': "In Cancer, this energy is filtered through deep emotion, protection, and nurturing sensitivity. You value security above all.",
                'Leo': "In Leo, this energy shines dramatically. You express it with warmth, creativity, and a need for recognition or applause.",
                'Virgo': "In Virgo, this energy is analytical and service-oriented. You seek perfection, order, and practical utility in this area.",
                'Libra': "In Libra, this energy seeks balance, harmony, and relationship. You express it through diplomacy and an aesthetic eye.",
                'Scorpio': "In Scorpio, this energy is intense, magnetic, and transformative. You seek depth and are not afraid of the shadows.",
                'Sagittarius': "In Sagittarius, this energy is adventurous and philosophical. You express it through a quest for truth and freedom.",
                'Capricorn': "In Capricorn, this energy is disciplined and ambitious. You express it through hard work, structure, and long-term goals.",
                'Aquarius': "In Aquarius, this energy is unconventional and innovative. You express it through rebellion against the norm and humanitarian ideals.",
                'Pisces': "In Pisces, this energy is compassionate and mystical. You express it through boundaries mental expansion and spiritual connection."
            },
            'tr': {
                'Aries': "Koç burcunda bu enerji dürtüsel, dinamik ve büyük bir cesaretle ifade edilir. İnisiyatif alır ve ateşle liderlik edersiniz.",
                'Taurus': "Boğa burcunda bu enerji topraklanmıştır; istikrar, konfor ve somut sonuçlar arar. Kasıtlı bir sabırla hareket edersiniz.",
                'Gemini': "İkizler burcunda bu enerji merak, uyum yeteneği ve sosyal bağlantı yoluyla tezahür eder. Çeşitlilik ve zeka ile beslenirsiniz.",
                'Cancer': "Yengeç burcunda bu enerji derin duygu, koruma ve besleyici hassasiyetle filtrelenir. Güvenliğe her şeyden çok değer verirsiniz.",
                'Leo': "Aslan burcunda bu enerji dramatik bir şekilde parlar. Onu sıcaklık, yaratıcılık ve takdir edilme ihtiyacıyla ifade edersiniz.",
                'Virgo': "Başak burcunda bu enerji analitik ve hizmet odaklıdır. Bu alanda mükemmellik, düzen ve pratik yarar ararsınız.",
                'Libra': "Terazi burcunda bu enerji denge, uyum ve ilişki arar. Onu diplomasi ve estetik bir gözle ifade edersiniz.",
                'Scorpio': "Akrep burcunda bu enerji yoğun, manyetik ve dönüştürücüdür. Derinlik ararsınız ve gölgelerden korkmazsınız.",
                'Sagittarius': "Yay burcunda bu enerji maceracı ve felsefidir. Onu hakikat ve özgürlük arayışıyla ifade edersiniz.",
                'Capricorn': "Oğlak burcunda bu enerji disiplinli ve hırslıdır. Onu çok çalışmak, yapı kurmak ve uzun vadeli hedeflerle ifade edersiniz.",
                'Aquarius': "Kova burcunda bu enerji gelenek dışı ve yenilikçidir. Onu norma isyan ve insani ideallerle ifade edersiniz.",
                'Pisces': "Balık burcunda bu enerji şefkatli ve mistiktir. Onu sınırsız zihinsel genişleme ve ruhsal bağlantı ile ifade edersiniz."
            }
        }

        # Sign Translations for Synthesis
        SIGN_NAMES_TR = {
            'Aries': 'Koç', 'Taurus': 'Boğa', 'Gemini': 'İkizler', 'Cancer': 'Yengeç',
            'Leo': 'Aslan', 'Virgo': 'Başak', 'Libra': 'Terazi', 'Scorpio': 'Akrep',
            'Sagittarius': 'Yay', 'Capricorn': 'Oğlak', 'Aquarius': 'Kova', 'Pisces': 'Balık'
        }

        planets_enriched = []
        for p in natal_data['planets']:
            # Generate English
            base_en = ARCHETYPES['en'].get(p['name'], "")
            mod_en = SIGNS_MEANING['en'].get(p['sign'], "")
            synth_en = f"{base_en} {mod_en} This placement suggests that this aspect of your personality is colored by the qualities of {p['sign']}."
            
            # Generate Turkish
            base_tr = ARCHETYPES['tr'].get(p['name'], "")
            mod_tr = SIGNS_MEANING['tr'].get(p['sign'], "")
            sign_tr = SIGN_NAMES_TR.get(p['sign'], p['sign'])
            synth_tr = f"{base_tr} {mod_tr} Bu yerleşim, karakterinizin bu yönünün {sign_tr} burcunun özellikleriyle şekillendiğini gösterir."

            # Store both
            p['interpretations'] = {
                'en': synth_en,
                'tr': synth_tr
            }
            # Fallback for old API consumers
            p['interpretation'] = synth_tr if lang == 'tr' else synth_en
            
            planets_enriched.append(p)
            
        # 3. Aspects
        aspects_raw = engine.calculate_aspects(planets_enriched)
        aspects_enriched = []
        from .models import AspectInterpretation
        
        for a in aspects_raw:
             interp = AspectInterpretation.objects.filter(
                Q(planet_1=a['p1'], planet_2=a['p2'], aspect_type=a['type']) |
                Q(planet_1=a['p2'], planet_2=a['p1'], aspect_type=a['type'])
             ).first()
             
             text = getattr(interp, f'text_{lang}', f"{a['type']} aspect") if interp else f"{a['p1']} {a['type']} {a['p2']}"
             
             aspects_enriched.append({
                 "p1": a['p1'], "p2": a['p2'], "type": a['type'],
                 "orb": a['orb'], "interpretation": text
             })

        # 4. Advanced Metrics
        birth_year = int(date_str.split('/')[0])
        current_year = datetime.now().year
        
        # Profection (Simple Modulo)
        profection = (current_year - birth_year) % 12 + 1
        
        # Dominants
        dominants = engine.calculate_dominants(planets_enriched)
        
        # Lucky Gem
        sun_sign = next((p['sign'] for p in planets_enriched if p['name'] == 'Sun'), 'Aries')
        # We can implement get_lucky_gems in engine or here. 
        # Engine has it? No, I removed it in replacement. Let's add simple dict here.
        gems = {
            'Aries': {'color': 'Red', 'stone': 'Ruby'}, 'Taurus': {'color': 'Green', 'stone': 'Emerald'},
            'Gemini': {'color': 'Yellow', 'stone': 'Agate'}, 'Cancer': {'color': 'Silver', 'stone': 'Moonstone'},
            'Leo': {'color': 'Gold', 'stone': 'Peridot'}, 'Virgo': {'color': 'Navy', 'stone': 'Sapphire'},
            'Libra': {'color': 'Blue', 'stone': 'Opal'}, 'Scorpio': {'color': 'Black', 'stone': 'Topaz'},
            'Sagittarius': {'color': 'Purple', 'stone': 'Turquoise'}, 'Capricorn': {'color': 'Brown', 'stone': 'Garnet'},
            'Aquarius': {'color': 'Cyan', 'stone': 'Amethyst'}, 'Pisces': {'color': 'Sea Green', 'stone': 'Aquamarine'}
        }
        lucky = gems.get(sun_sign, {'color': 'White', 'stone': 'Diamond'})
        
        # Draconic Calculation & Enrichment
        draconic_data = engine.calculate_draconic(natal_data['planets'], natal_data['north_node'])
        draconic_enriched = []
        for p in draconic_data:
            # English
            base_en = ARCHETYPES['en'].get(p['name'], "")
            mod_en = SIGNS_MEANING['en'].get(p['sign'], "")
            synth_en = f"In your Draconic Soul Chart: {base_en} {mod_en} This indicates your higher self's intent."
            
            # Turkish
            base_tr = ARCHETYPES['tr'].get(p['name'], "")
            mod_tr = SIGNS_MEANING['tr'].get(p['sign'], "")
            sign_tr = SIGN_NAMES_TR.get(p['sign'], p['sign'])
            synth_tr = f"Drakonik Ruh Haritanızda: {base_tr} {mod_tr} Bu, yüksek benliğinizin niyetini gösterir."
            
            p['interpretations'] = {'en': synth_en, 'tr': synth_tr}
            # Fallback for older frontend logic if needed
            p['interpretation'] = synth_tr if lang == 'tr' else synth_en
            draconic_enriched.append(p)

        response = {
            "planets": planets_enriched,
            "houses": [h['lon'] for h in natal_data['houses']], 
            "aspects": aspects_enriched,
                "meta": {
                    "profection_house": profection,
                    "dominants": dominants,
                    "lucky_color": lucky['color'],
                    "lucky_stone": lucky['stone'],
                    "sun_sign": sun_sign,
                    "rising_sign": natal_data['ascendant'],
                    "sun_lon_exact": next((p['lon'] for p in planets_enriched if p['name'] == 'Sun'), 0.0),
                    "calc_utc": natal_data.get('utc_time', 'Unknown'),
                    "local_timezone": natal_data.get('timezone', 'Unknown'),
                    "planetary_hours": [],
                    "draconic_chart": draconic_enriched,
                    "celebrity_match": {"name": "TBD", "score": 0},
                    "acg_lines": []
                }
        }
        return JsonResponse(response)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def calculate_synastry_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=405)

    try:
        data = json.loads(request.body)
        lang = data.get('lang', 'en')
        
        engine = AstroEngine()
        
        # Person 1
        d1 = data.get('date1', '1990/01/01')
        t1 = data.get('time1', '12:00')
        chart1 = engine.calculate_natal(d1, t1, 41.0, 28.0) # Default lat/lon for synastry generic
        
        # Person 2
        d2 = data.get('date2', '1990/01/01')
        t2 = data.get('time2', '12:00')
        chart2 = engine.calculate_natal(d2, t2, 41.0, 28.0)
        
        # Calculate
        result = engine.calculate_synastry(chart1['planets'], chart2['planets'], lang=lang)
        
        # Add Interpretation Texts
        # We can eventually move these to DB, for now hardcoded dynamic text
        summary = ""
        if result['score'] > 85:
            summary = "Soulmate Potential! Extremely high compatibility." if lang=='en' else "Ruh İkizi Potansiyeli! Son derece yüksek uyum."
        elif result['score'] > 70:
            summary = "Strong connection with good harmony." if lang=='en' else "İyi bir uyum ve güçlü bir bağ."
        elif result['score'] > 50:
            summary = "Average compatibility, requires work." if lang=='en' else "Ortalama uyum, çaba gerektirir."
        else:
            summary = "Challenging dynamic, karmic lessons." if lang=='en' else "Zorlayıcı dinamik, karmik dersler."
            
        result['summary'] = summary
        
        return JsonResponse(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

from datetime import datetime, timedelta
from .models import DailyTip

@csrf_exempt
@csrf_exempt
def get_weekly_forecast(request):
    """
    Returns a 7-day Multi-Dimensional Transit Forecast ("Fortune Telling Mode").
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'GET request required'}, status=405)
        
    lang = request.GET.get('lang', 'en')
    date_str = request.GET.get('date', None)
    
    if date_str:
        try:
            start_date = datetime.strptime(date_str, "%Y-%m-%d")
        except:
             try:
                 start_date = datetime.strptime(date_str, "%Y/%m/%d")
             except:
                 start_date = datetime.now()
    else:
        start_date = datetime.now()

    # Check Skyfield availability
    try:
        from skyfield.api import load
        from skyfield.framelib import ecliptic_frame
        eph = load('de421.bsp')
        ts = load.timescale()
        has_skyfield = True
    except:
        has_skyfield = False
        
    forecast = []
    
    # Fortune Messages
    MSGS_EN = {
        'high': "A powerful day! The stars align for success.",
        'low': "Caution advised. Energy is unstable, rest and reflect.",
        'mid': "A balanced day. Good for routine tasks.",
        'love_high': "Venus is smiling! Romance and beauty are favored.",
        'career_high': "Saturn builds. Great for ambitious moves.",
        'tension': "Squares detected. Avoid conflicts and hasty decisions."
    }
    MSGS_TR = {
        'high': "Güçlü bir gün! Yıldızlar başarı için hizalanıyor.",
        'low': "Dikkatli olun. Enerji dengesiz, dinlenin ve düşünün.",
        'mid': "Dengeli bir gün. Rutin işler için uygun.",
        'love_high': "Venüs gülümsüyor! Aşk ve güzellik günü.",
        'career_high': "Satürn inşa ediyor. Kariyer adımları için harika.",
        'tension': "Gergin açılar var. Çatışmadan ve acele karardan kaçının."
    }
    msgs = MSGS_TR if lang == 'tr' else MSGS_EN

    for i in range(7):
        target_date = start_date + timedelta(days=i)
        
        # Default Baselines
        total = 50
        love = 50
        career = 50
        comment = msgs['mid']

        if has_skyfield:
            t = ts.utc(target_date.year, target_date.month, target_date.day, 12, 0, 0)
            planets = {
                'Sun': eph['sun'], 'Moon': eph['moon'], 'Mars': eph['mars'], 
                'Saturn': eph['saturn barycenter'], 'Jupiter': eph['jupiter barycenter'], 
                'Venus': eph['venus']
            }
            pos = {}
            earth = eph['earth']
            for name, body in planets.items():
                astrometric = earth.at(t).observe(body)
                lat, lon, dist = astrometric.apparent().frame_latlon(ecliptic_frame)
                pos[name] = lon.degrees

            # Aspect Logic
            aspect_score = 0
            love_boost = 0
            career_boost = 0
            
            # Simple Transit Logic
            # Venus Aspects (Love)
            v_lon = pos['Venus']
            for p, l in pos.items():
                if p == 'Venus': continue
                diff = abs(v_lon - l) % 360
                if diff > 180: diff = 360 - diff
                if abs(diff - 120) < 5 or abs(diff - 60) < 4: love_boost += 15 # Trine/Sextile
                if abs(diff - 90) < 5 or abs(diff - 180) < 5: love_boost -= 10 # Square/Opp
            
            # Saturn/Jupiter Aspects (Career)
            s_lon = pos['Saturn']
            j_lon = pos['Jupiter']
             # Check Saturn aspects
            for p, l in pos.items():
                if p == 'Saturn': continue
                diff = abs(s_lon - l) % 360
                if diff > 180: diff = 360 - diff
                if abs(diff - 120) < 5 or abs(diff - 60) < 4: career_boost += 10
                if abs(diff - 90) < 5: career_boost -= 15 # Saturn squares depend hard work
            
            # General Aspects
            p_names = list(pos.keys())
            for idx1 in range(len(p_names)):
                for idx2 in range(idx1+1, len(p_names)):
                    p1 = p_names[idx1]; p2 = p_names[idx2]
                    d = abs(pos[p1] - pos[p2]) % 360
                    if d > 180: d = 360 - d
                    if abs(d-120)<5: aspect_score += 8
                    if abs(d-60)<4: aspect_score += 4
                    if abs(d-90)<5: aspect_score -= 8
                    if abs(d-180)<5: aspect_score -= 6
            
            total = 50 + aspect_score
            love = 50 + love_boost
            career = 50 + career_boost
            
            # Smart Commentary
            if love > 70: comment = msgs['love_high']
            elif career > 70: comment = msgs['career_high']
            elif total < 30: comment = msgs['tension']
            elif total > 70: comment = msgs['high']
            elif total < 45: comment = msgs['low']
        
        # Clamp
        total = max(10, min(100, total))
        love = max(10, min(100, love))
        career = max(10, min(100, career))

        forecast.append({
            "day": target_date.strftime("%a %d"), # Mon 18
            "full_date": target_date.strftime("%Y-%m-%d"),
            "score": int(total),
            "love": int(love),
            "career": int(career),
            "comment": comment
        })

    return JsonResponse({"forecast": forecast})


@csrf_exempt
def get_daily_planner(request):
    """
    Returns daily tips and planetary hours.
    """
    # Ensure engine is available
    engine = AstroEngine()
    if request.method != 'GET':
        return JsonResponse({'error': 'GET request required'}, status=405)
        
    try:
        lang = request.GET.get('lang', 'en')
        date_param = request.GET.get('date', None)
        lat = float(request.GET.get('lat', 41.0))
        lon = float(request.GET.get('lon', 28.0))
        
        now = datetime.utcnow()
        if date_param:
            try:
                target_date = datetime.strptime(date_param, "%Y-%m-%d")
                date_str = target_date.strftime("%Y-%m-%d")
            except:
                date_str = now.strftime("%Y-%m-%d")
        else:
            date_str = now.strftime("%Y-%m-%d")

        # Get Hours
        hours_data = engine.calculate_planetary_hours(date_str, lat, lon)
        
        # ... existing transit logic ...
        
        data = {'hours': hours_data}
        
        # Mock other data for now to prevent errors, since we focused on Hours
        data['retrogrades'] = []
        data['phase'] = 'Waxing Gibbous'
        data['daily_summary'] = "Focus on the planetary hours to guide your day."

        # Fetch Tips
        tips = DailyTip.objects.filter(phase=data['phase'])
        tips_data = []
        for t in tips:
            tips_data.append(getattr(t, f'text_{lang}', t.text_en))
            
        data['tips'] = tips_data
        
        # Static Retro warnings
        retro_warnings = []
        for r in data['retrogrades']:
            msg_en = f"{r} is currently in Retrograde! Be careful."
            msg_tr = f"{r} şu an retro harekette! Dikkatli olun."
            retro_warnings.append(msg_tr if lang == 'tr' else msg_en)
            
        data['retro_warnings'] = retro_warnings

        # --- Fetch NASA Daily Horoscope ---
        horoscope = DailyHoroscope.objects.filter(date=now.date()).first()
        
        if horoscope:
            data['daily_summary'] = getattr(horoscope, f'summary_{lang}', horoscope.summary_en)
            # Filter aspects for simplier display if needed, but returning all is fine
            data['daily_aspects'] = horoscope.aspects
        else:
            # Fallback if command not run
            if lang == 'tr':
                 data['daily_summary'] = "Günlük analiz genellikle öğlen gelir."
            else:
                 data['daily_summary'] = "Daily analysis usually arrives by noon."
                 
            data['daily_aspects'] = []

        return JsonResponse(data)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'trace': traceback.format_exc()}, status=500)


@csrf_exempt
@csrf_exempt
def draw_tarot(request):
    """
    Draws 3 cards (Past, Present, Future) and generates a synthesis.
    """
    try:
        # Select 3 unique cards
        selection = random.sample(tarot_deck, 3)
        
        response_cards = []
        positions = ['Past', 'Present', 'Future']
        positions_tr = ['Geçmiş', 'Şimdi', 'Gelecek']
        
        lang = request.GET.get('lang', 'en')
        
        # Scoring Logic
        # IDs are 0 to 21 based on Major Arcana index usually
        # 0:Fool, 1:Magician, 2:HighPriestess, 3:Empress, 4:Emperor, 5:Hierophant, 6:Lovers, 7:Chariot, 8:Strength
        # 9:Hermit, 10:Wheel, 11:Justice, 12:HangedMan, 13:Death, 14:Temperance, 15:Devil, 16:Tower, 17:Star, 18:Moon
        # 19:Sun, 20:Judgement, 21:World
        POSITIVE_CARDS = [1, 3, 4, 6, 7, 8, 10, 11, 14, 17, 19, 20, 21] 
        NEGATIVE_CARDS = [9, 12, 13, 15, 16, 18, 5] # Included Hierophant as neutral/strict
        
        total_score = 0
        meanings_list = []
        
        for i, card in enumerate(selection):
            is_reversed = random.choice([True, False])
            
            # Meaning
            if lang == 'tr':
                meaning = card['meaning_reversed_tr'] if is_reversed else card['meaning_upright_tr']
                name = card['name_tr']
                pos_name = positions_tr[i]
            else:
                meaning = card['meaning_reversed_en'] if is_reversed else card['meaning_upright_en']
                name = card['name_en']
                pos_name = positions[i]

            meanings_list.append(meaning)

            # Score Calculation
            card_id = card['id']
            score = 0
            if card_id in POSITIVE_CARDS:
                score = 10
            elif card_id in NEGATIVE_CARDS:
                score = -10
            else:
                score = 5 # Neutral/Slightly positive
                
            if is_reversed:
                score *= -0.5 # Reversal twists the energy (Bad becomes less bad/internal, Good becomes blocked)
                
            total_score += score

            response_cards.append({
                "id": card['id'],
                "name": name,
                "position": pos_name,
                "is_reversed": is_reversed,
                "meaning": meaning,
                "element": card['element'],
                "color": card['color']
            })
            
        # Synthesize
        if lang == 'tr':
            synthesis = f"Öncelikle geçmişte {meanings_list[0]} Şu anda {meanings_list[1]} Gelecekte ise {meanings_list[2]} Bu yolculuk senin elinde."
            
            # Wish Outcome
            wish_title = ""
            wish_text = ""
            if total_score >= 15:
                wish_title = "DİLEĞİN KABUL OLDU!"
                wish_text = "Evren seninle muazzam bir uyum içinde. İstediğin şey sana doğru hızla geliyor."
            elif total_score >= 5:
                wish_title = "OLUMLU GELİŞME"
                wish_text = "Yolun açık görünüyor. Küçük çabalarla büyük sonuçlar alabilirsin."
            elif total_score >= -5:
                wish_title = "BELİRSİZLİK HAKİM"
                wish_text = "Henüz hiçbir şey kesinleşmiş değil. İçsel rehberliğine güvenmen gereken bir dönem."
            else:
                wish_title = "ZORLU SÜREÇ"
                wish_text = "Şu an için engeller var. Biraz beklemen ve stratejini gözden geçirmen gerekebilir."
        else:
            synthesis = f"Basically, looking at the past, {meanings_list[0]} Currently, {meanings_list[1]} As for the future, {meanings_list[2]} The path is yours to walk."
            
            wish_title = ""
            wish_text = ""
            if total_score >= 15:
                wish_title = "DESTINY FULFILLED!"
                wish_text = "The universe aligns perfectly with your desire. Expect a magnificent outcome."
            elif total_score >= 5:
                wish_title = "POSITIVE OUTCOME"
                wish_text = "Success is likely with a bit of focus. The energy is supporting you."
            elif total_score >= -5:
                wish_title = "UNCERTAIN PATH"
                wish_text = "The mists have not yet cleared. Patience is your best ally right now."
            else:
                wish_title = "CHALLENGES AHEAD"
                wish_text = "Obstacles block the way for now. Reassess your approach before moving forward."

        return JsonResponse({
            'cards': response_cards,
            'synthesis': synthesis,
            'wish': {
                'title': wish_title,
                'text': wish_text,
                'score': int(total_score)
            }
        })
    except Exception as e:
         return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def calculate_career_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=405)

    try:
        data = json.loads(request.body)
        date_str = data.get('date', '1990/01/01')
        time_str = data.get('time', '12:00')
        lat = float(data.get('lat', 41.0))
        lon = float(data.get('lon', 28.0))
        lang = data.get('lang', 'en')
        
        engine = AstroEngine()
        
        # 1. Calc Natal to get Houses/Planets
        natal_data = engine.calculate_natal(date_str, time_str, lat, lon)
        
        # 2. Calc Career
        career_result = engine.calculate_career(natal_data)
        
        return JsonResponse(career_result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


def index(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            profile = None
        
        context = {
            'profile': profile,
            'user': request.user
        }
        return render(request, 'astrology/index.html', context)
    else:
        return render(request, 'astrology/landing.html')


def _mock_chart_data():
    """Fallback data when library is missing"""
    return {
        "planets": [
            {"name": "Sun", "sign": "Aries", "lon": 10.5, "signlon": 10.5, "house": 1, "interpretation": "Sun in Aries" },
            {"name": "Moon", "sign": "Taurus", "lon": 45.2, "signlon": 15.2, "house": 2, "interpretation": "Moon in Taurus" }
        ],
        "houses": [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330],
        "aspects": [],
        "meta": {
             "profection_house": 5,
             "dominants": {"Fire": 50, "Earth": 20, "Air": 20, "Water": 10},
             "lucky_color": "Red",
             "lucky_stone": "Ruby",
             "sun_sign": "Aries",
             "planetary_hours": [],
             "draconic_chart": [],
             "celebrity_match": {"name": "Beyonce", "score": 95, "reason": "Mock"},
             "acg_lines": []
        }
    }

# import geonamescache (Moved to top)

@csrf_exempt
def get_countries(request):
    """Returns a list of all countries sorted by name."""
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    # Format: { 'TR': 'Turkey', 'US': 'United States' }
    data = []
    for code, details in countries.items():
        data.append({'code': code, 'name': details['name']})
    
    # Sort by name
    data.sort(key=lambda x: x['name'])
    return JsonResponse({'countries': data})



from .turkey_data import TR_DATA, PROVINCE_NAMES

@csrf_exempt
def get_cities(request):
    """Returns cities/districts. Uses curated TR_DATA for Turkey."""
    country_code = request.GET.get('code')
    admin_code = request.GET.get('admin_code')
    
    if not country_code:
        return JsonResponse({'error': 'Country code required'}, status=400)
    
    # Priority 1: Check TR_DATA for detailed districts
    if country_code == 'TR' and admin_code and admin_code in TR_DATA:
        return JsonResponse({'cities': TR_DATA[admin_code]['districts']})
        
    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()
    
    filtered = []
    
    # Priority 2: Standard Geonames Fetch
    # If it's TR but not in our TR_DATA, we still fetch from Geonames.
    for cid, c in cities.items():
        if c['countrycode'] == country_code:
            if admin_code and c.get('admin1code') != admin_code:
                continue
            
            # For Turkey, geonames might list a district.
            filtered.append({
                'name': c['name'],
                'lat': c['latitude'],
                'lon': c['longitude'],
                'pop': c.get('population', 0)
            })
            
    filtered.sort(key=lambda x: x['name'])
    return JsonResponse({'cities': filtered})

@csrf_exempt
def get_provinces(request):
    """Returns Provinces. Uses PROVINCE_NAMES for TR to ensure distinct list."""
    country_code = request.GET.get('code')
    if not country_code:
        return JsonResponse({'error': 'Country code required'}, status=400)

    # Priority: TR Official List
    if country_code == 'TR':
        provinces = []
        for code, name in PROVINCE_NAMES.items():
            provinces.append({'code': code, 'name': name})
            
        provinces.sort(key=lambda x: x['name'])
        return JsonResponse({'provinces': provinces})


    # Standard Logic for other countries
    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()
    admin_groups = {}
    
    for cid, c in cities.items():
        if c['countrycode'] == country_code:
            ac = c.get('admin1code', '')
            if not ac: continue
            if ac not in admin_groups: admin_groups[ac] = []
            admin_groups[ac].append(c)
            
    provinces = []
    for ac, city_list in admin_groups.items():
        city_list.sort(key=lambda x: x.get('population', 0), reverse=True)
        # Fallback: limit province name length to avoid some garbage
        pname = city_list[0]['name']
        provinces.append({'code': ac, 'name': pname})
        
    provinces.sort(key=lambda x: x['name'])
    
    return JsonResponse({'provinces': provinces})

# --- AUTHENTICATION & PROFILE API ---

@csrf_exempt
def register_api(request):
    if request.method != 'POST': return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        
        # Validation
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)
            
        user = User.objects.create_user(username=username, password=password, email=email)
        
        # Init Profile with Data
        profile = UserProfile.objects.create(user=user)
        
        # Save Birth Data if provided
        if data.get('date'):
            profile.birth_date = dt.strptime(data['date'], "%Y-%m-%d").date()
        if data.get('time'):
            profile.birth_time = dt.strptime(data['time'], "%H:%M").time()
        if data.get('place'):
            profile.birth_place = data['place']
        if data.get('lat'):
            profile.lat = float(data['lat'])
        if data.get('lon'):
            profile.lon = float(data['lon'])
            
        profile.save()
        
        # Auto-Login
        login(request, user)
        
        return JsonResponse({'success': True, 'username': user.username})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def login_api(request):
    if request.method != 'POST': return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'username': user.username})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def logout_api(request):
    logout(request)
    return JsonResponse({'success': True})

def check_auth_api(request):
    if request.user.is_authenticated:
        # Get Profile Data
        try:
            p = request.user.profile
            return JsonResponse({
                'authenticated': True,
                'username': request.user.username,
                'is_superuser': request.user.is_superuser,
                'profile': {
                    'date': p.birth_date.strftime("%Y-%m-%d") if p.birth_date else "",
                    'time': p.birth_time.strftime("%H:%M") if p.birth_time else "",
                    'lat': p.lat,
                    'lon': p.lon,
                    'place': p.birth_place
                }
            })
        except:
            # Should exist via signal, but if not:
            return JsonResponse({
                'authenticated': True, 
                'username': request.user.username, 
                'is_superuser': request.user.is_superuser,
                'profile': None
            })
    else:
        return JsonResponse({'authenticated': False})

@csrf_exempt
def update_profile_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    try:
        data = json.loads(request.body)
        p, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Update Fields
        if 'date' in data: p.birth_date = datetime.datetime.strptime(data['date'], "%Y-%m-%d").date()
        if 'time' in data: p.birth_time = datetime.datetime.strptime(data['time'], "%H:%M").time()
        if 'lat' in data: p.lat = float(data['lat'])
        if 'lon' in data: p.lon = float(data['lon'])
        if 'place' in data: p.birth_place = data['place']
        
        p.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@user_passes_test(lambda u: u.is_superuser)
def custom_admin_dashboard(request):
    # Base Queryset: Exclude Superusers (Admins)
    base_qs = UserActivityLog.objects.exclude(user__is_superuser=True)

    # Date Filtering
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    if start_date_str:
        base_qs = base_qs.filter(timestamp__date__gte=start_date_str)
    if end_date_str:
        base_qs = base_qs.filter(timestamp__date__lte=end_date_str)

    # 1. Logs (Paginated)
    log_list = base_qs.select_related('user').order_by('-timestamp')
    paginator = Paginator(log_list, 20) # Show 20 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 2. Daily Stats (Based on Filtered Data)
    action_counts = base_qs.values('action').annotate(total=Count('action')).order_by('-total')
    
    # 3. Stats Summary (Filtered)
    unique_visitors = base_qs.values('ip_address').distinct().count()
    total_requests = base_qs.count()
    
    # 4. Active Known Users (In the filtered period)
    active_users = base_qs.filter(user__isnull=False).values('user__username').distinct()

    context = {
        'page_obj': page_obj, # Use page_obj for the loop
        'action_counts': action_counts,
        'unique_visitors': unique_visitors,
        'total_requests': total_requests,
        'active_users': [u['user__username'] for u in active_users],
        'total_users_count': User.objects.exclude(is_superuser=True).count(), # Total registered users (non-admin)
        # Pass back filter params to keep them in pagination links
        'start_date': start_date_str or '', 
        'end_date': end_date_str or ''
    }
    
    return render(request, 'astrology/custom_admin.html', context)

@csrf_exempt
def get_daily_horoscopes_api(request):
    lang = request.GET.get('lang', 'tr')
    today = datetime.now().date()
    # Create a seed based on date
    seed_base = int(today.strftime("%Y%m%d"))
    
    signs = SIGNS_TR if lang == 'tr' else SIGNS_EN
    sentences = SENTENCES['tr'] if lang == 'tr' else SENTENCES['en']
    
    results = []
    
    if not sentences: # Fallback
         sentences = ["Bugün şanslı gününüz.", "Dikkatli olun."]

    for idx, sign in enumerate(signs):
        # Deterministic Random Selection
        # Seed = Date + Sign Index
        random.seed(seed_base + idx)
        
        # Pick 2 distinctive sentences
        s1 = random.choice(sentences)
        s2 = random.choice(sentences)
        # Simple loop to ensure variety if list is large enough
        if len(sentences) > 1:
            while s1 == s2:
                s2 = random.choice(sentences)
            
        text = f"{s1} {s2}"
        
        # Assign a generic "mood" or "icon"
        moods = ['⭐', '💖', '🍀', '🚀', '🧘', '🔥']
        mood = random.choice(moods)

        results.append({
            'sign': sign,
            'text': text,
            'mood': mood,
            'date': today.strftime("%d.%m.%Y")
        })

    return JsonResponse({'horoscopes': results})

def auth_view(request):
    return render(request, 'astrology/auth.html')
