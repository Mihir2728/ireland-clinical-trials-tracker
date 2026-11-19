import requests

URL = "https://clinicaltrials.gov/api/v2/studies"
params = {
    "query.locn": "Ireland",
    "pageSize": 5,
    "countTotal": "true"
}

r = requests.get(URL, params=params, timeout=60)
r.raise_for_status()
data = r.json()

print("Total Studies:", data["totalCount"])

for study in data["studies"]:
    ps = study["protocolSection"]
    nct = ps["identificationModule"]["nctId"]
    sponsor = ps["sponsorCollaboratorsModule"]["leadSponsor"]["name"]
    phases = ps.get("designModule", {}).get("phases", [])
    start = ps.get("statusModule", {}).get("startDateStruct", {}).get("date")
    locs = ps.get("contactsLocationsModule", {}).get("locations", [])
    countries = sorted({loc.get("country") for loc in locs})
    print(nct, "|", sponsor, "|", phases, start, "|", countries)