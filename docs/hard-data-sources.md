# Hard Data Sources

This page documents the current research-grade sources that are more defensible
than the existing proxy workflow. They are official survey programs with formal
data-access rules, not open scrape targets.

## Practical boundary

This repository supports three separate stages:

1. Official source discovery and documentation
2. Local raw-data discovery after you manually download approved files
3. Downstream cleaning and analysis

It does **not** attempt to automate login, approval, or download for restricted
survey files.

## Current acquisition status

Status checked and recorded on `2026-03-08`:

- `CHFS`: access application is still under review, so no local raw files have
  been downloaded into this repository yet.
- `CFPS`: account registration succeeded, but the dataset access request has not
  been approved yet, so raw data still cannot be downloaded.

Current implication for this repository:

- the research-grade `CFPS + CHFS` path is implemented at the code level, but
  is blocked at the data-acquisition stage
- until approval is granted, only metadata inspection, configuration templates,
  and fallback-source preparation can continue locally

## Blocked-state fallback

If both `CFPS` and `CHFS` remain unavailable, the remaining work splits into two
categories:

1. Keep the survey pipeline ready
   - preserve the local raw-data contract
   - preserve profiling, mapping, aggregation, and plotting scripts
   - wait for approved raw files

2. Prepare alternate evidence paths
   - public-access survey or archive sources if they expose downloadable
     microdata
   - official published tables that can support a weaker but still documented
     non-microdata analysis

This means the current repository is not blocked technically; it is blocked by
external data-access approval.

## Current next-step branches

At the current stage, the project has two practical branches.

### Branch A: continue waiting for approval

This is the stricter research path.

- keep waiting for `CFPS` approval
- keep waiting for `CHFS` approval
- once either source is approved, place the raw files into the repository and
  continue with the existing local pipeline

This branch preserves the strongest evidence chain, but progress depends on
external approval.

### Branch B: switch to a non-official civil-source database

This is the fallback path if the official survey approvals do not arrive in
time.

- look for a `民间数据库` or other non-official salary source
- accept that the evidence strength will be weaker than `CFPS` or `CHFS`
- keep the repository labeling explicit so the result is not mistaken for an
  official survey estimate

This branch can keep the project moving, but it changes the methodological
strength of the final chart.

## Recommended first path

Use both `CFPS` and `CHFS`, but treat them as survey-year sources instead of an
annual official series.

- `CFPS` is a strong first source for labor and household outcomes and is
  typically used in two-year waves.
- `CHFS` is a strong companion source for income and household finance, but its
  access workflow is also controlled by the official project.

## CFPS

### Official entry points

- Project home: `https://www.isss.pku.edu.cn/cfps/`
- English overview: `https://www.isss.pku.edu.cn/cfps/en/`
- Public-data application page: `https://www.isss.pku.edu.cn/cfps/sjzx/gksj/index.htm`
- Official data platform: `https://cfpsdata.pku.edu.cn/#/home`
- Peking University open-data mirror: `https://opendata.pku.edu.cn/dataverse/CFPS`
- Data user agreement: `https://www.isss.pku.edu.cn/cfps/en/data/DataUserAgreement/index.htm`
- Questionnaires: `https://www.isss.pku.edu.cn/cfps/en/documentation/questionnaires/index.htm`

### Why it is a hard source

- It is an official long-running national family panel survey.
- The project provides formal documentation, questionnaires, and data-use
  rules.
- It is suitable for research-grade wage or labor-income estimation after
  variable mapping and sample restriction.

### Access note

As checked on `2026-03-08`, the official public-data application guide states
that users register through the official CFPS platform or the PKU open-data
platform and can download public data after review. This reinforces the
repository design choice: acquisition is manual, while local processing is
automated.

### Recommended starting years

For this repository, start with survey years:

- `2016`
- `2018`
- `2020`
- `2022`

These are a practical initial target for survey-year charts and avoid pretending
that the data is annual.

## CHFS

### Official entry points

- Project home: `https://chfs.swufe.edu.cn/`
- Official data site mentioned in the latest public release notice:
  `http://chfser.swufe.edu.cn/datas/`
- Data use notice: `https://chfs.swufe.edu.cn/info/1041/2131.htm`
- General school-internal green-channel notice:
  `https://chfs.swufe.edu.cn/info/1041/2161.htm`
- `2021` public release notice:
  `https://chfs.swufe.edu.cn/info/1041/4051.htm`
- `2023` data description: `https://chfs.swufe.edu.cn/info/1041/3981.htm`
- Eighth-wave survey announcement: `https://chfs.swufe.edu.cn/info/1041/3931.htm`

### Why it is a hard source

- It is an official national household finance survey with strong income and
  household-finance relevance.
- The project publishes usage rules and official data descriptions.
- It is well suited to wage and income research once raw files are available and
  the selected income variables are harmonized.

### Access note

The official CHFS notices checked on `2026-03-08` show a mixed access model:

- the `2021` release notice points users to the official CHFS data site for
  real-name registration and download
- the `2023` trial-data notices describe a school-internal green-channel model
  with data-security-platform access and no local export

This means the repository must stay flexible: some waves may be downloadable to
local files, while others may require controlled-platform access.

### Recommended starting years

For this repository, start with survey years:

- `2017`
- `2019`
- `2021`
- `2023`

## Local raw-data contract

After you obtain the files through the official access process, place them under
the repository root in:

- `data/raw/cfps/`
- `data/raw/chfs/`

The current scaffold accepts these extensions:

- `.dta`
- `.sav`
- `.csv`
- `.xlsx`
- `.xls`

The first implementation phase only checks what is present locally and reports
the available survey years. It does not yet claim a final wage-by-education
estimate from these sources.
