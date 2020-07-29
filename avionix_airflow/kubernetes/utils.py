from subprocess import check_output


def get_minikube_ip():
    return check_output(["minikube", "ip"]).decode("utf-8").strip()
