# Astronomer Airflow DAG Authoring Study Guide
In this repository we are going to explore the content required on the Airflow DAG Authoring Certification exam from Astronomer. The approach is to use the current README file as a guide for exploring the subjects, and also structure a repository to deploy Airflow locally to test core features.

## A few important notes
1. During this guide I'm going to use the expression "DAGs" and "data pipelines" as the same concept, as DAGs are abstractions for data pipelines inside Airflow.


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
  4. schedule_interval: Defines the frequency of the DAG runs. You can use Airflow expressions (like @daily), CRON expressions or timedelta objects.
  5. dag_run_timeout: Defines your DAG execution time limit, using timedelta objects
  6. tags: Customized tags related to your DAGs, helps you organize your data pipelines by groups, users or any other subject needed.
  7. catchup: Defines if your want to schedule automatically DAGs runs between the start_date and the current date. It's recommended to set it to False, in order to control the execution of past time DAG runs.
  8. max_active_runs: Thee total number of DAG runs that you can run at the same time. This parameter is important whenever you want to perform a backfill and your `catchup` equals to True (more details on the session bellow).

Below is a example of a DAG file `dag_customer_ingestion.py` with the mentioned parameters defined
  ```python
  from Airflow import DAG

  from datetime import datetime, timedelta

  with DAG(
      "customer_1_ingestion",
      description="Data pipeline responsible for batch ingestion of customer 1 data",
      start_date=datetime(2020,1,1),
      schedule_interval='@daily',
      dagrun_timeout=timedelta(minutes=45),
      tags=['customer_1', 'data_ingestion'],
      catchup=False
      ) as dag:

      # define the tasks below ...   
  ```

## DAG scheduling
DAG scheduling can be a little bit tricky if you don't understand a few important concepts presented as DAG parameters above. The parameter `start_date` defines the date the DAG start being scheduled, and the `schedule_interval` the frequency your DAG runs are executed. Also, the first `start_date` is equal to the `execution date`. But the first time your DAG is going to be triggered is actually the defined `start_date` added by the `schedule_interval`. 
```
first execution_date = start_date 
first triggered DAG run = start_date or execution_date + schedule_interval
second and following DAG runs = execution_date + schedule_interval
```
Let's go through a quick example to understand it better.
Imagine you define your 
## REVIEW THE SCHEDULING CONCEPTS

## CRON vs Timedelta
- CRON expression is stateless
- Timedelta is stateful 
- With CRON expression, the first DAG run is triggered based on the `start_date` addeing the interval

## Task indepotence and determinism
A task can be considered idepotent and deterministic if executed multiple times you consitently get the same results (outputs). And deterministic if the output of a task is the same whenever provided a specific input, showing no side effects.
In practice, we can illustrate it with a SQL DDL:
```sql
CREATE TABLE users (...)
```
If we run the above statement twice, the first time it would succeed, but the second time it would raise an error, because the table already exists. To make idepotent and deterministic you could use:
```sql
CREATE TABLE IF NOT EXISTS users (...)
```

Another important aspect of having idepotent task is that if your pipeline fails in any specific task, you could rerun the whole pipeline generating no side effects like duplicated rows or new error messages. Designing idepotent data pipelines is probably one of the most valuable skills a Data Engineer can display.


## Backfilling
Backfilling is the process scheduling DAG runs from a specific period in the past. In order to execute a backfilling you have 

## REVIEW BACKFILLING CONCEPTS

```bash
airflow dags backfill -s 2024-01-01 -e 2024-01-14
```

## Variables
Airflow provides a key-value store for you to centrally store your variables, and avoid harcoding it to your DAG, or creating a .env file. To create your variables you have 3 methods:
1. Webserver UI
2. Airflow CLI
3. Airflow REST API

![AIRFLOW UI VARIABLES]()

After creating your variables, to access it you only have to import inside your Python modules:
```python
from airflow.models import Variables
s3_staging_bucket = Variable.get('s3_staging_bucket_name')
```

If you are storing a sensitive information as variable, in order to prevent it to be displayed on the webserver UI or in the logs, you can simply add specific keywords like `password`, `passwd`, `api_key`, `api key` or `secret` to hide it. You can also customize the secret keywords for identify sensitive variables by changing the parameter  `sensitive_var_conn_names` on the Airflow settings file. 

One important think to note is that Airflow is storing all your defined variables on the metadata database (Postgres container). And every time your DAG file is parsed (by the scheduler, defined by the parameter `min_file_processing_interval` on your Airflow settings file), a new connection to your Postgres database is created, and it may impact your Airflow deployment performance. To prevent it from happening you can get the variables inside the functions definitions, not before instatiating the DAG.
```python
from airflow.models import Variables

def _extract():
    s3_staging_bucket = Variable.get('s3_staging_bucket_name')
    return s3_staging_bucket

``` 

You can also prevent useless connection to the Posgres database, whenever you need more than one value for a specific task, you can create a new variable with a JSON as value. To access it as a dictionary, you only need to specify a parameter `deserialize_json=True`),
```python
from airflow.models import Variables

json_variable_test = Variable.get('json_var_key', deserialize_json=True)
```
And finally, whenever you want to pass a variable as the parameter of your tasks, avoiding the creation of connections to the Postgres database, you can use the template engine:
```python
# Definition of the DAGs parameters
# ...
    extract = PythonOperator(
        task_id='extract',
        python_callable=extract,
        op_args=["{{ var.json.json_variable_test.json_key}}"]
    )
```
### Environment variables from Docker file
Another way to provide variables to your Airflow pipelines is to create environment variables from the Docker file.
```python

```
## ENVIRONMENT VARIABLES
## SECRET BACKEND


## Templating with Jinja 2 
In order to access variables associated to the DAG run runtime, you can use Jinja 2 templates.
- Describe the logic of capturing runtime variables
- How to add parameters to Postgres operator with CustomPostgresOperator

## Sharing data between tasks with XCOMs
XComs (short for “cross-communications”) are an Airflow resource that allows you to share data between tasks of the same DAG. By default, each task from a DAG run is isolated from rest of tasks. This allows you to deploy Airflow using multiple machines or containers with Celery or Kubernetes.

The way Airflow stores data from XCOMs is through the metadata database (Postgres), using a key-value approach. The way for you to use the XCOM feature is by leveraging the task instance object. Each task instance is associated with a unique set of values for `dag_id`, `task_id`, `execution_date` and `try_number`. Another importante aspect for a task instance is that it always displays a state associated with the task life cycle (`queued`, `running`, `success`, `failed`, and `skipped`). So you can leverage this object to carry data between tasks for your pipeline.
The original way to implement XCOMs is illustrated bellow:
```python
def _extract(ti):
    partner_name = 'netflix'
    ti.xcom_push(key='partner_name', value=partner_name)

def _process(ti):
    partner_name = ti.xcom_pull(key='partner_name', task_id='extract')
    print(partner_name)

```

Another way to achieve the above XCOM logic is by using the `return` statement:
```python
def _extract(ti):
    partner_name = 'netflix'
    return partner_name

def _process(ti):
    partner_name = ti.xcom_pull(task_id='extract')
    print(partner_name)
```
In order to pass multiple values between tasks through XCOM is by using a dictionary as JSON object.
```python
def _extract(ti):
    partner_name = 'netflix'
    partner_path = '/partners/netflix'
    return {"partner_name": partner_name, "partner_path": partner_path}

def _process(ti):
    partner_settings = ti.xcom_pull(task_id='extract')
    partner_name = partner_settings.get('partner_name')
    partner_path = partner_settings.get('partner_path')
    print(partner_name)
```


Important to note that before on Airflow version 1.x each XCOM data was pickled, and on current Airflow version onward, it's serialized. So you need to pass only Python serialized objects as XCOM.

### XCOM limitations
Although XCOMs can be an a handy feature for using through your data pipelines, it has some important limitations:
1. Size of XCOM
  - SQlite: 2GB
  - Postgres: 1GB
  - MySQL: 64KB

### XCOM backend
You can define a XCOM backend to replace your Metadata database (remeber that Postgres is the default) with other data stores like AWS S3, in order to have a more robust storage for your XCOMs. But even with an alternative XCOM backed, you need to be careful with the size of your XCOMs, otherwise you would end up with a memory overflow error.

## Creating DAGs with Taskflow API
The Taskflow API is a new approach (released on Airflow version 2) that enables you to create Python tasks that share XCOM data with a much simpler synthax, which reads more Pythonic. 
To use it, you need to leverage the Taskflow API decorator over your Python functions, in order for Airflow to understand it. And the second difference when using the Taskflow API is how you define your XCOM arguments, 

One important caveat is that as Taskflow API uses Python operators, you need to make sure you Airflow deploy is using an isolation for workers (Celery or Kubernetes), in order to avoid using the resources of your production machine, ending up with slow processing times or memory errors.
Let's remember a simple example on how to leverage XCOMs using the old approach:
```python
from airflow.decorators import task, dag # you import the Taskflow API decorators

@task.python
def extract():
    partner_name = 'netflix'
    return partner_name

@task.python
def process():
    print(partner_name)

with DAG("my_dag",
    # other DAG parameters
    ):
    extract() >> process()
```

```python
from airflow.decorators import task, dag # you import the Taskflow API decorators

@task.python
def extract():
    partner_name = 'netflix'
    return partner_name

@task.python
def process(partner_name):
    print(partner_name)

@dag(# other DAG parameters except dag_id
    )

def my_dag():
    process(extract())

```
By using the mentioned synthax Airflow is extracting the name of your task and DAG from the fuction names, but if you want you can define it by passing a parameter to the decorators.
```python
@task.python
def extract(task_id='extract_defined_name'):
    partner_name = 'netflix'
    return partner_name
```
Also, another important `task` decorator parameter `multiple_outpus=True` and Airflow would create a separated XCOM value for each key of your returned dictionary.
```python
@task.python
def extract(task_id='extract_defined_name', multiple_outpus=True):
    partner_name = 'netflix'
    return {"partner_name": partner_name, "partner_path": partner_path}
```
In the example above you would pass a XCOM parameter for `partner_name` and one for `partner_path`.
And finally, you can use Python type hints to implement the same thing above, in en even more elegant way.

```python
from type import Dict

@task.python
def extract() -> Dict[str, str]:
    partner_name = 'netflix'
    return {"partner_name": partner_name, "partner_path": partner_path}

@task.python
def process(partner_name, partner_path):
    print(partner_name, partner_path)

@dag(# other DAG parameters except dag_id
    )

def my_dag():
    partner_settings = extract()
    process(partner_settings['partner_name'], partner_settings['partner_path'])

```

## Grouping Tasks on your DAG
As you add more tasks and dependencies to your DAGs, it can become difficult to understand with a graph view with so much information. To organize your tasks into groups in order to increase the readability of your graph view, you have two options: SubDAGs (old and suboptimal way) and TaskGroups (new and ideal way). 

### SubDAGs








## TO DO LIST:
- Brief introduction of the purpose of the tutorial, mention Astronomer DAG Authoring course and DAG 101 white pages
- Explain to deploy Airflow using Docker Compose locally and compare it to Astro CLI
- How to use Airflow REST API to do stuff
- Describe Registry and add a few pictures




## References
1. [Get Docker (Docker Offical Documentation)](https://docs.docker.com/desktop/install/ubuntu/)
2. [Overview of installing Docker Compose (Docker Offical Documentation)](https://docs.docker.com/compose/install/)
3. [Running Airflow in Docker (Apache Airflow Offical Documentation)](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
4. [Install Astro CLI (Astronomer Docs)](https://docs.astronomer.io/astro/cli/install-cli?tab=linux#install-the-astro-cli)
5. [Airflow Components (Astronomer)](https://docs.astronomer.io/learn/airflow-components) 
6. [Apache Airflow Task Instance Guide (Restack)](https://www.restack.io/docs/airflow-knowledge-task-instance-state-machine-example-attributes)
7. [The Python pickle Module: How to Persist Objects in Python (Real Python)](https://realpython.com/python-pickle-module/)