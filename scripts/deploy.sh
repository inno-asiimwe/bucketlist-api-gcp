#!/bin/bash

access_gcloud_project_folder(){
    alias gcloud="/home/jenkins/google-cloud-sdk/bin/gcloud"
    gcloud auth activate-service-account --key-file $gcloud_service_key_file
    gcloud compute --project "andealcps" ssh --zone "us-west1-c" "bucketlist-api-server"
    cd /home/innocent_asiimwe/www/bucketlist-api-gcp
}

deploy_change(){
    sudo git pull
    sudo supervisorctl restart bucketlist_api_gcp
}

main(){
    access_gcloud_project_folder
    deploy_change
}

main