"""
build a staic world, create a car apply sensors, 
record images,
get information from world
apply navigation

"""

import pygame
import carla
import random
from carla import ColorConverter as cc
import numpy as np
from ..rl.environments.carla.sensors import Sensor
import sensors

def create_client(address: str, port, timeout):
    client = carla.Client(address,port)
    client.set_timeout(timeout)
    return client


class CarlaBaseEnv(object):
    def __init__(self, address = 'localhost', port = 2000, timeout = 10.0, town = 'Town01' ):
        self.client = create_client(address, port, timeout)
        self.world = self.client.get_world()
        self.map = None
        self.vehicle = None
        self.camera = None
        spawn_points = None
        self.synchronous_context = None
        self.restart(town,spawn_points)

    def restart(self, town: str, spwan_points = None):
        self.set_town(town)
        if(spwan_points is None):
            spwan_points = self.map.get_spawn_points()

        '''spwan vehicle'''
        blueprint = self.world.get_blueprint_library()
        vehicle_bp = random.choice(blueprint.filter('vehicle.*.*'))
        spwan_point = random.choice(spwan_points)
        self.vehicle = self.world.try_spawn_actor(vehicle_bp, spwan_point)

        '''set spectator camera'''
        self.set_spectator()

        # '''spwan camera'''
        # image_shape = ['400','300']
        # camera = Camera(self.vehicle,image_shape)
        # camera.set_sensor()
        # self.world.tick()
        # print("camera data: ")
        # print(camera.camera_data)

        my_sensors = {
            'camera' : 'sensor.camera.rgb',
            'collision' : 'sensor.other.collision'
        }

        camera_transforms = carla.Transform(
                carla.Location(x=-5.5, z=2.5), 
                carla.Rotation(pitch=8.0))
        sensor = Sensor(self.world, camera_transforms, my_sensors)

        for type in my_sensors.values:
            my_camera = sensor.create(type)
        



    def set_town(self,town: str):
        self.world = self.client.load_world(town)
        self.map = self.world.get_map()

    def set_spectator(self):
        spectator = self.world.get_spectator()
        spec_trans = carla.Transform(self.vehicle.get_transform().location + carla.Location(z = 20),
                                    carla.Rotation(pitch=-90))
        spectator.set_transform(spec_trans)


class Camera(object):
    def __init__(self,parent_actor,image_shape,recording = False):
        self.sensor = None
        self.recording = recording
        self._parent = parent_actor
        self.attachment = carla.AttachmentType.Rigid
        self.sensors = {
            'type':'sensor.camera.rgb',
            'color_converter': cc.Raw,
            'camera_name': 'Camera RGB'
            }
        self._camera_transforms = carla.Transform(
                carla.Location(x=-5.5, z=2.5), 
                carla.Rotation(pitch=8.0))
        world = self._parent.get_world()
        bp_library = world.get_blueprint_library()
        self.blp = bp_library.find(self.sensors.pop('type'))
        self.blp.set_attribute('image_size_x', image_shape[0])
        self.blp.set_attribute('image_size_y', image_shape[1])
        self.camera_data = None

    def set_sensor(self):
        if self.sensor is not None:
            self.sensor.destroy()
        self.sensor = self._parent.get_world().spawn_actor(
            self.blp,
            self._camera_transforms,
            attach_to= self._parent, 
            attachment_type = self.attachment
        )
   
    def convert_image(self, image: carla.Image, dtype=np.uint8, color_converter=None):
        color_converter = color_converter or self.color_converter or carla.ColorConverter.Raw
        image.convert(color_converter)

        array = np.frombuffer(image.raw_data, dtype=dtype)
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]
        return array
    
    
def main():
    world = CarlaBaseEnv()

if __name__=='__main__':
    main()