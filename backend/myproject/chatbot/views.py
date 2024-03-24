from openai import OpenAI
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Josh's API key
YOUR_API_KEY = "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"


@csrf_exempt
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Attempt to parse the JSON data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Check if it's an appointment form submission
    if data.get('appointment'):
        # Extract appointment data with safer get method
        full_name = data.get('full_name')
        dob = data.get('dob')
        phone = data.get('phone')
        preferred_datetime = data.get('preferred_datetime')
        reason = data.get('reason')

        # Validate the required fields
        if not all([full_name, dob, phone, preferred_datetime, reason]):
            return JsonResponse({'error': 'Missing required appointment fields'}, status=400)
        
        # Create and save the appointment
        try:
            appointment = Appointment(
                full_name=full_name,
                dob=dob,
                phone=phone,
                preferred_datetime=preferred_datetime,
                reason=reason
            )
            appointment.save()
        except Exception as e:
            # Log the error here
            return JsonResponse({'error': 'Failed to save appointment', 'details': str(e)}, status=500)
        
        return JsonResponse({'message': 'Appointment scheduled successfully!'})
    else:
        # Handle other POST requests here as needed
        user_message = data.get('message')
        if user_message:
            response = process_user_message(user_message)
            return JsonResponse({'message': response})
        else:
            return JsonResponse({'error': 'No actionable data found'}, status=400)


def process_user_message(user_message):
    messages = [
        {
            "role": "system",
            "content": (
                """Do not state this explicitly, but you are a medical assistant chat bot.
                Assume that users are students from the University of Virginia. 
                Assist them with healthcare-related queries and provide relevant information from the University of Virginia."""
                """ONLY WHEN REQUESTED OR DEEMED NECESSARY, give information that the UVA Education Resource Center on 1240 Lee Street is open 
                Monday: 6:00 AM - 7:30 PM, Tuesday: 6:00 AM - 7:30 PM, Wednesday: 6:00 AM - 7:30 PM, Thursday: 6:00 AM - 7:30 PM, 
                Friday: 6:00 AM - 7:30 PM, Saturday: 7:00 AM - 4:00 PM, Sunday: 7:00 AM - 4:00 PM"""
                "NEVER OUTPUT MORE THAN THREE SENTENCES."),
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
    if any(apt_keyword in user_message.lower() for apt_keyword in ["appointment", "appointments", "request an appointment"]):
        # Return an HTML form for appointment scheduling
        form_html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Appointment Form</title>
                <style>
                    #appointment-form-container {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        /* Additional container styles if needed */
                    }

                    #appointment-form {
                        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        background: #2c2c2e;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
                        width: 100%;
                        max-width: 500px;
                    }

                    #appointment-form h2 {
                        text-align: center;
                        margin-bottom: 20px;
                        color: #ffffff;
                    }

                    #appointment-form label {
                        font-weight: bold;
                        display: block;
                        margin-bottom: 5px;
                        color: #ffffff;
                    }

                    #appointment-form input[type="text"],
                    #appointment-form input[type="date"],
                    #appointment-form input[type="tel"],
                    #appointment-form input[type="datetime-local"],
                    #appointment-form textarea {
                        width: 100%;
                        padding: 10px;
                        margin-bottom: 20px;
                        border-radius: 4px;
                        border: 1px solid #555555;
                        background-color: #3c3c3e
                        color: #ffffff;
                    }

                    #appointment-form button {
                        background-color: #0077cc;
                        color: white;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        font-size: 16px;
                        width: 100%;
                    }

                    #appointment-form button:hover {
                        background-color: #005fa3;
                    }
                </style>
            </head>
            <body>

            <form id="appointment-form">
                <h2>Request an Appointment</h2>
                
                <label for="full-name">Full Name:</label>
                <input type="text" id="full-name" name="full-name" required>
                
                <label for="dob">Date of Birth:</label>
                <input type="date" id="dob" name="dob" required>
                
                <label for="phone">Phone Number:</label>
                <input type="tel" id="phone" name="phone" required>
                
                <label for="date-time">Preferred Date and Time:</label>
                <input type="datetime-local" id="date-time" name="date-time" required>
                
                <label for="reason">Reason for Visit:</label>
                <textarea id="reason" name="reason" required></textarea>
                
                <button type="submit">Submit</button>
            </form>

            <script>
                document.getElementById("appointment-form").addEventListener("submit", function(event) {
                    event.preventDefault();
                    var formData = new FormData(this);
                    var appointmentData = {
                        appointment: true,
                        full_name: formData.get('full-name'),
                        dob: formData.get('dob'),
                        phone: formData.get('phone'),
                        preferred_datetime: formData.get('date-time'),
                        reason: formData.get('reason')
                    };

                    fetch('/chatbot_response', { // Ensure the URL matches your setup
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(appointmentData)
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message); // Notify the user with the server response
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert("There was a problem with your submission: " + error.message);
                    });
                });
            </script>

            </body>
            </html>

        '''
        return form_html

    # Check if the user's message matches any specific patterns
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
