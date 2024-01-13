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
```bash

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



## References
1. [Get Docker (Docker Offical Documentation)](https://docs.docker.com/desktop/install/ubuntu/)
2. [Overview of installing Docker Compose (Docker Offical Documentation)](https://docs.docker.com/compose/install/)
3. [Running Airflow in Docker (Apache Airflow Offical Documentation)](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)