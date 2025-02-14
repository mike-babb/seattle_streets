# RUN CONSTANTS

import os

# INPUT FILE PATH
INPUT_FILE_PATH = '../data' 

# OUTPUT FILE PATH
OUTPUT_FILE_PATH = '../../../project/seattle_streets/data'

# ANALYSIS FILE PATH
ANALYSIS_OUTPUT_FILE_PATH = os.path.join(OUTPUT_FILE_PATH, 'analysis')

################################################################################
# STEP 1 CONSTANTS
################################################################################

# STEP 1: INPUT STREET NETWORK - THE STREETS AS DOWNLOADED FROM THE CITY OF SEATTLE
S01_SND_IN_FILE_NAME = 'Street_Network_Database_SND_5117857036965774451.gpkg'

# STEP 1: OUTPUT STREET NETWORK - STREETS AFTER PERFORMING MINOR FORMATTING
S01_SND_OUT_FILE_NAME = 'Street_Network_Database_Complete.gpkg'

# STEP 1: OUTPUT EXCEL FILE - THE LIST OF STREETS THAT NEED MANUAL CLASSFIFICATION
S01_BST_OUT_FILE_NAME = 'blank_street_type.xlsx'

################################################################################
# STEP 2 CONSTANTS
################################################################################

# STEP 2: INPUT STREET NETWORK - STREETS AS CREATED IN STEP 1
S02_SND_IN_FILE_NAME = S01_SND_OUT_FILE_NAME

# STEP 2: OUTPUT NODES - STREET ENDS / STREET INTERSECTIONS
S02_NODE_OUT_FILE_NAME = 'Street_Network_Nodes.gpkg'

# STEP 2: INPUT EXCEL FILE WITH THE MANUALLY UPDATED STREET CLASSIFICATIONS
S02_BST_IN_FILE_NAME = 'blank_street_type_working.xlsx'

# STEP 2: OUTPUT STREET NETWORK - ALL STREETS IN SEATTLE
S02_SND_FULL_OUT_FILE_NAME = 'Street_Network_Database_Seattle_Full.gpkg'

# STEP 2: INPUT STREET NETWORK ID STREETS IN THE CITY CENTRAL PART OF THE CITY - MANUALLY CREATED USING qGIS
S02_CENTRAL_STREETS_IN_FILE_NAME = 'city_sector.csv'

# STEP 2: OUTPUT CITY SECTORS AS CREATED BY A CONVEX HULL AND CONCAVE HULL OPERATION
S02_CITY_SECTORS_OUT_FILE_NAME = 'city_sectors.gpkg'

# STEP 2: OUTPUT CITY SECTORS AS CREATED BY A CONVEX HULL AND CONCAVE HULL OPERATION - 
S02_CITY_SECTORS_LINES_OUT_FILE_NAME = 'city_sectors_lines.gpkg'

# STEP 2: OUTPUT STREET NETWORK - THE WORKING STREETS IN THE CITY OF SEATTLE
S02_SND_WORKING_OUT_FILE_NAME = 'Street_Network_Database_Seattle_working.gpkg'

################################################################################
# STEP 3 CONSTANTS
################################################################################

# STEP 3: INPUT STREETS - THE WORKING STREETS FROM STEP 2
S03_SND_WORKING_IN_FILE_NAME = S02_SND_WORKING_OUT_FILE_NAME

# STEP 3: MANUALLY CREATED GROUP NAMES
S03_STREET_GROUP_IN_FILE_NAME = 'street_groups_working.xlsx'

# STEP 3: CLEANED AND COMBINED STREET NAMES
S03_CLEANED_STREET_GROUP_OUT_FILE_NAME = 'Street_Network_Database_Seattle_working_edits.gpkg'

################################################################################
# STEP 4 CONSTANTS
################################################################################

# STEP 4: INPUT STREETS - THE WORKING STREETS FROM STEP 2
S04_SND_WORKING_IN_FILE_NAME = S03_CLEANED_STREET_GROUP_OUT_FILE_NAME

# STEP 4: INPUT NODES - THE NODES FROM STEP 2
S04_NODE_IN_FILE_NAME = S02_NODE_OUT_FILE_NAME

# STEP 4: SHORTEST SEGMENT ANALYSIS
S04_SS_COUNT_OUT_FILE_NAME = 'shortest_segment_count.xlsx'

# STEP 4: OUTPUT STREET NETWORK - THE CONTINUOUS, DISCONTINUOUS, AND THE ADDED SEGMENTS
S04_MISSING_OUT_FILE_NAME = 'missing_segments_v2.gpkg'

################################################################################
# STEP 5 CONSTANTS
################################################################################

# STEP 5: OUTPUT STREET ANALYSIS FILE
S05_ANALYSIS_OUT_FILE_NAME = 'street_analysis.xlsx'

# STEP 5: INPUT STREET NETWORK
S05_MISSING_IN_FILE_NAME = S04_MISSING_OUT_FILE_NAME

S05_STREET_CONNECTION_CHECK_FILE_NAME = 'check_connections.gpkg'

################################################################################
# STEP 6 CONSTANTS
################################################################################

# STEP 6: INPUT STREET NETWORK
S06_MISSING_IN_FILE_NAME = S04_MISSING_OUT_FILE_NAME

################################################################################
# STEP 7 CONSTANTS
################################################################################

# STEP 7: STREET GROUP EXCEL FILE NAME
S07_STREET_GROUP_OUT_FILE_NAME = 'street_groups.xlsx'

# STEP 7: INDIVIDUAL PLOTS OUTPUT PATH
S07_PLOT_OUTPUT_FILE_PATH = '../../../project/seattle_streets/print/individual_streets'

################################################################################
# STEP 8 CONSTANTS
################################################################################

# STEP 8: CITY SECTOR GROUP CHECK OUTPUT PATH
S08_CPG_OUTPUT_FILE_NAME = 'city_sector_check_working.xlsx'

# STEP 8: CITY PORITON GROUP PLOTS
S08_PLOT_OUTPUT_FILE_PATH_CITY_SECTOR_GROUPS = '../../../project/seattle_streets/print/city_sector_groups'

################################################################################
# STEP 9 CONSTANTS
################################################################################

################################################################################
# STEP 10 CONSTANTS
################################################################################

################################################################################
# STEP 11 CONSTANTS
################################################################################
S11_NON_OVERLAPPING_CITY_SECTORS_FILE_NAME = 'city_sectors_non_overlapping.gpkg'

S11_NON_OVERLAPPING_CITY_SECTORS_POLY_INNER_RING_BUFFER_FILE_NAME = 'city_sectors_non_overlapping_poly.gpkg'

S11_NON_OVERLAPPING_CITY_SECTORS_LINE_INNER_RING_BUFFER_FILE_NAME = 'city_sectors_non_overlapping_line.gpkg'





