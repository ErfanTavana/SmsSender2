from rest_framework.response import Response
from rest_framework import status

def check_user_organization(request):
    """
    Checks if the user is authenticated and belongs to an organization.
    Returns a tuple (user, organization_user) if valid, otherwise returns a Response object with the appropriate error.
    """
    if not request.user.is_authenticated:
        return Response(data={'message': 'لطفا وارد شوید.', 'data': {}}, status=status.HTTP_401_UNAUTHORIZED), None, None

    user = request.user
    organization_user = user.organization

    if not organization_user:
        return Response({'message': 'از ادمین بخواهید سازمان شما را مشخص کند.', 'data': {}}, status=status.HTTP_400_BAD_REQUEST), user, None

    return None, user, organization_user
