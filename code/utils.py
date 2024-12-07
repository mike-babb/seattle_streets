# mike babb
# 2024 06 28
# what streets start and stop?

# standard
import os

# external
import geopandas as gpd
import math
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns


def write_gdf(gdf: gpd.GeoDataFrame, output_file_path:str, output_file_name:str):
    
    ofpn = os.path.join(output_file_path, output_file_name)

    if 'coords' in gdf.columns:
        output_gdf = gdf.drop(labels = ['coords'], axis = 1)
        output_gdf.to_file(filename = ofpn, driver = 'GPKG', index = False)
    else:
        gdf.to_file(filename = ofpn, driver = 'GPKG', index = False)

    return None

def subset_node_gdf(node_gdf:gpd.GeoDataFrame, other_node_df:pd.DataFrame):
    node_subset_gdf = pd.merge(left = node_gdf, right = other_node_df)
    return node_subset_gdf
    


def points2distance(start, end, unit):
    """
    Calculate distance (in kilometers) between two points given as (long, latt) pairs
    based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula).
    Implementation inspired by JavaScript implementation from
    http://www.movable-type.co.uk/scripts/latlong.html
    Accepts coordinates as tuples (deg, min, sec), but coordinates can be given
    in any form - e.g. can specify only minutes:
    (0, 3133.9333, 0)
    is interpreted as
    (52.0, 13.0, 55.998000000008687)
    """
    # earths_radius_km = 6371 # kilometers
    # earths_radius_miles = 3959 # miles
    start_long = math.radians(start[0])
    start_latt = math.radians(start[1])
    end_long = math.radians(end[0])
    end_latt = math.radians(end[1])
    d_latt = end_latt - start_latt
    d_long = end_long - start_long
    a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2
    c = 2 * math.atan2(math.sqrt(a),  math.sqrt(1-a))

    if unit=="miles":
        earths_radius = 3959
    else:
        earths_radius = 6731
    # return the distance between the two points
    return earths_radius * c



if __name__ == '__main__':
    print('find those streets')