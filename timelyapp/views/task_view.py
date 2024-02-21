from .imports import *

class TaskListCreateView(APIView):
    def get(self, request, schedule_id, format=None):
        tasks = Task.objects.filter(schedule_id=schedule_id)
        serializer = TaskSerializer(tasks, many=True)
        tasks_count = tasks.count()
        
        if serializer:
            return Response(
            status=status.HTTP_200_OK,
            data={
                "error": False,
                "error_message": "",
                "success_message": f"Tasks count for schedule {schedule_id} retrieved successfully.",
                "data": {
                    "schedule_id": schedule_id,
                    "tasks_count": tasks_count, 
                    "tasks" : serializer.data
                }
            }
        )

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
            "error": True,
            "error_message": serializer.errors,
            "success_message": "",
            "data": {}
        }
    )
    
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(
            status=status.HTTP_201_CREATED,
            data={
                "error": False,
                "error_message": "",
                "success_message": "Task created successfully",
                "data": serializer.data
            }
        )

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
            "error": True,
            "error_message": serializer.errors,
            "success_message": "",
            "data": {}
        }
    )

    def delete(self, request, task_id, format=None):
        task = Task.objects.filter(id = task_id)

        task.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={
            "error": False,
            "error_message": "",
            "success_message": "Task deleted successfully",
            "data": {}
        }
    )


