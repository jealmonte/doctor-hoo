from openai import OpenAI
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random

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
    elif "estimate" in user_message.lower():
        # Prompt the user to select a healthcare location in HTML format
        return '''Please select a healthcare location:
                <ol>
                    <li>UVA Health Culpeper Medical Center</li>
                    <li>UVA Health Haymarket Medical Center</li>
                    <li>UVA Health Prince William Medical Center</li>
                    <li>UVA University Hospital</li>
                </ol>'''
    if any(location in user_message.lower() for location in ["uva health culpeper medical center", "uva health haymarket medical center", "uva health prince william medical center", "uva university hospital"]):
        # Prompt the user to enter their insurance company
        return "Please enter the name of your insurance company:"
    if any(insurance_company in user_message.lower() for insurance_company in ["aetna", "anthem", "cigna", "medicare", "united healthcare"]):
            return "What service are you looking for?"
    service_cost_ranges = {
        "allergy": (25, 40),
        "cancer": (200, 500),
        "dentistry": (100, 300),
        "diabetes": (40, 80),
        "digestive health": (300, 400),
        "eye care": (90, 300),
        "lung disease": (250, 400),
    }
    if any(service in user_message.lower() for service in ["allergy", "cancer", "dentistry", "diabetes", "digestive health", "eye care", "lung disease"]):
        # Store the service and generate a random estimate
        for service, cost_range in service_cost_ranges.items():
            if service in user_message.lower():
                min_cost, max_cost = cost_range
                estimate = random.randint(min_cost, max_cost)
                return f"Based on your selected location, insurance company, and service '{service}', the estimated cost is ${estimate}."
    
    elif "find" in user_message.lower() and "doctor" in user_message.lower():
        return '''To search for a doctor by name, condition, or treatment, use the <a href="https://uvahealth.com/findadoctor" target="_blank" style="color: #add8e6; text-decoration: underline;">'Find a Doctor'</a> tool!'''
    
    elif any(service_keyword in user_message.lower() for service_keyword in ["service", "services"]):
        services_with_links = {
            "Allergy": "https://uvahealth.com/services/allergy",
            "Autoimmune Disease Treatment": "https://uvahealth.com/services/autoimmune-rheumatology",
            "Cancer Center": "https://uvahealth.com/services/cancer",
            "Dentistry": "https://uvahealth.com/services/dentistry",
            "Dermatology": "https://uvahealth.com/services/dermatology",
            "Diabetes Care": "https://uvahealth.com/services/diabetes-care",
            "Digestive Health": "https://uvahealth.com/services/gastro",
            "Ear Nose & Throat": "https://uvahealth.com/services/ear-nose-throat",
            "Endocrine Thyroid & Hormone Services": "https://uvahealth.com/services/endocrine",
            "Eye Care": "https://uvahealth.com/services/eye-care",
            "Heart & Vascular Center": "https://uvahealth.com/services/heart",
            "Hyperbaric Oxygen Therapy": "https://uvahealth.com/services/hyperbaric-oxygen-therapy",
            "Imaging & Radiology": "https://uvahealth.com/services/imaging",
            "Infectious Disease": "https://uvahealth.com/services/infectious-disease",
            "Kidney Care": "https://uvahealth.com/services/kidney-care",
            "Liver Disease Treatment": "https://uvahealth.com/services/liver-disease-treatment",
            "Lung Disease & Sleep Disorders": "https://uvahealth.com/services/pulmonary",
            "Men's Health": "https://uvahealth.com/services/mens-health",
            "Neurosciences & Mental Health": "https://uvahealth.com/services/neuro",
            "Orthopedics & Sports Medicine": "https://uvahealth.com/services/orthopedics",
            "Pediatric Care": "https://uvahealth.com/services/pediatric-care",
            "Pregnancy & Birth": "https://uvahealth.com/services/pregnancy-birth",
            "Primary Care": "https://uvahealth.com/services/primary-care",
            "Spine Services": "https://uvahealth.com/services/spine",
            "Surgery & Procedures": "https://uvahealth.com/services/surgery",
            "Transplant": "https://uvahealth.com/services/transplant",
            "Urology": "https://uvahealth.com/services/urology",
            "Weight-Loss Surgery": "https://uvahealth.com/services/weight-loss-surgery",
            "Women's Health & Gynecology": "https://uvahealth.com/services/womens-health",
        }

        # Generating an unordered list in HTML format with links
        services_list_html = "<ul>" + "".join(
            f"<li><a href='{url}' target='_blank' style='color: #ADD8E6;'>{service}</a></li>" 
            for service, url in services_with_links.items()
        ) + "</ul>"


        response = f"UVA Health provides a variety of medical services. Here is the list: {services_list_html} More info can be found by selecting a service!"
        return response
    
    if "bill" in user_message.lower() or "pay" in user_message.lower():
        return '''<style>
    p {
        color: #fff;
    }
    a {
        color: #add8e6; /* Light blue for a softer appearance */
        text-decoration: underline; /* Optional: ensures links are clearly indicated */
    }
    </style><p>To pay a medical bill, use UVA's <a href="https://mychart.healthsystem.virginia.edu/mychart/">MyChart</a> to pay online, or call to pay by phone: <a href="tel:844-377-0846">844.377.0846</a>!</p>'''    

    if "locations" in user_message.lower():
        return '''<style>
                a {
                    color: #add8e6; /* Light blue for a softer appearance */
                    text-decoration: underline; /* Keeps links underlined for clarity */
                }
                </style>
                <p>We have multiple locations across the state:</p>
                <ol>
                    <li><a href="https://example.com/education-resource-center" target="_blank">Education Resource Center</a></li>
                    <li><a href="https://example.com/emily-couric-clinical-cancer-center" target="_blank">Emily Couric Clinical Cancer Center</a></li>
                    <li><a href="https://example.com/orthopedic-center" target="_blank">Orthopedic Center</a></li>
                    <li><a href="https://example.com/primary-care-center" target="_blank">Primary Care Center</a></li>
                    <li><a href="https://example.com/university-hospital" target="_blank">University Hospital</a></li>
                </ol>
                <p>Try asking about where they're located, operating hours, or more specifics.</p>'''
    elif "patient" in user_message.lower() or "visitor" in user_message.lower():
        return "For general information regarding patient and visitors, " + '<a href="https://uvahealth.com/patients-visitors" target="_blank">click here!</a>'
    elif "other" in user_message.lower():
        return "What can I help you with? I can help you with hours, locations, doctors, and more!"
    elif "education resource center" in user_message.lower() and ("hours" in user_message.lower() or "open" in user_message.lower() or "where" in user_message.lower() or "address" in user_message.lower() or "located" in user_message.lower()):
        return """The Education Resource Center at 1240 Lee Street is open from 6:00AM to 7:30PM from Monday to Friday, 
    and open from 7:00AM to 4:00PM on Saturdays and Sundays."""
    elif "emily couric" in user_message.lower() and ("hours" in user_message.lower() or "open" in user_message.lower() or "where" in user_message.lower() or "address" in user_message.lower() or "located" in user_message.lower()):
        return """The Emily Couric Clinical Cancer Center at 1240 Lee Street is open from 6:00AM to 7:30PM from Monday to Friday, 
    and open from 7:30AM to 4:00PM on Saturdays and Sundays."""
    elif "orthopedic" and ("hours" in user_message.lower() or "open" in user_message.lower() or "where" in user_message.lower() or "address" in user_message.lower() or "located" in user_message.lower()):
        return """The Orthopedic Center at 2280 Ivy Road is open from 8:00AM to 5:00PM from Monday to Friday, 
    and closed on Saturdays and Sundays."""
    elif "primary care" and ("hours" in user_message.lower() or "open" in user_message.lower() or "where" in user_message.lower() or "address" in user_message.lower() or "located" in user_message.lower()):
        return """The Primary Care Center at 1221 Lee Street is open from 5:00AM to 9:00PM from Monday to Friday, 
    and closed on Saturdays and Sundays."""
    elif "university hospital" and ("hours" in user_message.lower() or "open" in user_message.lower() or "where" in user_message.lower() or "address" in user_message.lower() or "located" in user_message.lower()):
        return """The University Hospital at 1215 Lee Street is open 24/7 for every day of the week, but
    main lobby entrances are open from 5:00AM to 9:00PM whereas emergency services
    are open from 9:00PM to 5:00AM."""
    else:
        return assistant_response
