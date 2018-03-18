pipeline {
    agent { dockerfile true}
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
                echo 'set up postgres'
                sh 'chmod 777 ./scripts/pgfile.sh'
                sh './scripts/pgfile.sh'
            }
        }
        stage('Test') {
            steps {
                sh '#!/bin/bash \n '+
                "nosetests"
            }
        }
    }
}