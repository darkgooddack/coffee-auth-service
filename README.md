# coffee-auth-service


kubectl apply -f k8s/namespace.yaml

kubectl create secret generic coffee-auth-secrets --from-env-file=.env -n auth-dev

kubectl apply -f k8s/redis -n auth-dev

kubectl apply -f k8s/postgres -n auth-dev

kubectl apply -f k8s/kafka -n auth-dev

kubectl apply -f k8s/api -n auth-dev

kubectl apply -f k8s/worker -n auth-dev

