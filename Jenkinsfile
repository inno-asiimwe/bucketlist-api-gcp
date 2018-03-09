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
                    args '-u root:root'
                }
            }
            environment {
                APP_SETTINGS="testing"
            }
            steps {
                echo 'clone repo'
                checkout scm
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            echo Testing
        }
    }
}