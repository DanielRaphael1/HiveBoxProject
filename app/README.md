# Phase 3
Created app.py which defines the boxes, makes the api request, and runs flask, creates an additional endpoint at /temperature
---
Created boxes.env to keep env variables stored on file for safety and accessabillity
--- 
Dockerfile now opens our port at 5000, installs needed dependencies defined at requirements.txt.
---
Created lint.yaml to check py files and Docker files.
---
to run this app, first build the app
```bash
docker build -t version-app .
```
then run it
```bash
docker run -p 5000:5000 version-app
```
then visit local ip on the web to make sure everything works. : http://127.0.0.1:5000/temperature