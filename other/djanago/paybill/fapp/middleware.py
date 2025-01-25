# from django.conf import settings
# from django.http import HttpResponseRedirect
# from django.urls import reverse

# class AdminSessionMiddleware:
#     def __init__(self , get_response):
#         self.get_response = get_response

#     def __call__(self,request):
        
#         if request.path.startswith('/admin/'):
#             settings.SESSION_COOKIE_NAME = 'admin_session'
#         else:
#             settings.SESSION_COOKIE_NAME = 'user_session'
        
#         response = self.get_response
#         return response