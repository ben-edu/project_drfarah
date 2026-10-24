# Google Business Profile Live Baseline — 2026-10-24

> Location: Dr Farah VIP Urgent Care  
> Google location resource: `locations/6719840585856592244`  
> Source: live Google Business Profile connector via Windsor.ai  
> Purpose: preserve the before-state prior to broad profile changes.

## 1. Core identity

`FACT:` Public profile name: **Dr Farah VIP Urgent Care**

`FACT:` Open status: **OPEN**

`FACT:` Primary category: **Urgent care center**

Additional categories currently configured:

- Medical clinic
- Walk-in clinic
- IV therapy service
- Weight loss service
- Physical examination center

`FACT:` Primary phone: **(310) 467-0101**

`FACT:` Website: **https://drfarahvipurgentcare.com/**

`FACT:` Address:

- 9229 Wilshire Blvd
- Beverly Hills, CA 90210
- United States

`FACT:` Google reports Voice of Merchant = true.

`FACT:` No duplicate-location resource was returned in the baseline query.

`FACT:` Google Place ID: `ChIJF75Lm1G5woARtSl8dLk2BBs`.

## 2. Hours — material discrepancy found

Current live regular hours returned by Google:

- Monday: 8:30 AM–5:30 PM
- Tuesday: 8:30 AM–5:30 PM
- Wednesday: 8:30 AM–5:30 PM
- Thursday: 8:30 AM–5:30 PM
- Friday: **8:30 AM–4:30 PM**

The clinic-confirmed operating fact in the project is Monday–Friday 8:30 AM–5:30 PM Pacific Time, with the last patient accepted before 5:00 PM.

`RISK / CORRECTION CANDIDATE:` Friday GBP closing time conflicts with the clinic-confirmed regular hours.

Do not change it until the before-state is preserved and the clinic operating fact remains confirmed, then correct deliberately and record the date.

Current special-hours entries returned in the live configuration are historical entries for October 2–4, 2025. No current 2026 holiday schedule was established by this pull.

## 3. Reputation baseline

`FACT:` Current all-time rating returned by Google: **5.0**

`FACT:` Current all-time review count: **109**

This supersedes the prior screenshot baseline of 108 reviews.

Within the queried two-year review window, 104 reviews were returned with a 5.0 average.

## 4. Recent 90-day profile performance

For the most recent 90-day window queried through the connector:

- total impressions: **3,860**
- desktop Maps impressions: **387**
- desktop Search impressions: **631**
- mobile Maps impressions: **1,608**
- mobile Search impressions: **1,234**
- website clicks: **130**
- call clicks: **120**
- direction requests: **205**

These are profile interactions, not completed-patient outcomes.

## 5. Profile description

The current description positions Dr. Farah around acute care, emergency/family-medicine experience, rapid diagnosis/treatment and compassionate care.

`AUDIT NEED:` Review the wording against the current website positioning and operational scope. The description uses language such as “severe illnesses,” “critical moments,” “urgent treatment,” and “stabilizing patients in emergency situations.” Because the clinic is not an emergency department, this wording should be reviewed for accuracy and patient-expectation risk before optimization.

## 6. Services baseline — major complexity discovered

The live profile contains a large number of free-form service items across urgent care, medical clinic, IV therapy, weight loss and physical-examination categories.

Examples include:

- urgent care evaluations;
- wound/laceration repair;
- incision and drainage;
- respiratory conditions;
- urinary complaints;
- STI services;
- motor vehicle/personal injury;
- chest pain / shortness of breath evaluation;
- virtual consults and medication refills;
- labs and EKG;
- IV hydration / NAD+ / Myers cocktails;
- rejuvenation services;
- hormone replacement;
- weight-loss program;
- pre-op clearance.

Many service descriptions include specific prices, clinical claims, urgent/emergency language, medication references or treatment promises.

`RISK:` The service list is too consequential to edit piecemeal without a structured review. It creates factual, pricing, policy, expectation-management and maintenance risk.

`DECISION DIRECTION:` Preserve the current service list as evidence, then audit it against:

1. services actually offered now;
2. current approved pricing;
3. website service positioning;
4. Google Business Profile policy;
5. paid-advertising policy where the same service may later be promoted;
6. claims that require Dr. Farah approval;
7. whether each service materially helps local discovery or merely creates clutter.

## 7. Category interpretation

Primary category `Urgent care center` appears aligned with the core local-search use case and should not be changed casually.

Additional categories require evidence-based review rather than automatic removal. In particular:

- Medical clinic — plausible supporting category;
- Walk-in clinic — verify operational fit with actual appointment/walk-in process;
- IV therapy service — current service exists but marketing/policy positioning needs review;
- Weight loss service — health-sensitive marketing and service-policy review required;
- Physical examination center — potentially useful for pre-op/physical demand, but validate fit.

## 8. Immediate high-confidence actions after baseline acceptance

Potential near-term actions, subject to final verification/approval:

1. Correct Friday hours if clinic-confirmed 5:30 PM closing remains current.
2. Audit website and appointment links for source attribution.
3. Review the profile description for urgent-care vs emergency-room expectation clarity.
4. Classify and clean the service catalog rather than continuing to add services.
5. Establish a review-response/review-request operating cycle.
6. Analyze live search keywords and profile performance by month.
7. Compare GBP service/category choices with Search Console and paid-search demand once those sources are available.

## 9. Do not change yet

Until the service/category audit is completed, do not broadly:

- delete categories;
- remove large batches of services;
- rewrite the full profile;
- create duplicate/practitioner listings;
- change the business name for SEO;
- publish unverified medical/pricing claims.
