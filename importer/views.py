from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import importer.service as import_service


@api_view(['POST'])
@protected_resource()
def jmmb_importer(request, investor_id, portfolio_id):
    """
    Retrieve, update or delete a stock.
    """
    if request.method == 'POST':
        if request.FILES['file']:
            import_service.save_jmmb_uploaded_file(investor_id, portfolio_id, request.FILES['file'])
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
