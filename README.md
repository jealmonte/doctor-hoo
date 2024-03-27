# Dr. Hoo, the medical AI assistant

By: Joshua Almonte, Frank Hyun, Kareem Fenaish, Ayan Rasulova <br/> 
Our entry for the 2024 HooHacks competition

Problem statement:

The University of Virginia has a medical center, which also has a corresponding website: https://uvahealth.com/ <br/> 
At first glance, the website's appearance is simple, but with further analysis, it can be seen that some features are redundant or confusing. <br/> 
• "Appointments" allow you to make a REQUEST for appointment <br/> 
&emsp;- The list of reasons (or specialties) for making an appointment are somewhat specific, some options need referrals, but it's unclear on how to obtain one <br/> 
&emsp;- On top of the reasons, clarification or elaboration for the appointment is required <br/> 
&emsp;- Patient and contact information sections are repetitive <br/> 
• "Billing" can be assumed to be primarily used for payment of medical services or products received at medical centers <br/> 
&emsp;- Payment options include MyChart, by phone, or by mail, but it should also probably include in-person (at time of acquisition) <br/> 
&emsp;- Requesting a price estimate requires a lot of unnecessary effort, it should just have a database of services, products, and fees <br/> 
&emsp;- Price estimates are already available for common services on MyChart <br/> 
• "Find a Doctor" simply gives a directory of doctors, their location of operation, and phone number <br/> 
&emsp;- It is rather unusual to directly contact or consult doctors <br/> 
• "Services" gives a long list of various services <br/> 
&emsp;- Some are specific (e.g. "Endocrine, Thyroid, & Hormone Services") <br/> 
&emsp;- Others are broad or grouped inappropriately (e.g. "Men's Health" or "Lung Disease & Sleep Disorders") <br/> 
&emsp;- There are also two other main categories: "Support Services" and "Community and Business" which visually look unappealing and confusing <br/> 
• "Locations" gives multiple UVA medical center locations with corresponding addresses and phone numbers <br/> 
• "Patients & Visitors" provides a whole list that simply provides every service or information that has already been listed above

Our chatbot plans to remove all of these redundancies, and make the overall user experience more efficient and straightforward.

Since we don't have access to the source code or databases of the UVA health website, we used placeholders as substitute. <br/> 
The functionality is still there, but we don't have accurate information according to UVA webpages.

Here is how to setup Doctor Hoo:

Open the powershell terminal in vscode after cloning the repo, and type these to create the virtual environment for python and activate it:

cd backend
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
pip install openai
pip install django
pip install django-cors-headers

Then, make sure you have node.js installed: https://nodejs.org/

In a new terminal with the normal directory,
node -v (make sure node is installed)
npm install vite

To run frontend server, in the normal directory type:
npm run frontend

To run backend server, go to the views.py 
It is under: backend>myproject>chatbot>views.py, 
and then type in the quotation marks for YOUR_API_KEY the given API key

Then, activate the virtual environment in the terminal:
cd backend
venv\Scripts\Activate.ps1

And then direct to myproject:
cd myproject

And then run the server:
python manage.py runserver

Now, when you click on the localhost server given by the frontend command and talk to Doctor Hoo, it should respond. If it is not responding, and says there was an issue with your request, your backend server is not working due to an error in setting up the necessary packages. Send over the error to almontejoshua2@gmail.com, or try to run through the setup and make sure you've done everything correct.
