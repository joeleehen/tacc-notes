# Demo Notes
## UI Tweaks
We might wanna rethink abstracting the 'Disease Parameters' and 'Initial Cases' buttons behind the 'Set Scenario' dropdown.

Initial Cases/NPIs are listed in a table at the bottom of their respective modal windows before being submitted. Users want to *edit* the cases/interventions **inside the table** rather than having to delete and re-add.

We might have a typo in our catalog labels! Transmission, rather than severity, changes with disease. We should also check our preset values for each parameter (particularly Reproduction Number and Asymptomatic/Symptomatic Period), they say the vibes are off.

There was some confusion between Infection Fatality Rate and Case Fatality Rate. I think CFR is more clear to epidemiologists but small sample size.

We should add a line on the line-chart to denote when an NPI starts/stops.

$R_0$ doesn't necessarily capture socioeconomic situation, co-morbidities, confounding factors, or race. Do we allow for that level of granularity, or do we expect users to consider these externalities when setting an $R_0$ value?

NPIs can't be started on Day 0.

We should show attack rate after running the simulation.

Dr. Vinny wants to be able to specify an Incubation period. I'm not sure if this is distinct from asymptomatic period or just different verbiage for the same thing.

We should warn the user if they try to start a simulation without setting parameters or initial cases.

The table doesn't remember how the user has sorted the data. If you sort by descending infection rate, the table will flip back to alphabetical (default) order once a new day is calculated.

We should add a Statewide observation at the top of the table.
## Model Changes
Everything runs very quickly. This is probably because our `beta_scale` within the model is too low.

Public health people said our model doesn't behave the way they expect. We're currently modeling a *point source* spread (common with food-borne illnesses) with a single peak in infected count. They expect a *propagating* infection spread for airborne illnesses (or more particularly, for a disease with an $R_0 > 1$). Dr. Zaheer suggests looking into our model code to ensure we're actually using `reproductionNumber` in our calculations.
This is also why our model runs too quickly. No propagation means everything stabilizes faster.

Epidemiologists want us to pull from CDC [Social Vulnerability Index](https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html) to model disadvantaged groups.

## Pharmaceutical Interventions
From the Florida guy:
	Florida tells the federal government "I need 1 million antivirals for this specific region". After a lag period we distribute the antivirals within that region.