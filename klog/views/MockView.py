from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def getStructureWithExceptions(request):
    estructura = {
        "name": "src",
        "children": [
            {
                "name": "game",
                "children": [
                    {
                        "name": "map",
                        "children": [
                            {"name": "Rock", "size": 17},
                            {"name": "Tree", "size": 152}
                        ]
                    },
                    {"name": "login",
                     "children": [
                         {"name": "Login", "size": 453
                          }]
                     }]
            }]
    }
    return JsonResponse(estructura)