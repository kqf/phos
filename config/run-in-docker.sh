local_path=$HOME/Study/phos/protons/tasks/analysis-task-pp/
docker_path=/alice/AliPhysics/PWGGA/PHOSTasks/PHOS_LHC16_pp
image=aliworker:physics


docker run -v $local_path:$docker_path -it $image