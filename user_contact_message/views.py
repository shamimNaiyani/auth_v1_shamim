from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactForm(APIView):

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Message sent successfully!'}, status=201)
        return Response(serializer.errors, status=400)
