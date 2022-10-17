from docker.docker_functionality import *
from settings import settings

if __name__ == "__main__":

    # sudo screen -d -m sudo docker run --rm -p 2213:22 --gpus "device=0" -it --name torch_p0 torch_test_production:latest
    # SSH port range from settings file, check also that there are enough ports available
    # Taulu jossa ylläpidetään listaa GPU varauksista konttivaraukselle
    # Lista porttivarauksista konttivaraukselle
    # 2020 - 2200

    cont_details = {
      "name": f"tensorflow_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}",
      "image": "tensorflow",
      "username": "user",
      "cpus": 1,
      "memory": "1g",
      "shm_size": settings.docker["shm_size"],
      "ports": [ (2213, 22) ],
      "localMountFolderPath": settings.docker["mountLocation"],
      "password": "abc123"
    }

    cont_was_started, cont_name, cont_password = start_container(cont_details)

    # check running containers.
    print("Container was started: ", cont_was_started)
    print("Container name: ", cont_name)
    print("Docker.ps output:")
    print(docker.ps())

    send_email_container_started("riialin@gmail.com", "tensorflow", "localhost", 2213, "abc123")

    while True:
        command = input("stop or not")
        if command == "stop":
            docker.stop(cont_name)
            break
