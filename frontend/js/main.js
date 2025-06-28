// Function to add a message to the chat box
function addMessage(message, sender, type = 'text') {
    const chatBox = document.getElementById("chatBox");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(`${sender}-message`);

    if (type === 'html') {
        messageDiv.innerHTML = message;
    } else {
        messageDiv.textContent = message;
    }
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}

// Show/Hide Loading Overlay
function toggleLoading(show) {
    const loadingOverlay = document.getElementById("loadingOverlay");
    if (show) {
        loadingOverlay.classList.remove("hidden");
    } else {
        loadingOverlay.classList.add("hidden");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const birthForm = document.getElementById("birthForm");
    const formSection = document.getElementById("form-section");
    const chatSection = document.getElementById("chat-section");
    const chatBox = document.getElementById("chatBox");
    const userInput = document.getElementById("userInput");
    const sendChatButton = document.getElementById("sendChat");
    const downloadPdfButton = document.getElementById("downloadPdf");

    // --- Form Submission Handler (Initial Prediction) ---
    birthForm.addEventListener("submit", async (e) => {
        e.preventDefault(); // Prevent default form submission

        toggleLoading(true); // Show loading spinner

        const formData = {
            name: document.getElementById("name").value,
            gender: document.getElementById("gender").value,
            birthDate: document.getElementById("birthDate").value,
            birthTime: document.getElementById("birthTime").value,
            birthPlace: document.getElementById("birthPlace").value
        };

        try {
            const response = await fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log("Server response:", result);

            // Clear previous messages except initial bot message
            chatBox.innerHTML = `
                <div class="bot-message initial-message">
                    Hello! Provide your birth details to receive your personalized astrological predictions.
                </div>
            `;
            addMessage(result.message, "bot"); // Display initial prediction

            // Transition from form to chat interface
            formSection.classList.add("hidden");
            chatSection.classList.remove("hidden");
            chatSection.scrollIntoView({ behavior: 'smooth' }); // Scroll to chat section
            
            // Re-enable chat input
            userInput.disabled = false;
            sendChatButton.disabled = false;

        } catch (error) {
            console.error("Error fetching prediction:", error);
            addMessage(`Oops! Something went wrong: ${error.message}. Please try again.`, "bot");
        } finally {
            toggleLoading(false); // Hide loading spinner
        }
    });

    // --- Chat Input Handler (Follow-up Questions) ---
    const sendChatMessage = async () => {
        const userQuestion = userInput.value.trim();
        if (userQuestion === "") return; // Don't send empty messages

        addMessage(userQuestion, "user"); // Display user's question immediately
        userInput.value = ""; // Clear input field
        userInput.disabled = true; // Disable input during bot response
        sendChatButton.disabled = true;

        toggleLoading(true); // Show loading spinner for chat response

        try {
            const response = await fetch("http://127.0.0.1:5000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userQuestion })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            addMessage(result.reply, "bot"); // Display bot's reply

        } catch (error) {
            console.error("Error sending chat message:", error);
            addMessage(`I'm having trouble understanding right now: ${error.message}.`, "bot");
        } finally {
            toggleLoading(false); // Hide loading spinner
            userInput.disabled = false; // Re-enable input
            sendChatButton.disabled = false;
            userInput.focus(); // Focus back on input
        }
    };

    sendChatButton.addEventListener("click", sendChatMessage);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendChatMessage();
        }
    });

    // --- PDF Download Handler ---
    downloadPdfButton.addEventListener("click", async () => {
        toggleLoading(true); // Show loading spinner while generating PDF

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        // Get the content of the chat box
        const chatContent = document.getElementById('chatBox');

        // Prepare content for PDF
        let pdfContent = "JyotishAI Astrological Report\n\n";
        
        // Add form data to PDF
        pdfContent += `Name: ${document.getElementById("name").value}\n`;
        pdfContent += `Gender: ${document.getElementById("gender").value}\n`;
        pdfContent += `Date of Birth: ${document.getElementById("birthDate").value}\n`;
        pdfContent += `Time of Birth: ${document.getElementById("birthTime").value}\n`;
        pdfContent += `Place of Birth: ${document.getElementById("birthPlace").value}\n\n`;
        
        // Add chat messages to PDF
        chatContent.querySelectorAll('.bot-message, .user-message').forEach(msgDiv => {
            const sender = msgDiv.classList.contains('bot-message') ? 'AstroAI' : 'You';
            const text = msgDiv.textContent.trim();
            if (text && !msgDiv.classList.contains('initial-message')) { // Exclude initial welcome message
                pdfContent += `${sender}: ${text}\n\n`;
            }
        });

        // Add to PDF and save
        doc.setFontSize(12);
        doc.text(pdfContent, 10, 10, { maxWidth: 180 }); // Adjust maxWidth as needed

        doc.save("JyotishAI_Astrology_Report.pdf");
        
        toggleLoading(false); // Hide loading spinner
        alert("Your astrological report is being downloaded!");
    });

    // Initially disable chat input until form is submitted
    userInput.disabled = true;
    sendChatButton.disabled = true;
});