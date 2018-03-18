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
                sh 'pip3 install nose'
                sh 'pip3 install -r requirements.txt'
                echo 'set up postgres'
                sh 'chmod 777 ./scripts/pgfile.sh'
                sh './scripts/pgfile.sh'
            }
        }
        stage('Test') {
            steps {
                sh '#!/bin/bash \n '+
                   'python3 -m pytest '
            }
        }
        stage('Deploy') {
            withCredentials([file(credentialsId:'gcloudsecretkeyfile', variable:'gcloud_service_key_file')]){
                sh './scripts/deploy.sh'
            }
        }
    }
}