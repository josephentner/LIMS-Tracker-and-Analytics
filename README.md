# MySQL + Flask LIMS Project

A laboratory information management system (or LIMS for short) is 
an essential for any biotech company. It allows you to keep track of
any samples and associated data. This project creates a LIMS that 
contains mock data with protein samples and associated data related
to assays (experiments) conducted on these samples.

This repo spins up 2 docker containers: 
1. A MySQL 8 container to create the database
1. A Python Flask container to implement a REST API

In the backend, the database is created with 14 tables including 
a users, experiment, protein, protein batch, target, cell line,
and 8 assay-specific tables. The database uses the relational model 
for design and is normalized to 3NF.

A Flask app is created to interact with the database and there are multiple
routes that can be called that both display aggregated data and allow 
updates and insert of new data. 

The flask routes are split into three categories, each being a "persona"
associated with the database. The first is the lab assistant, who runs
assays related sample properties and composition. The second is scientist, 
who can track other scientists/lab assistants, create new proteins, 
and run in vitro assays (placing samples in cell culture). The third is data analyst, 
who can view the raw data as well as aggregated data to help make
conclusions regarding the samples.

Along with these backend components, there is a frontend AppSmith UI that
demonstrates interactivity with the Flask routes. A demo of the Flask routes 
and UI can be found here: https://www.youtube.com/watch?v=PWOa2mDRACQ

To run this project:
    - Ensure Docker Desktop and MySQL are installed
    - Clone the repository
    - Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
    - Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the `webapp` user. 
    - Open a terminal, navigate to the project
    - Build the images with `docker compose build`
    - Start the containers with `docker compose up`




