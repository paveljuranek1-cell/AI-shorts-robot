import json


print("Spouštím video generátor...")


# načtení scénářů

with open(
    "shorts_scenare.json",
    "r",
    encoding="utf-8"
) as file:
    scenarios = json.load(file)


print(f"Nalezeno scénářů: {len(scenarios)}")


# vezmeme první scénář

video = scenarios[0]


print("\nPřipravuji video:")
print("--------------------")

print("TITULEK:")
print(video["title"])

print("\nHOOK:")
print(video["hook"])

print("\nTEXT VIDEA:")
print(video["script"])


print("\nVideo data připravena ✅")
