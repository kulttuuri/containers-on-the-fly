#! /usr/bin/python3
from python_on_whales import docker

def start_container(image, gpus, memory,port, user, folder, cpus, image_version="latest", remove=True, detatch=True):
    """
    image string
    gpus tuple
    memory int
    port int
    folder a string
    cpus int
    optionals:
    image_version_latest
    """
    # todo check if user folder exists, if not check where is space to create it
    # create folder

    # to deside, should we have folders for datasets? or should they be part of images


    docker.run(
        f"{image}:{image_version}",
        volumes=[(folder, f"/home/{user}")],
        #user=user,
        gpus=f"device={gpus}",
        name=user,
        memory=memory,
        remove=remove,
        cpus=cpus,
        publish=[(port,22)],
        detach=detatch,
        kernel_memory= memory
    )
    d = docker.execute(container=user, command=["echo '${USER}:pass' | chpasswd"])
    print(d)


if __name__ == "__main__":

    # sudo screen -d -m sudo docker run --rm -p 2213:22 --gpus "device=0" -it --name torch_p0 torch_test_production:latest
    cont = start_container("torch_test_production", 5, "48g",2218, "user", "/home/toni/user_folders/tonaalt", 8, remove=True)
    print(cont)
    # check running containers.
    print(docker.ps())

    while True:
        command = input("stop or not")
        if command == "stop":
            docker.stop("user")
            break
