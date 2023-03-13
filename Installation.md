# Installation CARLA and ROS
Build CARLA from source, written by (https://github.com/MyIDis12138)

## Prerequisites
**System requirements**: 

* __Ubuntu 18.04.__ CARLA provides support for previous Ubuntu versions up to 16.04. **However** proper compilers are needed for Unreal Engine to work properly. Dependencies for Ubuntu 18.04 and previous versions are listed separatedly below. Make sure to install the ones corresponding to your system.
* __130 GB disk space.__ Carla will take around 31 GB and Unreal Engine will take around 91 GB so have about 130 GB free to account for both of these plus additional minor software installations. 
* __An adequate GPU.__ CARLA aims for realistic simulations, so the server needs at least a 6 GB GPU although 8 GB is recommended. A dedicated GPU is highly recommended for machine learning. 
* __Two TCP ports and good internet connection.__ 2000 and 2001 by default. Make sure that these ports are not blocked by firewalls or any other applications. 


   references:


      https://carla.readthedocs.io/en/0.9.10/build_linux/
      
      https://carla.readthedocs.io/en/0.9.10/ros_installation/


## Desktop Version Installation


### Install dependency packages
   ```
   sudo apt-get update &&
   sudo apt-get install wget software-properties-common &&
   sudo add-apt-repository ppa:ubuntu-toolchain-r/test &&
   wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add - &&
   sudo apt-add-repository "deb http://apt.llvm.org/$(lsb_release -c --short)/ llvm-toolchain-$(lsb_release -c --short)-14 main" &&
   sudo apt-get update
   ```

   ```
   sudo apt-get install build-essential clang-8 lld-8 g++-7 cmake ninja-build libvulkan1 python python-pip python-dev python3-dev python3-pip libpng-dev libtiff5-dev libjpeg-dev tzdata sed curl unzip autoconf libtool rsync libxml2-dev &&
   sudo apt install python-distro
   pip2 install --user setuptools &&
   pip3 install --user setuptools
   ```

### Env configuration
make sure that CARLA and UE use the same Clang version

   ```
   sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/lib/llvm-8/bin/clang++ 180 &&
   sudo update-alternatives --install /usr/bin/clang clang /usr/lib/llvm-8/bin/clang 180
   ```
- install git

   `sudo apt install git`

- [register UE account](https://www.unrealengine.com/) and [connect to your github](https://www.unrealengine.com/en-US/blog/updated-authentication-process-for-connecting-epic-github-accounts)

   you can verify your connection by checking if you can see the private repository [UnrealEngine ](https://github.com/EpicGames/UnrealEngine)
   
---
## Build Unreal engine and CARLA

1. install Unreal engine

   ```
   git clone --depth=1 -b 4.24 https://github.com/EpicGames/UnrealEngine.git ~/UnrealEngine_4.24
   cd ~/UnrealEngine_4.24
   ./Setup.sh && ./GenerateProjectFiles.sh && make
   ```

- If fail to clone, you need to generate a Personal access tokens to log in in `Settings ->  Developer settings -> Personal access tokens`. If you prefer .zip file, you could download and extract [4.24.3](https://github.com/EpicGames/UnrealEngine/archive/refs/tags/4.24.3-release.zip) then rename it to UrealEngine_4.24 and make.




2. check Unreal engine

   `cd ~/UnrealEngine_4.24/Engine/Binaries/Linux && ./UE4Editor`

   Please be careful at the first launch, it will take some time to finish compiling shaders.
   Then export your path to unreal engine to UE4_ROOT
   
   `export UE4_ROOT=~/UnrealEngine_4.24 #(change to your path to UE4)`  

3. Clone Carla Github

   ```
   cd ~
   git clone https://github.com/carla-simulator/carla
   cd ~/carla
   git checkout tags/0.9.10.1
   ./Update.sh
   ```

3. Make Carla 

   ```
   make PythonAPI #(complie Python API for client)
   make launch #(complie server)
   make LibCarla #(prepare the CARLA library to be imported anywhere)
   ```
   
   Alternatively, you can make PythonAPI with the python version you like, 
   
   ```
   make PythonAPI ARGS="--python-version=x.x"
   ```
   
   __Causion__: ROS Melodic(for ubuntu 16.04)/Kinetic(for ubuntu 18.04) users cannot use the latest CARLA release packages. Since 0.9.10 (included), CARLA does not provide support for Python2, so users will have to make the build from source, and compile the PythonAPI for Python2.
  
4. export .egg file

 - when you successfully make Python API, you will find a ` .egg ` file according to your python version at `carla/PythonAPI/carla/dist`, export the .egg to your PYTHONPATH will enable programs to import carla
   ```
   export PYTHONPATH = PTATH_TO_CARLA/PythonAPI/carla/dist/carla-0.9.10-py3.x-linux-x86_64.egg
   ```
- Alternatively, it can be installed with easy_install
   ```
   easy_install2 --user --no-deps PythonAPI/carla/dist/carla-0.9.10-py2.x-linux-x86_64.egg
   easy_install3 --user --no-deps PythonAPI/carla/dist/carla-0.9.10-py3.x-linux-x86_64.egg
   ```   

- the relationships in carla

 ![Screenshot from 2022-06-14 18-17-41](https://user-images.githubusercontent.com/91805924/173638143-dba2b6f9-2d65-4254-8551-04b0347cc3e1.png)



### test

- Start the server simulation 
   ```
   cd ~/carla
   make launch
   ```
   
   press play in carla UE4, and open another terminal window to run the example
   
   ```
   cd ~/carla/PythonAPI/examples
   python3 automatic_control.py
   ```
- If the simulation is running at very low FPS rates, go to Edit/Editor preferences/Performance in the UE editor and disable Use less CPU when in background.

### common issues in building

- ERROR: 'memory' file not found #include // boost.TR1 include order fix

   It may caused by ROS. If you have fully installed ROS in your system, maybe you are unable to make PthonAPI. This issue has been disscussed in https://github.com/carla-simulator/carla/issues/2792 and https://github.com/carla-simulator/carla/issues/4933. 


- ERROR: 'pyconfig.h' file not found 

   it may caused by conda environment, the issue is sovled by https://github.com/carla-simulator/carla/issues/199. If you do not install miniconda or anaconda before installation, I highly recommend not to install them before bulding carla. 

---
## ROS bridge installation for ROS 1

- install ROS according to operating system

   - [__ROS Kinetic__](http://wiki.ros.org/kinetic/Installation) — For Ubuntu 16.04 (Xenial)
 
   - [__ROS Melodic__](https://wiki.ros.org/melodic/Installation/Ubuntu) — For Ubuntu 18.04 (Bionic)
 
   - [__ROS Noetic__](https://wiki.ros.org/noetic#Installation) — For Ubuntu 20.04 (Focal)
 
- The version of Python needed to run the ROS bridge depends on the ROS version being used. 

  
  - __ROS Melodic and ROS Kinetic — Python2.__ 
  - __ROS Noetic — Python3.__ 
  
  
  
## Bridge installation Using source repository
A catkin workspace is needed to use the ROS bridge. It should be cloned and built in there. The following code creates a new workspace, and clones the repository in there. 

      
      # Setup folder structure
      mkdir -p ~/carla-ros-bridge/catkin_ws/src
      cd ~/carla-ros-bridge
      git clone https://github.com/carla-simulator/ros-bridge
      cd ros-bridge
      git checkout tags/0.9.10.1 #match your CARLA version
      git submodule update --init
      cd ../catkin_ws/src
      ln -s ../../ros-bridge
      source /opt/ros/melodic/setup.bash # Watch out, this sets ROS Melodic
      cd ..
      
      
      # Install required ros-dependencies
      rosdep update
      rosdep install --from-paths src --ignore-src -r
      
      # Build
      catkin_make
      
      
### Run the ROS bridge
1)  Run CARLA. The way to do so depends on the CARLA installation.
      -  Quick start/release package. `./CarlaUE4.sh` in `carla/`.
      -  Build installation. `make launch` in `carla/`. 

2)  Add the correct CARLA modules to your Python path
  
      ```
      export CARLA_ROOT=<path-to-carla>
      export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla/dist/carla-<carla_version_and_arch>.egg:$CARLA_ROOT/PythonAPI/carla
      ```
      You will need to add the appropriate `.egg` file to your Python path. You will find the file in either `/PythonAPI/` or `/PythonAPI/dist/` depending on the CARLA installation. Choose 2.x.egg file for ROS melodic and ROS Kinetic, 3.x.egg file for ROS Noetic.
      
      To check the CARLA library can be imported correctly, run the following command and wait for a success message:
      
      ```
       python3 -c 'import carla;print("Success")' # python3

       or

       python -c 'import carla;print("Success")' # python2
       ```
   
3)  Add the source path. The source path for the workspace has to be added, so that the ROS bridge can be used from a terminal.

   - Source for apt ROS bridge
   
      `source /opt/ros/melodic/setup.bash  #for ROS melodic `

   - Source for ROS bridge repository download.

      ` source ~/carla-ros-bridge/catkin_ws/devel/setup.bash `
   
      
      Important:  The source path can be set permanently, but it will cause conflict when working with another workspace. 
                  Before launch ros, make sure your default python(2.x or 3.x) fit your ros version 
                  
               
          # you could check your default python version by
          python --version
                  
          # your all python versions and their alternative
          sudo update-alternatives --config python
              
          # assign a larger weight than your default python
          sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 x # x represnts the weight
                  or 
          sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 x # x represnts the weight
                  
   
4) Start the ROS bridge. Use any of the different launch files available to check the installation. Here are some suggestions.

   ```
   # Option 1: start the ros bridge
   roslaunch carla_ros_bridge carla_ros_bridge.launch

   # Option 2: start the ros bridge together with RVIZ
   roslaunch carla_ros_bridge carla_ros_bridge_with_rviz.launch

   # Option 3: start the ros bridge together with an example ego vehicle
   roslaunch carla_ros_bridge carla_ros_bridge_with_example_ego_vehicle.launch
   ```
   

