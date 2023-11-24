# robovisor
workspace pra desenvolver código ROS2 para o projeto de iniciação científica MAI/DAI Robovisor 
2023 sob supervisão do Prof. Dr. Roberto Inoue

## dependências

instalar as dependências Gazebo e slam_toolbox

```
$ sudo apt install ros-iron-gazebo*
$ sudo apt install ros-iron-slam-toolbox
$ sudo apt install ros-iron-navigation2
$ sudo apt install ros-iron-nav2*
```

## instalação

criar um workspace ros2:
```
$ mkdir -p robovisor_ws/src
$ cd robovisor_ws
$ colcon build
$ cd src
```
clonar o workspace localmente com ```git clone git@github.com:augustocamaral2003/robovisor.git```.
compilar novamente o ambiente com ```colcon build --symlink-install``` em ```robovisor_ws```.

## estrutura

- **urdf**
  
  contém descrição do robô em urdf, com macros para simulação em Gazebo e macros de inércia.

- **rviz**
  
  contém configs para visualização no rviz.

- **maps**
  
  contém mapas salvos mapeados por SLAM.

- **launch**
  
  contém launch files.

- **config**
  
  contém configs para o slam_toolbox e Nav2.

- **worlds**

  contém mapas salvos para excecução no Gazebo.

## launch files

- ```ros2 launch robovisor publisher.launch.py```

  inicia robot_state_publisher e rviz para visualização do robô.

- ```ros2 launch robovisor view.launch.py```

  inicia visualizador do robô.

- ```ros2 launch robovisor simulation.launch.py```

  inicia Gazebo com mapa padrão, inicializa robô na simulação.

- ```ros2 launch robovisor slam.launch.py use_sim_time:=true```

  inicia mapeamento SLAM.

- ```ros2 launch robovisor navigation.launch.py use_sim_time:=true```

  inicia navegação com Nav2.
