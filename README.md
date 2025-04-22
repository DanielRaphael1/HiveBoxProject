# HiveBoxProject
We created a simple docker app, that for now only prints the current version of our development.
---
in order to run the docker file you must ofcourse install all the needed dependencies, such as docker, etc. Then use :
```bash 
git clone <your-repo>
```
navigate to you project folder 
```bash 
cd /path/hiveboxproject
```
then we build and run the container
```bash
docker build -t hive .
docker run --rm hive
```
if all went smoothly we should get :
 Running version: v0.0.1

