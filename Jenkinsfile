pipeline {
    agent {
        docker {
            image 'python:3.5-onbuild'
            args '-u root:root -p 5432:5432'
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
                sh 'python manage.py db upgrade'
            }
        }
        stage('Test') {
            steps {
                sh 'nosetests --cover-package=app'
            }
        }
    }
}