# Continuous Data Integration System (CDIS)

The Continuous Data Integration System (CDIS) is a scalable platform designed to simulate the generation of sensor data, process this data, and visualize it using Flask. The architecture leverages Kafka for data streaming and SQLite for data storage.

## Components and Data Flow
 + data_generator.py: Generates simulated sensor data, temperature_datam humidity_data, and sesnor_logs_data  and pushes it to a Kafka topic.
 + data_processor.py: Consumes the Kafka-streamed data, processes it, and stores it in an SQLite database.
 + Flask App (app.py): Presents stored data in an interactive graph, updated every minute, showing average temperature and humidity alongside the latest logs by sensors, using Plotly for visualization.

 The data flow starts with the Data Generator, proceeds to the Data Processor, and finally gets visualized in the Flask app.

 ## Tables
 <img src="photo/diagram.png" alt="Tables" width="300"/>

## Prerequisites
 + Docker and docker-compose
 + Kubernetes (For this project, Minikube was used as the Kubernetes environment.)
 + Kafka
 + SQLite
 + Helm (for Kubernetes deployment)

## Jenkins Deployment with Docker-Compose
1. Navigate to the Docker directory
2. Execute the following command:
```
docker-compose up -d
```

This will set up Jenkins in a Docker container, exposing it on port 8080.

## Jenkins Pipeline Deployment
The system is designed to be deployed on Kubernetes using the provided Jenkins pipeline script in Groovy. The Jenkins pipeline does the following:

1. Checks out the main branch of the repository.
2. Installs pytest dependencies.
3. Runs unit tests.
4. Builds Docker images for data_generator, data_processor, and flask_app.
5. Pushes Docker images to DockerHub.
6. Deploys Persistent Volumes and Persistent Volume Claims for SQLite storage.
7. Deploys NodePort services.
8. Deploys the main applications to Kubernetes.

Reference the provided pipeline script in the ci-cd directory.

Note: All necessary unit tests are run as part of the Jenkins pipeline.

## Usage
Once the system is deployed, you can access the Flask application. If you are using Minikube, access the application via:
```
http://<minikube ip>:50000
```
Replace <minikube ip> with the actual IP address obtained from running `minikube ip`.
