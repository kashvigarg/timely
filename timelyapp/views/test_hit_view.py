from .imports import *


class TestHitView(APIView):
    def get(self, request, format= None):
        return Response(
            status=status.HTTP_200_OK,
            data={
                "error": False,
                "error_message": "",
                "success_message": "API test successful.",
                "data": {
                    
                }
            }
           )
    
