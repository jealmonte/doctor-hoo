// app.js
async function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    // Display user message in the chat
    document.getElementById('chat-messages').innerHTML += '<div class="user-message">You: ' + userInput + '</div>';
    // Get bot response asynchronously
    getBotResponse(userInput).then(botResponse => {
        // Display bot response in the chat
        document.getElementById('chat-messages').innerHTML += '<div class="bot-message">Dr. Hoo: ' + botResponse + '</div>';
        // Scroll to the bottom of the chat container
        var chatContainer = document.querySelector('.chat-body');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    });
    // Clear the user input field
    document.getElementById('user-input').value = '';
}
async function getBotResponse(userInput) {
    try {
        let response = await fetch('http://localhost:8000/api/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userInput }),
        });
        if (response.ok) {
            let jsonResponse = await response.json();
            return jsonResponse.message; // Assuming the Django response contains {message: "response text"}
        } else {
            console.error('Server error:', response);
            return 'Sorry, there was a problem processing your request.';
        }
    } catch (error) {
        console.error('Error:', error);
        return 'Sorry, there was an error connecting to the chatbot.';
    }
}
// Function to start the conversation
function startConversation() {
    const chatBody = document.getElementById('chat-messages');
    const initialMessage = document.createElement('div');
    chatBody.appendChild(initialMessage);
    chatBody.scrollTop = chatBody.scrollHeight;
}
// Function to handle the enter key press event
function handleEnterKey(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
}
// Function to animate the owl image and intro text
function animateOwlImage() {
    const owlImage = document.getElementById('owl-image');
    const introText = document.getElementById('intro-text');
    // Show the image and fade it in
    owlImage.style.display = 'block';
    setTimeout(() => {
        owlImage.classList.add('fade-in');
    }, 100); // Add a slight delay for the fade-in effect

    // Slide the image to the left after it fades in
    setTimeout(() => {
        owlImage.classList.add('slide-left');
        // Fade in the intro text after the image slides to the left
        introText.style.display = 'block';
        setTimeout(() => {
            introText.classList.add('fade-in');
        }, 500);
    }, 1100); // Adjust the delay based on the fade-in duration

}
// Start the conversation and animate the owl image when the page loads
window.onload = function () {
    startConversation();
    animateOwlImage();
    // Attach event listener to send button
    document.getElementById('send-btn').addEventListener('click', sendMessage);

    // Attach event listener for enter key press on the user input field
    document.getElementById('user-input').addEventListener('keypress', handleEnterKey);
}
