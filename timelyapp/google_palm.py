import google.generativeai as palm
from django.conf import settings
import csv, json
from .models import Task, TimeSlab, TimeTable, Day

palm.configure(api_key=settings.PALM_API_KEY)
# Input message
input_message = json.dumps(
    {
  "longest_sitting_time": 2,
  "duration": 3,
  "starts_on": "21/02/24",
  "no_of_tasks": 3,
  "tasks": [
    {
      "task_id": 1,
      "task_name": "Task1",
      "priority": "HIGH",
      "estimated_length": 4,
      "difficulty": "EASY"
    },
    {
      "task_id": 2,
      "task_name": "Task2",
      "priority": "LOW",
      "estimated_length": 4,
      "difficulty": "EASY"
    },
    {
      "task_id": 3,
      "task_name": "Task3",
      "priority": "LOW",
      "estimated_length": 1,
      "difficulty": "MEDIUM"
    }
  ]
})

# Expected output message as a Python dictionary
output_message = {
  "timeslabs": [
    {
      "start_time": "09:00:00",
      "end_time": "11:00:00",
      "task_id": 1,
      "task_name": "Task1", 
      "date" : "2024-02-21T12:30:00", 
      "day" : "Wednesday"
    },
    {
      "start_time": "01:00:00",
      "end_time": "03:00:00",
      "task_id": 1,
      "task_name": "Task1", 
      "date" : "2024-02-21T12:30:00", 
      "day" : "Wednesday"
    },
    {
      "start_time": "09:00:00",
      "end_time": "11:00:00",
      "task_id": 2,
      "task_name": "Task2", 
      "date" : "2024-02-22T12:30:00", 
      "day" : "Thursday"
    },
    {
      "start_time": "01:00:00",
      "end_time": "03:00:00",
      "task_id": 2,
      "task_name": "Task2",
      "date" : "2024-02-22T12:30:00", 
      "day" : "Thursday"
    },
    {
      "start_time": "09:00:00",
      "end_time": "10:00:00",
      "task_id": 3,
      "task_name": "Task3", 
      "date" : "2024-02-23T12:30:00", 
      "day" : "Friday"
    }
  ]
}

# Convert the dictionary to a JSON-formatted string
output_message_json = json.dumps(output_message)

# Example with input and output
example = {"input": input_message, "output": output_message_json}

def get_response(schedule_duration_days, starts_on, longest_sitting_time_minutes, user_behaviour, tasks):
    msg = json.dumps({
    'schedule_duration_days': schedule_duration_days,
    'starts_on': starts_on,
    'longest_sitting_time_hours': longest_sitting_time_minutes,
    'user_behaviour': user_behaviour,
    'tasks': tasks
})

    response = palm.chat(messages='You will be provided with a schedule that has a start date, a fixed duration (in days), and a number of tasks. Each of these tasks has a difficulty value [EASY, MEDIUM, HARD], a priority, [LOW, HIGH, MEDIUM] and an estimated length (time period). You will also be provided with a LONGEST SITTING TIME in hours, that defines the total continuous period of study that the user is comfortable with. Generate a smart time table for the user, in accordance with this data. The output data should contain the following parameters in a structured format; For each provided task, a start and end time, the date and day within the deadline when they are to be studied. Please note that the user can have multiple sittings of studying one subject, but it is essential to complete the estimated length / time period for each task. Try to adjust the tasks within the given start date and the end date according to the given duration. Also account for adequate breaks. All the tasks must be completed, please ensure all tasks are present in the schedule. Adjust the start and end times according to the assumed breaks. Also please try to spread out the work evenly over the duration of days. Also the longest sitting time of the user must be taken into consideration. generate a time table for this, and return the solution in json format, Please do not create unmentioned tasks or task ids', context=(msg), examples=example)

    ans = response.last 
    ans_list = ans.split('```json')
    ans_f = ans_list[1].split('```')
    res = ans_f[0]
    f= json.loads(res)
    return f

