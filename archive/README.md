# Flask Application on Google Kubernetes Engine (GKE)

## Project Overview

This project is a simple **Python Flask application** that displays a greeting message along with the node/machine information it is running on. The application is containerized using Docker and deployed to **Google Kubernetes Engine (GKE)** using **Google Cloud Build** for CI/CD automation.

## Features

- **Simple Flask App**: Displays a greeting message and the node information.
- **Dockerized**: Easily build and run the application as a Docker container.
- **CI/CD Pipeline**: Automated builds and deployments using Google Cloud Build.
- **Scalable Deployment**: Deployed to GKE for auto-scaling and high availability.

## Prerequisites

- **Google Cloud SDK** installed and configured.
- A **GKE cluster** created.
- **Google Artifact Registry** or **Google Container Registry (GCR)** set up for storing Docker images.
- **Docker** installed locally for building images.
- A **Cloud Build trigger** configured for automatic deployments on code push.

## Project Structure

- **app.py**: Main Flask application file.
- **Dockerfile**: Instructions for building the Docker image.
- **requirements.txt**: Python dependencies for the project.
- **cloudbuild.yaml**: Cloud Build configuration file for CI/CD pipeline.
- **deployment.yaml**: Kubernetes manifest for deploying the application.
- **.gitignore**: List of files and directories to ignore in the repository.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2.  Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application Locally

```bash
python app.py
```

Visit [http://localhost:8080](http://localhost:8080) in your browser. You should see a message like:

```csharp
Hello, World from Flask! Served by node: <your-machine-name>, Hostname: <your-machine-name>
```

### 4. Build the Docker Image

```bash
docker build -t gcr.io/my-project/my-flask-app .
```

### 5. Push the Docker Image to Artifact Registry

```bash
docker push gcr.io/my-project/my-flask-app
```

### 6. Deploy the Application to GKE

Apply the Kubernetes manifest to your GKE cluster:

```bash
kubectl apply -f deployment.yaml
```

### 7. Access the Application

Get the external IP of the service and visit it in your browser:

```bash
kubectl get services
```

## CI/CD with Google Cloud Build

The project includes a `cloudbuild.yaml` configuration file for Google Cloud Build. The CI/CD pipeline:

1. Builds the Docker image.
1. Pushes the image to Google Artifact Registry.
1. Deploys the image to GKE.

To trigger a build manually:

```bash
gcloud builds submit --config=cloudbuild.yaml .
```

## Environment Variables

The following environment variables are used in the application:

- **NODE_NAME**: Provided by Kubernetes to display the node name.

## Additional Notes

- Ensure that your Cloud Build service account has the necessary IAM roles for deploying to GKE and pushing images to Artifact Registry.
- You can customize the `cloudbuild.yaml` and `deployment.yaml` files to fit your project needs.

## Troubleshooting

- If you encounter import errors for Flask, make sure you have activated your Python virtual environment.
- If the application does not display node information, check the environment variable configuration in your Kubernetes manifest.

## Licence

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any issues or questions, please open an issue in the repository or contact the maintainer:

- **Your Name**
- **Email**: your-email@example.com
- **GitHub**: your-username
