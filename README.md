# Identifying Seattle's disconnected Streets
## Michael Babb, PhD
### Created: July 1, 2024
### Updated: December 31, 2024

# Seattle's (disconnected) Street Network
How many streets in Seattle are disconntinuous? Or, "How frequently do roads in Seattle, start, stop, and resume?" This typically looks like a road running for a few blocks, terminating, and then resuming a few blocks later. A prime example is Galer Street. Galer street is an east-west street that runs through the neighborhoods of Magnolia, Queen Anne, Capitol Hill, and Madison Park.  
<img src="./graphics/ex_01_galer.png" alt="galer" width="1000" height="130"/>

The streets colored black are the existing streets with discontinuities. The red lines are the "missing portions" joining the end of one section of street to another. (Note: this color scheme of red and black is used throughout this project in the graphics and maps.) Galer is also separated into different streets based on city directional section and road type. Accordingly, there are five streets that feature the name "Galer" and three out of those five streets feature a discontinuity. (The number of discontinuities is equal to the number of portions minus one.) The table below summarizes the number of discontinuties in each portion of the street.  

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
<img src="./graphics/seattle_sections.png" alt="seattle sections" width="1000" height="530"/>  

The map on the left features the sections identified by direction prefix or direction suffix. Roads without a direction prefix or suffix are labeled as "No direction". The majority of roads without a direction prefix or suffix are located in the central business district. Throughout Seattle, streets run east/west and avenues run north/south. In the central business district, both streets and avenues are directionless. North of Denny way, streets are directionless while avenues are not. East of Broadway, streets feature a direction while avenues do not. Note that throughout the city, there are streets without a direction prefix or suffix, but this is limited to specific roads and road types (trails and interstates, for example). The image on the right is the convex hull surrounding each directional prefix / suffix (after removing certain roads and types). Before starting this project, I had a general idea about the extents of the city sections. These maps was helpful in diagnosing why some roads were being connected and some where not. [Step 01](/code/step_01_import_export_street_data.ipynb) and [step 02](/code/step_02_export_nodes_seattle_streets.ipynb) identifies the city sections on the streets and creates the convex hulls.

# Data
The data powering this analysis is a single GeoPackage from the City of Seattle:
https://data-seattlecitygis.opendata.arcgis.com/datasets/783fd63545304bdf9d3c5f2065751614_0/explore

These are the streets in and near the City of Seattle. This dataset appears to be updated frequently, so I saved the version I downloaded on 2024/11/09 at 5:20 PM into the [data](/data/Street_Network_Database_SND_5117857036965774451.gpkg) folder of this repo.  

# The technique
Finding discontinuities in Seattle streets is accomplished across three Jupyter notebooks with two notebooks containing additional analyses.
* [step_01_import_export_street_data.ipynb](/code/step_01_import_export_street_data.ipynb)
* [step_02_export_nodes_seattle_streets.ipynb](/code/step_02_export_nodes_seattle_streets.ipynb)
* [step_03_find_discontinuities.ipynb](/code/step_03_find_discontinuities.ipynb)
* [step_04_prepare_graphs_and_states.ipynb](/code/step_04_prepare_graphs_and_states.ipynb)
* [step_05_drawn_an_nx_graph.ipynb](/code/step_05_drawn_an_nx_graph.ipynb)

In `step 01`, the downloaded street network data is loaded as a GeoPandas GeoDataFrame and I perform some moderate data clean up. `Step 02` features additional data pre-processing and the creation of the city sections as seen in the figure above. After removing certain types of roads and roads within the City of Seattle, the count of segments decreases from ~34K to ~27K across 2,497 unique roads. In this case, a unique road includes both the road name, the road type, and direction prefix or suffix. Under this schema, W GALER ST is not the same as GALER ST which is not the same as E GALER ST. In `Step 03` I use [GeoPandas](https://geopandas.org/en/stable/getting_started/introduction.html) and [NetworkX](https://networkx.org/) to identify disconnected streets and create segments joining the disconnected streets. There are four NetworkX libraries I use to identify the disconnected streets:
* [nx.from_pandas_edgelist()](https://networkx.org/documentation/stable/reference/generated/networkx.convert_matrix.from_pandas_edgelist.html) to create an undirected graph (nodes are intersections, edges are roads)
* [nx.connected_components()](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.connected_components.html) to identify discontinuities in the graph (disconnected roads)
* [nx.non_edges()](https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.non_edges.html) to compute the set of possible “missing edges” (many possible ways to connect disconnected street ends)
* [nx.k_edge_augmentation()](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.connectivity.edge_augmentation.k_edge_augmentation.html) to find the optimal missing edge (the path between disconnected street ends guaranteeing full graph traversal)

I then use various [shapely](https://shapely.readthedocs.io/en/stable/manual.html) objects to build the missing street sections as geospatial data and GeoPandas to collect and store these data. In `step 04`, I conduct a series of analyses to better understand the distribution of the missing streets. I write out several worksheets to an Excel workbook in order to get a sense of the types of streets in Seattle. In particular, I create a histogram of the added segements. Most missing segments are short: the average added segment length is a little less than a quarter of a mile. `Step 05` is a utility file that shows how to create a simple plot of W Galer ST as a NetworkX graph. Throughout this project I used this [qGIS map](./maps/seattle_streets.qgz) file to showcase many aspects of the missing streets. This map is fully symbolized and after running all of the notebooks, the layers should load appropriately. The image below is an overall picture of the addded streets. Again, the red lines are the added streets joining disconnected segements and the black lines are the existing streets.    
<img src="./graphics/ex_02_overall.png" alt="overall" width="500" height="565"/>

At the scale of the city - and due to the number of added street connections - it's hard to get a sense of the number of added streets. This image below is centered on north Capitol Hill and showcases many street discontinuities (check out Galer from West to East, in particular).
<img src="./graphics/ex_03_north_capitol_hill.png" alt="North Capitol Hill" width="500" height="267"/>

This image below is illustrative of many of the reasons for the discontinuties in Seattle:  
* Seattle’s topography
* Water features
* Parks / campuses / large plots of land
* Seattle’s development from downtown to current day boundaries 
* Annexation of older cities (differently aligned grids)
* State routes (520 / HW 99) and I-5  

## Facts about the streets added:
* 2,497 roads in the study area | 1,933 road miles: see these graphics for a comparison of [miles](/graphics/barplot_miles.png) and [road segments](/graphics/barplot_segment_count.png)  
* 1,357 roads without discontinuities | 421 road miles  
* 1,140 roads with discontinuities | 1,512 road miles  
* 3,643 segments added across 1,140 roads | 834 miles   
* Average of ~3.2 segments per uniquely named road
* Average segment length: ~0.23 Miles
* Median segment length: ~443 Feet
* Greatest number of segments added: 14 (1ST AVE NW, 30TH AVE S, 35TH AVE S, W RAYE ST)
* Longest segment: ~5 Miles:  7Th PL S 
* Shortest segment: ~4 Feet: SW Cloverdale ST

Below is a histogram of the added streets:
![histogram of added streets](/graphics/histogram_ALL_streets.png)
This figure features a number of descriptive statistics showcasing the distribution of the length of the added segments. In general, most of the added segments are rather short, less than a quarter of a mile. `Step 04` creates this histogram and histograms for each street type and additional summary graphics.

# File Tree and File Description 
├── README.md - This file  
├── code  
│   ├── run_constants.py - file paths used throughout the notebooks.  
│   ├── step_01_import_export_street_data.ipynb - import data and perform minimal formatting.  
│   ├── step_02_export_nodes_seattle_streets.ipynb - curate the set of working streets, create the city sections.  
│   ├── step_03_find_discontinuities.ipynb - use NetworkX to identify discontinuities and create the missing segments.  
│   ├── step_04_prepare_graphs_and_states.ipynb - conduct analyses on the missing segments.  
│   ├── step_05_drawn_an_nx_graph.ipynb - plot a NetworkX graph object of Galer. The plot changes everytime the code is run.  
│   ├── streets_to_remove.txt - a list (nine, as of 2024/12/25) of short segments from the original data that can be removed. These are most likely erronneous data artifacts inadvertently left in during data processing by the City of Seattle. These were discovered by panning around a qGIS map visually identifying oddities. I have no doubt there are more to discover. In step 2, this file can be loaded and used to remove the erroneous segments.  
│   └── utils.py - functions used throughout the notebooks.  
├── data  
│   ├── Seattle_City_Limits_3136622578314448116.gpkg - Seattle City Limits downloaded from the City of Seattle. Only used in the qGIS map.  
│   ├── Street_Network_Database_SND_5117857036965774451.gpkg - Stree Network downloaded from the City of Seattle. This is the starting file.  
│   ├──  Street_Network_Database_Seattle_Central_Streets.csv - A list of Street IDs curated using qGIS. Included for use in Step 02.  
│   └── blank_street_type_modified.xlsx - Roads with a manually created classifications. Used to ensure that every road has a classification (AVE, WAY, PL, for example.)  
├── graphics  
│   ├── barplot_miles.png - barplot of the total miles by road type and road status.  
│   ├── barplot_segment_count.png - barplot of the total number of segments by road type and road status.  
│   ├── ex_01_galer.png - missing street sections added to Galer.    
│   ├── ex_02_overall.png - missing street sections added across the City of Seattle.  
│   ├── ex_03_north_capitol_hill.png - missing street sections added in north Capitol Hill.  
│   ├── ex_04_51.png - missing street sections for all roads named 51st.  
│   ├── histogram_ALL_streets.png - histogram for all roads.  
│   ├── histogram_AVE.png - histograms for roads of type: Avenue  
│   ├── histogram_BLVD.png - histogram for roads of type: Boulevard  
│   ├── histogram_CT.png - histogram for roads of type: Court  
│   ├── histogram_DR.png - histogram for roads of type: Drive  
│   ├── histogram_LN.png - histogram for roads of type: Lane  
│   ├── histogram_PKWY.png - histogram for roads of type: Parkway  
│   ├── histogram_PL.png - histogram for roads of type: Place  
│   ├── histogram_RD.png - histogram for roads of type: Road  
│   ├── histogram_ST.png - histogram for roads of type: Street  
│   ├── histogram_WAY.png - histogram for roads of type: Way  
│   └── seattle_sections.png - maps of the sections in the City of Seattle.  
├── maps  
│   ├── seattle_streets.qgz - qGIS map showcasing different aspects of the added street types. After running all notebooks, this layer should load.  
│   └── test_map.html - Initial attempt at creating a web map.  
└── seattles_disconnected_streets_2024_11_20.pptx - Presentation I gave to the [CUGOS](https://cugos.org/) group on November 20, 2024 showcasing the motivation, findings, limitations and next steps of this project. This presentation encompasses a lot of the work as described in this `README.md` file.

# Future work
Making v1.0 of this repo publically availably was my first goal. My next two goals are as follows:  
1) Create a webmap to embed in either this repo or a different blog. I'm currently exploring a combination of [PyScript](https://pyscript.net/) and [Folium](https://python-visualization.github.io/folium/latest/getting_started.html) to accomplish this. 
2) Connect streets based on name, not just street type. While it's easy to see that a case could be made to connect Galer across the city, other streets are less obvious. For example, there are many streets with the name '51st'. The image below showcases this phenomenon:  

<img src="./graphics/ex_04_51.png" alt="51st" width="500" height="648"/>

There are five streets named 51st: NE 51st ST, 51st AVE NE, 51st AVE SW, and 51st AVE S, and 51st PL S. Should 51st AVE S and 51st AVE NE be connected? Perhaps! Upon visual inspection, they align to a quasi-grid. But then, so do most of the streets in Seattle. Version 2.0 will feature connections between streets that should mostly likely be connected. For example, W GALER ST will connect to GALER ST which will connect to E GALER ST. The best way to accomplish this is to use a combination programmatic identification and manual review to create the combination. With approximately 2.5K uniquely named roads, that's a few hours work to identify logical groupings using python and then review for consistency.




