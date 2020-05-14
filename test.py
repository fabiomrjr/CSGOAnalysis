
map = {}

map = {"Mirage":
       {"Pick": 1, "Win": 0, "Confidence": 0.0}}

if map.get("Train") == None:
    map2 = {"Train": {"Pick":1, "Win":0, "Confidence": 0.0} }
    map2["Train"]["Win"] = 5
    map.update(map2)
    #map4 = {"Train": {"Win": 2}}
    #map.update(map4)
    map.get("Win")
    print("A")

for item in map:
    map[item]["Confidence"] = 100 * map[item]["Win"]/map[item]["Pick"]

print("Testes")