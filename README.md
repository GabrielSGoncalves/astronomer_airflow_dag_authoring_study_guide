# Astronomer Airflow DAG Authoring Study Guide
In this repository we are going to explore the content required on the Airflow DAG Authoring Certification exam from Astronomer. The approach is to use the current README file as a guide for exploring the subjects, and also structure a repository to deploy Airflow locally to test core features.

## 1. Installing Docker
One of the easiest ways to deploy Airflow is through Docker containers. To do it, we first need to install Docker and Docker Compose. The recommended way is by following the official tutorials, for [Docker](https://docs.docker.com/desktop/install/ubuntu/) and for [Docker Compose](https://docs.docker.com/compose/install/). After installing both tools, try the following terminal commands to make sure the installations were successful:
```bash
docker --version
## The returned output should display something similar to:
# Docker version 24.0.7, build afdd53b
```
And for Docker Compose:
```bash
docker compose version
## For Docker Compose the returned output is similiar to:
# Docker Compose version v2.21.0
```

## Installing the Astronomer CLI
Although we could follow the [official Airflow documentation]((https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)) and deploy it locally using Docker Compose, Astronomer has developed an easier way to do it, by using Astro CLI, as it offers a few advantages over the official Airflow package. The commands described bellow are suited for a Linux machine, but you can find information on how to do it in Windows or Mac in the [Astro CLI install page](https://docs.astronomer.io/astro/cli/install-cli?tab=linux#install-the-astro-cli).
```bash
curl -sSL install.astronomer.io | sudo bash -s
```
You should get a return on your terminal like:
```
astronomer/astro-cli info Using Latest(v1.21.0) version
astronomer/astro-cli info found version: 1.21.0 for v1.21.0/linux/amd64
astronomer/astro-cli info installed /usr/local/bin/astro
```
To check if you install Astro CLI with success just type `astro` on your terminal and you should get:
```

 ________   ______   _________  ______    ______             ______   __        ________
/_______/\ /_____/\ /________/\/_____/\  /_____/\           /_____/\ /_/\      /_______/\
\::: _  \ \\::::_\/_\__.::.__\/\:::_ \ \ \:::_ \ \   _______\:::__\/ \:\ \     \__.::._\/
 \::(_)  \ \\:\/___/\  \::\ \   \:(_) ) )_\:\ \ \ \ /______/\\:\ \  __\:\ \       \::\ \
  \:: __  \ \\_::._\:\  \::\ \   \: __ '\ \\:\ \ \ \\__::::\/ \:\ \/_/\\:\ \____  _\::\ \__
   \:.\ \  \ \ /____\:\  \::\ \   \ \ '\ \ \\:\_\ \ \          \:\_\ \ \\:\/___/\/__\::\__/\
    \__\/\__\/ \_____\/   \__\/    \_\/ \_\/ \_____\/           \_____\/ \_____\/\________\/

Welcome to the Astro CLI, the modern command line interface for data orchestration. You can use it for Astro, Astronomer Software, or Local Development.

Current Context: Astro

Usage:
  astro [command]

Available Commands:
  completion   Generate the autocompletion script for the specified shell
  config       Manage a project's configurations
  context      Manage Astro & Astronomer Software contexts
  deploy       Deploy your project to a Deployment on Astro
  deployment   Manage your Deployments running on Astronomer
  dev          Run your Astro project in a local Airflow environment
  help         Help about any command
  login        Log in to Astronomer
  logout       Log out of Astronomer
  organization Manage Astronomer Organizations
  registry     Interact with the Astronomer Registry
  run          Run a local DAG with Python by running its tasks sequentially
  version      List running version of the Astro CLI
  workspace    Manage Astro Workspaces

Flags:
  -h, --help               help for astro
      --verbosity string   Log level (debug, info, warn, error, fatal, panic (default "warning")

Use "astro [command] --help" for more information about a command.

```

## 3. Creating a repository for local Airflow deployment
After installing all the required tools mentioned above (Docker, Docker Compose and Astro CLI) we are ready for structuring our local repository. To do it, you first can create a new folder (I named my `astronomer_airflow_dag_authoring_study_guide`), that we are going to use as our repository folder:
```bash
mkdir airflow_dag_authoring_study_guide
cd airflow_dag_authoring_study_guide
```
The next step is going to show us how easy is to deploy a test Airflow on your local environment.
```bash
astro dev init
``` 
The previous commands creates all the needed files and folders for your local Airflow deployment, including folders for your dags, plugins, include and tests, and config files like Dockerfile image and DAG examples. To have a sense of the repository boilerplate structure you can run the command `tree` on your terminal.
```bash
tree
``` 
```
.
├── airflow_settings.yaml
├── dags
│   ├── example_dag_advanced.py
│   └── example_dag_basic.py
├── Dockerfile
├── include
├── packages.txt
├── plugins
├── README.md
├── requirements.txt
└── tests
    └── dags
        └── test_dag_example.py

5 directories, 8 files

``` 
We are going to have a deeper understanding of each one of the components inside your repository in the following sessions. For now, we can simply run the next command to deploy our local Airflow infrastructure using Docker Containers.
```bash
astro dev start
```
With previous command you pull the images of each one of the main components of Airflow (Postgres-Database, Triggerer, Scheduler, Webserver) and starts its containers. 
```
Airflow is starting up!

Project is running! All components are now available.

Airflow Webserver: http://localhost:8080
Postgres Database: localhost:5432/postgres
The default Airflow UI credentials are: admin:admin
The default Postgres DB credentials are: postgres:postgres

``` 

You can check the running containers with the following command:

```bash
astro dev ps
```
```
Name									State		Ports
astronomer-airflow-dag-authoring-study-guide_c76029-webserver-1		running		8080
astronomer-airflow-dag-authoring-study-guide_c76029-scheduler-1		running
astronomer-airflow-dag-authoring-study-guide_c76029-triggerer-1		running
astronomer-airflow-dag-authoring-study-guide_c76029-postgres-1		running		5432
```

As you can see, we have 4 containers representing Airflow main components: Scheduler, Trigger, Webserver and Database (Postgres). If you want to understand this architecture deeply I highly recommend you checking out [Astronomer Airflow components documentation](https://docs.astronomer.io/learn/airflow-components). 

## Defining your DAGs
- 
- DAG parsing, need to have airflow or dag on the file name
- You can change this behaviour by changing the parameter DAG_DISCOVERY_SAFE_MODE on the setting file to False and Airflow would parse all your files. This may impact the performance of your deploy, so it's not recommended.
- You can add `.airflowignore` file to list all the folders and files that you want Airflow to avoid parsing. It's same logic used for .gitignore file.
- The recommended structure for your DAG code is using the context manager (`with` statement)
```python
with DAG(dag_id=) as dag:
```
- Important parameters:
  1. dag_id : unique name for your dag. Important to note that if you have 2 DAGs with the same dag_id you won't be able to define which one was parsed
  2. description: Simple text to describe the purpose of your DAG
  3. start_date: The initial date for yout DAG to start being scheduled. You can also customize start_date for your DAGs tasks individually.
  4. schedule_interval:

## References
1. [Get Docker (Docker Offical Documentation)](https://docs.docker.com/desktop/install/ubuntu/)
2. [Overview of installing Docker Compose (Docker Offical Documentation)](https://docs.docker.com/compose/install/)
3. [Running Airflow in Docker (Apache Airflow Offical Documentation)](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
4. [Install Astro CLI (Astronomer Docs)](https://docs.astronomer.io/astro/cli/install-cli?tab=linux#install-the-astro-cli)
5. [Airflow Components (Astronomer)](https://docs.astronomer.io/learn/airflow-components) 