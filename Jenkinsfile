pipeline {
    agent any

    stages {
        stage('Deploy to EC2') {
            steps {
                sshagent(['forec2instance']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@16.171.241.211 "
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
