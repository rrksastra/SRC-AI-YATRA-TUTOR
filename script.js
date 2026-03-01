const API = "http://127.0.0.1:8000";
const chat = document.getElementById("chat");

function addMsg(text, cls){
    const div = document.createElement("div");
    div.className = "msg " + cls;
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

// 📄 Upload PDF
document.getElementById("pdf").addEventListener("change", async (e) => {
    const file = e.target.files[0];

    const form = new FormData();
    form.append("file", file);

    await fetch(API + "/upload", {
        method: "POST",
        body: form
    });

    alert("PDF uploaded!");
});

// 💬 Send
async function send(){
    const text = document.getElementById("text").value;
    const lang = document.getElementById("lang").value;

    addMsg(text, "user");

    const form = new FormData();
    form.append("question", text);
    form.append("lang", lang);

    const res = await fetch(API + "/ask", {
        method: "POST",
        body: form
    });

    const data = await res.json();

    let reply = data.answer + "\n(Source pages: " + data.source + ")";
    addMsg(reply, "bot");

    speak(data.answer, lang);
}

// 🎤 Voice Input
function voice(){
    const rec = new webkitSpeechRecognition();

    rec.lang = document.getElementById("lang").value === "tamil" ? "ta-IN" : "en-US";

    rec.onresult = (e) => {
        document.getElementById("text").value = e.results[0][0].transcript;
    };

    rec.start();
}

// 🔊 Voice Output
function speak(text, lang){
    const u = new SpeechSynthesisUtterance(text);

    u.lang = lang === "tamil" ? "ta-IN" : "en-US";

    speechSynthesis.speak(u);
}