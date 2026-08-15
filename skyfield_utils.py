from skyfield.api import load, wgs84
from skyfield import almanac
from skyfield.framelib import ecliptic_frame
from zoneinfo import ZoneInfo
import math

class AstronomyEngine:

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(self):

        print("Loading Astronomy Engine...")

        self.ts = load.timescale()
        self.eph = load("de421.bsp")

        # Celestial Bodies
        self.earth = self.eph["Earth"]
        self.sun = self.eph["Sun"]
        self.moon = self.eph["Moon"]

        # Planets
        self.planets = {
            "Mercury": self.eph["Mercury Barycenter"],
            "Venus": self.eph["Venus"],
            "Mars": self.eph["Mars"],
            "Jupiter": self.eph["Jupiter Barycenter"],
            "Saturn": self.eph["Saturn Barycenter"],
        }

        self.timezone = ZoneInfo("Asia/Kolkata")

        # 27 Nakshatras
        self.nakshatras = [
            "Ashwini",
            "Bharani",
            "Krittika",
            "Rohini",
            "Mrigashira",
            "Ardra",
            "Punarvasu",
            "Pushya",
            "Ashlesha",
            "Magha",
            "Purva Phalguni",
            "Uttara Phalguni",
            "Hasta",
            "Chitra",
            "Swati",
            "Vishakha",
            "Anuradha",
            "Jyeshtha",
            "Mula",
            "Purva Ashadha",
            "Uttara Ashadha",
            "Shravana",
            "Dhanishta",
            "Shatabhisha",
            "Purva Bhadrapada",
            "Uttara Bhadrapada",
            "Revati"
        ]

        print("Astronomy Engine Ready!\n")
    # =====================================================
    # Helpers
    # =====================================================

    def create_time(self, date, time):
        """Create a Skyfield time from user selected date and time."""

        return self.ts.utc(
            date.year,
            date.month,
            date.day,
            time.hour,
            time.minute,
            getattr(time, "second", 0),
        )


    def to_local(self, utc_datetime):
        """Convert UTC datetime to local timezone."""

        return utc_datetime.astimezone(self.timezone)

    # =====================================================
    # Moon Phase
    # =====================================================

    def moon_phase(self, date, time):
        """
        Calculate the Moon phase for the given observation date and time.

        Returns:
            phase (str): Moon phase name.
            phase_angle (float): Phase angle in degrees.
        """

        # Create Skyfield time object
        t = self.create_time(date, time)

        # Calculate phase angle
        phase_angle = almanac.moon_phase(self.eph, t).degrees

        # Determine Moon phase
        if phase_angle < 22.5:
            phase = "New Moon"

        elif phase_angle < 67.5:
            phase = "Waxing Crescent"

        elif phase_angle < 112.5:
            phase = "First Quarter"

        elif phase_angle < 157.5:
            phase = "Waxing Gibbous"

        elif phase_angle < 202.5:
            phase = "Full Moon"

        elif phase_angle < 247.5:
            phase = "Waning Gibbous"

        elif phase_angle < 292.5:
            phase = "Last Quarter"

        elif phase_angle < 337.5:
            phase = "Waning Crescent"

        else:
            phase = "New Moon"

        return phase, round(phase_angle, 2)

    # =====================================================
    # Moon Illumination
    # =====================================================

    def moon_illumination(self, phase_angle):

        illumination = (1 - math.cos(math.radians(phase_angle))) / 2

        return round(illumination * 100, 2)

    # =====================================================
    # Sunrise / Sunset
    # =====================================================

    def get_sunrise_sunset(self, latitude, longitude, date):

        observer = wgs84.latlon(latitude, longitude)

        t0 = self.ts.utc(date.year, date.month, date.day)
        t1 = self.ts.utc(date.year, date.month, date.day + 1)

        f = almanac.sunrise_sunset(self.eph, observer)

        times, events = almanac.find_discrete(t0, t1, f)

        sunrise = None
        sunset = None

        for t, event in zip(times, events):

            local = self.to_local(t.utc_datetime())

            if event:
                sunrise = local
            else:
                sunset = local

        sunrise_str = sunrise.strftime("%I:%M %p") if sunrise else "N/A"
        sunset_str = sunset.strftime("%I:%M %p") if sunset else "N/A"

        if sunrise and sunset:
            day_length = sunset - sunrise
            hours = day_length.seconds // 3600
            minutes = (day_length.seconds % 3600) // 60
            day_length = f"{hours}h {minutes}m"
        else:
            day_length = "N/A"

        return sunrise_str, sunset_str, day_length

    # =====================================================
    # Moonrise / Moonset
    # =====================================================

    def get_moonrise_moonset(self, latitude, longitude, date):

        observer = wgs84.latlon(latitude, longitude)

        t0 = self.ts.utc(date.year, date.month, date.day)
        t1 = self.ts.utc(date.year, date.month, date.day + 1)

        f = almanac.risings_and_settings(
            self.eph,
            self.moon,
            observer
        )

        times, events = almanac.find_discrete(t0, t1, f)

        moonrise = None
        moonset = None

        for t, event in zip(times, events):

            local = self.to_local(t.utc_datetime())

            if event:
                moonrise = local
            else:
                moonset = local

        moonrise = moonrise.strftime("%I:%M %p") if moonrise else "N/A"
        moonset = moonset.strftime("%I:%M %p") if moonset else "N/A"

        return moonrise, moonset

    # =====================================================
    # Visible Planets
    # =====================================================
    def get_visible_planets(self, latitude, longitude, date, time):

        observer = self.earth + wgs84.latlon(latitude, longitude)

        t = self.create_time(date, time)

        visible_planets = []

        for name, planet in self.planets.items():

            astrometric = observer.at(t).observe(planet)

            apparent = astrometric.apparent()

            altitude, azimuth, distance = apparent.altaz()

            if altitude.degrees > 10:
                visible_planets.append(name)
        return visible_planets

    # =====================================================
    # Visible Constellations
    # =====================================================

    def get_visible_constellations(self, date, time):
        """
        Return major constellations visible based on the month.
        Suitable for educational purposes.
        """

        month = date.month

        constellation_calendar = {
            1: ["Orion", "Taurus", "Gemini"],
            2: ["Orion", "Canis Major", "Gemini"],
            3: ["Leo", "Cancer", "Hydra"],
            4: ["Leo", "Virgo", "Boötes"],
            5: ["Virgo", "Boötes", "Libra"],
            6: ["Scorpius", "Libra", "Hercules"],
            7: ["Scorpius", "Sagittarius", "Cygnus"],
            8: ["Sagittarius", "Cygnus", "Aquila"],
            9: ["Pegasus", "Cygnus", "Aquarius"],
            10: ["Pegasus", "Andromeda", "Cassiopeia"],
            11: ["Cassiopeia", "Perseus", "Andromeda"],
            12: ["Orion", "Taurus", "Auriga"],
        }

        return constellation_calendar.get(month, [])

    # =====================================================
    # Nakshatra
    # =====================================================

    def get_nakshatra(self, date, time):
        """
        Calculate the Moon's Nakshatra using its ecliptic longitude.
        """

        # Observation time
        t = self.create_time(date, time)

        # Moon position as seen from Earth
        moon = self.earth.at(t).observe(self.moon).apparent()

        # Ecliptic coordinates
        lat, lon, distance = moon.frame_latlon(ecliptic_frame)

        # Longitude (0–360°)
        longitude = lon.degrees % 360

        # Each Nakshatra spans 13°20' = 13.333333°
        nakshatra_size = 360 / 27

        # Nakshatra index
        index = int(longitude // nakshatra_size)

        return self.nakshatras[index]

    # =====================================================
    # Astronomy Report
    # =====================================================

    def get_astronomy_report(self, latitude, longitude, date, time):
        """
        Generate a complete astronomy report for the selected
        location, date, and observation time.
        """

        # Moon Information
        phase, angle = self.moon_phase(date, time)
        illumination = self.moon_illumination(angle)

        # Sunrise / Sunset
        sunrise, sunset, day_length = self.get_sunrise_sunset(
            latitude,
            longitude,
            date
        )

        # Moonrise / Moonset
        moonrise, moonset = self.get_moonrise_moonset(
            latitude,
            longitude,
            date
        )

        # Visible Planets
        visible_planets = self.get_visible_planets(
            latitude,
            longitude,
            date,
            time
        )

        # Visible Constellations
        visible_constellations = self.get_visible_constellations(date, time)

        # Nakshatra
        nakshatra = self.get_nakshatra(
            date,
            time
        )

        # Final Report
        return {

            "moon_phase": phase,

            "moon_phase_angle": angle,

            "moon_illumination": illumination,

            "sunrise": sunrise,

            "sunset": sunset,

            "day_length": day_length,

            "moonrise": moonrise,

            "moonset": moonset,

            "visible_planets": visible_planets,

            "visible_constellations": visible_constellations,

            "nakshatra": nakshatra

        }
# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    from datetime import date, time

    astro = AstronomyEngine()

    report = astro.get_astronomy_report(
        latitude=20.2961,
        longitude=85.8245,
        date=date.today(),
        time=time(21, 0)
    )
    print("\nAstronomy Report")
    print("-" * 50)

    for key, value in report.items():
        print(f"{key:25}: {value}")
