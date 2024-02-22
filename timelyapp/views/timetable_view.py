from .imports import *

class TimetableView(APIView):
    def create_timetable_from_response(self, timeslab_data, schedule_color, user_id, schedule_id):
        timetable_data = {
            "user": user_id,
            "schedule": schedule_id,
            "timetable_color": schedule_color
        }

        timetable_serializer = TimeTableSerializer(data=timetable_data)
        timeslab_instance = None
        if timetable_serializer.is_valid():
            timetable_instance = timetable_serializer.save()
        else:
            return {
                "error": True,
                "error_message": timetable_serializer.errors,
                "success_message": "",
                "data": {}
            }

        all_timeslabs = []
        for timeslab in timeslab_data:
            tasks_id = timeslab['task_id']
            
            task_objs = Task.objects.filter(id = tasks_id)
            
            if task_objs.count() == 0:
                
                continue
            timeslab_data = {
                "date": timeslab['date'],
                "day": timeslab['day'],
                "start_time": timeslab['start_time'],
                "end_time": timeslab['end_time'],
                "timetable": timetable_instance.id,
                "task": timeslab['task_id'],
                "task_name": timeslab['task_name'],
                "timeslab_color": schedule_color
            }

            timeslab_serializer = TimeSlabSerializer(data=timeslab_data)
            if timeslab_serializer.is_valid():
                timeslab_instance = timeslab_serializer.save()
                all_timeslabs.append(timeslab_serializer.data)
            else:
                # Rollback timetable creation if timeslab creation fails
                timetable_instance.delete()
                return {
                    "error": True,
                    "error_message": timeslab_serializer.errors,
                    "success_message": "",
                    "data": {}
                }

        return {
            "timetable_serializer": timetable_serializer,
            "timetable_id": timetable_instance.id,
            "all_timeslabs": all_timeslabs
        }

    def post(self, request, format=None):
        user_id = request.data['user_id']
        schedule_id = request.data['schedule_id']

        schedule = Schedule.objects.filter(user_id=user_id, id=schedule_id).first()

        schedule_serializer = ScheduleSerializer(schedule)
        schedule_duration_days = schedule_serializer.data['duration']
        starts_on = schedule_serializer.data['starts_on']
        longest_sitting_time_minutes = schedule_serializer.data['longest_sitting_time']
        user_behaviour = schedule_serializer.data['behaviour']

        all_tasks = Task.objects.filter(schedule_id=schedule_id)

        task_serializer = TaskSerializer(all_tasks, many=True)
        tasks = task_serializer.data

        palm_data = get_response(schedule_duration_days, starts_on, longest_sitting_time_minutes, user_behaviour, tasks)
        result = self.create_timetable_from_response(timeslab_data=palm_data['timeslabs'], schedule_color=schedule.schedule_color, user_id=user_id, schedule_id=schedule_id)

        if not result.get("error", False):
            timetable_serializer = result["timetable_serializer"]
            timetable_id = result["timetable_id"]
            all_timeslabs = result["all_timeslabs"]

            if timetable_serializer.is_valid():
                schedule.has_timetable = True
                schedule.save()

                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "error": False,
                        "error_message": "",
                        "success_message": f"Timetable fetched successfully.",
                        "data": {
                            "timetable": timetable_serializer.data,
                            "timeslabs": all_timeslabs
                        }
                    }
                )
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        "error": True,
                        "error_message": "Time table couldn't be generated for the given schedule id",
                        "success_message": "",
                        "data": {}
                    }
                )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=result
            )
