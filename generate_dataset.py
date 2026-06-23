import pandas as pd
import random

categories = {
    "Water Issue": [
        "Water leakage near {place}",
        "No water supply in {place} since morning",
        "Dirty water coming from taps in {place}",
        "Low water pressure in {place}",
        "Pipeline burst near {place}",
        "Water tank overflowing in {place}",
        "Drinking water smells bad in {place}",
        "Major water leakage near {place}",
        "Water supply stopped in {place}",
        "Contaminated water reported in {place}"
    ],

    "Road Issue": [
        "Huge pothole near {place}",
        "Road damaged after rain in {place}",
        "Broken road causing accidents near {place}",
        "Road repair needed urgently in {place}",
        "Uneven road surface near {place}",
        "Road cave-in reported at {place}",
        "Potholes filled with rainwater near {place}",
        "Main road damaged in {place}",
        "Bad road condition near {place}",
        "Road surface cracked near {place}"
    ],

    "Garbage": [
        "Garbage not collected in {place}",
        "Dustbin overflowing near {place}",
        "Waste dumped on roadside in {place}",
        "Garbage pile causing bad smell near {place}",
        "Trash scattered near {place}",
        "Garbage vehicle not arrived in {place}",
        "Waste lying near school in {place}",
        "Unclean surroundings in {place}",
        "Dead animal lying near {place}",
        "Garbage attracting stray dogs in {place}"
    ],

    "Traffic": [
        "Heavy traffic jam near {place}",
        "Traffic signal not working at {place}",
        "Vehicles stuck near {place}",
        "Traffic congestion during evening near {place}",
        "Improper traffic management at {place}",
        "Long vehicle queue near {place}",
        "Road blocked causing traffic near {place}",
        "Signal timing issue at {place}",
        "Traffic movement very slow near {place}",
        "Frequent traffic jam in {place}"
    ],

    "Street Light": [
        "Street light not working near {place}",
        "Entire lane is dark in {place}",
        "Street light flickering near {place}",
        "Broken street lamp near {place}",
        "Pole light not functioning at {place}",
        "No lighting in {place} at night",
        "Street light damaged near {place}",
        "Dark road causing safety issue near {place}",
        "Light pole issue reported at {place}",
        "Street lamp off since yesterday near {place}"
    ],

    "Drainage": [
        "Drainage blocked near {place}",
        "Drain overflowing after rain in {place}",
        "Waterlogging due to drainage issue near {place}",
        "Drain cover broken near {place}",
        "Blocked gutter causing smell in {place}",
        "Rainwater not draining near {place}",
        "Drainage line choked in {place}",
        "Open drain causing danger near {place}",
        "Drain water entering road near {place}",
        "Severe drainage problem in {place}"
    ],

    "Electricity": [
        "Power outage in {place}",
        "Electric pole damaged near {place}",
        "Open electric wire hanging near {place}",
        "Transformer sparking in {place}",
        "Frequent power cuts in {place}",
        "Electric box open near {place}",
        "Street electric wire issue in {place}",
        "Voltage fluctuation in {place}",
        "Electric pole leaning near {place}",
        "Power supply problem in {place}"
    ],

    "Public Safety": [
        "Unsafe construction site near {place}",
        "Broken railing near {place}",
        "Open manhole causing danger in {place}",
        "Dangerous spot near {place}",
        "Accident risk due to broken road near {place}",
        "Uncovered pit near {place}",
        "Public safety issue reported in {place}",
        "Risky area without warning sign near {place}",
        "Damaged public structure near {place}",
        "Pedestrian safety concern in {place}"
    ],

    "Noise Complaint": [
        "Loud music at night in {place}",
        "Construction noise disturbing residents in {place}",
        "Factory noise issue near {place}",
        "Loudspeaker noise late night near {place}",
        "Noise pollution in {place}",
        "Continuous drilling noise in {place}",
        "Vehicle horn noise near {place}",
        "Late night event noise in {place}",
        "High volume sound system near {place}",
        "Noise disturbance reported in {place}"
    ],

    "Illegal Parking": [
        "Illegal parking near {place}",
        "Vehicles parked on footpath in {place}",
        "Cars blocking road near {place}",
        "No parking rule violation near {place}",
        "Two wheelers parked wrongly in {place}",
        "Illegal parking causing traffic near {place}",
        "Vehicles blocking society gate in {place}",
        "Parking issue near market in {place}",
        "Road blocked due to illegal parking near {place}",
        "Unauthorized parking in {place}"
    ]
}

places = [
    "Kandivali West", "Borivali station", "Malad West", "Andheri East",
    "Dahisar", "Goregaon", "Thane", "Navi Mumbai", "Dadar",
    "Bandra", "Kurla", "Vasai", "Mira Road", "Powai", "Mulund",
    "Mahada Kandivali", "Ekta Nagar", "Charkop", "Sion", "Chembur"
]

extra_phrases = [
    "",
    "Please resolve this issue quickly.",
    "This problem is happening for many days.",
    "Residents are facing daily trouble because of this.",
    "This issue is causing inconvenience to people.",
    "The situation becomes worse during evening time.",
    "It is creating safety problems for citizens.",
    "Kindly take urgent action.",
    "This is affecting daily life in the area.",
    "People are complaining about this repeatedly."
]

rows = []

for category, templates in categories.items():
    for i in range(100):
        complaint = random.choice(templates).format(place=random.choice(places))

        if i % 3 == 0:
            complaint = complaint + " " + random.choice(extra_phrases)

        rows.append({
            "complaint": complaint,
            "category": category
        })

df = pd.DataFrame(rows)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv("../DATA/RAW DATA/complaint_v2.csv", index=False)

print("Dataset created successfully")
print(df.shape)
print(df["category"].value_counts())

