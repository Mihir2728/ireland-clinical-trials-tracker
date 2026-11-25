"""Flatten the raw ClinicalTrials.gov download into DuckDB tables."""
import gzip
import json
from pathlib import Path

import duckdb
import pandas as pd

RAW = Path("data/raw/ctgov_studies.jsonl.gz")
DB = Path("data/trials.duckdb")


def read_studies(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def flatten(studies):
    trials, sites, mesh = [], [], []                                              # FIXED
    for st in studies:
        ps = st.get("protocolSection", {})
        ident = ps.get("identificationModule", {})
        status = ps.get("statusModule", {})
        sponsor = ps.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {})  # FIXED
        design = ps.get("designModule", {})
        nct = ident.get("nctId")                                                   # FIXED

        trials.append({
            "nct_id": nct,
            "title": ident.get("briefTitle"),
            "overall_status": status.get("overallStatus"),
            "start_date": status.get("startDateStruct", {}).get("date"),
            "study_type": design.get("studyType"),
            "phases": "|".join(design.get("phases", [])),
            "enrollment": design.get("enrollmentInfo", {}).get("count"),
            "lead_sponsor": sponsor.get("name"),
            "sponsor_class": sponsor.get("class"),
        })

        for loc in ps.get("contactsLocationsModule", {}).get("locations", []):
            sites.append({
                "nct_id": nct,
                "facility": loc.get("facility"),
                "city": loc.get("city"),
                "country": loc.get("country"),
                "site_status": loc.get("status"),
            })

        browse = st.get("derivedSection", {}).get("conditionBrowseModule", {})
        for kind in ("meshes", "ancestors"):
            for m in browse.get(kind, []):
                mesh.append({"nct_id": nct, "term": m.get("term"), "level": kind})

    return trials, sites, mesh                                                    # FIXED


COLUMNS = {
    "raw_trials": ["nct_id", "title", "overall_status", "start_date", "study_type",
                   "phases", "enrollment", "lead_sponsor", "sponsor_class"],
    "raw_sites": ["nct_id", "facility", "city", "country", "site_status"],
    "raw_mesh": ["nct_id", "term", "level"],                                      # FIXED
}


def main():
    trials, sites, mesh = flatten(read_studies(RAW))                              # FIXED
    if DB.exists():
        DB.unlink()            # start fresh each run
    con = duckdb.connect(str(DB))
    for name, rows in [("raw_trials", trials), ("raw_sites", sites),
                       ("raw_mesh", mesh)]:                                       # FIXED
        df = pd.DataFrame(rows, columns=COLUMNS[name])
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM df")
        print(f"{name}: {len(df):,} rows")
    con.close()


if __name__ == "__main__":
    main()