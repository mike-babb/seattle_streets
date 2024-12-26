# Determine how often Seattle streets stop, start, and resume
## Michael Babb, PhD
### Created: July 1, 2024
### Updated:

# Seattle's (disconnected) Street Network
How many streets in Seattle are disconntinuous? A lot, it turns out. Another way to phrase this question is, "How frequently do roads in Seattle, start, stop, and resume? In Seattle, this typically looks like a road running for a few blocks, terminating, and then resuming a few blocks later. A prime example is Galer Street. Galer street is an east-west street that runs through the neighborhoods of Magnolia, Queen Anne, Capitol Hill, and Madison Park. This street is not continuous. Rather, it is separated into different streets based on city directional section and road type. There are five streets that feature the name "Galer" and three out of those five streets feature a discontinuity. (The number of discontinuities is equal to the number of portion minus one.)

The table below summarizes the number of discontinuties in each portion.

| Street Name | Portions| Discontinuities|
|---|----|---|
|E Galer ST | 5| 4|
|Galer PL N | 1| 0|
|Galer ST | 2| 1|
|W Galer ST | 5 | 4|
|W Galer ST Flyover | 1 | 0|

The streets with the name Galer differ based on street prefix and street type. E Galer Street is found in the Eastern Portion of the city and W Galer is found in the wester portion of the city. The suffix 'ST' indicates the road is of type "street" - a navigatable road - while the suffix 'PL' indicates the road is of type "Place", a road with a dead end that is accessible only from a main street. One of the components driving the disconnected streets is the different sections of the city and when streets transition from one section to another. 

# City Sections
Seattle is divided into eight sections, basesd on compass directions. The eight sections can be seen in the image below.
![sections in Seattle](/graphics/seattle_sections.png) 
The map on the left features the sections identified by direction prefix or direction suffix. Roads without a direction prefix or suffix are label as No direction. Interestingly, the majority of roads without a direction prefix or suffix are located in the central business district. Throughout Seattle, streets run east/west and avenues run north/south. In the central business district, both streets and avenues are directionless. North of Denny way, streets are directionless while avenues are not. East of Broadway, streets feature a direction while avenues do not. Note that throughout the city, there are streets without a direction prefix or suffix, but this is limited to specific roads and road types (trails and interstates, for example). The image on the right is the convex hull surrounding each road type (after removing certain roads and typs). Before starting this project, I had a general idea about the extents of the city sections. These maps was helpful in diagnosing why some roads were being connected and some where not. I'll explain more about that in a bit. [Step 01](/code/step_01_import_export_street_data.ipynb) and [step 02](/code/step_02_export_nodes_seattle_streets.ipynb) identify the city sections on the streets and create these data.

# Data
The data powering this analysis is a single GeoPackage from the City of Seattle:
https://data-seattlecitygis.opendata.arcgis.com/datasets/783fd63545304bdf9d3c5f2065751614_0/explore

These are the streets in and near the City of Seattle. This dataset appears to be
updated frequently, so I saved the version I downloaded into the [/data](/data/Street_Network_Database_SND_5117857036965774451.gpkg) of this repo. 
I downloaded a copy of the street network dataset on 2024/11/09 at 5:20 PM.

# The technique
Finding discontinuities in Seattle streets is spread across three Jupyter notebooks with two notebooks containing additional analysess.
* [step_01_import_export_street_data.ipynb](/code/step_01_import_export_street_data.ipynb)
* [step_02_export_nodes_seattle_streets.ipynb](/code/step_02_export_nodes_seattle_streets.ipynb)
* [step_03_find_discontinuities.ipynb](/code/step_03_find_discontinuities.ipynb)
* [step_04_prepare_graphs_and_states.ipynb](/code/step_04_prepare_graphs_and_states.ipynb)
* [step_05_drawn_an_nx_graph.ipynb](/code/step_05_drawn_an_nx_graph.ipynb)

In `step 01`, the downloaded street network data is loaded as GeoPandas GeoDataFrame and I perform some moderate data clean up. `Step 02` features additional data pre-processing and the creation of the city sections as seen in the figure above. After removing certain types of roads and roads within the City of Seattle, the count of segments decreases from ~34K to ~27K across 2,497 unique roads. In this case, a unique road includes both the road name, the road type, and direction prefix or suffix. In this case, `W GALER ST != GALER ST != E GALER ST`. `Step 03` features the identification of disconnected streets and the creation of segments joining the disconnected streets. These data are saved to a geopackage. In `step 04`, I conduct a series of analyses to better understand the distribution of created streets. In particular, I create a histogram of the added segements. Most missing segments are short: the average added segment length is a little less than a quarter of a mile. `Step 05` is a utility file that shows how to create a simple plot of the networkx graph.

## Facts about the streets added:
* 2,497 roads in the study area | 1,933 road miles
* 1,357 roads without discontinuities | 421 road miles
* 1,140 roads with discontinuities | 1,512 road miles
* 3,643 segments added across 1,140 roads | 834 miles 
* Average of ~3.2 segments per road
* Average segment length: ~0.23 Miles
* Median segment length: ~443 Feet
* Greatest number of segments added: 14
* (1ST AVE NW, 30TH AVE S, 35TH AVE S, W RAYE ST)
* Longest segment: ~5 Miles:  7Th PL S 
* Shortest segment: ~4 Feet: SW Cloverdale ST

Below is a histogram of the added streets:
![histogram of added streets](/graphics/_all_streets_dist_histogram.png)
This figure features a number of descriptive statistics showcasing the distribution of the length of the added segments. `Step 04` also features the creation of histograms for each street type.

# File Tree and File Description
 
├── README.md - This file  
├── graphics 
│   ├── AVE_dist_histogram.png - histograms for roads of type: Avenue  
│   ├── BLVD_dist_histogram.png - histograms for roads of type: Boulevard  
│   ├── CT_dist_histogram.png - histograms for roads of type: Court  
│   ├── DR_dist_histogram.png - histograms for roads of type: Drive  
│   ├── LN_dist_histogram.png - histograms for roads of type: Lane  
│   ├── PKWY_dist_histogram.png - histograms for roads of type: Parkway  
│   ├── PL_dist_histogram.png - histograms for roads of type: Place  
│   ├── RD_dist_histogram.png - histograms for roads of type: Road  
│   ├── ST_dist_histogram.png - histograms for roads of type: Street  
│   ├── WAY_dist_histogram.png - histograms for roads of type: Way  
│   ├── _all_streets_dist_histogram.png - histograms for all roads  
│   └── seattle_sections.png - maps of the sections in the City of Seattle  
├── code  
│   ├── step_01_import_export_street_data.ipynb - import data and perform minimal formatting.  
│   ├── step_02_export_nodes_seattle_streets.ipynb - curate the set of working streets, create the city sections.  
│   ├── step_03_find_discontinuities.ipynb - use NetworkX to identify discontinuities and create the missing segments.  
│   ├── step_04_prepare_graphs_and_states.ipynb - conduct analyses on the missing segments.
│   ├── step_05_drawn_an_nx_graph.ipynb  - plot a NetworkX graph object of Galer. The plot changes everytime the code is run. 
│   ├── streets_to_remove.txt - a list (nine, as of 2024/12/25) of short  segments from the original data that can be removed. These are most likely erronneous data artifacts inadvertently left in. These were discovered by panning around an instance of qGIS visually identifying oddities. I have no doubt there are more to discover.
│   └── utils.py  
├── data  
│   ├── Seattle_City_Limits_3136622578314448116.gpkg  
│   ├── Street_Network_Database_SND_5117857036965774451.gpkg  
│   ├── Street_Network_Database_Seattle_Central_Streets.csv  
│   └── blank_street_type_modified.xlsx  
├── dir_tree.txt  
├── maps  
│   └── seattle_streets.qgz  
├── seattles_disconnected_streets_2024_11_20.pptx  
└── test_map.html  
  
4 directories, 28 files







