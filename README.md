# objectives-service
_Manage the user objectives_

[![Build Status](https://travis-ci.org/ytbeepbeep/objectives-service.svg?branch=master)](https://travis-ci.org/ytbeepbeep/objectives-service)
[![Coverage Status](https://coveralls.io/repos/github/ytbeepbeep/objectives-service/badge.svg?branch=master)](https://coveralls.io/github/ytbeepbeep/objectives-service?branch=master)

_This microservice works on port 5004._

## First setup
Export the address and the port of the [data-service](https://github.com/ytbeepbeep/data-service) microservice,
the default is `127.0.0.1:5002`.

A smart way to do this is to create a file `variables.sh` in the project root, as follows.
```
#!/bin/bash
export DATA_SERVICE="127.0.0.1:5002"
export OBJECTIVE_SERVICE="127.0.0.1:5004"
```
You can load the variables with `source variables.sh`.

#### Install for development
```
pip install -r requirements.txt
pip install pytest pytest-cov
python setup.py develop
```

#### Install for production
```
pip install -r requirements.txt
python setup.py install
```


## Run the microservice
`python objectives/app.py`

**Important note:** use python 3.6.


## Docker
[![Image size](https://images.microbadger.com/badges/image/ytbeepbeep/objectives-service.svg)](https://microbadger.com/images/ytbeepbeep/objectives-service)
[![Latest version](https://images.microbadger.com/badges/version/ytbeepbeep/objectives-service.svg)](https://microbadger.com/images/ytbeepbeep/objectives-service)

A Docker Image is available on the public Docker Hub registry. You can run it with the command below.

`docker run -d --name objectives-service ytbeepbeep/objectives-service`

**Important note:** if you need to expose the service outside you Docker installation (e.g. to third part services) use the option `-p 5002:5002`

#### Locally
You can also build your own image from this repository.
- Build with `docker build -t ytbeepbeep/objectives-service .`
- Run as usually, with the commands specified above
