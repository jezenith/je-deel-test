
# Reverse IP Web Application


## Je-Deel-Test: Flask Application & Helm Chart

This repository contains a Flask application that captures and stores reversed IP addresses and a Helm chart to deploy it on a Kubernetes cluster. The application has two main routes: the root (`/`) that displays the client's IP address and the reversed IP, and `/all` that shows all reversed IPs stored so far.

The CI/CD pipeline ensures that any changes pushed to the main branch of the repository are tested, built into a Docker image, and deployed to the Kubernetes cluster.

### Prerequisites

1. Docker
2. Kubernetes cluster
3. Helm v3 or newer
4. kubectl command-line tool
5. Jenkins CI/CD tool
### Usage

Clone the repository:

```bash
git clone hhttps://github.com/jezenith/je-deel-test.git
cd je-deel-test
```

The Jenkins CI/CD pipeline will handle the rest: it will build the Docker image, push it to Docker registry, and deploy the application to the Kubernetes cluster using helm.

### CI/CD Pipeline

Our CI/CD pipeline is configured using Jenkins. The pipeline runs on every push to the `main` branch. Here's what happens in each job:

1. **Install Dependencies**: Installs the required Python packages and Pylint for code quality checking.

2. **Unit Test**: Runs the unit tests using Python's unittest module.

3. **Pylint**: Performs static code analysis using Pylint.

4. **Build Image**: Builds the Docker image.

5. **Deploy Docker Image**: Pushes the Docker image to the Docker registry.

6. **Remove Unused Docker Image**: Removes the unused Docker image from the Jenkins agent.

7. **Deploy to Kubernetes**: Deploys the application to the Kubernetes cluster using the Helm chart.

All these steps are defined in the `Jenkinsfile` in the root directory of this repository.

### URL of Deployed Application

The application is deployed and accessible at the Elb link from kubectl get svc -namespace prod  

http://a097c34b874164f4cbccd229c609a36d-71451285.us-east-2.elb.amazonaws.com/

### Troubleshooting

If you encounter any issues, please check the logs of the pods. You can do this by running:

```bash
kubectl logs <pod-name> -n prod
```

Replace `<pod-name>` with the name of the pod you're interested in.

### Contribute

---