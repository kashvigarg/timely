from .imports import *

class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            user = serializer.save()

            success_message = f"Account created for {username}"
            error_message = ""
            error = False
            data = {
                "user_id" : user.id
            }

            return Response(
                status= status.HTTP_200_OK,
                data = {
                    "error" : error, 
                    "error_message" : error_message, 
                    "success_message" : success_message, 
                    "data" : data
                }
        )
        
        error_message = serializer.errors
        error = True
        success_message = ""
        data = { }
        return Response(
            status= status.HTTP_400_BAD_REQUEST,
                data = {
                    "error" : error, 
                    "error_message" : error_message, 
                    "success_message" : success_message, 
                    "data" : data
                }
        )


class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
   
            authenticate(request, username=email, password=password)
            user = get_user_model().objects.get(email=email)
            if user is not None and user.is_active:
                
                auth.login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                print(token)
                

                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "error": False,
                        "error_message": "",
                        "success_message": "Logged in successfully",
                        "data": {
                            "token": token.key
                        }
                    }
                )

            elif user is not None and not user.is_active:
                error_message = "User account is not active. Please contact support."

            else:
                error_message = "Invalid credentials."

        else:
            error_message = serializer.errors

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={
                "error": True,
                "error_message": error_message,
                "success_message": "",
                "data": {}
            }
        )
    

class GetIdView(APIView):
    def post(self, request, format=None):
       serializer = EmailSerializer(request.data)
       
       email = serializer.data['email']
       print(serializer.data['email'])
      
       user = CustomUser.objects.filter(email=email).get()
       
       if not user:
           return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={
                "error": True,
                "error_message": f"User with email {email} doesn't exist.",
                "success_message": "",
                "data": {
                    
                }
            }
           )
       else:
           
           return Response(
            status=status.HTTP_200_OK,
            data={
                "error": False,
                "error_message": "",
                "success_message": f"User with email {email} fetched successfully.",
                "data": {
                    "user_id": user.id,
                    "email" : email,
                    "username" : user.username
                }
            }
           )