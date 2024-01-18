"""Creating views for health-check"""



from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def health_check(request):
    """Return successful response."""
    return Response({'healthy': True})