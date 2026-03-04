# DevOps Project: CI/CD Pipeline for a Two-Tier Flask Application using Jenkins, Docker and AWS

## Author

Pradeep

---

# Table of Contents

1. Project Overview
2. Architecture
3. Technologies Used
4. Infrastructure Setup
5. Application Containerization
6. Jenkins CI/CD Pipeline
7. Deployment Workflow
8. Verification
9. Future Improvements

---

# 1. Project Overview

This project demonstrates the implementation of a **CI/CD pipeline for deploying a two-tier web application** using Jenkins, Docker, GitHub, and AWS EC2.

The application consists of:

* **Frontend:** Flask web application
* **Backend:** MySQL database

The deployment process is automated using Jenkins so that whenever new code is pushed to GitHub, Jenkins automatically deploys the latest version to an EC2 instance.

This project demonstrates practical DevOps concepts including:

* CI/CD pipeline automation
* Containerization using Docker
* Cloud deployment using AWS EC2
* Infrastructure automation using Jenkins pipelines

---

# 2. Architecture

```
Developer
    │
    │ Push Code
    ▼
GitHub Repository
    │
    │ Jenkins Pipeline Trigger
    ▼
Jenkins Server (Docker Container)
    │
    │ SSH Deployment
    ▼
AWS EC2 Instance
    │
    │ Docker Compose
    ▼
Application Containers
    ├── Flask Application
    └── MySQL Database
    │
    ▼
End User accesses Web App
```

---

# 3. Technologies Used

### Cloud

AWS EC2

### CI/CD

Jenkins

### Containerization

Docker
Docker Compose

### Programming

Python (Flask)

### Database

MySQL

### Version Control

Git
GitHub

---

# 4. Infrastructure Setup

## Launch EC2 Instance

1. Go to AWS EC2 console
2. Launch an instance

Configuration:

```
AMI: Ubuntu 22.04
Instance Type: t2.micro
```

### Configure Security Group

Add inbound rules:

| Type       | Port |
| ---------- | ---- |
| SSH        | 22   |
| HTTP       | 80   |
| Custom TCP | 5000 |
| Custom TCP | 8080 |

---

## Connect to EC2

```
ssh -i key.pem ubuntu@<EC2-PUBLIC-IP>
```

---

# 5. Install Dependencies on EC2

Update system

```
sudo apt update && sudo apt upgrade -y
```

Install required tools

```
sudo apt install git docker.io -y
```

Enable Docker

```
sudo systemctl start docker
sudo systemctl enable docker
```

Allow Docker without sudo

```
sudo usermod -aG docker ubuntu
```

---

# 6. Application Containerization

## Dockerfile

```
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python","app.py"]
```

---

## Docker Compose

```
version: "3"

services:

  mysql:
    image: mysql
    environment:
      MYSQL_DATABASE: devops
      MYSQL_ROOT_PASSWORD: root
    ports:
      - "3306:3306"

  flask:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - mysql
```

---

# 7. Jenkins Setup

Jenkins is run **inside a Docker container** on the local system.

Start Jenkins container:

```
docker run -d \
-p 8080:8080 \
-p 50000:50000 \
--name jenkins \
-v jenkins_home:/var/jenkins_home \
jenkins/jenkins:lts
```

Open Jenkins dashboard:

```
http://localhost:8080
```

Unlock Jenkins:

```
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Install recommended plugins.

---

# 8. Jenkins Pipeline

The Jenkins pipeline deploys the application to EC2 automatically.

### Jenkinsfile

```
pipeline {
    agent any

    stages {

        stage('Deploy to EC2') {

            steps {

                sshagent(['ec2-ssh-key']) {

                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@<EC2-IP> "
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

# 9. Deployment Workflow

1. Developer pushes code to GitHub

2. Jenkins pulls the repository

3. Jenkins reads the Jenkinsfile

4. Jenkins connects to EC2 using SSH

5. Jenkins executes deployment commands

```
git pull
docker-compose down
docker-compose up --build -d
```

6. Containers restart with updated code

---

# 10. Access the Application

Open in browser:

```
http://<EC2-PUBLIC-IP>:5000
```

Example

```
http://16.171.241.211:5000
```

---

# 11. Verification

Check running containers:

```
docker ps
```

Expected containers:

```
flask-app
mysql
```

---

# 12. Future Improvements

Possible improvements to make the project production ready:

* Use **Amazon ECR** for Docker image storage
* Use **Amazon RDS** for managed MySQL
* Add **Nginx reverse proxy**
* Implement **GitHub webhooks**
* Deploy using **Kubernetes (EKS)**

---

# Conclusion

This project demonstrates how a DevOps CI/CD pipeline can automate application deployment using Jenkins, Docker, and AWS.

The pipeline ensures that every code update pushed to GitHub can be automatically deployed to the cloud infrastructure with minimal manual intervention.

---