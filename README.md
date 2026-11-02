# UK Vendor Bake-Off Prospecting Setup

This repository contains **public, non-sensitive workflow code and generic ICP configuration** for a small UK prospecting pilot using [LeadForge](https://github.com/AbdulrahmanAmer/leadforge).

## Safety boundary

- Do not commit prospect names, personal/business email lists, lead exports, CRM data, API keys, access tokens, or mailbox credentials.
- Do not upload LeadForge exports or workflow artifacts while this repository is public.
- The GitHub Actions workflow is manual and **plan-only**. It does not scrape prospects, export contact data, connect to the CRM, or send email.
- No outreach is sent by this project. Human approval remains mandatory for any future outreach.

## Pilot ICP

The configuration targets UK geospatial, GIS, mapping, location-intelligence and POI/data businesses in major UK hubs. It is a starting discovery profile, not proof that a company meets the final employee/turnover criteria. Every candidate must be checked against the CRM for duplicates and manually qualified.

## Run the safe plan

1. Open the **Actions** tab.
2. Select **LeadForge UK pilot (plan only)**.
3. Choose **Run workflow**.
4. Review the plan output. It should contain query/configuration planning only, not contact records.

The workflow installs the upstream LeadForge project temporarily on the runner and runs its planning command. It does not persist generated lead data.

## Next stage

Before any real lead collection, we must arrange a private destination for the output (for example, the existing private Google Sheets CRM) and verify that no personal data is exposed through public logs or artifacts. Do not change the workflow to scrape/export until that is in place.

LeadForge upstream project: https://github.com/AbdulrahmanAmer/leadforge
