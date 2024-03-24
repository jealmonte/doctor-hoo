# UVA-HooHacks-2024-Project

By: Joshua Almonte, Frank Hyun, Kareem Fenaish, Ayan Rasulova
Our entry for the 2024 HooHacks competition

Problem statement:

The University of Virginia has a medical center, which also has a corresponding website: https://uvahealth.com/
At first glance, the website's appearance is simple, but with further analysis, it can be seen that some features are redundant or confusing.
• "Appointments" allow you to make a REQUEST for appointment
    - The list of reasons (or specialties) for making an appointment are somewhat specific, some options need referrals, but it's unclear on how to obtain one
    - On top of the reasons, clarification or elaboration for the appointment is required
    - Patient and contact information sections are repetitive
• "Billing" can be assumed to be primarily used for payment of medical services or products received at medical centers
    - Payment options include MyChart, by phone, or by mail, but it should also probably include in-person (at time of acquisition)
    - Requesting a price estimate requires a lot of unnecessary effort, it should just have a database of services, products, and fees
    - Price estimates are already available for common services on MyChart
• "Find a Doctor" simply gives a directory of doctors, their location of operation, and phone number
    - It is rather unusual to directly contact or consult doctors
• "Services" gives a long list of various services 
    - Some are specific (e.g. "Endocrine, Thyroid, & Hormone Services")
    - Others are broad or grouped inappropriately (e.g. "Men's Health" or "Lung Disease & Sleep Disorders")
    - There are also two other main categories: "Support Services" and "Community and Business" which visually look unappealing and confusing
• "Locations" gives multiple UVA medical center locations with corresponding addresses and phone numbers
• "Patients & Visitors" provides a whole list that simply provides every service or information that has already been listed above

Our chatbot plans to remove all of these redundancies, and make the overall user experience more efficient and straightforward.

Since we don't have access to the source code or databases of the UVA health website, we used placeholders as substitute.
The functionality is still there, but we don't have accurate information according to UVA webpages.