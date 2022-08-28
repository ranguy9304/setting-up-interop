from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2
import png
from auvsi_server_params import URL, USERNAME, PASSWORD

import json
import os
import io
import PIL.Image as Image

from array import array

def get_obstacles(dictionary, mission):
    # message: StationaryObstacle (latitude, longitude, radius, height)
    obstacles = mission.stationary_obstacles
    dictionary["stationaryObstacles"] = []
    for indx in range(len(obstacles)):
        temp_dictionary = dict()
        curr_obstacle = obstacles[indx]
        temp_dictionary["latitude"] = curr_obstacle.latitude
        temp_dictionary["longitude"] = curr_obstacle.longitude
        temp_dictionary["radius"] = curr_obstacle.radius
        temp_dictionary["height"] = curr_obstacle.height
        dictionary["stationaryObstacles"].append(temp_dictionary)
    return dictionary

def get_flyzone(dictionary, mission):
    # message: FlyZone (altitude_min, altitude_max, boundary_points(type:position))
    flyzones = mission.fly_zones
    dictionary["flyZones"] = []
    for flyzone in flyzones:
        flyzone_dictionary = {"altitudeMax" : flyzone.altitude_max, "altitudeMin" : flyzone.altitude_min} # COOOOL GANG GANG
        flyzone_dictionary["boundaryPoints"] = []
        boundary_points = flyzone.boundary_points
        for indx in range(len(boundary_points)):
            curr_point = boundary_points[indx]
            temp_dictionary = dict()
            temp_dictionary["latitude"] = curr_point.latitude
            temp_dictionary["longitude"] = curr_point.longitude
            flyzone_dictionary["boundaryPoints"].append(temp_dictionary)
        dictionary["flyZones"].append(flyzone_dictionary)
    return dictionary

def get_waypoints(dictionary, mission):
    # message: Position(latitude, longitude, altitude)
    waypoints = mission.waypoints
    dictionary["waypoints"] = []
    for indx in range(len(waypoints)):
        curr_point = waypoints[indx]
        temp_dictionary = dict()
        temp_dictionary["latitude"] = curr_point.latitude
        temp_dictionary["longitude"] = curr_point.longitude
        temp_dictionary["altitude"] = curr_point.altitude
        dictionary["waypoints"].append(temp_dictionary)
    return dictionary

# --------------- #

def get_id(dictionary, mission):
    dictionary["id"] = mission.id    
    return dictionary

def get_lost_comms_pos(dictionary, mission):
    curr_point = mission.lost_comms_pos
    temp_dictionary = dict()
    temp_dictionary["latitude"] = curr_point.latitude
    temp_dictionary["longitude"] = curr_point.longitude
    dictionary["lostCommsPos"] = temp_dictionary
    return dictionary

def get_search_grid_points(dictionary, mission):
    search_grid_points = mission.search_grid_points
    dictionary["searchGridPoints"] = []
    for indx in range(len(search_grid_points)):
        curr_point = search_grid_points[indx]
        temp_dictionary = dict()
        temp_dictionary["latitude"] = curr_point.latitude
        temp_dictionary["longitude"] = curr_point.longitude
        dictionary["searchGridPoints"].append(temp_dictionary)
    return dictionary

def get_off_axis_odlc_pos(dictionary, mission):
    curr_point = mission.off_axis_odlc_pos
    temp_dictionary = dict()
    temp_dictionary["latitude"] = curr_point.latitude
    temp_dictionary["longitude"] = curr_point.longitude
    dictionary["offAxisOdlcPos"] = (temp_dictionary)
    return dictionary


def get_map_center_pos(dictionary, mission):
    curr_point = mission.map_center_pos
    temp_dictionary = dict()
    temp_dictionary["latitude"] = curr_point.latitude
    temp_dictionary["longitude"] = curr_point.longitude
    dictionary["mapCenterPos"] = (temp_dictionary)
    return dictionary


def get_map_height(dictionary, mission):
    dictionary["mapHeight"] = mission.map_height
    return dictionary

def get_emergent_last_known_pos(dictionary, mission):
    curr_point = mission.emergent_last_known_pos
    temp_dictionary = dict()
    temp_dictionary["latitude"] = curr_point.latitude
    temp_dictionary["longitude"] = curr_point.longitude
    dictionary["emergentLastKnownPos"] = (temp_dictionary)
    return dictionary


def get_air_drop_boundary_points(dictionary, mission):
    air_drop_boundary_points = mission.air_drop_boundary_points
    dictionary["airDropBoundaryPoints"] = []
    for indx in range(len(air_drop_boundary_points)):
        curr_point = air_drop_boundary_points[indx]
        temp_dictionary = dict()
        temp_dictionary["latitude"] = curr_point.latitude
        temp_dictionary["longitude"] = curr_point.longitude
        dictionary["airDropBoundaryPoints"].append(temp_dictionary)
    return dictionary

def get_air_drop_pos(dictionary, mission):
    curr_point = mission.air_drop_pos
    temp_dictionary = dict()
    temp_dictionary["latitude"] = curr_point.latitude
    temp_dictionary["longitude"] = curr_point.longitude
    dictionary["airDropPos"] = (temp_dictionary)
    return dictionary

def get_ugv_drive_pos(dictionary, mission):
    curr_point = mission.ugv_drive_pos
    temp_dictionary = dict()
    temp_dictionary["latitude"] = curr_point.latitude
    temp_dictionary["longitude"] = curr_point.longitude
    dictionary["ugvDrivePos"] = (temp_dictionary)
    return dictionary

# ------------------ #

def dictionary_to_json(dictionary, json_file_name):
    with open(f"{json_file_name}.json", "w") as json_file:
        json.dump(dictionary, json_file)
def readimage(path):
    count = os.stat(path).st_size / 2
    with open(path, "rb") as f:
        return bytearray(f.read())

def main():
    clientx = client.Client(url=URL, username=USERNAME, password=PASSWORD)
    mission = clientx.get_mission(1)
    mission_map_generator_dict = dict()
    mission_map_generator_dict = get_obstacles(mission_map_generator_dict, mission)
    mission_map_generator_dict = get_flyzone(mission_map_generator_dict, mission)
    mission_map_generator_dict = get_waypoints(mission_map_generator_dict, mission)
    mission_map_generator_dict = get_id(mission_map_generator_dict, mission)
    mission_map_generator_dict = get_lost_comms_pos(mission_map_generator_dict, mission)
    mission_map_generator_dict = get_search_grid_points(mission_map_generator_dict, mission)
    mission_map_generator_dict = get_off_axis_odlc_pos(mission_map_generator_dict, mission)
    mission_map_generator_dict = get_map_center_pos(mission_map_generator_dict, mission)
    mission_map_generator_dict = get_map_height(mission_map_generator_dict, mission)
    mission_map_generator_dict = get_emergent_last_known_pos(mission_map_generator_dict, mission)
    mission_map_generator_dict = get_air_drop_boundary_points(mission_map_generator_dict, mission)
    mission_map_generator_dict = get_air_drop_pos(mission_map_generator_dict, mission)
    mission_map_generator_dict = get_ugv_drive_pos(mission_map_generator_dict, mission)
    print(clientx.get_odlc_image(15))





    image = Image.open(io.BytesIO(clientx.get_odlc_image(12)))
    image.save("test.png")



    # print(mission_map_generator_dict)
    dictionary_to_json(mission_map_generator_dict, "condensed_mission2")

if __name__ == "__main__":
    main()

# print(mission)
# print()
# print(mission.search_grid_points[0].altitude)
# print(type(mission.search_grid_points[0].altitude))
# print(type(mission))
