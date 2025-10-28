import pandas as pd
from geopy.distance import distance
from shapely.geometry import Point
import geopandas as gpd
from datetime import datetime

def load_highway_data(filepath):
    return gpd.read_file(filepath)

def load_user_coordinates(filepath):
    return pd.read_csv(filepath)

def buffer_point(point, crs, buffer_distance=0.0009):
    buffered_point = point.buffer(buffer_distance)
    return gpd.GeoDataFrame([{'geometry': buffered_point}], crs=crs)

def highway_used(gdf, current_point):
    buffer_distance = 0.0009
    buffered_point_gdf = buffer_point(current_point, gdf.crs, buffer_distance)
    result = gpd.sjoin(gdf, buffered_point_gdf)

    if not result.empty:
        highway_names = result['Highway'].unique()
        return highway_names[0]
    return None

def calculate_distance(point1, point2):
    return distance((point1.y, point1.x), (point2.y, point2.x)).km

def process_journey(gdf, user_coordinates, max_error=0.0008):
    """Process the user's journey and calculate distances per highway."""
    user_highway_distance = {}
    user_distance = 0
    last_point = None
    on_highway = False
    current_highway = None
    highway_entry_exit_points = []
    
    points = [Point(lon, lat) for lat, lon in zip(user_coordinates['latitude'], user_coordinates['longitude'])]
    timestamps = pd.to_datetime(user_coordinates['Timestamp'], format='%H:%M:%S')
    vehicle_number = user_coordinates['VehicleID'].iloc[0]
    start_time = timestamps.iloc[0]
    end_time = timestamps.iloc[-1]
    total_time_traveled = (end_time - start_time).total_seconds() / 60.0  # in minutes
    
    for idx, point in enumerate(points):
        try:
            current_point = point
            if last_point and current_point != last_point:
                dist = calculate_distance(last_point, current_point)
                user_distance += dist
                
                highway_detected = False
                for idx, row in gdf.iterrows():
                    line = row['geometry']
                    highway_name = row['Highway']
                    if current_point.distance(line) <= max_error:
                        highway_detected = True
                        if on_highway:
                            if current_highway == highway_name:
                                # Continue on the same highway
                                interp1 = line.interpolate(line.project(last_point))
                                interp2 = line.interpolate(line.project(current_point))
                                dist1 = interp1.distance(interp2) * 111.32
                                user_highway_distance[current_highway] = user_highway_distance.get(current_highway, 0) + dist1
                                if len(highway_entry_exit_points) % 2 == 0 or points[-1] == current_point:
                                    highway_entry_exit_points.append(current_point)
                            else:
                                # Switched to a different highway
                                on_highway = True
                                current_highway = highway_name
                                if len(highway_entry_exit_points) % 2 != 0:
                                    highway_entry_exit_points.append(current_point)
                        else:
                            # Just entered a highway
                            on_highway = True
                            current_highway = highway_name
                            if len(highway_entry_exit_points) % 2 == 0 or points[-1] == current_point:
                                highway_entry_exit_points.append(current_point)
                        break
                if not highway_detected and on_highway:
                    # Exiting a highway
                    on_highway = False
                    current_highway = None
                    if len(highway_entry_exit_points) % 2 != 0:
                        highway_entry_exit_points.append(current_point)
            last_point = current_point
        except Exception as e:
            print(f"Error: {e}")

    # After processing, check for highways bypassed (<= 100 meters)
    bypassed_highways = []
    for highway, dist in user_highway_distance.items():
        if dist <= 0.1:  # 100 meters
            bypassed_highways.append(highway)
    
    # Remove bypassed highways from the main distance dictionary
    for highway in bypassed_highways:
        user_highway_distance.pop(highway, None)
    
    return user_highway_distance, user_distance, highway_entry_exit_points, total_time_traveled, bypassed_highways, vehicle_number


def DataAnalysisuser(highway, userdata):
    # Load highway and user data
    gdf = load_highway_data(highway)
    user_coordinates = load_user_coordinates(userdata)

    # Assuming the file contains only one vehicle ID
    vehicle_data = user_coordinates

    # Process journey data
    user_highway_distance, user_distance, highway_entry_exit_points, total_time_traveled, bypassed_highways , vehicle_number= process_journey(gdf, vehicle_data)

    # Calculate and display results
    Usertotaldistance = round(user_distance, 2)
    Usertotaltime = round(total_time_traveled, 2)
    Total_km_on_highway = round(sum(user_highway_distance.values()), 2)
    Average_speed = round(user_distance / (total_time_traveled / 60.0), 2) if total_time_traveled else 0

    EachHighwayDistance = {highway: dist for highway, dist in user_highway_distance.items()}

    # Print results
    print("Total distance traveled by user:", Usertotaldistance, "km")
    print("Total time traveled by user (minutes):", Usertotaltime, "Min")
    print("Distance on each highway:")
    for highway, dist in EachHighwayDistance.items():
        print(f".  {highway}: {dist:.2f} km")
    print("Bypassed highways:")
    for highway in bypassed_highways:
        print(f".  {highway}")
    print("Total Km On Highway are:", Total_km_on_highway, "km")
    print("Average speed (km/h):", Average_speed, "KM/H")
    print('Vehcile Number:', vehicle_number)

    return Usertotaldistance, Usertotaltime, EachHighwayDistance, Total_km_on_highway, Average_speed, vehicle_number


def Total_Journey_Distance(starting_point, ending_point):
    if (starting_point == 'Mathura' and ending_point == 'Palwal') or (starting_point == 'Palwal' and ending_point == 'Mathura'):
        return 85.8
    elif (starting_point == 'Mathura' and ending_point == 'Hathras') or (starting_point == 'Hathras' and ending_point == 'Mathura'):
        return 44.83
    elif (starting_point == 'Mathura' and ending_point == 'Aligarh') or (starting_point == 'Aligarh' and ending_point == 'Mathura'):
        return 75.1
    elif (starting_point == 'Aligarh' and ending_point == 'Hathras') or (starting_point == 'Hathras' and ending_point == 'Aligarh'):
        return 29.5
    elif (starting_point == 'Aligarh' and ending_point == 'Palwal') or (starting_point == 'Palwal' and ending_point == 'Aligarh'):
        return 82.5
    elif (starting_point == 'Hathras' and ending_point == 'Palwal') or (starting_point == 'Palwal' and ending_point == 'Hathras'):
        return 120
    
    
