import geopandas as gpd
import pandas as pd
import os

def extract_and_save_bounding_box_coordinates(shapefile_paths):
    for shapefile_path in shapefile_paths:
        # Load the shapefile using GeoPandas
        gdf = gpd.read_file(shapefile_path)
        
        # List to hold the bounding box coordinates for each polygon
        bounding_box_list = []
        
        for geom in gdf.geometry:
            if geom.geom_type == 'Polygon':
                polygons = [geom]
            elif geom.geom_type == 'MultiPolygon':
                polygons = geom.geoms
            else:
                continue
            
            for poly in polygons:
                # Calculate the bounding box for each polygon
                min_x, min_y, max_x, max_y = poly.bounds
                # Define the bounding box coordinates in the order: bottom-left, top-left, top-right, bottom-right, bottom-left
                bounding_box_coords = [
                    (min_x, min_y),  # bottom-left
                    (min_x, max_y),  # top-left
                    (max_x, max_y),  # top-right
                    (max_x, min_y),  # bottom-right
                    (min_x, min_y)   # back to bottom-left to close the polygon
                ]
                bounding_box_list.append({'polygon': bounding_box_coords})

        # Create a DataFrame and save to CSV
        df = pd.DataFrame(bounding_box_list)
        
        # Extract the base name of the shapefile without extension
        base_name = os.path.splitext(os.path.basename(shapefile_path))[0]
        
        # Create output CSV path
        output_csv_path = f'D:\\Thesis\\DATA\\Ground Truth\\Turkey 2023 Xiao Yu\\{base_name}_bounding_box_coordinates.csv'
        df.to_csv(output_csv_path, index=False)

        # Calculate the bounding box for the entire GeoDataFrame (min_x, min_y, max_x, max_y)
        min_x, min_y, max_x, max_y = gdf.total_bounds
        bounding_box = {
            'bottom_left': (min_x, min_y),
            'bottom_right': (max_x, min_y),
            'top_left': (min_x, max_y),
            'top_right': (max_x, max_y)
        }

        # Print the bounding box coordinates
        print(f"Bounding Box Coordinates for {shapefile_path}:")
        for key, value in bounding_box.items():
            print(f"{key}: {value}")

# Example usage
shapefile_paths = [
    'D:\\Thesis\\DATA\\Ground Truth\\Turkey 2023 Xiao Yu\\GT_ka_shps\\GT_ka_0.shp',
    'D:\\Thesis\\DATA\\Ground Truth\\Turkey 2023 Xiao Yu\\GT_ka_shps\\GT_ka_1.shp',
    'D:\\Thesis\\DATA\\Ground Truth\\Turkey 2023 Xiao Yu\\GT_ka_shps\\GT_ka_2.shp',
    'D:\\Thesis\\DATA\\Ground Truth\\Turkey 2023 Xiao Yu\\GT_ka_shps\\GT_ka_3.shp',
    'D:\\Thesis\\DATA\\Ground Truth\\Turkey 2023 Xiao Yu\\GT_ka_shps\\GT_ka_4.shp'
]

extract_and_save_bounding_box_coordinates(shapefile_paths)
