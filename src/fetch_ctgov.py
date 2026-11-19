"""Download every ClinicalTrials.gov study with a location matching Ireland."""
import gzip
import json
import time
from pathlib import Path

import requests

URL = "https://clinicaltrials.gov/api/v2/studies"
OUT = Path("data/raw/ctgov_studies.jsonl.gz")

FIELDS = ",".join([
    "protocolSection.identificationModule",
    "protocolSection.statusModule",
    "protocolSection.sponsorCollaboratorsModule",
    "protocolSection.designModule",
    "protocolSection.conditionsModule",
    "protocolSection.contactsLocationsModule.locations",
    "derivedSection.conditionBrowseModule",
])

def main():
    params = {
        "query.locn": "Ireland",
        "fields": FIELDS,
        "pageSize": 1000,
        "countTotal": "true",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    n, page = 0, 0
    
    with gzip.open(OUT, "wt", encoding="utf-8") as f:
        while True:
            page += 1
            r = requests.get(URL, params=params, timeout=90)
            r.raise_for_status()
            data = r.json()
            if page == 1:
                print("Studies to download:", data["totalCount"])
            
            for study in data["studies"]:
                f.write(json.dumps(study) + "\n")
                n += 1
            print(f"page {page}: {n} saved")

            token = data.get("nextPageToken")
            if not token:          # no token = last page
                break
            params["pageToken"] = token
            time.sleep(0.5)        # be polite to the server

    print("Done:", n, "studies ->", OUT)


if __name__ == "__main__":
    main()