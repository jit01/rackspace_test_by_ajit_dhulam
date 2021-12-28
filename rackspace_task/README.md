# Rackspace task - Ajit Dhulam.
https://gist.github.com/jbartels/d75a9f5282abebe071694723a5f25f0e

## Overview:
This app depends on Django.

Used **python3** as base image.

This repo contains Django app and test cases. 

Users can add items from list available. 

Total and price of each item, coupons applied will be updated automatically once the user click the **Submit** button in UI.

Implemented all 4 coupons - **BOGO**, **APPL**, **CHMK**, and **APOM**.
As there were no example cases for 4th coupon **APOM** in problem statement, so by definition I consider limit 1  

I thought of using database for storing items. But realised that it becomes much complex for this simple use case.

The final output UI is not as per the list mentioned in problem statement, But in a readable format. please refer attach
screenshots.

## Pre-requisites:
1. Docker

## Steps to run.
Run the commands in **powershell** or **terminal**, at root folder of this project

1. Build the docker image using the Dockerfile provided and following command:
   
   `docker-compose build`
2. Run the docker container using following command.
   
   `docker-compose up`
3. Django Server will be up and running. Open the browser and hit http://127.0.0.1:8000/ to see UI. 
   You can add new items from UI and the list will be automatically updated and coupons will be automatically applied.
   
4. After cloning the repo locally, run test cases locally using below command it covered all 4 rules in test :

   `python rackspace_task/online_fruit/tests.py`

   ###Note: 
   another simple way to run all test cases is, open project in pycharm IDE right click on a test file and choose 
   "Run 'pytest in test.py' "
   
   
![Input](https://github.com/jit01/Rackspace_ajit/rackspace_task/input.png)
![Output](https://github.com/jit01/Rackspace_ajit/rackspace_task/output.png)

