from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .ai_service import analyze_image
from .models import Image
from .serializers import ImageSerializer


class ImageUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        image = Image.objects.create(
            file=file,
            filename=file.name,
        )

        result = analyze_image(image.file.path)

        image.tags = result['tags']
        image.description = result['description']
        image.is_processed = True
        image.save()

        return Response(ImageSerializer(image).data, status=status.HTTP_201_CREATED)


class ImageListView(APIView):
    def get(self, request):
        images = Image.objects.all().order_by('-uploaded_at')
        return Response(ImageSerializer(images, many=True).data)


class ImageSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'error': 'Query parameter "q" is required.'}, status=status.HTTP_400_BAD_REQUEST)

        images = Image.objects.filter(tags__contains=query).order_by('-uploaded_at')
        return Response(ImageSerializer(images, many=True).data)
