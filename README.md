# Identifying Seattle's Discontinuous Streets
## Michael Babb, PhD
### Created: July 1, 2024
### Updated V1.0: December 31, 2024
### Updated V2.0: February 18, 2025

# Seattle's (discontinuous) Street Network
How many streets in Seattle are disconntinuous? Or, "How frequently do roads in Seattle, start, stop, and resume?" This typically looks like a road running for a few blocks, terminating, and then resuming a few blocks later. A prime example is Galer Street. Galer street is an east-west street that runs through the neighborhoods of Magnolia, Queen Anne, Capitol Hill, and Madison Park.  
<img src="./graphics/ex_11_galer_v2.png" alt="galer" width="1000" height="130"/>

[SEE THIS PAGE FOR v2.0 OF AN INTERACTIVE MAP OF THE ADDED STREETS](https://mike-babb.github.io/media/discontinuous_streets_v2.html)
[SEE THIS PAGE FOR v1.0 OF AN INTERACTIVE MAP OF THE ADDED STREETS](https://mike-babb.github.io/media/discontinuous_streets.html)

The streets colored black are the existing streets with discontinuities. The red lines are the "missing segments" joining the end of one section of a street to another. (Note: this color scheme of red and black is used throughout this project in the graphics and maps.) Galer is also separated into different streets based on city directional sector and road type. Accordingly, there are five streets that feature the name "Galer" and three out of those five streets feature a discontinuity. (The number of discontinuities is equal to the number of segments minus one. A segment is a portion of a street that runs for any length.) The table below summarizes the number of discontinuties in each street with 'Galer' in its name.

| Street Name | Segments | Discontinuities|
|---|----|---|
|E Galer ST | 5| 4|
|Galer PL N | 1| 0|
|Galer ST | 2| 1|
|W Galer ST | 5 | 4|
|W Galer ST Flyover | 1 | 0|

The streets with the name Galer differ based on street prefix and street type. E Galer Street is found in the eastern sector of the city (Capitol Hill) and W Galer is found in the western sector of the city (Magnolia and Queen Anne). The suffix 'ST' indicates the road is of type "street" - a navigatable road - while the suffix 'PL' indicates the road is of type "Place", a road with a dead end that is accessible only from a larger street. One of the components driving the discontinuous streets is the different sectors of the city and when streets transition from one sector to another. More on this in the future work section.

# City Sections
Seattle is divided into eight sectors, basesd on compass directions. The eight sectors can be seen in the image below.  
<img src="./graphics/seattle_sectors.png" alt="seattle sectors" width="1000" height="530"/>  

The map on the left features the sectors identified by direction prefix or direction suffix. Roads without a direction prefix or suffix are labeled as "No direction". The majority of roads without a direction prefix or direction suffix are located in the central business district. Throughout Seattle, streets run east/west and avenues run north/south. In the central business district, both streets and avenues are directionless. North of Denny way, streets are directionless while avenues are not. East of Broadway, streets feature a direction while avenues do not. Note that throughout the city, there are streets without a direction prefix or suffix, but this is limited to specific roads and road types (trails and interstates, for example). The image on the right is the convex hull surrounding each directional prefix / suffix (after removing certain roads and types). Before starting this project, I had a general idea about the extents of the city sectors. These maps was helpful in diagnosing why some roads were being connected and some where not. [Step 01](/code/step_01_import_export_street_data.ipynb) and [step 02](/code/step_02_export_nodes_seattle_streets.ipynb) identifies the city sectors on the streets and creates the convex hulls. And new for version 2.0, I create concave hulls in step 02 and I create non-overlapping sectors in [step 11](/code/step_11_prep_for_webmap.ipynb)

# Data
The data powering this analysis is a single GeoPackage from the [City of Seattle](https://data-seattlecitygis.opendata.arcgis.com/datasets/783fd63545304bdf9d3c5f2065751614_0/explore).

These are the streets in and near the City of Seattle. This dataset appears to be updated frequently, so I saved the version I downloaded on 2024/11/09 at 5:20 PM into the [data](/data/Street_Network_Database_SND_5117857036965774451.gpkg) folder of this repo.  

# The technique
Finding discontinuities in Seattle streets is accomplished across three Jupyter notebooks with eight notebooks containing additional analyses.
* [step_01_import_export_street_data.ipynb](/code/step_01_import_export_street_data.ipynb)
* [step_02_export_nodes_seattle_streets.ipynb](/code/step_02_export_nodes_seattle_streets.ipynb)
* [step_03_merge_data.ipynb](/code/step_03_merge_data.ipynb)
* [step_04_find_discontinuities.ipynb](/code/step_04_find_discontinuities.ipynb)
* [step_05_prepare_graphs_and_stats.ipynb](/code/step_05_prepare_graphs_and_stats.ipynb)
* [step_06_draw_an_nx_graph.ipynb](/code/step_06_draw_an_nx_graph.ipynb)
* [step_07_format_data_for_v2_plot_single_streets.ipynb](/code/step_07_format_data_for_v2_plot_single_streets.ipynb)
* [step_08_format_data_for_v2_plot_street_groups.ipynb](/code/step_08_format_data_for_v2_plot_street_groups.ipynb)
* [step_09_compare_edge_differences.ipynb](/code/step_09_compare_edge_differences.ipynb)
* [step_10_update_central_streets.ipynb](/code/step_10_update_central_streets.ipynb)
* [step_11_prep_for_webmap.ipynb](/code/step_11_prep_for_webmap.ipynb)


In `step 01`, the downloaded street network data is loaded as a GeoPandas GeoDataFrame and I perform some moderate data clean up. `Step 02` features additional data pre-processing and the creation of the city sectors as seen in the figure above. After removing certain types of roads and roads within the City of Seattle, the count of segments decreases from ~34K to ~27K across 2,457 unique roads. In this case, a unique road includes both the road name, the road type, and direction prefix or suffix. Under this schema, W GALER ST is not the same as GALER ST which is not the same as E GALER ST. In `Step 04` I use [GeoPandas](https://geopandas.org/en/stable/getting_started/introduction.html) and [NetworkX](https://networkx.org/) to identify discontinuous streets and create segments joining the discontinuous streets. There are ~~four~~ five NetworkX libraries I use to identify the discontinuous streets:
* [nx.from_pandas_edgelist()](https://networkx.org/documentation/stable/reference/generated/networkx.convert_matrix.from_pandas_edgelist.html) to create an undirected graph (nodes are intersections, edges are roads)
* [nx.connected_components()](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.connected_components.html) to identify discontinuities in the graph (discontinuous roads)
* [nx.non_edges()](https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.non_edges.html) to compute the set of possible edges to add (many possible ways to connect discontinuous street ends)
* [nx.k_edge_augmentation()](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.connectivity.edge_augmentation.k_edge_augmentation.html) to find the optimal edge to add (the path between discontinuous street ends guaranteeing full graph traversal)
* [nx.degree_centrality()](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.degree_centrality.html#networkx.algorithms.centrality.degree_centrality) is used to fine-tune the edge weighting so that street-ends are connected to street-ends. In practice, this means that a little over 30 streets have slightly different connectivity. See `step 09` for this analysis.

I then use various [shapely](https://shapely.readthedocs.io/en/stable/manual.html) objects to build the missing street segments as geospatial data and GeoPandas to collect and store these data. In `step 05`, I conduct a series of analyses to better understand the distribution of the added streets. I write out several worksheets to an Excel workbook in order to get a sense of the types of streets in Seattle. In particular, I create a histogram of the added segements. Most added segments are short: the average added segment length is a little less than a quarter of a mile. `Step 06` is a utility file that shows how to create a simple plot of W Galer ST as a NetworkX graph. Throughout this project I used this [qGIS map](./maps/seattle_streets.qgz) file to showcase many aspects of the added streets. This map is fully symbolized and after running all of the notebooks, the layers should load appropriately. The image below is an overall picture of the addded streets. Again, the red lines are the added streets joining discontinuous segements and the black lines are the existing streets. In v2.0, the blue lines are the lines connecting streets that cross the different city sectors.  
<img src="./graphics/ex_12_overall_v2.png" alt="overall" width="500" height="565"/>

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
* 2,497 roads in the study area | 1,932 road miles: see these graphics for a comparison of [miles](/graphics/barplot_miles.png) and [road segments](/graphics/barplot_segment_count.png)  
* 1,362 roads without discontinuities | 437 road miles  
* 1,135 roads with discontinuities | 1,495 road miles  
* 3,632 segments added across 1,135 roads | 832 miles   
* Average of ~3.2 segments added per uniquely named road
* Average added segment length: ~0.23 Miles
* Median added segment length: ~443 Feet
* Greatest number of segments added: [14 (1ST AVE NW, 30TH AVE S, 35TH AVE S, W RAYE ST)](/graphics/ex_04_most_added_segments.png)
* Longest segment: ~5 Miles:  [7TH PL S (10 longest added segment)](/graphics/ex_05_longest_added_segments.png)
* Shortest segment: ~4 Feet: [SW Cloverdale ST ](/graphics/ex_06_shortest_segment.png)

I particularly like the image of SW Cloverdale ST because it exemplifies how connectivity is in part a function of mode of travel. Clearly, a pedestrian can navigate around that barrier while a vechicle cannot.

Below is a histogram of the added streets:
![histogram of added streets](/graphics/histogram_ALL_streets.png)
This figure features a number of descriptive statistics showcasing the distribution of the length of the added segments. In general, most of the added segments are rather short, less than a quarter of a mile. Of all the added segments (3,632), 95% are less than one mile. `Step 04` creates this histogram and histograms for each street type and additional summary graphics.

# File Tree and File Description 
├── README.md - This file  
├── code  
│   ├── run_constants.py - file paths used throughout the notebooks.  
│   ├── step_01_import_export_street_data.ipynb - import data and perform minimal formatting.  
│   ├── step_02_export_nodes_seattle_streets.ipynb - curate the set of working streets, create the city sectors.  
│   ├── step_03_find_discontinuities.ipynb - use NetworkX to identify discontinuities and create the added segments.  
│   ├── step_04_prepare_graphs_and_stats.ipynb - conduct analyses on the added segments.  
│   ├── step_05_drawn_an_nx_graph.ipynb - plot a NetworkX graph object of Galer. The plot changes everytime the code is run.  
│   └── utils.py - functions used throughout the notebooks.  
├── data  
│   ├── Seattle_City_Limits_3136622578314448116.gpkg - Seattle City Limits downloaded from the City of Seattle. Only used in the qGIS map.  
│   ├── Street_Network_Database_SND_5117857036965774451.gpkg - Stree Network downloaded from the City of Seattle. This is the starting file.  
│   ├── Street_Network_Database_Seattle_Central_Streets.csv - A list of Street IDs curated using qGIS. Included for use in Step 02.  
│   ├── blank_street_type_modified.xlsx - Roads with a manually created classifications. Used to ensure that every road has a classification (AVE, WAY, PL, for example.)  
│   └── streets_to_remove.txt - a list (12, as of 2024/1/10) of short segments from the original data that can be removed. These are most likely erronneous data artifacts inadvertently left in during data processing by the City of Seattle. These were discovered by panning around a qGIS map visually identifying oddities. I have no doubt there are more to discover. In step 2, this file can be loaded and used to remove the erroneous segments.  
├── graphics  
│   ├── barplot_miles.png - barplot of the total miles by road type and road status.  
│   ├── barplot_segment_count.png - barplot of the total number of segments by road type and road status.  
│   ├── ex_01_galer.png - street segments added to Galer.    
│   ├── ex_02_overall.png - street segments added across the City of Seattle.  
│   ├── ex_03_north_capitol_hill.png - street segments added in north Capitol Hill.  
│   ├── ex_04_most_added_segments.png - streets with the most added segments.  
│   ├── ex_05_longest_added_segments.png - street with the longest added segments.  
│   ├── ex_06_shortest_segment.png - screenshot of the shortest added segment.  
│   ├── ex_07_51.png - street segments added for all roads named 51st.  
│   ├── ex_08_15th_ave_w.png - erroneous segments for 15TH AVE W.  
│   ├── ex_09_sw_florida_st.png - erroneous segments for SW FLORDIA ST.  
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
│   └── seattle_sections.png - maps of the sectors in the City of Seattle.  
├── maps  
│   ├── all_streets_diss.geojson - continuous, discontinous, and added roads in geojson format.  
│   ├── discontinuous_streets.html - interactive webmap featuring the continuous, discontinous, and added roads.  
│   └── seattle_streets.qgz - qGIS map showcasing different aspects of the added street types. After running all notebooks, this layer should load.  
└── seattles_discontinuous_streets_2024_11_20.pptx - Presentation I gave to the [CUGOS](https://cugos.org/) group on November 20, 2024 showcasing the motivation, findings, limitations and next steps of this project. This presentation encompasses a lot of the work as described in this `README.md` file.

# Future work
Making v1.0 of this repo publically availably was my first goal. My next two goals are as follows:  
1) ~~Create an interactive webmap to embed the results.~~ [Click here for an interactive webmap](https://mike-babb.github.io/media/discontinuous_streets.html)

2) Ensure connectivity is street-end to street-end. [nx.k_edge_augmentation()](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.connectivity.edge_augmentation.k_edge_augmentation.html) is phenomenal and very fast, especially when a pool of candidate edges of supplied. Those weight of the candidate edges is the straigt-line distance between any two nodes. Sometimes, the shortest edge connecting two discontinuous street segments is not street-end to street-end but sometimes street-end to mid-point. This is rare, but it has been observed upon visual inspection. This image showcases this phenomenon: 

<img src="./graphics/ex_10_woodlawn_ave_n.png" alt="woodlawn" width="500" height="528"/>


 One way to fix this is to use the [nx.degree_centrality](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.degree_centrality.html#networkx.algorithms.centrality.degree_centrality) to further winnow down the list of nodes that can be used to form connections between disconnected segments. The more connected the node, the more "central" is the node. In general, the nodes at the end of the street are going to be less connected than the nodes in the center of the road. Definitely something to incorporate in v2.0.

2) Connect streets based on name, not just street type. While it's easy to see that a case could be made to connect Galer across the city, other streets are less obvious. For example, there are many streets with the name '51st'. The image below showcases this phenomenon:  

<img src="./graphics/ex_07_51.png" alt="51st" width="500" height="648"/>

There are five streets that include 51st in the name: NE 51st ST, 51st AVE NE, 51st AVE SW, and 51st AVE S, and 51st PL S. (Only 4 are shown at this scale; 51st PL S is obscured by 51st AVE S.) Should 51st AVE S and 51st AVE NE be connected? Perhaps! Upon visual inspection, the two streets align to a quasi-grid. But then, so do most of the streets in Seattle. Version 2.0 will feature connections between streets that should mostly likely be connected. For example, W GALER ST will connect to GALER ST which will connect to E GALER ST. The best way to accomplish this is through a combination programmatic identification and manual review to create the template for the street connections. 
