# Astronomer Airflow DAG Authoring Study Guide
The goal of this repository is to be a guide for anyone studying for Astronomer Airflow DAG Authoring Certification. 

This study guide follows the [official preparatory course](https://academy.astronomer.io/astronomer-certification-apache-airflow-dag-authoring-preparation) presented by [Marc Lamberty](https://www.linkedin.com/in/marclamberti/), but suggests other references specially [Directed Acyclic Graphs (DAGs): The Definitive Guide](https://www.astronomer.io/ebooks/dags-definitive-guide/), [Astronomer Docs](https://docs.astronomer.io/) and the [Airflow official documentation](https://airflow.apache.org/docs/).

The idea is to review concepts and explore in practice with a local Airflow deployment and DAG creations.

## A few important notes
1. During this guide I'm going to use the expression "DAGs" and "data pipelines" as the same concept, as DAGs are abstractions for data pipelines inside Airflow.
astronomer 

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
- SubDAG definitions
- Code example with the 'parent_dag.subdag' convention
- Mixing subDAGs with Taskflow API is confusing!

### TaskGroups
TaskGroups were introduced in Airflow v2 making grouping tasks much easier than using SubDAGs.
One important concept is that TaskGroups are just a visual feature, not impacting in the structure of yout DAG. 


```python
# Add Taskgroup code logic here


```

The other way to call TaskGroups is by using its decorator:
```python
# decorator logic
```
If you want you can move your TaskGroup to another file to make your DAG file much cleaner. You would only need to import yout TaskGroup function and pass it to the DAG instance.

And finally, you can nest TaskGroups, creating one TaskGroup inside the other whenever needed.

## Advanced Airflow Concepts
In this session we are going to review a few advanced concepts related to Airflow.

### Creating dynamic tasks
You can create dynamic tasks based on Python objects like lists or dictionaries in order to avoid repeating your code (following the [DRY principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)). But you can it based on the output of tasks, like XCOMs or results returned from an API request. 
```python
# Example of dynamic tasks based on dictionary
```

### Branching
Branching is a feature that allows you to define different paths for your data pipeline based on conditions. There are a few available operators for performing branching like `BranchSQLOperator`, `BranchDateTimeOperator`, and others (see the list on [here](https://docs.astronomer.io/learn/airflow-branch-operator)), but in general the most used is the `BranchPythonOperator`.

The way you implement branching on your DAGs is by creating a function that returns different values of task_ids names you want to execute in the next step, and pass it to the selected branch operator.
```python
def _choosing_partner_based_on_day(execution_date):
   day = execution_date.day_of_week

   if day == 1:
      return 'extract_partner_snowflake1

```
### Trigger rules
A trigger rule defines the premises your DAG must reach in order for a specific task to be triggered. In other words, it's the states the upstream tasks must display for a specific task to execute.

The default parameter for your Operators is `trigger_rule='all_sucess'`, meaning that all upstream tasks must suceed in order for this tasks to be triggered. Other available parameters can be:
- `all_failed`: Trigger the task if all parents tasks have failed
- `all_done`: Trigger the task whenever all parents tasks have finished running, without worrying about it succeding or failing.
- `one_failed`: Trigger the task whenever one parent task fails
- `one_success`: Trigger the task whenever one parent task succeds
- `none_failed`: Trigger the task whenever only if parents tasks are not displaying failed
- `none_skipped`: Trigger the task whenever only if parents tasks were not skipped
- `none_failed_or_skipped`: Trigger the task whenever only if parents tasks were not skipped or failed
- `dummy`: Does not impose any trigger rule

### Defining dependencies
In order to define dependencies between tasks of your DAG you have a few synthax options.
The oldest (and less used) is using `set_downstream` and `set_upstream`.
```python
with DAG (
    'dependency', 
    schedule_interval='@daily', 
    default_args=default_args, 
    catchup=False
    ) as dag:

    t1 = DummyOperator(task_id='t1')
    t2 = DummyOperator(task_id='t2')
    
    t1.set_downstream(t2) # one way 
    t2.set_upstream(t1)  # or the other
```
Or using the bit shift operators, which is much the most used approach.

```python
with DAG (
    'dependency', 
    schedule_interval='@daily', 
    default_args=default_args, 
    catchup=False
    ) as dag:

    t1 = DummyOperator(task_id='t1')
    t2 = DummyOperator(task_id='t1')
    
    t1 >> t2
```
If you have a situation that you want to implement dependencies between two lists of tasks (like `[t1, t2] >> [t3, t4]), the bit shift operator won't allow you to do it, an error would be raised. In order to do it, you need to leverage the `cross_downstream` function.
```python
from airflow.models.basdeoperator import cross_downstream
with DAG (
    'dependency', 
    schedule_interval='@daily', 
    default_args=default_args, 
    catchup=False
    ) as dag:

    t1 = DummyOperator(task_id='t1')
    t2 = DummyOperator(task_id='t2')
    t3 = DummyOperator(task_id='t3')
    t4 = DummyOperator(task_id='t4')
    t5 = DummyOperator(task_id='t5')
    t6 = DummyOperator(task_id='t6')
    t7 = DummyOperator(task_id='t7')

    cross_downstream([t1, t2, t3], [t4, t5, t6])
    [t4, t5, t6] >> t7
```
And finally, you can use the `chain` function to implement dependencies.
```python
from airflow.models.basdeoperator import chain
with DAG (
    'dependency', 
    schedule_interval='@daily', 
    default_args=default_args, 
    catchup=False
    ) as dag:

    t1 = DummyOperator(task_id='t1')
    t2 = DummyOperator(task_id='t2')
    t3 = DummyOperator(task_id='t3')
    t4 = DummyOperator(task_id='t4')
    t5 = DummyOperator(task_id='t5')
    t6 = DummyOperator(task_id='t6')

    chain(t1, [t2, t3], [t4, t5], t6)
```
### Parallelism, concurrency and related parameters
There are a few parameters that you can specify at the Airflow level, changing parameters on `airflow.cfg` file, in order to control concurrency of tasks, DAGs and DAG runs:
- `parallelism`: The maximum number of tasks that can be executed at the same time on your Airflow instance (default=32).
- `dag_concurrency`: The maximum number of tasks that can be executed at same time for any given DAG(default=16).
- `max_active_runs_per_dag`: The maximum number of runs that can be executed at same time for any given DAG (default=16).
If you want to set the parameters on a DAG level, you have the option to define `concurrency`, maximun number of tasks running at the same time for all DAG runs, and `max_active_runs`.
 
```python
with DAG (
    'dependency', 
    schedule_interval='@daily', 
    default_args=default_args, 
    catchup=False,
    concurrency=2,
    max_active_runs=1
    ) as dag:
    
    # ...
```
And finally, you can also set the parameters `task_concurrency` on a task level, to have even more control over your data pipelines.

```python
with DAG (
    'dependency', 
    schedule_interval='@daily', 
    default_args=default_args, 
    catchup=False,
    ) as dag:
    
    t1 = DummyOperator(task_id='t1', task_concurrency=1)
```

### Pools
Pools are a feature that allows you define groups of worker slots in order to prioritize specific tasks. By default you have a `default_pool` with 128 slots, but you can change this value and create new pools with the size you want, always thinking about the resources you have available for your Airflow deployment. The reason you use pools is to control the concurrency of specific groups of tasks, isolating the resources (workers) from the other pools.

### Defining priorities to critical tasks
Whenever you need to give a priority to specific tasks on your DAG you can change the `priority_weight` parameter of it operator to a different value. By default, `priority_weight=1`, so you can increase this value to set a higher priority.
```python
with DAG (
    'priority', 
    schedule_interval='@daily', 
    default_args=default_args, 
    catchup=False
    ) as dag:

    t1 = DummyOperator(task_id='t1')
    t2 = DummyOperator(task_id='t2', priority_weight=2)
    t3 = DummyOperator(task_id='t3', priority_weight=1)
    t4 = DummyOperator(task_id='t4')
    
    t1 >> [t2, t3] >> t4
```
The example above we would have a priority execution of t2 over t3.
One thing to remember about `priority_weight` is that it's define on a pool level, so if you have tasks belonging to different pools, the priority will follow it's respective pool.

You can also define how the weights of your tasks are computed in the context of your DAG called `weight_rule`. This DAG parameter has a default `weight_rule=downstream` and the effective weight of the task is the aggregate sum of all downstream descendants. You can also have it set to `weight_rule=uptream`, we the opposite effect to default. And `weight_rule=absolute`, with the effective weight being the exact `priority_weight`.

### Defining dependencies between DAG runs
In some cases, it's important that your data pipelines must only be executed if the previous run was successful (or skipped). In Airflow you can control this on the your task level with the parameter `depends_on_past=True`. Whenever set to `True`, every task run will only be triggered if the the same task on the previous was successful. One important thing about this control is that you can't control it at a DAG level, only at the task level. For example, if you have a pipeline with `t1 >> t2 >> t3` and during the first run t3 failed, in the next DAG run, you would still have `t1` and `t2` triggered, but not `t3`. In this case, `t3` won't have a task state and your DAG would be stuck (don't forget to define a timeout for your DAG, or you'll have a DAG "running" forever).

Another way for you to control the execution of a DAG run based on the previouns run is through the use of the operator parameter `wait_for_downstream=True`. With this parameter set to `True` your task will only be triggered if the immediately downstream of the previous run to be finish successfully or be skipped. Important to note this parameter only consider the immediately downstream of the previous task instance.

### Sensors
Sensors are task operators that have a waiting state the only changes when a pre-defined condition changes to `True`, before moving to the next task. There are a few different sensors, like `S3KeySensor`, `DateTimeSensor`, `ExternalTaskSensor`, `HttpSensor` and `SqlSensor` but they all derive from the base class `BaseSensorOperator`, sharing a few parameters:
- `mode`: Can be set to `poke` to occupy a worker slot during the waiting time, or `reschedule` to release the worker slot and add the task to the pool queue again.
- `poke_interval`: The frequency in seconds the sensor checks for the condition (default is 60 seconds).
- `exponential_backoff`: If `True`, every new poke interval is exponentially longer than the before.
- `timeout`: The maximun amount of the sensor is set to wait before raising an fail error.
- `soft_fail`: If set to `True`, when `timeout` is reached, the tasks is skipped instead of failing.

You can find more valuable information abour sensors on [Astronomer sensors documentation](https://docs.astronomer.io/learn/what-is-a-sensor?tab=traditional#example-implementation).

### Setting timeouts for your DAGs and tasks
It's a best practice to always set timeouts for every DAG you create to avoid having problems with wasted resources (workers) with long running DAGs. To do it you define the parameter `dagrun_timeout` just like the example below. You can also specify the timeout at the task level with the parameter `execution_timeout`.
```python
from datetime import timedelta


with DAG (
    'timeout', 
    schedule_interval='@daily', 
    default_args=default_args, 
    catchup=False,
    dagrun_timeout=timedelta(minutes=15)
    ) as dag:

    t1 = DummyOperator(task_id='t1',execution_timeout=timedelta(minutes=10))
    t2 = DummyOperator(task_id='t1',execution_timeout=timedelta(minutes=10))
    
    t1 >> t2
```

### Callbacks
Callbacks are a feature from both DAGs and tasks that can be triggered in case of reaching specific state like `success` or `failure`.
At the DAG level you can define a both of the parameters `on_sucess_callback` or `on_failure_callback` and the argument that you need to pass is a function that gets called in each case.

At the task level, you have an extra parameter for callback called `on_retry_callback` to be used whenever a retry is executed on that task.

```python
# add callback examples here
```

### Levereging retries
Retries are useful parameters that enables you to have a better control over the behaviour of your DAGs and tasks. Specially for tasks that are accessing external service like API, it might be a good idea to define a retry value in order to execute it more than once if there's a problem with connection.
You can define the parameter `retries` on your DAG or tasks instances, and by default it follows the value that's set on the `airflow.cfg` file on `default_task_retry` (CHECK THIS PARAMETER).
To define the time your tasks must wait before retrying you can set the parameter `retry_delay` (the default is `300` seconds, 5 minutes).
The `retry_exponential_backoff` parameter doubles your retry delay time on every round (example, 5 minutes, 10 minutes, 20 minuted, ...) and `max_retry_delay` sets the maximun time your can retry reach when doubling.

### SLAs
Service Level Agreements are a kind of contracts associated to digital products that states specific behaviours it's suppose to display. The idea behind of SLAs is to stablish a threshold of specific metrics so that the customer can verify if it's suitable for the intended use.

In the case of your DAG, you define an SLA for the maximun time it's supposed to run, and if this threshold is reached, Airflow sends you a message stating all the informations about it.

To implement SLAs on your tasks, you need to define the parameter `sla` with a `datetime.delta` object. And in order to receive the message, you must create a custom function and pass it to your DAG parameter `sla_miss_callback`.

```python
# add code for sla callback function and parameter definition
```

Important to notice that you need to configure the SMTP server and email parameters for your DAG to receive the SLA missed callback message. More information on how to do it can be found in the [Astronomer Manage Airflow DAG notifications Documentation](https://docs.astronomer.io/learn/error-notifications-in-airflow#email-notifications).
And finally, if you trigger you DAGs manually, the SLA won't be checked, only when it follows the schedule date.

### DAG versioning
Airflow has some limitations in term of DAG versioning. Let's see each type of update you can have with yout DAGs to decide how to proper deal with limitations.

1. **Updating task code/logic:** Whenever you update the code of a task what's going to happen is that new task instances are going to be executed with this new logic. So the only problem that you may have is when looking at logs from previous task instances, the output of the log won't be correlated with the current state of the `< > Code` tab.
2. **Adding new tasks:** Whenever new tasks are added to your DAG, Airflow display empty tasks squares related to new task on the grid tab. But in practical terms, you won't have problems with future executions.
3. **Removing tasks from your DAG:** This is the most problematic, as the removed task information and its logs from would not be accessible anymore. So you should avoid it at all cost.

A good practice to try to implement a rudimentary version system to your DAGs is by adding a sufix to the `dag_id` with the versioning convention `1_0_0`. So whenever you change something that might be critical to your DAG, you simply replace the `dagname_1_0_0`, with `dagname_1_0_1`, and a new DAG would be created, keeping the old version saved. Just don't forget to turn off the old DAG, and turn on the new one.

### Dynamic DAGs

## TO DO LIST:

- Explain to deploy Airflow using Docker Compose locally and compare it to Astro CLI
- How to use Airflow REST API to do stuff
- Describe Registry and add a few pictures
- Add session on ShortCircuit operator on branching
- Add code for SLA



## References
1. [Get Docker (Docker Offical Documentation)](https://docs.docker.com/desktop/install/ubuntu/)
2. [Overview of installing Docker Compose (Docker Offical Documentation)](https://docs.docker.com/compose/install/)
3. [Running Airflow in Docker (Apache Airflow Offical Documentation)](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
4. [Install Astro CLI (Astronomer Docs)](https://docs.astronomer.io/astro/cli/install-cli?tab=linux#install-the-astro-cli)
5. [Airflow Components (Astronomer)](https://docs.astronomer.io/learn/airflow-components) 
6. [Apache Airflow Task Instance Guide (Restack)](https://www.restack.io/docs/airflow-knowledge-task-instance-state-machine-example-attributes)
7. [The Python pickle Module: How to Persist Objects in Python (Real Python)](https://realpython.com/python-pickle-module/)
8. [Branching in Airflow](https://docs.astronomer.io/learn/airflow-branch-operator)
9. [Airflow sensors (Astronomer)](https://docs.astronomer.io/learn/what-is-a-sensor?tab=traditional#example-implementation)
10. [Manage Airflow DAG notifications (Astronomer)](https://docs.astronomer.io/learn/error-notifications-in-airflow#email-notifications)