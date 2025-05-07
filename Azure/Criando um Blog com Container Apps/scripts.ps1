docker build -t blog-diomedocker-app:latest .

docker run -d -p 80:80 blog-diomedocker-app:latest

az login 

#Criar o resource group
az group create --name containerappslab03 --location brazil south

az acr create --resource-group containerappslab03 --name blogcomdocker --sku Basic

#Login no ACR
az acr login --name blogcomdocker

docker tag blog-diomedocker-app:latest blogcomdocker.azurecr.io/blog-diomedocker-app:latest