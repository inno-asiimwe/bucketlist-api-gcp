#!/bin/bash

access_gcloud_project_folder(){
    gcloud auth activate-service-account --key-file $gcloud_service_key_file
    gcloud compute scp "./server_update.sh" "bucketlist-api-server":~/
    
}

deploy_change(){
   gcloud compute --project "andealcps" ssh --zone "us-west1-c" "bucketlist-api-server" -- '~/server_update.sh' 
}

main(){
    sudo find / -name gcloud
    alias gcloud="/home/jenkins/google-cloud-sdk/bin/gcloud"
    access_gcloud_project_folder
    deploy_change
}

main