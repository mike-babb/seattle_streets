# Determine how often Seattle streets stop, start, and resume
## Michael Babb, PhD
### Created: July 1, 2024
### Updated:

# Seattle's (disconnected) Street Network
How many streets in Seattle are disconntinuous? A lot, it turns out. Another way to phrase this question is, "How frequently do roads in Seattle, start, stop, and resume? In Seattle, this typically looks like a road running for a few blocks, terminating, and then resuming a few blocks later. A prime example is Galer Street. Galer street is an east-west street that runs through the neighborhoods of Magnolia, Queen Anne, Capitol Hill, and Madison Park. This street is not continuous. Rather, it is separated into different streets based on city directional section and road type. There are five streets that feature the name "Galer" and three out of those five streets feature a discontinuity. (The number of discontinuities is equal to the number of portion minus one.)

The table below summarizes the number of discontinuties in each portion.

| Street Name | Portions| Discontinuities|
|---|----|---|
|E Galer St | 5| 4|
|Galer PL N | 1| 0|
|Galer ST | 2| 1|
|W Galer ST | 5 | 4|
|W Galer ST Flyover | 1 | 0|

The streets with the name Galer differ based on street prefix and street type. E Galer Street is found in the Eastern Portion of the city and W Galer is found in the wester portion of the city. The suffix St indicates the road is of type "street" - a navigatable road - while the suffix PL indicates the road is of type Place, a road with a dead end that is accessible only from a main street. 






# Data
The data powering this analysis is a single GeoPackage from the City of Seattle
https://data-seattlecitygis.opendata.arcgis.com/datasets/783fd63545304bdf9d3c5f2065751614_0/explore

These are the streets in and near the City of Seattle. This dataset appears to be
updated frequently, so I saved the version I downloaded into the [/data](data) of this repo. 
I downloaded a copy of the streetnetwork dataset on 2024/11/09 at 5:20 PM.






