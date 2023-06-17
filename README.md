# Readme for IP Address Tracking Flask App

This is a Flask web application that tracks IP addresses of its visitors. It stores the IP addresses in a SQLite database and provides endpoints for viewing the IP addresses, viewing their reversals, and checking the health of the app.

## Application Structure
The application is built using Python's Flask framework and uses SQLAlchemy for interacting with the SQLite database.

Here's a brief overview of the main parts of the application:

- **Database setup**: The application uses SQLAlchemy, a Python SQL toolkit and Object-Relational Mapping (ORM) library, to interact with a SQLite database. The database file is located in the `instance` directory and is named `test.db`. A single table named `IP` is created in the database with two columns: `id` (a primary key) and `reversed_ip` (a string that stores the reversed IP address).

- **Logging**: The application uses Python's built-in logging module to log errors. The log file is named `app.log`.

- **Proxy Fix**: The application uses Werkzeug's `ProxyFix` middleware to get the correct IP address of the client when the app is deployed behind a proxy (like Nginx).

- **Flask routes**: The application has three routes: 
  - `/`: This route fetches the client's IP address, reverses it, checks if it already exists in the database, and if not, adds it to the database. The client's IP and its reversal are then displayed.
  - `/all`: This route fetches all reversed IP addresses from the database and displays them.
  - `/health`: This route checks the health of the application by running a simple SELECT query on the database. If the query is successful, it returns a positive response; if not, it returns a negative response.

- **Database creation**: If the `instance` directory does not exist when the application is started, it is created, and the database is initialized.

## Note
This application is intended to be run in a Kubernetes cluster. When deployed, a service of type `LoadBalancer` is created, which makes the application accessible from outside the cluster. The IP address logged by the application is the IP address of the client accessing the application, not the IP address of the pod running the application.

currently live on: http://a4ad3bf68b8fd4e5592201ee190a240c-76aca2ca093d6c7b.elb.us-east-2.amazonaws.com/

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- Docker
- Kubernetes cluster
- Helm v3 or newer
- kubectl command-line tool
- Jenkins CI/CD tool

<img src="./images/k8s-je.svg" width="50%" height="50%">
## Running Locally

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

1. Apply the Kubernetes manifest in the kubernetes folder:

    ```bash
    kubectl apply -f .
    ```

2. The application will be deployed on a network load balancer:

    ```bash
    kubectl get svc je-deel-test-service
    ```

The application will be available at the external IP or load balancer endpoint of the service.

### Deploying with Jenkins using Helm

1. Prepare your Jenkins server and add the SCM to poll from Jenkinsfile in the master branch:

    ```bash
    Click 'Build Now' or 

    merge to the master branch. 
    
    The pipeline will trigger and build, deploy the web app automatically.
    ```

2. Get the external IP of the service:

    ```bash
    kubectl get svc je-deel-test-service
    ```

The application will be available at the external IP or ELB endpoint of the service.

## CI/CD Pipeline

The CI/CD pipeline is configured using Jenkins. The pipeline runs on every push to the `master` branch. Here's what happens in each job:

1. **Install Dependencies**: Installs the required Python packages and Pylint for code quality checking.
2. **Unit Test**: Runs the unit tests using Python's unittest module.
3. **Pylint**: Performs static code analysis using Pylint.
4. **Build Image**: Builds the Docker image.
5. **Deploy Docker Image**: Pushes the Docker image to the Docker registry.
6. **Remove Unused Docker Image**: Removes the unused Docker image from the Jenkins agent.
7. **Deploy to Kubernetes**: Deploys the application to the Kubernetes cluster using the Helm chart.

All these steps are defined in the `Jenkinsfile` in the root directory of this repository.

## Helm Chart

The Helm chart, located in the je-deel-test-chart directory, is structured as follows:

Chart.yaml: This is the main file that includes the description of the Helm chart. It includes the version of the chart and the app version.

values.yaml: This file defines the default configuration values for this chart. It includes the replica count, image details, service details, resource requests and limits, and the details for the readiness and liveness probes.

templates/deployment.yaml: This file defines the Kubernetes Deployment for the application. It uses the values from values.yaml to set the number of replicas, the Docker image to use, the container port, and the readiness and liveness probes.

templates/service.yaml: This file defines the Kubernetes Service for the application. It uses the values from values.yaml to set the service type, port, and target port.

templates/hpa.yaml: This file defines the Horizontal Pod Autoscaler (HPA) for your application. It uses the values from values.yaml to set the minimum and maximum number of replicas and the CPU utilization threshold for scaling.

_helpers.tpl: This is a helper file that defines template functions used in other files in the chart. It includes functions for generating the name and fullname of the resources based on the chart and release names.

The Helm chart allows to package the web application and deploy it on a Kubernetes cluster with a single command, helm install. The values in values.yaml can be overridden at install time, allowing for flexibility and customization.

## Troubleshooting

If you encounter any issues, please check the logs of the pods. You can do this by running:

```bash
kubectl logs <pod-name>
