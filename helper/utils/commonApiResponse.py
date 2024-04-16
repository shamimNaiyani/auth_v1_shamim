from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status 


def CommonApiResponse(data=None, message=None, status_code=None, errors=None):
    response_data = {
        "success": status.is_success(status_code),
        "status_code": status_code,
        "message":  message if message else status.HTTP_200_OK,
        "data": data if data else {},
        "errors": errors if errors else {},
    }
    
    response = Response(response_data, status=status_code)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json" 
    response.renderer_context = {}
    response.render()
    
    return response 