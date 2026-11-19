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