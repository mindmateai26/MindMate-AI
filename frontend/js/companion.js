// MindMate AI - Companion Chat Controller

document.addEventListener("DOMContentLoaded", () => {
  const chatMessages = document.getElementById("chat-messages");
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const sendBtn = document.getElementById("send-btn");
  const typingIndicator = document.getElementById("typing-indicator");
  const langSelect = document.getElementById("lang-select");
  const emotionPill = document.getElementById("detected-emotion-pill");
  const quickPromptsBar = document.getElementById("quick-prompts-bar");

  // API Key UI Elements
  const toggleKeyBtn = document.getElementById("toggle-key-btn");
  const apiKeyPanel = document.getElementById("api-key-panel");
  const apiKeyInput = document.getElementById("api-key-input");
  const saveKeyBtn = document.getElementById("save-key-btn");
  const clearKeyBtn = document.getElementById("clear-key-btn");
  const keyStatusLabel = document.getElementById("key-status-label");

  // In-memory conversation history for this active session
  let conversationHistory = [];

  // Load any existing assessment context
  const assessmentContext = Storage.getLatestAssessment();

  // Initialize API Key State
  function updateKeyUI() {
    const savedKey = localStorage.getItem("mindmate_gemini_api_key") || "";
    if (savedKey) {
      if (keyStatusLabel) keyStatusLabel.textContent = "Gemini Connected ✓";
      if (apiKeyInput) apiKeyInput.value = savedKey;
      if (toggleKeyBtn) toggleKeyBtn.style.borderColor = "var(--primary)";
    } else {
      if (keyStatusLabel) keyStatusLabel.textContent = "Gemini Key";
      if (apiKeyInput) apiKeyInput.value = "";
      if (toggleKeyBtn) toggleKeyBtn.style.borderColor = "var(--border)";
    }
  }

  updateKeyUI();

  if (toggleKeyBtn && apiKeyPanel) {
    toggleKeyBtn.addEventListener("click", () => {
      const isHidden = apiKeyPanel.style.display === "none" || !apiKeyPanel.style.display;
      apiKeyPanel.style.display = isHidden ? "block" : "none";
      if (isHidden && apiKeyInput) apiKeyInput.focus();
    });
  }

  if (saveKeyBtn) {
    saveKeyBtn.addEventListener("click", () => {
      const keyVal = (apiKeyInput.value || "").trim();
      if (keyVal) {
        localStorage.setItem("mindmate_gemini_api_key", keyVal);
        alert("Google Gemini API Key saved for this session!");
      } else {
        localStorage.removeItem("mindmate_gemini_api_key");
      }
      updateKeyUI();
      if (apiKeyPanel) apiKeyPanel.style.display = "none";
    });
  }

  if (clearKeyBtn) {
    clearKeyBtn.addEventListener("click", () => {
      localStorage.removeItem("mindmate_gemini_api_key");
      if (apiKeyInput) apiKeyInput.value = "";
      updateKeyUI();
      alert("API key cleared. Companion will use the dynamic local engine.");
    });
  }

  // Handle Quick Prompt Clicks
  quickPromptsBar.addEventListener("click", (e) => {
    const btn = e.target.closest(".prompt-pill");
    if (btn && btn.dataset.text) {
      chatInput.value = btn.dataset.text;
      sendMessage(btn.dataset.text);
    }
  });

  // Handle Form Submit
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text) return;
    sendMessage(text);
  });

  async function sendMessage(text) {
    // 1. Render User Message on Right
    appendMessage("user", text);
    chatInput.value = "";
    chatInput.focus();

    // 2. Add to history
    conversationHistory.push({ sender: "user", text: text });

    // 3. Show typing indicator
    showTyping(true);
    sendBtn.disabled = true;

    try {
      const savedApiKey = localStorage.getItem("mindmate_gemini_api_key") || "";
      const payload = {
        message: text,
        history: conversationHistory.slice(-10), // pass recent 10 turns
        language: langSelect.value,
        assessmentContext: assessmentContext ? {
          riskCategory: assessmentContext.riskCategory,
          score: assessmentContext.score
        } : null,
        apiKey: savedApiKey || null
      };

      const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorJson = await response.json().catch(() => ({}));
        throw new Error(errorJson.detail || `Server returned HTTP ${response.status}`);
      }

      const resData = await response.json();
      showTyping(false);
      sendBtn.disabled = false;

      // 4. Render AI Message on Left with source badge
      appendMessage("ai", resData.text, resData.moodTag, resData.language, resData.source);
      conversationHistory.push({ sender: "ai", text: resData.text });

      // 5. Update Emotion Pill
      if (resData.moodTag) {
        emotionPill.style.display = "inline-block";
        emotionPill.textContent = resData.moodTag;
      }

      // 6. Update Dynamic Quick Follow-ups
      if (resData.followUps && Array.isArray(resData.followUps) && resData.followUps.length > 0) {
        updateQuickPrompts(resData.followUps);
      }

      // 7. Crisis Alert check
      if (resData.isEmergency) {
        const modal = document.getElementById("crisis-modal");
        if (modal) modal.classList.add("show");
      }

    } catch (err) {
      console.warn("Chat request error:", err);
      showTyping(false);
      sendBtn.disabled = false;

      const fallbackReply = `I'm right here with you. Could you rephrase what you're feeling right now? (Notice: ${err.message || 'Connection check'})`;
      appendMessage("ai", fallbackReply, "Listening", "auto");
      conversationHistory.push({ sender: "ai", text: fallbackReply });
    }
  }

  function formatMarkdown(text) {
    if (!text) return "";
    let safe = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
    // Bold: **text**
    safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    // Italic: *text*
    safe = safe.replace(/\*(.*?)\*/g, "<em>$1</em>");
    // Clean linebreaks
    safe = safe.replace(/\n/g, "<br>");
    return safe;
  }

  function appendMessage(sender, text, moodTag = null, lang = null, source = null) {
    const row = document.createElement("div");
    row.className = `message-row ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.innerHTML = formatMarkdown(text);

    const meta = document.createElement("div");
    meta.className = "bubble-meta";

    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    if (sender === "user") {
      meta.innerHTML = `<span>You</span> &bull; <span>${timeStr}</span>`;
    } else {
      let extraTag = moodTag ? `<span class="mood-tag-badge">${moodTag}</span>` : "";
      let sourceTag = source === "gemini" ? `<span style="font-size:0.75rem; color:var(--primary); font-weight:700;">✨ Gemini AI</span>` : "";
      meta.innerHTML = `<span>MindMate</span> ${sourceTag} &bull; <span>${timeStr}</span> ${extraTag}`;
    }

    bubble.appendChild(meta);
    row.appendChild(bubble);
    chatMessages.appendChild(row);

    // Scroll smoothly to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function showTyping(isTyping) {
    typingIndicator.style.display = isTyping ? "flex" : "none";
    if (isTyping) {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }

  function updateQuickPrompts(prompts) {
    quickPromptsBar.innerHTML = "";
    prompts.forEach(p => {
      const btn = document.createElement("button");
      btn.className = "prompt-pill";
      btn.dataset.text = p;
      btn.textContent = p;
      quickPromptsBar.appendChild(btn);
    });
  }

  // Voice Input Speech-to-Text Setup
  const micBtn = document.getElementById("mic-btn");
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (micBtn) {
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;

      let isListening = false;

      micBtn.addEventListener("click", () => {
        if (!isListening) {
          try {
            // Adapt recognition language to selector if Tamil
            if (langSelect && langSelect.value === "ta") {
              recognition.lang = "ta-IN";
            } else {
              recognition.lang = "en-US";
            }
            recognition.start();
            isListening = true;
            micBtn.classList.add("listening");
            micBtn.setAttribute("title", "Listening... Click to stop");
          } catch (err) {
            console.warn("Recognition start error:", err);
            isListening = false;
            micBtn.classList.remove("listening");
          }
        } else {
          recognition.stop();
          isListening = false;
          micBtn.classList.remove("listening");
        }
      });

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (transcript) {
          chatInput.value = (chatInput.value ? chatInput.value + " " : "") + transcript;
          chatInput.focus();
        }
      };

      recognition.onerror = (event) => {
        console.warn("Voice recognition error:", event.error);
        isListening = false;
        micBtn.classList.remove("listening");
      };

      recognition.onend = () => {
        isListening = false;
        micBtn.classList.remove("listening");
        micBtn.setAttribute("title", "Voice Input (Click to Speak / Stop)");
      };

    } else {
      micBtn.addEventListener("click", () => {
        alert("Speech Recognition is not supported on this browser. Try Google Chrome or Microsoft Edge.");
      });
    }
  }
});
