# Booker-API

Booker-API is a Django-Rest based movie ticket booking api integrating with Sqlite and optimized database query using indexed and various other ways. And, also automated deleting of expired tickets using crontab(time-based job scheduler in Unix).

Features of the api:

1. Book a ticket using a user’s name, phone number, and timings.
2. Update a ticket timing.
3. View all the tickets for a particular time.
4. Delete a particular ticket.
5. View the user’s details based on the ticket id.
6. Mark a ticket as expired if there is a diff of 8 hours between 
   the ticket timing and current time.
7. Delete all the tickets which are expired automatically.

## Preview

1. Booking a ticket using name, phone, time and date.
![Create Ticket](https://raw.githubusercontent.com/SDISON/Booker-API/master/images/CreateTicket.png)

2. Update the registered ticket time.
![Update Time](https://raw.githubusercontent.com/SDISON/Booker-API/master/images/UpdateTime.png)

3. View all tickets of a particular time.

* Using old time used in registered.
![View ByTime-old](https://raw.githubusercontent.com/SDISON/Booker-API/master/images/ViewByTime-OLD.png)

* Using the updated time.
![View ByTime-new](https://raw.githubusercontent.com/SDISON/Booker-API/master/images/ViewByTime-Update.png)

4. Delete a ticket using ticket id.
![Delete Ticket](https://raw.githubusercontent.com/SDISON/Booker-API/master/images/DeleteTicket-1.png)

5. View a ticket from ticket id.

* Before delete
![View Ticket](https://raw.githubusercontent.com/SDISON/Booker-API/master/images/ViewTicket.png)

* After delete.
![View Ticket-del](https://raw.githubusercontent.com/SDISON/Booker-API/master/images/ViewTicket-DEL.png)

6. Mark a ticket expire.
![Mark Expire](https://raw.githubusercontent.com/SDISON/Booker-API/master/images/Mark-Expire.png)

7. Delete all expire ticket using cron-job.

## Implemenation Details

This project is divided into 2 parts:
1. Booker app - Contains the helper functions for api to interact with databse and update the changes.
2. API app - Contains all api functions to interact with the user.

### Ticket Table:
    
Model a Ticket table to store the user information like name, date, phone and time. We need to have a unique ticket-id so we indexed our database on this to query efficiently.\
As, we have unique id of object, we use it in this formula to get the ticket-id for the ticket.

##### [ticket-id = 1000000 + (3128 * id)]

The queries effectively outputted using this are:

* Update the time of a ticket.
* Delete a ticket.
* View ticket details.
* Mark a ticket expire.

### Time-Based Table:

This model table is used to store the slots and the ticket-id registered for that slot.\
As, we know to output query like tickets of a particular time we need to search the whole database but to optimized this query, we need to generate this slot table.

##### Features of Slot Table:
 
1. Unique Slot id which helps in indexing the database and query all the slot tickets optimizely. Slot-id is generated using the concatenation of date and time.

##### [SlotId = ((((year X 10+month) X 10+date) X 10+hour) X 10+minute)]    '+' is concatenation

So, for a given time we just generate the slot-id and output all the tickets fastly.

### Cron-Job:

We have written a cron-job using the django-cron to run a function to check all the tickets whether they are expired or not is yes then it delete all these type of tickets from the database. Our cron-job runs every 1 hour to check the entries in the databse.

## Api Links

1. [http://127.0.0.1:8000/api/CreateTicket/]() - POST
   
2. [http://127.0.0.1:8000/api/UpdateTime/(?P<pk>[0-9]+)]() - PUT

3. [http://127.0.0.1:8000/api/ViewByTime/]() - POST

4. [http://127.0.0.1:8000/api/DeleteTicket/(?P<pk>[0-9]+)]() - DELETE

5. [http://127.0.0.1:8000/api/ViewTicket/(?P<pk>[0-9]+)]() - GET

6. [http://127.0.0.1:8000/api/MarkExpire/(?P<pk>[0-9]+)]() - PUT

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all requirements.
```bash
pip3 install -r requirements.txt
```

Run the command to run the server
```bash
python3 manage.py runserver
```
To use the cron-job move to the etc/crontab and add a line at the end.
```
 */1 *	* * *	root    source <path-to-bashrc>-
 && source <path-to-virtual-environment>-
 && python <path-to-manage.py> runcrons
```
Please remember to set the PATH = $PATH and SHELL = bin/bash

## Testing

To run the API test case on all api functions.
```bash
python manage.py test
```

To run the cron-job.
```bash
python manage.py runcrons
```
