#!/bin/bash

access_gcloud_project_folder(){
    /home/jenkins/google-cloud-sdk/bin/gcloud auth activate-service-account --key-file $gcloud_service_key_file
    /home/jenkins/google-cloud-sdk/bin/gcloud compute scp --zone "us-west1-c" "./server_update.sh" "bucketlist-api-server":~/
    
}

deploy_change(){
   /home/jenkins/google-cloud-sdk/bin/gcloud compute --project "andealcps" ssh --zone "us-west1-c" "bucketlist-api-server" -- '~/server_update.sh' 
}

main(){
    access_gcloud_project_folder
    deploy_change
}

main