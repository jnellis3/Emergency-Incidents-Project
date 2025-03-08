## Requirements

Given an incident data, enrich it and then display the location and data on a map for easy validation. Try to utilize best practices where possible given available time. 

Enrichments
-----------
* Weather at the time of the incident (use a weather service of your choice, but https://dev.meteostat.net/ does include free historical queries).

Notes
-----
* Example incidents are provided in the data folder.
* We will test the project with an arbitrary incident file that is also from Richmond, VA and in the same format.
* It would be sufficient for the app to only handle one incident file at a time.
* The incident location and attributes should be displayed on a map in the browser.
* You can enrich the incident and get it on a map however you wish.
* We would like for you to spend up to 4 hours. It is okay if you spend less time or more time so long as you return the project within 24 hours of receiving it.
* Use the technology stack and approach of your choice.


## Plan of Action

Given my time constraints, I'm leaning towards using the [Datasette](https://docs.datasette.io/en/stable/) as the backend since I am familiar with using it for geo data.

On the front end, I want to have a map of Richmond displayed, a place at the top to upload new incidents, and a list of previously saved incidents at the bottom. Users will be able to select which incidents they would like overlayed on the map, and time-permitting, will be able to use a timeline slider to see the order in which the events occured.

For the map, I'd like to use the mapbox api to create the map and overlay data.