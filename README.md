# SCALAR - Streaming ChALlenge plAtfoRm
![Logo](./logo.PNG)


SCALAR is the first of its kind, platform to organize Machine Learning competitions on Data Streams.
It was used to organize a real-time ML competition on IEEE Big Data Cup Challenges 2019.

## Features

**Data stream mining competitions** - With SCALAR you can organize the real-time competitions on Data Streams. 
It is inspired by [Kaggle](https://www.kaggle.com/), platform for offline machine learning competitions.



**Simple, user friendly interface** - SCALAR has a WEB application that allows you to easily browse and 
subscribe to the competitions. Its simple and intuitive design, let's you to easily upload the datasets, and create the 
competition. 

![Dialog competition](./add_competition.png)

**Live results and leaderboard** - Since the competition is real-time, the results are also updated in real time. 
During the competition, you can follow performance of your model in the WEB application. Leaderboard will show how 
do you compare to other users, and live chart shows the comparison with baseline model.

**Secure, bi-directional streaming communication** - We use a combination of `gRPC` and `Protobuf` to provide secure, 
low latency bi-directional streaming communication between server and users.

![Architecture](./Architecture.png)

**Freedom to choose a programming language** - SCALAR lets users to choose their preferred environment. The only 
requirement is to be able to communicate through `gRPC` and `Protobuf`, which is supported for many programming 
languages: Python, Java, C++, GO... Additionally, SCALAR provides support for R. Apart from that, users can choose 
their setup, environment and additional resources to train better models.

**** 

## Getting Started

The project is done in Python and organized in Docker containers.
Each service is a separate Docker container.

### Prerequisites

To run the platform locally, Docker is needed:

[Install Docker](https://docs.docker.com/get-docker/)

Also, Docker compose should be installed:

[Install Docker compose](https://docs.docker.com/compose/install/)

### Running

Running is done using Docker-compose.

### Quick setup (to test the functionality of the platform)

- Run ```setup.py``` and follow the instructions to setup the environment. The script will set up the 
time zone and create the docker network for all containers.

 - Once the ```setup.py``` finished successfully, the platform can be run by:
```
docker-compose up
```

### In depth setup (If you want to use it for organizing competitions and enable the registration):

 - Download the code locally and then adjust the [config.json](provider/my_application/config.json) and [docker-compose.yml](./docker-compose.yml) files. More details in [config-ReadMe.txt](provider/config-ReadMe.txt) and in [docker-compose-ReadMe.txt](./docker-compose-ReadMe.txt).

 - Set up an email account which will be used to send the registration confirmation message and authentication token.
For that, you will need to set up your email account to allow the access of less secure apps.
For a quick start, update only email information in [config.json](provider/my_application/config.json).

 - In [docker-compose.yml](./docker-compose.yml) update only the local paths to mount a persistent volumes, following the [docker-compose-ReadMe.txt](./docker-compose-ReadMe.txt).

 - Run [setup.py](./setup.py) and follow the instructions to setup the environment. The script will set up the 
time zone and create the docker network for all containers.
```python3 setup.py```

 - Once the ```setup.py``` finished successfully, the platform can be run by:
```
docker-compose up
```

This command will pull all necessary containers and run them.
When all services are up, web application will be available on [localhost:80](http://localhost:80)

To log in to the platform, you can use default credentials: `admin:admin`

For the test purposes, the test competition will be created automatically.

It will be scheduled to start ```5 minutes``` after starting the platform.

Once you log in, you will be able to see the competition under ```Competitions/Coming``` tab.

In order to subscribe to the competition, click on it and then click the ```Subscribe``` button.
![Subscribe to competition](./subscribe_competition.png)

### Setting up the client

Navigate to [example_data](./example_data) directory, and run:

```python3 client_setup.py```

Once the necessary packages have been installed, go to [Python client directory](./example_data/user_code/Code/Python)
and edit the [client.py](./example_data/user_code/Code/Python/client.py) file. Copy the ```Competition code``` and
```Secret key``` from a competition page and add it in ```client.py``` as shown in the figure below:

![Client setup](./client_setup.png)

Once the competition has started, run ```client.py```, and you should be able to see how the messages and predictions are exchanged.
Then you will be able to see the live chart and leaderboard on the competition page. (You will have to refresh the page to get new measures.)

To get to know around the platform use the the [Quick Start Guide](./SCALAR_Quick_Start_Guide.pdf). 
To create and participate in the competition use the provided [examples](./example_data).
* **Nedeljko Radulovic**
* **Dihia Boulegane**
* **Albert Bifet**
* **Nenad Stojanovic**


## Acknowledgments

Open source Docker containers were used:
* [MongoDB](https://hub.docker.com/_/mongo)
* [Spark Docker container by GettyImages](https://hub.docker.com/r/gettyimages/spark)
* [MySQL](https://hub.docker.com/_/mysql)
* [Kafka by Wurstmeister](https://hub.docker.com/r/wurstmeister/kafka)
* [Zookeeper by Wurstmeister](https://hub.docker.com/r/wurstmeister/zookeeper)

## References

* [Boulegane, Dihia, et al. "Real-Time Machine Learning Competition on Data Streams at the IEEE Big Data 2019." 2019 IEEE International Conference on Big Data (Big Data). IEEE, 2019.](https://ieeexplore.ieee.org/abstract/document/9006357?casa_token=f0mJeR8-WfYAAAAA:yEt_Mix9dumrPpo64uPBbI0XI4Kvfim4Pkg5xNVVzXqK4AGToX0XcJPKgETkE1hs86Pcc0u5xYc)
* [IEEE Big Data Cup 2019](https://bigmine.github.io/real-time-ML-competition/index.html)


