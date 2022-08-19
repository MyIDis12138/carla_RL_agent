import random
import carla
import pygame
import cv2
import numpy as np

pygame.init()
pygame.font.init()
window_size = [600,600]


# def convert_image(image: carla.Image, dtype=np.uint8):
#     array = np.frombuffer(image.raw_data, dtype=dtype)
#     array = np.reshape(array, (image.height, image.width, 4))
#     array = array[:, :, :3]
#     array = array[:, :, ::-1]
#     return array

# def get_display(window_size, mode=pygame.HWSURFACE | pygame.DOUBLEBUF):
#     """Returns a display used to render images and text.
#         :param window_size: a tuple (width: int, height: int)
#         :param mode: pygame rendering mode. Default: pygame.HWSURFACE | pygame.DOUBLEBUF
#         :return: a pygame.display instance.
#     """
#     return pygame.display.set_mode(window_size, mode)


# def resize(image, size, interpolation=cv2.INTER_CUBIC):
#     """Resize the given image.
#         :param image: a numpy array with shape (height, width, channels).
#         :param size: (width, height) to resize the image to.
#         :param interpolation: Default: cv2.INTER_CUBIC.
#         :return: the reshaped image.
#     """
#     return cv2.resize(image, dsize=size, interpolation=interpolation)

# def display_image(display, image, window_size=(800, 600), blend=False):
#     """Displays the given image on a pygame window
#     :param blend: whether to blend or not the given image.
#     :param window_size: the size of the pygame's window. Default is (800, 600)
#     :param display: pygame.display
#     :param image: the image (numpy.array) to display/render on.
#     """
#     # Resize image if necessary
#     if (image.shape[1], image.shape[0]) != window_size:
#         image = resize(image, size=window_size)

#     if len(image.shape) == 2:
#         # duplicate image three times along depth if grayscale
#         image = np.stack((image,) * 3, axis=-1)

#     image_surface = pygame.surfarray.make_surface(image.swapaxes(0, 1))

#     if blend:
#         image_surface.set_alpha(100)

#     display.blit(image_surface, (0, 0))




#create client
client = carla.Client('localhost',2000)
client.set_timeout(10.0)

#set world connection
world = client.get_world()
world = client.load_world('Town01')

#managing the blueprint library
# get the world blueprint
blueprint_library = world.get_blueprint_library()



#spwan ego-vehicle
spectator = world.get_spectator()
vehicle_bp = random.choice(blueprint_library.filter('vehicle.*.*'))
#map.get_spawn_points() for vehicles; world.get_random_location() for walkers
spwan_points = world.get_map().get_spawn_points()
transform = random.choice(spwan_points)
vehicle: carla.Vehicle = None
vehicle = world.spawn_actor(vehicle_bp,transform)

# Wait for world to get the vehicle actor
world.tick()

world_snapshot = world.wait_for_tick()
actor_snapshot = world_snapshot.find(vehicle.id)


spec_trans = carla.Transform(vehicle.get_transform().location + carla.Location(z=50),
                            carla.Rotation(pitch=-90))
# Set spectator at given transform (vehicle transform)
#The spectator is a special type of actor created by Unreal Engine, 
#usually with ID=0, that acts as a camera and controls the view in the simulator window.
spectator.set_transform(spec_trans)


# Attach sensors on vechicle
camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '600')
camera_bp.set_attribute('image_size_y', '600')
attachment_type = carla.AttachmentType.Rigid
transform2 = carla.Transform(carla.Location(x=-8.0, z=6.0), carla.Rotation(pitch=6.0))
camera = world.spawn_actor(camera_bp, transform2, vehicle, attachment_type)
camera.listen(lambda image: image.save_to_disk('output/%06d.png' % image.frame))


print(vehicle.get_acceleration())



# camera = world.spawn_actor(rgb_camera_bp, 
#                             transform, 
#                             attach_to=vehicle, 
#                             attachment_type=Attachment.Rigid)


# #set weather, weather parameters are explained at https://carla.readthedocs.io/en/0.9.10/python_api/#carla.WeatherParameters
# weather = carla.WeatherParameters(
#     cloudiness=80.0,
#     precipitation=30.0,
#     sun_altitude_angle=70.0)
# world.set_weather(weather)

# #debug text
# debug = world.debug
# debug.draw_box(carla.BoundingBox(actor_snapshot.get_transform().location,
#                                 carla.Vector3D(0.5,0.5,2)),
#                                 actor_snapshot.get_transform().rotation, 
#                                 0.05, carla.Color(255,0,0,0),0)

