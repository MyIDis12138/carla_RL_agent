import logging
from datetime import datetime
import carla
import random
import numpy as np

# --------------
# Create world
# --------------

client = carla.Client('localhost',2000)
world = client.get_world()
world = client.load_world('Town01')


# --------------
# Spawn ego vehicle
# --------------

#get blueprint library
ego_bp = world.get_blueprint_library().find('vehicle.tesla.model3')

#set rolename for ego-vehicle
ego_bp.set_attribute('role_name', 'ego')
print('\nEgo role_name is set')

#set color for ego-vehicle
ego_color = random.choice(ego_bp.get_attribute('color').recommended_values)
ego_bp.set_attribute('color', ego_color)
print('\nEgo color is set')

#get spwan points
spawnpoints = world.get_map().get_spawn_points()
number_of_spwanpoints = len(spawnpoints)

if number_of_spwanpoints > 0:
    random.shuffle(spawnpoints)
    ego_transform = spawnpoints[0]
    #spawn ego vehicle
    ego_vehicle = world.spawn_actor(ego_bp,ego_transform)
else:
    logging.warning('Could not find any spawn points')

# --------------
# Spectator on ego position
# --------------
spectator = world.get_spectator()
world_snapshot = world.wait_for_tick()
spec_trans = carla.Transform(ego_vehicle.get_transform().location + carla.Location(z = 30),
                            carla.Rotation(pitch=-90))
spectator.set_transform(spec_trans)


# --------------
# Spawn attached RGB camera
# --------------
cam_bp = None
cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')
cam_bp.set_attribute("image_size_x",str(400))
cam_bp.set_attribute("image_size_y",str(300))
#camera applied relate transform
cam_location = carla.Location(2,0,1)
cam_rotation = carla.Rotation(0,180,0)
cam_transform = carla.Transform(cam_location,cam_rotation)
ego_cam = world.spawn_actor(cam_bp,
                            cam_transform,
                            attach_to=ego_vehicle, 
                            attachment_type=carla.AttachmentType.Rigid)
time_start = datetime.now().second
while True:
    ego_cam.listen()
    time_end = datetime.now().second
    if time_end-time_start > 30.0: 
        break
    else:
        continue

def callback(data):
    array = np.frombuffer(data.raw_data, dtype=np.uint8)
    array = np.reshape(array, (400, 300, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    return array
