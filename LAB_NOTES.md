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