##########################################################################################
### This script installs all requirements for the web servers to work on this machine. ### 
##########################################################################################

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "This script must be run with sudo privileges."
    exit 1
fi

echo "Running with sudo privileges."

# Update and install initial packages
sudo apt update

# TODO: NGINX
# TODO: MARIADB