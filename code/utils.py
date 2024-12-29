# mike babb
# utility functions for seattle streets

# standard
import os

# external
import geopandas as gpd
import math
import numpy as np
import pandas as pd
from shapely.geometry import Point


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

def create_city_portion(my_row:pd.Series) -> str:
    """Identifies the portion of the city the street is in.
    Args:
        my_row (pd.Series): row from a pandas' dataframe

    Returns:
        str: concatenated street suffix prefix.
    """

    opd = my_row['ord_pre_dir']
    osd = my_row['ord_suf_dir']

    outcome = opd + ' ' + osd
    outcome = outcome.strip()
    # if the prefix is blank and the suffix is blank, mark the segment as being
    # in the center of the city
    if outcome == '':
        outcome = 'CNTR'    
    
    return outcome

def generate_street_end_vertices(gdf:gpd.GeoDataFrame) -> gpd.GeoDataFrame | gpd.GeoDataFrame:
    """ Generate a geodataframe with the street ends.
    Args:
        gdf (gpd.GeoDataFrame): Streets

    Returns:
        gpd.GeoDataFrame | gpd.GeoDataFrame: street network, street ends
    """    
    
    # export the vertex of each street end. 
    gdf['start_coord'] = gdf['geometry'].map(lambda x: x.coords[0])
    
    gdf['end_coord'] = gdf['geometry'].map(lambda x: x.coords[-1])
    
    f_node_gdf = gdf[['f_intr_id', 'start_coord']].copy().rename(columns = {'f_intr_id':'node_id',
                                                                           'start_coord':'coord'})
    t_node_gdf = gdf[['t_intr_id', 'end_coord']].copy().rename(columns = {'t_intr_id':'node_id',
                                                                         'end_coord':'coord'})
    
    # stack the datagrame
    node_df = pd.concat(objs = [f_node_gdf, t_node_gdf]).drop_duplicates()
    
    # make a gdf
    node_gdf = gpd.GeoDataFrame(data = node_df, geometry =
                                node_df['coord'].map(lambda x: Point(x)), crs = 'epsg:4326')
    
    node_gdf = node_gdf.drop(labels = ['coord'], axis = 1)

    # remove the start and end coordinates
    gdf = gdf.drop(labels = ['start_coord', 'end_coord'], axis = 1)
    
    return gdf, node_gdf

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