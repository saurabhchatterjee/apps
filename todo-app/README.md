# todo app

create namespace
```shell
kubectl create -f k8s/namespace.yml
# expected output
namespace/todo-app created
# set current context to use this namespace
kubectl config set-context --current --namespace=todo-app
# expected output
Context "minikube" modified.
```

apply secrets
```shell
echo -n '<my password>' | base64
kubectl apply -f app-secrets.yml
# expected output
secret/todo-secrets created

kubectl get secrets -n todo
# expected output
NAME                 TYPE     DATA   AGE
todo-secrets   Opaque   1      53s
```

create app config 
```shell
k create -f k8s/app-configs.yml 
configmap/app-config created
```

apply persistent volume yml
```shell
kubectl apply -f mysql-pv.yml
# expected output
persistentvolume/mysql-pv-volume created
persistentvolumeclaim/mysql-pv-claim created
```

```shell
kubectl describe pv mysql-pv-volume -n todo
#expeted output
Name:            mysql-pv-volume
Labels:          type=local
Annotations:     pv.kubernetes.io/bound-by-controller: yes
Finalizers:      [kubernetes.io/pv-protection]
StorageClass:    manual
Status:          Bound
Claim:           default/mysql-pv-claim
Reclaim Policy:  Retain
Access Modes:    RWO
VolumeMode:      Filesystem
Capacity:        2Gi
Node Affinity:   <none>
Message:         
Source:
    Type:          HostPath (bare host directory volume)
    Path:          /mnt/data
    HostPathType:  
Events:            <none>
```

```shell
kubectl describe pvc mysql-pv-claim -n todo
# expected output
Name:          mysql-pv-claim
Namespace:     default
StorageClass:  manual
Status:        Bound
Volume:        mysql-pv-volume
Labels:        <none>
Annotations:   pv.kubernetes.io/bind-completed: yes
               pv.kubernetes.io/bound-by-controller: yes
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:      2Gi
Access Modes:  RWO
VolumeMode:    Filesystem
Mounted By:    <none>
Events:        <none>
```

deploy mysql
```shell
k apply -f mysql-deployment.yml 
# expected output
service/mysql created
deployment.apps/mysql created
```

check deployment
```shell
kubectl describe deployment mysql
Name:                   mysql
Namespace:              todo
CreationTimestamp:      Sun, 03 Sep 2023 23:23:22 -0500
Labels:                 app=db
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=db
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=db
  Containers:
   mysql:
    Image:      mysql
    Port:       3306/TCP
    Host Port:  0/TCP
    Environment:
      MYSQL_ROOT_PASSWORD:  <set to the key 'db_root_password' in secret 'todo-secrets'>  Optional: false
    Mounts:
      /var/lib/mysql from mysql-persistent-storage (rw)
  Volumes:
   mysql-persistent-storage:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-pv-claim
    ReadOnly:   false
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   mysql-6966479b7f (1/1 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  43s   deployment-controller  Scaled up replica set mysql-6966479b7f to 1
```

check work till now
```shell
kubectl get pods,svc,pv,pvc -A
NAMESPACE     NAME                                   READY   STATUS    RESTARTS        AGE
kube-system   pod/coredns-5d78c9869d-h4tnm           1/1     Running   1 (10h ago)     10h
kube-system   pod/etcd-minikube                      1/1     Running   1 (10h ago)     10h
kube-system   pod/kube-apiserver-minikube            1/1     Running   1 (10h ago)     10h
kube-system   pod/kube-controller-manager-minikube   1/1     Running   1 (10h ago)     10h
kube-system   pod/kube-proxy-64bbq                   1/1     Running   1 (10h ago)     10h
kube-system   pod/kube-scheduler-minikube            1/1     Running   1 (10h ago)     10h
kube-system   pod/storage-provisioner                1/1     Running   13 (125m ago)   10h
todo    pod/mysql-6966479b7f-cvf55             1/1     Running   0               3m9s

NAMESPACE     NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                  AGE
default       service/kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP                  10h
kube-system   service/kube-dns     ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP   10h
todo    service/mysql        NodePort    10.98.185.164   <none>        3306:31873/TCP           3m9s

NAMESPACE   NAME                               CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                       STORAGECLASS   REASON   AGE
            persistentvolume/mysql-pv-volume   2Gi        RWO            Retain           Bound    todo/mysql-pv-claim   manual                  4m37s

NAMESPACE    NAME                                   STATUS   VOLUME            CAPACITY   ACCESS MODES   STORAGECLASS   AGE
todo   persistentvolumeclaim/mysql-pv-claim   Bound    mysql-pv-volume   2Gi        RWO            manual         4m37s
```

create database
```shell
# Step 1: Decode your encoded password
base64 -d <<< <encoded password>
# Step 2: Run a MySQL client to connect to the server
kubectl run -it --rm --image=mysql --restart=Never mysql-client -- mysql --host mysql --password=<decoded password>
# Step 3: Create the database
CREATE DATABASE todoapp;
```








