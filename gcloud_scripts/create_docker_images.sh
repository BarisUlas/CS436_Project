docker build ./express --tag express:local
docker build ./socketio --tag socketio:local
docker build ./client --tag client:local

kind create cluster

kind load docker-image express:local
kind load docker-image socketio:local
kind load docker-image client:local