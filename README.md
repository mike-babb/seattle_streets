# Determine how often Seattle streets stop, start, and resume
## Michael Babb, PhD
### Created: July 1, 2024
### Updated:

# Seattle's (disconnected) Street Network
How many streets in Seattle are disconntinuous? A lot, it turns out. Another way to phrase this question is, "How frequently do roads in Seattle, start, stop, and resume? In Seattle, this typically looks like a road running for a few blocks, terminating, and then resuming a few blocks later. A prime example is Galer Street. Galer street is an east-west street that runs through the neighborhoods of Magnolia, Queen Anne, Capitol Hill, and Madison Park. This street is not continuous. The image below showcases portions of West Galer ST and East Galer ST.
![Galer](/graphics/galer.png)  
The streets colored black are the existing streets with discontinuities. The red lines are the "missing portions" joining the end of one section of street to another. (Note: this color scheme of red and black is used throughout this project in the graphics and maps.) In addition, Galer is separated into different streets based on city directional section and road type. Accordingly, there are five streets that feature the name "Galer" and three out of those five streets feature a discontinuity. (The number of discontinuities is equal to the number of portions minus one.) The table below summarizes the number of discontinuties in each portion of the street.  

| Street Name | Portions| Discontinuities|
|---|----|---|
|E Galer ST | 5| 4|
|Galer PL N | 1| 0|
|Galer ST | 2| 1|
|W Galer ST | 5 | 4|
|W Galer ST Flyover | 1 | 0|

The streets with the name Galer differ based on street prefix and street type. E Galer Street is found in the eastern portion of the city (Capitol Hill) and W Galer is found in the western portion of the city (Magnolia and Queen Anne). The suffix 'ST' indicates the road is of type "street" - a navigatable road - while the suffix 'PL' indicates the road is of type "Place", a road with a dead end that is accessible only from a larger street. One of the components driving the disconnected streets is the different sections of the city and when streets transition from one section to another. More on this in the future work section.

# City Sections
Seattle is divided into eight sections, basesd on compass directions. The eight sections can be seen in the image below.
![sections in Seattle](/graphics/seattle_sections.png) 
The map on the left features the sections identified by direction prefix or direction suffix. Roads without a direction prefix or suffix are label as No direction. Interestingly, the majority of roads without a direction prefix or suffix are located in the central business district. Throughout Seattle, streets run east/west and avenues run north/south. In the central business district, both streets and avenues are directionless. North of Denny way, streets are directionless while avenues are not. East of Broadway, streets feature a direction while avenues do not. Note that throughout the city, there are streets without a direction prefix or suffix, but this is limited to specific roads and road types (trails and interstates, for example). The image on the right is the convex hull surrounding each road type (after removing certain roads and typs). Before starting this project, I had a general idea about the extents of the city sections. These maps was helpful in diagnosing why some roads were being connected and some where not. I'll explain more about that in a bit. [Step 01](/code/step_01_import_export_street_data.ipynb) and [step 02](/code/step_02_export_nodes_seattle_streets.ipynb) identify the city sections on the streets and create these data.

# Data
The data powering this analysis is a single GeoPackage from the City of Seattle:
https://data-seattlecitygis.opendata.arcgis.com/datasets/783fd63545304bdf9d3c5f2065751614_0/explore

These are the streets in and near the City of Seattle. This dataset appears to be updated frequently, so I saved the version I downloaded at 2024/11/09 at 5:20 PM into the [/data](/data/Street_Network_Database_SND_5117857036965774451.gpkg) folder of this repo.  

# The technique
Finding discontinuities in Seattle streets is spread across three Jupyter notebooks with two notebooks containing additional analyses.
* [step_01_import_export_street_data.ipynb](/code/step_01_import_export_street_data.ipynb)
* [step_02_export_nodes_seattle_streets.ipynb](/code/step_02_export_nodes_seattle_streets.ipynb)
* [step_03_find_discontinuities.ipynb](/code/step_03_find_discontinuities.ipynb)
* [step_04_prepare_graphs_and_states.ipynb](/code/step_04_prepare_graphs_and_states.ipynb)
* [step_05_drawn_an_nx_graph.ipynb](/code/step_05_drawn_an_nx_graph.ipynb)

In `step 01`, the downloaded street network data is loaded as a GeoPandas GeoDataFrame and I perform some moderate data clean up. `Step 02` features additional data pre-processing and the creation of the city sections as seen in the figure above. After removing certain types of roads and roads within the City of Seattle, the count of segments decreases from ~34K to ~27K across 2,497 unique roads. In this case, a unique road includes both the road name, the road type, and direction prefix or suffix: `W GALER ST != GALER ST != E GALER ST`. `Step 03` features the identification of disconnected streets and the creation of segments joining the disconnected streets. These data are saved to a geopackage. In `step 04`, I conduct a series of analyses to better understand the distribution of the missing streets. In particular, I create a histogram of the added segements. Most missing segments are short: the average added segment length is a little less than a quarter of a mile. `Step 05` is a utility file that shows how to create a simple plot of the networkx graph. Also of interest is the [qGIS map](./maps/seattle_streets.qgz) showcasing many aspects of the missing streets. This map is fully symbolized and after running all of the notebooks, the layers should load appropriately. The image below is an overall picture of the addded streets.
![overall](/graphics/overall.png)

At the scale of the City - and due to the number of added street connections - it's hard to get a sense of the number of added streets. This image below is centered on north Capitol Hill and showcases many street disconnections.
![North Capitol Hill](/graphics/north_capitol_hill.png)
This image below is illustrative of many of the reasons for the street disconnections (check out Galer from West to East to get a sense of the  disconnections for understand the disconnections):
* Seattle’s topography
* Water features
* Parks / campuses / large plots of land
* Seattle’s development from downtown to current day boundaries 
* Annexation of older cities (differently aligned grids)
* State routes (520 / HW 99) and I-5

## Facts about the streets added:
* 2,497 roads in the study area | 1,933 road miles [(see this graphic for a comparison across road types)](/graphics/_all_streets_dist_count.png)
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
This figure features a number of descriptive statistics showcasing the distribution of the length of the added segments.
`Step 04` also features the creation of histograms for each street type and additional summary graphics.

# File Tree and File Description
 
├── README.md - This file  
├── code  
│   ├── run_constants.py - file paths used throughout the notebooks.
│   ├── step_01_import_export_street_data.ipynb - import data and perform minimal formatting.  
│   ├── step_02_export_nodes_seattle_streets.ipynb - curate the set of working streets, create the city sections.  
│   ├── step_03_find_discontinuities.ipynb - use NetworkX to identify discontinuities and create the missing segments.  
│   ├── step_04_prepare_graphs_and_states.ipynb - conduct analyses on the missing segments.
│   ├── step_05_drawn_an_nx_graph.ipynb - plot a NetworkX graph object of Galer. The plot changes everytime the code is run. 
│   ├── streets_to_remove.txt - a list (nine, as of 2024/12/25) of short  segments from the original data that can be removed. These are most likely erronneous data artifacts inadvertently left in during data. These were discovered by panning around an instance of qGIS visually identifying oddities. I have no doubt there are more to discover. In step 2, this file can be loaded and used to remove the erroneous segments.
│   └── utils.py - functions used throughout the notebooks.
├── data
│   ├── Seattle_City_Limits_3136622578314448116.gpkg - Seattle City Limits downloaded from the City of Seattle. Only used in the qGIS map.
│   ├── Street_Network_Database_SND_5117857036965774451.gpkg - Stree Network downloaded from the City of Seattle. This is the starting file.
|   ├── Street_Network_Database_Seattle_Central_Streets.csv - A list of Street IDs curated using qGIS. Included for use in Step 02.
│   └── blank_street_type_modified.xlsx - Roads with a manually created classification.
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
│   ├── __seattle_sections.png - maps of the sections in the City of Seattle.
│   ├── _all_streets_dist_count.png - barplot of the total miles by road type and road status.
│   ├── _all_streets_dist_histogram.png - histograms for all roads.
│   └── _all_streets_segment_count.png - barplot of the total number of segments by road type and road status.
├── maps  
│   └── seattle_streets.qgz  - qGIS map showcasing different aspects of the street type. After running all notebooks, this layer should load.
│   └── test_map.html - Initial attempt at creating a web map. 
└── seattles_disconnected_streets_2024_11_20.pptx - Presentation I gave to the [CUGOS](https://cugos.org/) group on November 20, 2024 showcasing the findings of this project and the next steps.

  
4 directories, 30 files


# Future work
Making v1.0 of this repo publically availably was my first goal. My next two goals are as follows:
1. Create a webmap to embed in either this repo or on a different blog. 




