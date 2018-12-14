# Run on lxplus

Use following command to enable CVMS environment on lxplus machine. It will load packages and initialize a token if needed.

```bash

./setup-env.sh
```


# Setup the environment
Use [`alidock`](https://github.com/dberzano/alidock). It's a set of scripts to automatize all the process connected with docker. It automatically manages images and selects the most recent base image compatible with the alisoft.

# Development
Copy analysis task to the docker volume
```bash
./copy-to-docker.sh
```

To modify the library structure do the following

```bash
# Add source files here in alphabetical order
#
vim $ALICE_PHYSICS/PWGGA/PHOSTasks/CMakeLists.txt

# Link sources in the hierarchical order
#
vim $ALICE_PHYSICS/PWGGA/PHOSTasks/PWGGAPHOSTasksLinkDef.h
```

# Setup docker image (deprecated)

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
docker run -v $HOME/alice/:/alice -it aliworker:physics
# Now you are working in aliworker:physics' shell

cd AliPhysics/
git remote add kqf git@github.com:kqf/AliPhysics
cd -
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

# Run (deprecated)
To run existing image use following command

```bash
docker run -v $HOME/path/to/workdir/:/alice/AliPhysics/PWGGA/PHOSTasks/workdir -it aliworker:physics


# For this repo run the script
./run-in-docker.sh
```

