gcloud container clusters create mongo-cluster \
    --zone europe-north1 \
    --num-nodes=1 \
    --disk-type=pd-standard \
    --disk-size=30GB