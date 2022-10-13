from docker.docker_functions import *

if __name__ == "__main__":

    # sudo screen -d -m sudo docker run --rm -p 2213:22 --gpus "device=0" -it --name torch_p0 torch_test_production:latest
    # SSH port range from settings file, check also that there are enough ports available
    # Taulu jossa ylläpidetään listaa GPU varauksista konttivaraukselle
    # Lista porttivarauksista konttivaraukselle
    # 2020 - 2200
    cont = start_container("databasecourse", 0, "1g", 2218, "user", settings.docker["mountLocation"], 1, remove=True)
    print(cont)
    # check running containers.
    print(docker.ps())

    while True:
        command = input("stop or not")
        if command == "stop":
            docker.stop("user")
            break
