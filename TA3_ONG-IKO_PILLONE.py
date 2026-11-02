import json
import os

# These are the sample disaster cases that the program already knows.
cases = [
    {
        "name": "Typhoon Ursula (2019)",
        "type": "Typhoon",
        "flood": "High",
        "area": "Urban",
        "severity": "Severe",
        "population": 10000,
        "solution": "Evacuate residents in flood-prone areas, open shelters, and prepare food, water, and medical supplies."
    },
    {
        "name": "Typhoon Odette (2021)",
        "type": "Typhoon",
        "flood": "Medium",
        "area": "Coastal",
        "severity": "Severe",
        "population": 8000,
        "solution": "Prioritize vulnerable families, prepare evacuation vehicles, and provide basic supplies in shelters."
    },
    {
        "name": "Urban Flood Event",
        "type": "Flood",
        "flood": "High",
        "area": "Urban",
        "severity": "Moderate",
        "population": 6000,
        "solution": "Warn residents in low areas and prepare temporary evacuation centers."
    },
    {
        "name": "Earthquake Event",
        "type": "Earthquake",
        "flood": "Low",
        "area": "Urban",
        "severity": "Severe",
        "population": 12000,
        "solution": "Check buildings for damage and prepare safe areas for people who need shelter."
    },
    {
        "name": "Typhoon Event",
        "type": "Typhoon",
        "flood": "Medium",
        "area": "Rural",
        "severity": "Moderate",
        "population": 5000,
        "solution": "Monitor rivers, warn nearby communities, and prepare transportation for evacuation."
    }
]


# Read saved cases if the program has been used before.
# If there is no saved file, start with the five sample cases.
if os.path.exists("disaster_cases.json"):
    with open("disaster_cases.json", "r") as file:
        cases = json.load(file)


print("======================================")
print(" DISASTER RESPONSE DECISION SUPPORT")
print("======================================")
print("Number of saved cases:", len(cases))

# Get information about the new disaster.
print("\n--- NEW DISASTER INFORMATION ---")
event_name = input("Event name: ")
disaster_type = input("Disaster type (Typhoon/Flood/Earthquake): ").title()
flood_level = input("Expected flooding (Low/Medium/High): ").title()
area_type = input("Area type (Urban/Coastal/Rural): ").title()
severity = input("Severity (Low/Moderate/Severe): ").title()

while True:
    try:
        population = int(input("Estimated affected population: "))
        if population > 0:
            break
        print("Enter a population greater than zero.")
    except ValueError:
        print("Please enter a whole number.")

# Keep the input values in one dictionary so they can be compared and saved.
new_case = {
    "name": event_name,
    "type": disaster_type,
    "flood": flood_level,
    "area": area_type,
    "severity": severity,
    "population": population
}

# Compare the new disaster with every case in the list.
print("\n--- SIMILARITY RESULTS ---")
ranked_cases = []

for old_case in cases:
    similarity = 0

    if new_case["type"].lower() == old_case["type"].lower():
        similarity += 25

    if new_case["flood"].lower() == old_case["flood"].lower():
        similarity += 25

    if new_case["area"].lower() == old_case["area"].lower():
        similarity += 20

    # A closer severity level receives a higher score.
    severity_levels = {"Low": 1, "Moderate": 2, "Severe": 3}
    difference = abs(
        severity_levels.get(new_case["severity"], 2) -
        severity_levels.get(old_case["severity"], 2)
    )
    similarity += 15 - (difference * 7.5)

    # Compare the affected population. A closer number gets more points.
    population_difference = abs(new_case["population"] - old_case["population"])
    population_score = 15 - (
        population_difference / max(new_case["population"], 1) * 15
    )
    if population_score < 0:
        population_score = 0

    similarity += population_score
    similarity = round(similarity, 2)

    print(old_case["name"], "-", similarity, "%")

    ranked_cases.append((similarity, old_case))

# Put the highest similarity score at the top.
ranked_cases.sort(reverse=True, key=lambda item: item[0])

best_score = ranked_cases[0][0]
best_case = ranked_cases[0][1]

print("\n--- MOST SIMILAR PAST CASE ---")
print("Event:", best_case["name"])
print("Similarity:", best_score, "%")
print("Previous response:", best_case["solution"])

# Use the old response as a guide, then adjust it for the new disaster.
print("\n--- RECOMMENDED RESPONSE ---")

if severity == "Severe":
    evacuation = "Start early evacuation in high-risk communities and help children, older adults, and people who need assistance first."
elif severity == "Moderate":
    evacuation = "Prepare evacuation for people living in high-risk areas and continue monitoring official warnings."
else:
    evacuation = "Prepare the response teams and keep residents updated about the situation."

if flood_level == "High":
    flood_action = "Focus on low-lying areas and avoid roads that may become flooded."
elif flood_level == "Medium":
    flood_action = "Monitor rivers and drainage systems and prepare other possible evacuation routes."
else:
    flood_action = "Continue monitoring the weather and local conditions."

# Use a simple estimate to decide how many people may need shelter.
if severity == "Severe":
    evacuee_rate = 0.20
elif severity == "Moderate":
    evacuee_rate = 0.10
else:
    evacuee_rate = 0.05

evacuees = int(population * evacuee_rate)
shelter_capacity = evacuees

resources = "Prepare transportation, food, drinking water, and basic medical supplies."

print(evacuation)
print(flood_action)
print(resources)
print("Estimated evacuees:", evacuees)
print("Suggested shelter capacity:", shelter_capacity, "people")

# Save the new case and the response so it can be used next time.
new_case["solution"] = evacuation + " " + flood_action + " " + resources
new_case["estimated_evacuees"] = evacuees
new_case["shelter_capacity"] = shelter_capacity

cases.append(new_case)

with open("disaster_cases.json", "w") as file:
    json.dump(cases, file, indent=4)

print("\nNew case saved successfully!")

# Show the cases after adding the new disaster.
print("\n--- UPDATED CASE BASE ---")
for case in cases:
    print(
        case["name"], "|",
        case["type"], "|",
        case["flood"], "|",
        case["area"], "|",
        case["severity"]
    )

print("\nTotal cases:", len(cases))
