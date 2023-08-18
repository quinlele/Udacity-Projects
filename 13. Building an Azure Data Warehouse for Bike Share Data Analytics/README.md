# Building an Azure Data Warehouse for Bike Share Data Analytics

Divvy is a bike sharing program in Chicago, Illinois USA that allows riders to purchase a pass at a kiosk or use a mobile application to unlock a bike at stations around the city and use the bike for a specified amount of time. The bikes can be returned to the same station or to another station. The City of Chicago makes the anonymized bike trip data publicly available for projects like this where we can analyze the data.

### The Goal of this project is to develop a data warehouse solution using Azure Synapse Analytics:

- Design a star schema based on the business outcomes listed below
- Import the data into Synapse.
- Transform the data into the star schema
- and finally, view the report from Analytics.
  
### The business outcomes you are designing for are as follows:

1. Analyze how much time is spend per ride

- Based on date and time factors such as day of week and time of day
- Based on which station is the startin and / or ending station
- Based on age of the rider at time of the ride
- Based on whether the rider is a memeber or a casual rider

2. Analyze how much money is spent

- Per month, quarter, year
- Per member, based on the age of the rider at account start

3. EXTRA CREDIT - Analyze how much money is spent per member

- Based on how many rides the rider averages per month
- Based on how many minutes the rider spends on a bike per month

## Task 1: Create Azure resources

<img width="1277" alt="image" src="https://github.com/quinlele/Udacity-Projects/assets/52246911/ebef73dd-b036-4fde-9ee0-06f575237881">

## Task 2: Design a star schema

<img width="1128" alt="image" src="https://github.com/quinlele/Udacity-Projects/assets/52246911/2a432110-6688-41a1-945b-c6adb8c94ed9">
