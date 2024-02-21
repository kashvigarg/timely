from .imports import *

class ScheduleListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None):
        schedules = Schedule.objects.filter(user=user_id)
        serializer = ScheduleSerializer(schedules, many=True)
        if not serializer.data:
            return Response(
                status= status.HTTP_404_NOT_FOUND,
                data = {
                    "error" : True, 
                    "error_message" : "No schedules exist for user.", 
                    "success_message" : "", 
                    "data" : {}
                }
        )
        return Response(
                status= status.HTTP_200_OK,
                data = {
                    "error" : False, 
                    "error_message" : "", 
                    "success_message" : "", 
                    "data" : serializer.data
                }
        )

    def post(self, request, format=None):
        try:
            
            serializer = ScheduleSerializer(data=request.data)
            if serializer.is_valid():
                user_id = request.user.id
                
                user = get_user_model().objects.get(id=user_id)
                if not user:
                    raise PermissionDenied("User doesn't exist")

                serializer.save()

                
                return Response(
                status=status.HTTP_201_CREATED,
                data={
                "error": False,
                "error_message": "",
                "success_message": "Schedule created successfully",
                "data": serializer.data
                }
            )

        except get_user_model().DoesNotExist:
            raise PermissionDenied("User not found.")

        except PermissionDenied as e:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={
                    "error": True,
                    "error_message": str(e),
                    "success_message": "",
                    "data": {}
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

