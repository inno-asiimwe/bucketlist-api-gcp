pipeline {
    agent {
        docker {
            image 'python:3.5-onbuild'
            args '-u root:root'
        }
    }
    environment {
        SECRET="My-secret-a-long-string"
    }
    stages {
        stage('Build') {
            environment {
                APP_SETTINGS="testing"
            }
            steps {
                echo 'clone repo'
                checkout scm
                sh 'pip install nose'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'nosetests --cover-package=app'
            }
        }
    }
}