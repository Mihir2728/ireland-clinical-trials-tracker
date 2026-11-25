# Lab notes

## Lab 0: ClinicalTrials.gov field paths
- NCT ID: protocolSection.identificationModule.nctId
- Lead sponsor: protocolSection.sponsorCollaboratorsModule.leadSponsor.name
- Phase: protocolSection.designModule.phases (a list)
- Start date: protocolSection.statusModule.startDateStruct.date
- Site country: protocolSection.contactsLocationsModule.locations[].country (one per site)

Example trial: NCT00567580, sponsor: Radiation Therapy Oncology Group (NETWORK), Phase 3, started 2008-02
Surprises:
- Search returns old trials too (2008), so I need a start-date filter
- overallStatus is UNKNOWN: the sponsor stopped updating it, so statuses aren't reliable
- Start date has only year and month, no day

## Lab 1A
- Total studies matching "Ireland": 3172 (all types and years, before any filtering)
- What I noticed about countries:
  - Most trials are multinational. Ireland is often one site among many.
    - Novartis Phase 3 (NCT07225504): 35+ countries across Europe, the Americas, Asia and Africa
    - Medtronic Vascular device trial (NCT06907147): 6 countries
    - Cytokinetics Phase 2 (NCT03160898): 6 countries incl. Australia, Canada, US
  - So "trial with an Irish site" ≠ "Irish trial". The tracker should count
    trials with at least one Irish site and say this clearly on the dashboard.
  - Many sponsors are non-Irish companies (US, Swiss) running global trials,
    so a sponsor with an Irish site may hire through a CRO rather than locally.
  - Start dates range from 2009 to 2025, so I need a start-date filter.
  - Phase "NA" = no drug phase (device/procedure studies like Medtronic's).

  Handled git amend, rebase, ignoring files and fixing a rejected push.

## Lab 2: Load into DuckDB
### Tables built (src/build_db.py)
- raw_trials: 3,172 rows (one per trial)
- raw_sites: 276,920 rows (one per site; big global trials list hundreds of sites)
- raw_mesh: 29,737 rows (MeSH condition terms + their broader "ancestor" categories)

### Query answers
a) Study types: INTERVENTIONAL 2,656 · OBSERVATIONAL 507 · EXPANDED_ACCESS 9
   → Keep interventional only, so ClinicalTrials.gov matches CTIS (which only holds interventional trials).
b) Trials with no site listed in Ireland: ____
   → Why: the "Ireland" search matches location text loosely (e.g. "Northern Ireland" sites, listed under United Kingdom), so I need an exact country filter.
c) Top 10 lead sponsors:
   1. ____ (__)
   2. ____ (__)
   3. ____ (__)
   ...
d) Trials by overall_status:
   ____ __ · ____ __ · ____ __
   My query: ____

### Therapeutic areas (MeSH ancestors, top results)
- Neoplasms 1,047 trials: cancer is by far the largest area
- Terms overlap (Neoplasms / Neoplasms by Site / by Histologic Type) and some are too generic
  ("Pathological Conditions, Signs and Symptoms"), so I'll need a mapping table to ~15 clean areas.

### Bugs I fixed
1. API gap: browseBranches wasn't in the response, so raw_branches was empty and pandas
   couldn't build a table with 0 columns. Fix: give each table a fixed column list, and
   use MeSH "meshes" + "ancestors" instead of branches.
2. NameError 'mesh': I renamed the list in one place but not the others.
   Fix: Find & Replace all, then search to confirm 0 matches.
3. Silent data bugs (no error, wrong data):
   - NCT ID read from the wrong place with the wrong case ("nctID" vs "nctId") → every ID was {}
   - Sponsor read one level too high (missed "leadSponsor") → every sponsor was None
   Lesson: .get() never crashes on a wrong key, it quietly returns the default.
   Always look at a few rows before trusting counts.

### Other lessons
- Save before running (the ● on a tab = unsaved). Turned on Auto Save.
- query.py needs the SQL after the filename; the ▶ button runs it with nothing, so sys.argv[1] fails.