from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Temporarily disable CSRF token for testing
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data['message']
        # Logic to get chatbot response
        chatbot_response = "Echo: " + user_message  # Simplified response logic for testing
        return JsonResponse({'message': chatbot_response})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
