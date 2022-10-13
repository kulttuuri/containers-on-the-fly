#! /usr/bin/python3
from python_on_whales import docker
from send_emails import send_email
from datetime import datetime
import string
import secrets

ip = "10.103.6.20"

def create_password():
    possible_chars = string.ascii_letters + string.digits
    random_password = "".join(secrets.choice(possible_chars) for i in range(20))
    return random_password

def start_container(image, 
                    gpus, 
                    memory,
                    ssh_port,
                    jupyter_port, 
                    user, 
                    folder, 
                    cpus, 
                    email,
                    password=create_password(), 
                    image_version="latest", 
                    remove=True, 
                    detatch=True,
                    shm_size="16g",):
    """
    image string
    gpus tuple
    memory int
    port int
    folder a string
    cpus int
    password string
    optionals:
    image_version_latest
    """
    # todo check if user folder exists, if not check where is space to create it
    # create folder

    #todo: take ip of the machine from database, now everything is running in one machine, and 1 ip 

    # to deside, should we have folders for datasets? or should they be part of images

    container_name = f"{image}_{ssh_port}_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}"
    docker.run(
        f"{image}:{image_version}",
        volumes=[(folder, f"/home/{user}/persistent")],
        #user=user,
        gpus=f"device={gpus}",
        name=container_name,
        memory=memory,
        remove=remove,
        cpus=cpus,
        publish=[(ssh_port,22),(jupyter_port,8888)],
        detach=detatch,
        kernel_memory= memory,
        shm_size=shm_size
    )
    docker.execute(container=container_name, command=["/bin/bash","-c", f"/bin/echo 'user:{password}' | /usr/sbin/chpasswd"], user="root")
    
    body = f"""    Container {image} is ready to use. 
    You need to be in school network to accees the machine, 
    from home you can use studentVPN, to connect to machine.
    IP of the machine is {ip}, and port is {ssh_port}. connecting
    from unix terminal: ssh user@{ip} -p {ssh_port} 
    password is: {password}

    In case you are using jupyter lab, it will be forwarded
    to port {jupyter_port}, so use {ip}:{jupyter_port} + the token.
    
    NOTE! only files and folders from ~/persistent folder are
    saved after container stops, so save trained networks, 
    checkpoint files, logs, your datasets etc to that folder.

    THIS IS NOREPLY ACCOUNT, DO NOT REPLY TO THIS EMAIL
    If you need help contact: toni.aaltonen@samk.fi
    """

    send_email(email,"server is ready to use",body)

    return container_name

def kill_container(container_name):
    docker.stop(container_name)

if __name__ == "__main__":

    # sudo screen -d -m sudo docker run --rm -p 2213:22 --gpus "device=0" -it --shm-size=16gb --name torch_p0 torch_test_production:latest
    cont = start_container("tensorflow2_9_0",
                            1,#gpu id
                            "64g",# ram
                            2219,#port
                            8219,#jupyter-port
                            "user", 
                            "/home/toni/user_folders/tonaalt",
                            8,#cpu:s
                            "toni.aaltonen@samk.fi",
                            "oedEJJGR9hduh36gSKOFJ", 
                            remove=True)

    """
    cont = start_container("tensorflow2_9_0",
                            0,#gpu id
                            "128g",# ram
                            2220,#port
                            8220,#jupyter-port
                            "user", 
                            "/home/toni/user_folders/tonaalt",
                            16,#cpu:s
                            "toni.aaltonen@samk.fi",
                            "oedEJJGR9hduh36gSKOFJ", 
                            remove=True)
    """



    """
                            
                            5, #gpu id
                            "48g", # ram
                            2216, #port
                            8216, 
                            "user", 
                            "/home/toni/user_folders/juuso_lehtonen",
                            16,
                            "juuso.2.lehtonen@samk.fi", 
                            remove=True)
                         
    """

    print(cont)
    # check running containers.
    print(docker.ps())
    """
    while True:
        command = input("stop or not")
        if command == "stop":
            docker.stop(input(" give name of container to stop"))
            break
    """

