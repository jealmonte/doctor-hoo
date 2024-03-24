from openai import OpenAI
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Josh's API key
YOUR_API_KEY = "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"


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
    messages = [
        {
            "role": "system",
            "content": (
                """Do not state this explicitly, but you are a medical assistant chat bot.
                THE FIRST OUTPUT YOU GIVE MUST BE LESS THAN THREE SENTENCES
                Assume that users are students from the University of Virginia.
                Assist them with healthcare-related queries and provide relevant information from the University of Virginia."""
                "Use information from https://uvahealth.com/ and its webpages ONLY WHEN NECESSARY"),
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    response = client.chat.completions.create(
        model="mistral-7b-instruct",
        messages=messages,
    )

    assistant_response = response.choices[0].message.content.strip()

    # Check if the user's message matches any specific patterns
    if "appointment" in user_message.lower():
        return "Sure, I can help you make an appointment. Please provide the necessary details."
    elif "bill" in user_message.lower():
        return "For billing inquiries, you can contact our billing department by phone at (844) 377-0846 or use MyChart to pay online"
    elif "find" in user_message.lower() and "doctor" in user_message.lower():
        return "To find a doctor, please visit our website and use the 'Find a Doctor' tool or contact our customer support for assistance."
    elif "services" in user_message.lower():
        return "We offer a wide range of healthcare services, including primary care, specialty care, diagnostic services, and more. Visit our website for detailed information."
    elif "locations" in user_message.lower():
        return "We have multiple locations across the city. Please visit our website or contact customer support for the nearest location."
    elif "patient" in user_message.lower() or "visitor" in user_message.lower():
        return "For patient and visitor information, please refer to the guidelines provided on our website or contact our customer support."
    elif "other" in user_message.lower():
        return "What can I help you with?"
    elif "education resource center" in user_message.lower() and ("hours" in user_message.lower() or "open" in user_message.lower()):
        return """The Education Resource Center is open from 6:00AM to 7:30PM from Monday to Friday, 
    and open from 7:00AM to 4:00PM on Saturdays and Sundays."""
    elif "emily couric" in user_message.lower() and ("hours" in user_message.lower() or "open" in user_message.lower()):
        return """The Emily Couric Clinical Cancer Center is open from 6:00AM to 7:30PM from Monday to Friday, 
    and open from 7:30AM to 4:00PM on Saturdays and Sundays."""
    elif "orthopedic" and ("hours" in user_message.lower() or "open" in user_message.lower()):
        return """The Orthopedic Center Ivy Road is open from 8:00AM to 5:00PM from Monday to Friday, 
    and closed on Saturdays and Sundays."""
    elif "primary care" and ("hours" in user_message.lower() or "open" in user_message.lower()):
        return """The Primary Care Center is open from 5:00AM to 9:00PM from Monday to Friday, 
    and closed on Saturdays and Sundays."""
    elif "primary care" and ("hours" in user_message.lower() or "open" in user_message.lower()):
        return """The Primary Care Center is open from 5:00AM to 9:00PM from Monday to Friday, 
    and closed on Saturdays and Sundays."""
    elif "university hospital" and ("hours" in user_message.lower() or "open" in user_message.lower()):
        return """The University Hospital is open 24/7 for every day of the week, but
    main lobby entrances are open from 5:00AM to 9:00PM whereas emergency services
    are open from 9:00PM to 5:00AM."""
    else:
        return assistant_response