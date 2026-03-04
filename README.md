    ---

# 1. README Documentation

## Project: Two-Tier Web Application Deployment with Docker, Jenkins, and AWS

### Overview

This project demonstrates a **complete CI/CD pipeline** for deploying a two-tier web application using modern DevOps practices.

The system automates the process of:

* Pulling source code from GitHub
* Building and running Docker containers
* Deploying the application on AWS EC2
* Using Jenkins to automate the deployment process

The application consists of:

Frontend: Flask Web Application
Backend: MySQL Database

Deployment and automation are handled using:

* Docker
* Docker Compose
* Jenkins
* GitHub
* AWS EC2

---

## Architecture

System flow:

Developer → GitHub → Jenkins → EC2 → Docker Containers → End User

Components:

**Developer (Admin)**
Pushes code changes to GitHub.

**GitHub Repository**
Stores the source code and Jenkins pipeline file.

**Jenkins (running inside Docker)**
Handles CI/CD automation:

* pulls the repository
* runs pipeline steps
* connects to EC2 using SSH
* triggers deployment

**AWS EC2 Instance**
Hosts the application containers.

Inside EC2:

* Flask container
* MySQL container

**User**
Accesses the deployed application through the EC2 public IP.

---

## Technology Stack

Backend
Flask (Python)

Database
MySQL

Containerization
Docker
Docker Compose

CI/CD
Jenkins Pipeline

Cloud
AWS EC2

Version Control
Git
GitHub

---

## Project Structure

```
two-tier-web-aws
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
│
└── templates
    └── index.html
```

---

## CI/CD Pipeline Flow

Step 1
Developer pushes code to GitHub.

Step 2
Jenkins pulls the repository.

Step 3
Jenkins reads the Jenkinsfile.

Step 4
Pipeline connects to EC2 via SSH.

Step 5
Deployment commands run on EC2:

```
cd two-tier-web-aws
git pull
docker-compose down
docker-compose up --build -d
```

Step 6
Docker rebuilds containers.

Step 7
Updated application becomes available to users.

---

## Jenkins Pipeline

Example Jenkinsfile used in the project:

```
pipeline {
    agent any

    stages {
        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@EC2-IP "
                        cd two-tier-web-aws &&
                        git pull &&
                        docker-compose down &&
                        docker-compose up --build -d
                    "
                    '''
                }
            }
        }
    }
}
```

---

## Deployment Steps

### 1 Install Docker on EC2

```
sudo apt update
sudo apt install docker.io -y
```

Add user to docker group:

```
sudo usermod -aG docker ubuntu
```

---

### 2 Install Docker Compose

```
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) \
-o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```

---

### 3 Clone the repository

```
git clone git@github.com:Pradeep43724/two-tier-web-aws.git
cd two-tier-web-aws
```

---

### 4 Run the application

```
docker-compose up --build -d
```

---

## Accessing the Application

Open in browser:

```
http://<EC2-PUBLIC-IP>:5000
```

---

## Key DevOps Concepts Demonstrated

This project demonstrates practical experience in:

* CI/CD pipeline creation
* Infrastructure automation
* Docker containerization
* Cloud deployment
* Jenkins pipeline configuration
* SSH based deployment automation

---

## Possible Improvements

Future improvements for production environments:

* Use **Amazon ECR** for Docker image storage
* Use **Amazon RDS** for managed database
* Add **Nginx reverse proxy**
* Implement **GitHub Webhooks for automatic builds**
* Add **testing stage in Jenkins pipeline**

---
