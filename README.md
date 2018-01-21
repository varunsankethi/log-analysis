# LOG-ANALYSIS-PROJECT

This project is used to generate a report based on logs generated from a newspaper website
Running the program will yield answers to the below 3 questions

-- What are the most popular three articles of all time?
-- Who are the most popular article authors of all time? 
-- On which days did more than 1% of requests lead to errors?

# LANGUAGE SPECIFICATION

The project is implemented in python and uses PostgreSQL as its backend database

# PRE-REQUISITS

1. Install Vagrant and virtual box
2. Download udacity vagrant directory
3. Download common code for database as a zip file from [here](https://github.com/udacity/fullstack-nanodegree-vm)
4. Step 2 will provide newsdata.sql

# INSTALL

1. Go into udacity vagrant directory (from command prompt/gitbash shell) which you unzipped
2. run `vagrant up` to bring up the virtual machine
3. run `winpty vagrant ssh` on windows or `vagrant ssh` on linux based machine to connect to the linux machine on vagrant
4. change into /vagrant directory
5. use command psql -d news -f newsdata.sql to load database 
6. run `python log.py`

# PSQL VIEWS

## view full_log_count

`CREATE OR REPLACE VIEW full_log_count as
SELECT date(time) time_as_date , COUNT(*) as full_count FROM log
GROUP BY time_as_date 
ORDER BY full_count desc;`

## view bad_request_log_count 

`CREATE OR REPLACE VIEW bad_request_log_count as
SELECT date(time) as tad , COUNT(*) as bad_request_count FROM log
WHERE status = '404 NOT FOUND'
GROUP BY tad
ORDER BY bad_request_count desc;`

## view percentage_error

`CREATE OR REPLACE VIEW percentage_error as
SELECT full_log_count.time_as_date,
round((100.0*bad_request_log_count.bad_request_count)/full_log_count.full_count,3) AS err
FROM bad_request_log_count, full_log_count
WHERE bad_request_log_count.tad=full_log_count.time_as_date;`
