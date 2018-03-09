pipeline {
    agent none
    environment {
        SECRET="My-secret-a-long-string"
    }
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:2-alphine'
                }
            }
            environment {
                APP_SETTINGS="testing"
            }
            steps {
                sh "sudo apt-get install virtualenv"
                sh "sudo virtualenv venv"
                sh "./venv/bin/activate && pip install -r requirements.txt"
            }
        }
    }
}