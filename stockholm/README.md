# Stockholm Program

**Disclaimer:** This program is intended solely for educational purposes and should not be used for any malicious activities. Always use responsibly and ethically.

## Introduction
Stockholm, is a program designed for educational use in a Linux environment. It encrypts and decrypts files using the AES256-CBC algorithm, providing options to reverse the encryption, display help, show version information, and manage silent mode.

## Requirements
- Operating system: Linux
- Virtual environment: Use a Docker container to build and run the Stockholm program.

## Usage
The Makefile provides several commands to manage the Docker container and the Stockholm program:

1. **Building the Docker Image**
   - Command: `make build`
   - Description: Builds the Docker image named "stockholm".

2. **Running the Docker Container**
   - Command: `make up`
   - Description: Starts the Docker container in detached mode using the "stockholm" image.

3. **Starting the Program**
   - Command: `make start`
   - Description: Executes the `make build` and `make up` commands consecutively.

4. **Stopping the Docker Container**
   - Command: `make stop`
   - Description: Stops all running Docker containers associated with the "stockholm" image.

5. **Purging Docker Containers**
   - Command: `make purge`
   - Description: Removes all stopped Docker containers related to the "stockholm" image.

6. **Rebuilding and Restarting**
   - Command: `make re`
   - Description: Stops all running containers, purges them, rebuilds the Docker image, and restarts the container.

## Execution Environment
- Ensure Docker is properly installed and configured on your system.
- Use the provided Makefile commands to manage the Docker container for the Stockholm program.

## Security Precautions
- Limit the usage of this program to educational purposes.
- Avoid deploying this program in sensitive or production environments to prevent unintended consequences.

Remember to handle the Stockholm program and Docker container with care and responsibility. Explore its functionalities in a controlled environment using the provided Makefile commands.