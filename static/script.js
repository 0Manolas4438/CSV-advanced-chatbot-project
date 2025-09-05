const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

function addMessage(text, className) {
    const msgDiv = document.createElement("div");
    msgDiv.className = className;
    chatBox.appendChild(msgDiv);

    let i = 0;
    function typeEffect() {
        if (i < text.length) {
            msgDiv.innerHTML += text.charAt(i);
            i++;
            setTimeout(typeEffect, 20); // type speed
        } else {
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }
    typeEffect();
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", function(e){
    if (e.key === "Enter") sendMessage();
});

function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, "user-msg");
    userInput.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => addMessage(data.response, "bot-msg"));
}
