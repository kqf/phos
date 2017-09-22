# Run on lxplus

Use following command to enable CVMS environment on lxplus machine. It will load packages and initialize a token if needed.

```bash

./setup-env.sh
```

# Setup docker image

The first step is to copy your ssh-key to the directory with the `Dockerfile`. Unfortunately `ln -s` doesn't work.
```bash
cd /path/to/Dockerfile
cp ~/.ssh/id_rsa .
```

Then change github user name in `Dockerfile` and build a base image with dependencies only. It will update the system and install all necessary packages.
```bash
docker build -t aliworker:physics .
```

Then log in to `aliworker`, and install `AliPhysics`:

```bash
docker run -it aliworker:physics
# Now you are working in aliworker:physics' shell


aliBuild build AliPhysics

# don't close the terminal, don't exit the container
```

The last step is to save changes
```bash
# In running docker container 
hostname

# copy the output of this command, it's a container ID
exit

# Now on your machine
docker commit <container ID> aliworker:physics
```


# Run
To run existing image use following command

```bash
docker run -v $HOME/path/to/workdir/:/alice/AliPhysics/PWGGA/PHOSTasks/workdir -it aliworker:physics


# For this repo run the script
./run-in-docker.sh
```