# class TaskDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return Task.objects.get(pk=pk)
#         except Task.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         task = self.get_object(pk)
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ScheduleDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return Schedule.objects.get(pk=pk)
#         except Schedule.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         schedule = self.get_object(pk)
#         serializer = ScheduleSerializer(schedule)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         schedule = self.get_object(pk)
#         serializer = ScheduleSerializer(schedule, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         schedule = self.get_object(pk)
#         schedule.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class TimeTableListCreateView(APIView):
#     def get(self, request, format=None):
#         timetables = TimeTable.objects.all()
#         serializer = TimeTableSerializer(timetables, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = TimeTableSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TimeTableDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return TimeTable.objects.get(pk=pk)
#         except TimeTable.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         timetable = self.get_object(pk)
#         serializer = TimeTableSerializer(timetable)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         timetable = self.get_object(pk)
#         serializer = TimeTableSerializer(timetable, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         timetable = self.get_object(pk)
#         timetable.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

