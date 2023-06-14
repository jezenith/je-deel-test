# Reverse IP Web Application

This is a simple Flask application that captures and stores reversed IP addresses. The application has two main routes: the root (`/`) that displays the client's IP address and the reversed IP, and `/all` that shows all reversed IPs stored so far.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- Docker
- Kubernetes cluster
- Helm v3 or newer
- kubectl command-line tool
- Jenkins CI/CD tool

![Alt text](./images/k8s-flow.svg)

### Running Locally

1. Clone the repository:

    ```bash
    git clone https://github.com/jezenith/je-deel-test.git
    cd je-deel-test
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python app.py
    ```

The application will be available at `http://localhost:5001`.

### Running with Docker

1. Build the Docker image:

    ```bash
    docker build -t je-deel-test .
    ```

2. Run the Docker container:

    ```bash
    docker run -p 5001:5001 je-deel-test
    ```

The application will be available at `http://localhost:5001`.

### Deploying with Kubernetes

Navigate to the Kubernetes folder:

1. Apply the Kubernetes manifest:

    ```bash
    kubectl apply -f k8s-manifest.yaml
    ```

2. The application will be deployed on a network load balancer:

    ```bash
    kubectl get svc je-deel-test-service
    ```

The application will be available at the external IP or load balancer endpoint of the service.

### Deploying with Jenkins using Helm

1. Prepare your Jenkins server and add the SCM to poll from Jenkinsfile in the master branch:

    ```bash
    Click 'Build Now' or do a merge to the master branch. The pipeline will trigger and build, deploy the web app automatically.
    ```

2. Get the external IP of the service:

    ```bash
    kubectl get svc je-deel-test-service
    ```

The application will be available at the external IP of the service.

## CI/CD Pipeline

The CI/CD pipeline is configured using Jenkins. The pipeline runs on every push to the `main` branch. Here's what happens in each job:

1. **Install Dependencies**: Installs the required Python packages and Pylint for code quality checking.
2. **Unit Test**: Runs the unit tests using Python's unittest module.
3. **Pylint**: Performs static code analysis using Pylint.
4. **Build Image**: Builds the Docker image.
5. **Deploy Docker Image**: Pushes the Docker image to the Docker registry.
6. **Remove Unused Docker Image**: Removes the unused Docker image from the Jenkins agent.
7. **Deploy to Kubernetes**: Deploys the application to the Kubernetes cluster using the Helm chart.

All these steps are defined in the `Jenkinsfile` in the root directory of this repository.

## Troubleshooting

If you encounter any issues, please check the logs of the pods. You can do this by running:

```bash
kubectl logs <pod-name>
