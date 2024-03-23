// app.js
async function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    // Display user message in the chat
    document.getElementById('chat-messages').innerHTML += '<div class="user-message">You: ' + userInput + '</div>';
    // Get bot response asynchronously
    getBotResponse(userInput).then(botResponse => {
        // Display bot response in the chat
        document.getElementById('chat-messages').innerHTML += '<div class="bot-message">Doctor Hoo: ' + botResponse + '</div>';
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
    initialMessage.classList.add('bot-message');
    initialMessage.innerHTML = 'Hello! I am Doctor Hoo, your virtual medical assistant. How can I help you ? <br> 1) Request an appointment<br> 2) See a price estimate<br> 3) Pay a medical bill<br> 4) Other';
    chatBody.appendChild(initialMessage);
    chatBody.scrollTop = chatBody.scrollHeight;
}
// Start the conversation when the page loads
window.onload = startConversation;
// Attach event listener to send button
document.getElementById('send-btn').addEventListener('click', sendMessage);