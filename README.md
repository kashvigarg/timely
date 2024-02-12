# Django API for TIMELY 

## Overview

This repository contains a Django API for generating timetables based on user schedules and tasks. The API leverages the Google PALM algorithm for efficient timetable creation. Additionally, it includes user authentication, task management, and schedule creation functionalities.


## Features

- **Timetable Generation**: Utilizes the Google PALM algorithm to generate timetables based on user schedules and tasks.

- **User Authentication**: Secure user registration and login functionalities are implemented using Django authentication and token-based authentication.

- **Task Management**: Users can create, retrieve, and manage tasks associated with their schedules.

- **Schedule Creation**: Allows users to create schedules with specific parameters for the timetable generation algorithm.


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repository.git

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Apply migrations:
   ```bash
   python manage.py migrate

4. Run the development server:
   ```bash
   python manage.py runserver
   
The API will be accessible at http://localhost:8000/.


## API Endpoints

### `/palm_response/`

Endpoint for testing the Google PALM algorithm. Returns a JSON response with a timetable based on a sample prompt.

### `/tasks/{schedule_id}/`

- **GET**: Retrieve all tasks for a specific schedule.
- **POST**: Create a new task for the specified schedule.

### `/schedules/`

- **GET**: Retrieve all schedules for the authenticated user.
- **POST**: Create a new schedule for the authenticated user.

### `/schedules/{schedule_id}/timetable/`

- **GET**: Generate a timetable for the specified schedule based on PALM algorithm.
