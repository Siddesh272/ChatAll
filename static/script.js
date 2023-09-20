const micButton = document.getElementById("micButton");
const userInput = document.getElementById("userInput");
const botResponse = document.getElementById("botResponse");
const chatHistory = document.getElementById("chatHistory");

micButton.addEventListener("click", startRecording);

function startRecording() {
    if ("webkitSpeechRecognition" in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = "en-US";

        recognition.onstart = () => {
            micButton.classList.add("active");
        };

        recognition.onend = () => {
            micButton.classList.remove("active");
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
        };

        recognition.start();
    } else {
        console.log("Speech recognition not available.");
    }
}

function updateChatHistory(userMessage, botMessage) {
    const userDiv = document.createElement("div");
    userDiv.classList.add("user-message");
    userDiv.innerHTML = "<span class='message-label'>You:</span> " + userMessage;

    const botDiv = document.createElement("div");
    botDiv.classList.add("bot-message");
    botDiv.innerHTML = "<span class='message-label'>Bot:</span> " + botMessage;

    chatHistory.appendChild(userDiv);
    chatHistory.appendChild(botDiv);

    // Scroll to the bottom to show the latest messages
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function getTextResponse() {
    const userQuestion = userInput.value;

    fetch("/get_response", {
        method: "POST",
        body: new URLSearchParams({
            user_input: userQuestion,
        }),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
    })
    .then(response => response.json())
    .then(data => {
        updateChatHistory(userQuestion, data.response);
        speak(data.response); // Speak the bot's response
    });

    userInput.value = ""; // Clear the input field after sending the message
}

// Function to speak text
function speak(text) {
    const msg = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(msg);
}
