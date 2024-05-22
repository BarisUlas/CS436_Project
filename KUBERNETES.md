# KUBERNETES INSTALLATION

## Resolving Docker compose file
1. mkdir k8s && cd k8s && docker-compose config > ../docker-compose-resolved.yaml
## Conversion
2. kompose convert -f ../docker-compose-resolved.yaml
