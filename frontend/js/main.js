document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("birthForm");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById("name").value,
            birthDate: document.getElementById("birthDate").value,
            birthTime: document.getElementById("birthTime").value,
            birthPlace: document.getElementById("birthPlace").value
        };

        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        console.log("Server response:", result);

        document.getElementById("chatBox").innerHTML += `
            <div class="bot-message">${result.message}</div>
        `;
    });
});
