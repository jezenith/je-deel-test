
# Reverse IP Web Application

This is a simple Flask web application that takes the IP of the client and returns it in reversed order (e.g. 1.2.3.4 becomes 4.3.2.1). The reversed IP is also stored in a SQLite database.

## Installation

1. Ensure you have Python 3.8+ and pip installed.

2. Clone this repository:

   ```bash
   git clone https://github.com/jezenith/je-deel-test.git
   ```

3. Navigate into the cloned repository:

   ```bash
   cd je-deel-test
   ```

4. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the Flask application:

   ```bash
   python app.py
   ```

The application will be accessible at `http://localhost:5000/`.

## Database

The application uses a SQLite database to store the reversed IPs. The database file is `ips.db`.

## Testing

To test the application, simply navigate to `http://localhost:5000/` in your web browser. You should see a message displaying your reversed IP.

## Dockerization

To build a Docker image of the application, follow these steps:

1. Ensure you have Docker installed.

2. Build the Docker image:

   ```bash
   docker build -t reverse-ip-webapp .
   ```

3. Run the Docker container:

   ```bash
   docker run -p 5000:5000 reverse-ip-webapp
   ```

The application will be accessible at `http://localhost:5000/` in your web browser.

## Deployment on Kubernetes

1. Ensure you have `kubectl` and `helm` installed.

2. Create a new Kubernetes cluster or use an existing one.

3. Navigate to the `helm` directory:

   ```bash
   cd helm
   ```

4. Install the Helm chart:

   ```bash
   helm install reverse-ip-webapp .
   ```

The application should now be deployed on your Kubernetes cluster.

## CI/CD Pipeline

The application uses GitHub Actions for the CI/CD pipeline. The pipeline automatically builds the Docker image, pushes it to Docker Hub, and deploys it to the Kubernetes cluster whenever changes are pushed to the main branch of the repository.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
```

Replace `<your-github-username>` with your actual GitHub username. This README file provides instructions for installing, testing, Dockerizing, and deploying the application, as well as information on the CI/CD pipeline.