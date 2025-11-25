const API_BASE_URL = "http://127.0.0.1:8000"; // FastAPI dev URL

const questionInput = document.getElementById("question");
const askButton = document.getElementById("ask-btn");
const responseBox = document.getElementById("response");
const answerText = document.getElementById("answer-text");
const infoText = document.getElementById("info-text");

askButton.addEventListener("click", async () => {
  const question = questionInput.value.trim();
  if (!question) {
    alert("Please enter a question.");
    return;
  }

  askButton.disabled = true;
  askButton.textContent = "Thinking...";

  try {
    const res = await fetch(`${API_BASE_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    if (!res.ok) {
      throw new Error(`Server returned ${res.status}`);
    }

    const data = await res.json();
    answerText.textContent = data.answer || "(no answer)";
    infoText.textContent = data.info || "";
    responseBox.classList.remove("hidden");
  } catch (err) {
    answerText.textContent = "Error fetching response.";
    infoText.textContent = String(err);
    responseBox.classList.remove("hidden");
  } finally {
    askButton.disabled = false;
    askButton.textContent = "Ask";
  }
});
