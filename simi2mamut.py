import simi
from mamut_xml_templates import *

# Convert Simi data into MaMuT XML format.

# TODO:
#   - This script should ultimately be a function within simi.py

# Incomplete list of spiral edges.
spiral_edges = [
        ['ABCD', 'AB'],
        ['ABCD', 'CD'],
        ['AB', 'A'],
        ['AB', 'B'],
        ['CD', 'C'],
        ['CD', 'D'],
        ['A', '1A'],
        ['A', '1a'],
        ['B', '1B'],
        ['B', '1b'],
        ['C', '1C'],
        ['C', '1c'],
        ['D', '1D'],
        ['D', '1d'],
        ['1A', '2A'],
        ['1A', '2a'],
        ['1a', '1a1'],
        ['1a', '1a2'],
        ['1B', '2B'],
        ['1B', '2b'],
        ['1b', '1b1'],
        ['1b', '1b2'],
        ['1C', '2C'],
        ['1C', '2c'],
        ['1c', '1c1'],
        ['1c', '1c2'],
        ['1D', '2D'],
        ['1D', '2d'],
        ['1d', '1d1'],
        ['1d', '1d2'],
        ]

# Parse a Simi BioCell .sbd file.
s = simi.Sbd('lineage.sbd')

# Declare initial variables.
spot_id = 1
last_frame = s.last_frame

# Lists aggregating spots and edges.
cell_edges = []

# Build template for spots per frame.
spots_per_frame = []
for f in range(0, last_frame + 1):
    spots_per_frame.append([])

# Iterate through cells.
for key, cell in s.valid_cells.items():
    # Define a list of edges.
    cell.spot_edges = []
    # Iterate through cell spots.
    for spot in cell.spots:
        # Define new id variable.
        spot.id = spot_id
        # Define new cell variable.
        spot.cell = key
        # Fix X value to MaMuT (based on CALIBRATION field of .sbc).
        spot.x = spot.x * 1.869565217
        # Fix Y value to MaMuT.
        spot.y = spot.y * 1.869565217
        # Fix Z value to MaMuT (multiply by 10).
        spot.z = spot.z * 10.0
        # Append spot to the list of his frame.
        spots_per_frame[spot.frame].append(spot)
        # Is this the first spot?
        spot_index = cell.spots.index(spot)
        # If not, create an edge (first spot is skipped).
        if spot_index != 0:
            # Create an edge using the previous spot as source and current spot as target.
            cell.spot_edges.append(edge_template.format(source_id=spot_id-1, target_id=spot_id))
        # Increment unique spot id.
        spot_id += 1
    # Define cell's source_id == the id of the last spot.
    cell.source_id = cell.spots[-1].id
    # Define cell's target_id == the id of the first spot.
    cell.target_id = cell.spots[0].id
    # Append cells to generate cell edges.
    cell_edges.append(cell)

# Begin XML file.
print(begin_template)

# Begin AllSpots.
print(allspots_template.format(nspots=spot_id))

# Loop through lists of spots.
for frame, spots in enumerate(spots_per_frame):
    if spots:
        print(inframe_template.format(frame=frame))
        for mamut_spot in spots:
            print(spot_template.format(id=mamut_spot.id, name=mamut_spot.cell, frame=mamut_spot.frame, x=mamut_spot.x, y=mamut_spot.y, z=mamut_spot.z))
        print(inframe_end_template)
    else:
        print(inframe_empty_template.format(frame=frame))

# End AllSpots.
print(allspots_end_template)

# Begin AllTracks.
print(alltracks_template)

# Begin Track.
print(track_template.format(id=0, duration=last_frame, stop=last_frame, nspots=spot_id))

# Get list of CD descendants.
cd = s.cells['CD'].get_descendants()

# Loop through cells printing cell and spot edges.
for cell in cell_edges:
    if cell.generic_name in cd.keys():
        if cell.parent:
            try:
                print(edge_template.format(source_id=cell.parent.source_id, target_id=cell.target_id))
            except:
                pass
        for edge in cell.spot_edges:
            print(edge)

# Loop through spot edges.
# for edge in spot_edges:
    # print(edge)

# # Loop through cell edges.
# for cell in cell_edges:
    # if cell.parent:
        # try:
            # print(edge_template.format(source_id=cell.parent.source_id, target_id=cell.target_id))
        # except:
            # pass

# End Track.
print(track_end_template)

# Begin Track.
print(track_template.format(id=1, duration=last_frame, stop=last_frame, nspots=spot_id))

# Get list of AB descendants.
ab = s.cells['AB'].get_descendants()

# Loop through cells printing cell and spot edges.
for cell in cell_edges:
    if cell.generic_name in ab.keys():
        if cell.parent:
            try:
                print(edge_template.format(source_id=cell.parent.source_id, target_id=cell.target_id))
            except:
                pass
        for edge in cell.spot_edges:
            print(edge)

# End Track.
print(track_end_template)

# End AllTracks.
print(alltracks_end_template)

# End XML file.
print(end_template)

