pipeline {
    agent any

    stages {
        stage('Deploy to EC2') {
            steps {
                sshagent(['username123']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@13.53.190.141 "
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
