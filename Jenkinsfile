pipeline {
    agent none
    environment {
        SECRET="My-secret-a-long-string"
    }
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:3.5-onbuild'
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