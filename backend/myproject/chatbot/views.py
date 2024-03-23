from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import nltk
from nltk.chat.util import Chat, reflections

# Define your chatbot patterns and responses
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how are you today?"]
    ],
    [
        r"hi|hey|hello",
        ["Hello!", "Hey there!"]
    ],
    [
        r"what is your name?|whats your name|what's your name|what's your name?|what is your name|whats your name?",
        ["You can call me Doctor Hoo. I'm here to assist you!"]
    ],
    [
        r"make an appointment|appointment",
        ["Sure, I can help you make an appointment. Please provide the necessary details."]
    ],
    [
        r"billing",
        ["For billing inquiries, please contact our billing department at billing@example.com or call 123-456-7890."]
    ],
    [
        r"find doctor",
        ["To find a doctor, please visit our website and use the 'Find a Doctor' tool or contact our customer support for assistance."]
    ],
    [
        r"services",
        ["We offer a wide range of healthcare services, including primary care, specialty care, diagnostic services, and more. Visit our website for detailed information."]
    ],
    [
        r"locations",
        ["We have multiple locations across the city. Please visit our website or contact customer support for the nearest location."]
    ],
    [
        r"patient|visitor",
        ["For patient and visitor information, please refer to the guidelines provided on our website or contact our customer support."]
    ],
    [
        r"quit",
        ["Thank you for chatting with me. Have a great day!"]
    ],
]

chatbot = Chat(pairs, reflections)

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data['message']
        
        response = process_user_message(user_message)
        
        return JsonResponse({'message': response})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def process_user_message(user_message):
    response = chatbot.respond(user_message)
    
    if response:
        return response
    else:
        return "I'm sorry, I didn't understand your request. Please try again."