const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const messagesContainer = document.getElementById("messages");

chatForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) return;

    const messageElement = document.createElement("div");
    messageElement.classList.add("message", "user");
    messageElement.textContent = message;

    messagesContainer.appendChild(messageElement);

    messageInput.value = "";
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
});