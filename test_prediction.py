from prediction import predict_quality

sample = {

    "Date": "2026-07-24",

    "Location_Name": "Bhubaneswar",

    "Lat": 20.2961,

    "Lon": 85.8245,

    "Moon_Phase": 0.25,

    "Moon_Illum": 18,

    "Moon_RiseSet": "18:30 / 04:30",

    "Sun_RiseSet": "05:15 / 18:20",

    "Cloud_Cover": 12,

    "Humidity": 70,

    "Temperature": 28,

    "Wind_Speed": 5,

    "Light_Pollution": 45,

    "Visible_Planets": "Jupiter, Saturn",

    "Visible_Constellations": "Orion",

    "Nakshatra": "Rohini"

}

print(predict_quality(sample))