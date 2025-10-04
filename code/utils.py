# mike babb
# 2025 10 03
# utility functions for seattle streets

# standard
import os
import re

# external
import geopandas as gpd
import math
import numpy as np
import pandas as pd
import shapely.geometry
from shapely.geometry import Point
from shapely.ops import linemerge


def subset_node_gdf(node_gdf:gpd.GeoDataFrame, other_node_df:pd.DataFrame):
    node_subset_gdf = pd.merge(left = node_gdf, right = other_node_df)
    return node_subset_gdf   

def create_city_sector(my_row:pd.Series) -> str:
    """Identifies the sector of the city the street is in.
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

def get_sort_order(sn):
    # simple function to return the numeric sector of a street name
    # if it is numeric, pad it with zeros
    re_outcome = re.findall(pattern=r'\d+', string = sn)
    if re_outcome:
        outcome = re_outcome[0]
        outcome = outcome.zfill(3)
    else:
        outcome = sn
    
    return outcome


def create_name(row):
    ostnc = row['ord_stname_concat']
    cp = row['city_sector']

    if cp not in ostnc:
        outcome = ostnc + ' ' + cp
    else:
        outcome = ostnc
    return outcome


if __name__ == '__main__':
    print('find those streets')