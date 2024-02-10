import google.generativeai as palm
from django.conf import settings
import csv, json

palm.configure(api_key=settings.PALM_API_KEY)
# Input message
input_message = json.dumps({
    "schedule_duration_days": 1,
    "starts_on": "10/02/2024",
    "longest_sitting_time_minutes": 120,
    "user_behaviour": "lazy",
    "tasks": [
        {"id": 1, "name": "Task1", "difficulty": 2, "priority": 1, "no_of_revisions": 2, "schedule_id": 1, "task_id": 1},
        {"id": 2, "name": "Task2", "difficulty": 2, "priority": 1, "no_of_revisions": 2, "schedule_id": 1, "task_id": 2}
    ]
})

# Expected output message as a Python dictionary
output_message = {
    "timetable": {
        "days": {
            "day_1": {
                "date": "10/02/2024",
                "time_slabs": [
                    {
                        "start_time": "08:00 AM",
                        "end_time": "10:00 AM",
                        "tasks": [
                            {
                                "id": 1,
                                "name": "Task1",
                                "difficulty": 2,
                                "priority": 1,
                                "no_of_revisions": 2,
                                "schedule_id": 1,
                                "task_id": 1
                            }
                        ]
                    },
                    {
                        "start_time": "10:30 AM",
                        "end_time": "12:30 PM",
                        "tasks": [
                            {
                                "id": 2,
                                "name": "Task2",
                                "difficulty": 2,
                                "priority": 1,
                                "no_of_revisions": 2,
                                "schedule_id": 1,
                                "task_id": 2
                            }
                        ]
                    },
                    {
                        "start_time": "01:30 PM",
                        "end_time": "03:30 PM",
                        "tasks": []
                    },
                    {
                        "start_time": "04:00 PM",
                        "end_time": "06:00 PM",
                        "tasks": []
                    }
                ]
            }
        }
    }
}

# Convert the dictionary to a JSON-formatted string
output_message_json = json.dumps(output_message)

# Example with input and output
example = {"input": input_message, "output": output_message_json}

def get_response(schedule_duration_days, starts_on, longest_sitting_time_minutes, user_behaviour, tasks):
    msg = json.dumps({
    'schedule_duration_days': schedule_duration_days,
    'starts_on': starts_on,
    'longest_sitting_time_minutes': longest_sitting_time_minutes,
    'user_behaviour': user_behaviour,
    'tasks': tasks
})

# [
#             {"id": 1, "name": "Task1", "difficulty": 2, "priority": 1, "no_of_revisions": 2, "schedule_id": 1, "task_id": 1},
#             {"id": 2, "name": "Task2", "difficulty": 2, "priority": 1, "no_of_revisions": 2, "schedule_id": 1, "task_id": 2}
#         ]
    response = palm.chat(messages='Generate a time table for the given schedule, keeping in mind the priority of the tasks, the user\'s behaviour and plan sets of tasks according to the schedule duration days limit as mentioned, with the longest_sitting_time as the longest contiguous study chunk. return time table in json', context=(msg), examples=example)
    # print(response.last)
    ans = response.last 
    ans_list = ans.split('```json')
    ans_f = ans_list[1].split('```')
    res = ans_f[0]
    print(ans_f[0])
    f= json.loads(res)
    return f



    # with open('./timelyapp/timely_prompts.csv') as file:
    #     csv_reader = csv.DictReader(file)
    #     examples = []
    #     for row in csv_reader:
    #         input_message = row['input:']
    #         output_message = row['output:']
    #         examples.append({"input": input_message, "output": output_message})

    # print(examples)