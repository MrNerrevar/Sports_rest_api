# Spectate REST API

This is a simple REST API built with Python and Sanic that manages multiple sports, events, and selections.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation and Running](#installation-and-running)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Example Requests](#example-requests)

## Overview
- Manage Sports, Events and Selections with multiple relational parameters.
- Automatically fetch and store team logos when creating events.
- Containerized using docker.

## Project Structure
````
├── app.py 
├── models.py
├── enums.py
├── db.py
├── routes/
│ ├── sports.py
│ ├── events.py
│ ├── selections.py
│ ├── populate.py
│ ├── init.py
├── tests/
│ ├── utils_test.py
├── requirements.txt
├── Dockerfile
├── compose.yml
├── populate.json
└── README.md
````

## Installation and Running
- Clone the repository:
    ```sh
    git clone https://github.com/MrNerrevar/spectate_rest_api.git
    cd spectate_rest_api
    ```
- Build and run the docker container:
    ```sh
    docker build --tag=spectate_rest_api
    docker run -p 8000:8000 spectate_rest_api
    ```
- The API will be accessible via `http://localhost:8000`


## Usage
### API Endpoints

#### Sports
- **GET /sport**: Get all sports
- **POST /sport**: Create a new sport
- **PATCH /sport/{sport_id}**: Update a sport
- **POST /sport/search**: Search for sports by name

#### Events
- **GET /event**: Get all events
- **POST /event**: Create a new event
- **PATCH /event/{event_id}**: Update an event

#### Selections
- **GET /selection**: Get all selections
- **POST /selection**: Create a new selection
- **PATCH /selection/{selection_id}**: Update a selection

### Populate
- **POST /populate**: Clear all data from the database and repopulate with dummy json data

## Example Requests
### Sports
- The Slug is auto generated from the provided name
- Active status is defaulted to False until the sport has an active associated event
    ```
    {
        "Name": "Football"
    }
    ```

### Events
- The Slug is auto generated from the provided name
- Active status is defaulted to False until the sport has an active associated event
- The ActualStart value is generated when the event Status is set to "STARTED"
- Logos are fetched automatically based on the teams provided in the event name
    ```
    {
        "Name": "Chelsea vs Arsenal",
        "Type": "PREPLAY",
        "Sport": "1",
        "Status": "PENDING",
        "ScheduledStart": "2024-07-10T15:00:00"
    }
    ```

### Selections
- Selections have no auto generated values
- When the selection is set to Active, it will propagate that Active status back through associated events and sports
    ```
    {
        "Name": "Match Bet",
        "Event": 1,
        "Price": 35.48,
        "Active": 0,
        "Outcome": "LOSE"
    }
    ```