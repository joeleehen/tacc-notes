# Meeting 2: 10/8/24
### On Case Fatality Rate
CFR is, in Lauren's words, a compound rate.
$$CFR = P(\text{I die} | \text{I'm already infected})$$
Is somebody going to die? If so, what's the expected number of days until death?
We're entering values between 0 and 1; 1 means they'll die with certainty if infected.

### Features
Lauren wants an 'all' option for applying NPIs statewide.

This is the second time that Lauren's opened the page on a small (probably mobile-sized) screen and mentioned it looks bad. While it shouldn't be a priority, it'd be nice to have an idea for a "mobile" layout.
I figure we already have a layout in mind for full-sized viewports. If we have a layout for skinny small screens, we can find in-between layouts to make sure the website always looks good.

### Fixes
Leaflet still renders each county weird. We think it happens when you zoom out of the Leaflet component and zoom into the webpage (or maybe vice-versa).  *Look into Leaflet docs/issues for a fix*.

Lauren will send text snippets to display on tooltip hover

The summary information on the left-hand pane doesn't update dynamically; you have to refresh the page to see NPIs you add. I think the solution here is to store the list of NPIs to be displayed as a state variable and use some React hook to re-render the `SavedParameters` component as needed.

### Things to Consider for the Future
Displaying summary info for NPIs is kinda gross. We should ask *how many NPIs* users expect to enter so we can design around that number. We're currently displaying all the information for each NPI, but maybe we want to rephrase it as a sentence (similar to how we summarize our initial cases):
```js
"NPI on day" {npi.name} "on Day" {npi.day} "in" {npi.location}
```
but this doesn't show any information about age group effectiveness.

Texas (and the c++ app) uses **Health Service Regions** to define large groups of counties at once for interventions.  Not all states use HSRs, Remy said that HSRs in New England span across states.
Massachusetts doesn't use counties for epidemiological stuff, they divide the state using *cities and towns*.
We'll probably have to account for county/city and HSRs on a state-by-state basis.

In the c++ app, vaccines and antivirals are administered through user-defined Priority Groups. These priority groups consist of a Risk Category and Age Group. For example:
	Lauren's Priority Group 1 is for High Risk people aged 5-24. Lauren's Priority Group 2 are for High Risk people aged 65+. Once we've administered everything to Priority Group 1, we make sure everyone in Priority Group 2 gets the intervention. Once they're good, we administer the intervention *pro rata*.
So we'll have to design a Priority Group form once we're ready to implement vaccines.

The models are pretty complex, especially once we start adding more interventions. With all the added functionality and user-definition that Lauren wants to add, handling data is gonna get complicated. During the demos next week, we should ask other epidemiologists what level of nuance they want and what we can get away with hardcoding/not adding.