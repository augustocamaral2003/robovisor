# robovisor
workspace pra desenvolver código ROS2 para o projeto de iniciação científica MAI/DAI Robovisor 
2023 sob supervisão do Prof. Dr. Roberto Inoue

## dependências

instalar as dependências Gazebo e slam_toolbox

```
$ sudo apt install ros-iron-gazebo*
$ sudo apt install ros-iron-slam-toolbox
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
  
  contém mapas para execução no Gazebo.

- **launch**
  
  contém launch files.

- **config**
  
  contém configs para o slam_toolbox.

## launch files

- ```ros2 launch robovisor robovisor_sp.launch.py```

  inicia robot_state_publisher e rviz para visualização do robô (no momento com erro ao calcular o
  transfer das rodas, apenas mostra visualização correta no rviz com Gazebo aberto.

- ```ros2 launch robovisor gazebo.launch.py world:=maps/maze.world```

  inicia Gazebo e carrega mapa labirinto.
