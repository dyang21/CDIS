pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: '9b392fc2-c43e-4faf-a5bd-1677bdc3160f', url: 'git@github.com:dyang21/Continuous-Data-Integration-System.git'
            }
        }
        stage('Install Pytest Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate; pip install -r test/pytest_requirements.txt'
            }
        }
        stage('Run Pytest') {
            steps {
                sh '. venv/bin/activate; pytest -v'
            }
        }
        stage('Build Docker images') {
            steps {
                script {
                    sh 'docker build -t data-generator -f Docker/Dockerfile/Dockerfile.datagenerator python/'
                    sh 'docker build -t flask-app -f Docker/Dockerfile/Dockerfile.flaskapp python/'
                    sh 'docker build -t data-processor -f Docker/Dockerfile/Dockerfile.dataprocessor python/'
                }
            }
        }
        stage('Push Docker images') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub_credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USER" --password-stdin'
                        sh 'docker tag data-generator $DOCKER_USER/data-generator:latest'
                        sh 'docker push $DOCKER_USER/data-generator:latest'
                        sh 'docker tag flask-app:latest $DOCKER_USER/flask-app'
                        sh 'docker push $DOCKER_USER/flask-app:latest'
                        sh 'docker tag data-processor:latest $DOCKER_USER/data-processor'
                        sh 'docker push $DOCKER_USER/data-processor:latest'
                    }
                }
            }
        }
        stage('Deploy PersistentVolume and PersistentVolumeClaim') {
            steps {
                sh('kubectl apply -f kubectl/pv-pvc/my-sensor-data-pv.yaml --kubeconfig /var/jenkins_home/kubeconfig.yaml')
                sh('kubectl apply -f kubectl/pv-pvc/my-sensor-data-pvc.yaml --kubeconfig /var/jenkins_home/kubeconfig.yaml')
            }
        }
        stage('Deploy NodePort') {
            steps {
                sh('kubectl apply -f kubectl/service/my-node-port.yaml --kubeconfig /var/jenkins_home/kubeconfig.yaml')
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh('kubectl apply -f kubectl/deployment/data-generator-deployment.yaml --kubeconfig /var/jenkins_home/kubeconfig.yaml')
                sh('kubectl apply -f kubectl/deployment/data-processor-deployment.yaml --kubeconfig /var/jenkins_home/kubeconfig.yaml')
                sh('kubectl apply -f kubectl/deployment/my-app.yaml --kubeconfig /var/jenkins_home/kubeconfig.yaml')
            }
        }
    }
    post {
        always {
            sh 'rm -rf venv'
        }
    }
}
