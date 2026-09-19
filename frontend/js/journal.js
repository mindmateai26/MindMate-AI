// MindMate AI - AI Journaling & Emotion Analysis Controller

document.addEventListener("DOMContentLoaded", () => {
  const journalForm = document.getElementById("journal-form");
  const journalInput = document.getElementById("journal-input");
  const clearBtn = document.getElementById("clear-journal-btn");
  const clearAllBtn = document.getElementById("clear-all-journals-btn");
  const entriesContainer = document.getElementById("journal-entries-container");
  const micBtn = document.getElementById("journal-mic-btn");
  const micStatus = document.getElementById("journal-mic-status");
  const promptButtons = document.querySelectorAll(".journal-prompt");

  const previewBox = document.getElementById("journal-analysis-preview");
  const previewBadge = document.getElementById("preview-emotion-badge");
  const previewText = document.getElementById("preview-analysis-text");
  const previewLang = document.getElementById("preview-analysis-lang");

  // Load Saved Journal Entries
  function getJournalEntries() {
    try {
      const data = localStorage.getItem("mindmate_journals");
      if (data) return JSON.parse(data);
    } catch (e) {
      console.warn("Could not read journals from localStorage:", e);
    }
    // Default demo entries if empty
    return [
      {
        id: "j_demo1",
        date: "Yesterday, 09:15 PM",
        text: "Had two tests back-to-back today. Felt very tired by afternoon, but took a short walk around the campus hostel and felt slightly refreshed.",
        emotion: "Academic pressure",
        moodTag: "Fatigued & Reflective",
        language: "English",
        reflection: "Recognizing physical fatigue and stepping outdoors for a walk demonstrates proactive somatic regulation."
      },
      {
        id: "j_demo2",
        date: "3 days ago, 07:30 PM",
        text: "inniku romba tension ah irunthuchu project deadline kaaga. Ana friend kooda pesinadhukku appram mind konjam relax aachu.",
        emotion: "Stress",
        moodTag: "Relieved / Calming",
        language: "Thanglish",
        reflection: "Reaching out to close peers when under pressure is one of the most effective ways to lower cortisol levels."
      }
    ];
  }

  function saveJournalEntries(entries) {
    try {
      localStorage.setItem("mindmate_journals", JSON.stringify(entries));
    } catch (e) {
      console.warn("Could not save journals:", e);
    }
  }

  let entries = getJournalEntries();

  function renderEntries() {
    if (!entriesContainer) return;
    if (entries.length === 0) {
      entriesContainer.innerHTML = `
        <div style="text-align: center; color: var(--text-muted); padding: 24px;">
          No journal entries yet. Take a moment to write down what you are feeling above!
        </div>
      `;
      return;
    }

    entriesContainer.innerHTML = entries.map(entry => {
      let badgeStyle = "background: #e0f2fe; color: #0284c7;";
      if (entry.emotion === "Stress" || entry.emotion === "Academic pressure") {
        badgeStyle = "background: #fef3c7; color: #d97706;";
      } else if (entry.emotion === "Anxiety" || entry.emotion === "Anger") {
        badgeStyle = "background: #fee2e2; color: #dc2626;";
      } else if (entry.emotion === "Positive/Calm") {
        badgeStyle = "background: #dcfce7; color: #16a34a;";
      }

      return `
        <div class="journal-entry-card">
          <div class="journal-meta">
            <span>📅 ${entry.date} &bull; <small style="color: var(--text-muted);">${entry.language || 'English'}</small></span>
            <span class="journal-tag" style="${badgeStyle}">${entry.emotion || 'Reflective'} (${entry.moodTag || 'Tone'})</span>
          </div>
          <p style="font-size: 0.92rem; color: var(--text-main); line-height: 1.6; margin-bottom: 10px; white-space: pre-wrap;">${entry.text}</p>
          <div style="padding: 10px 14px; border-radius: var(--radius-sm); background: var(--bg-main); border-left: 3px solid var(--primary); font-size: 0.84rem; color: var(--text-muted);">
            💡 <strong>AI Reflection:</strong> ${entry.reflection || 'Gentle self-awareness recorded.'}
          </div>
        </div>
      `;
    }).join("");
  }

  renderEntries();

  // Handle Form Submission with Emotion API or Local Rule Engine
  if (journalForm) {
    journalForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const text = (journalInput.value || "").trim();
      if (!text) return;

      const submitBtn = document.getElementById("save-journal-btn");
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Analyzing...";
      }

      let detectedEmotion = "Reflective";
      let moodTag = "Calm";
      let language = "English";
      let aiReflection = "Validating and recording your honest internal dialogue helps release subconscious cognitive tension.";

      // Try Backend Emotion Analysis Endpoint
      try {
        const res = await fetch(`${API_BASE}/emotion`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: text, language: "auto" })
        });
        if (res.ok) {
          const data = await res.json();
          detectedEmotion = data.emotion || detectedEmotion;
          moodTag = data.moodTag || moodTag;
          language = data.language === "ta" ? "Tamil" : (data.language === "thanglish" ? "Thanglish" : "English");
        }
      } catch (err) {
        console.warn("Emotion endpoint unavailable, using intelligent local evaluator:", err);
        // Fallback local heuristic
        const lower = text.toLowerCase();
        if (lower.includes("exam") || lower.includes("test") || lower.includes("study") || lower.includes("assignment")) {
          detectedEmotion = "Academic pressure";
          moodTag = "Concerned";
          aiReflection = "Academic milestones are temporary, but your mental well-being is lifelong. Break tomorrow into micro-tasks.";
        } else if (lower.includes("stress") || lower.includes("tension") || lower.includes("bhaaram") || lower.includes("load")) {
          detectedEmotion = "Stress";
          moodTag = "Overwhelmed";
          aiReflection = "High stress narrows mental clarity. Try engaging in 5 minutes of gentle box breathing or stretching.";
        } else if (lower.includes("happy") || lower.includes("calm") || lower.includes("peace") || lower.includes("nalla")) {
          detectedEmotion = "Positive/Calm";
          moodTag = "Content";
          aiReflection = "Cultivating positive awareness builds emotional reserves for challenging days ahead.";
        }
      }

      // Show Analysis preview
      if (previewBox) {
        previewBox.style.display = "block";
        if (previewBadge) previewBadge.textContent = `${detectedEmotion} (${moodTag})`;
        if (previewText) previewText.textContent = `AI Observation: ${aiReflection}`;
        if (previewLang) previewLang.textContent = `Language detected: ${language}`;
      }

      // Add to entries list
      const newEntry = {
        id: "j_" + Date.now(),
        date: new Date().toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }),
        text: text,
        emotion: detectedEmotion,
        moodTag: moodTag,
        language: language,
        reflection: aiReflection
      };

      entries.unshift(newEntry);
      saveJournalEntries(entries);
      renderEntries();

      journalInput.value = "";
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = "Analyze & Save Entry ➔";
      }
    });
  }

  // Clear Input Button
  if (clearBtn && journalInput) {
    clearBtn.addEventListener("click", () => {
      journalInput.value = "";
      journalInput.focus();
    });
  }

  // Clear All Entries Button
  if (clearAllBtn) {
    clearAllBtn.addEventListener("click", () => {
      if (confirm("Are you sure you want to clear all your journal entries?")) {
        entries = [];
        saveJournalEntries(entries);
        renderEntries();
      }
    });
  }

  // Prompt Pill Click
  promptButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const text = btn.getAttribute("data-text");
      if (text && journalInput) {
        journalInput.value = text;
        journalInput.focus();
      }
    });
  });

  // Voice Input Speech-to-Text for Journaling
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (micBtn) {
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      let isRecording = false;

      micBtn.addEventListener("click", () => {
        if (!isRecording) {
          try {
            recognition.lang = "en-US";
            recognition.start();
            isRecording = true;
            micBtn.classList.add("listening");
            if (micStatus) micStatus.textContent = "Listening... Speak your mind";
          } catch (err) {
            console.warn("Recognition start error:", err);
            isRecording = false;
            micBtn.classList.remove("listening");
          }
        } else {
          recognition.stop();
          isRecording = false;
          micBtn.classList.remove("listening");
          if (micStatus) micStatus.textContent = "Voice input stopped";
        }
      });

      recognition.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        if (transcript && journalInput) {
          journalInput.value = (journalInput.value ? journalInput.value + " " : "") + transcript;
          journalInput.focus();
        }
      };

      recognition.onerror = (e) => {
        console.warn("Journal mic error:", e.error);
        isRecording = false;
        micBtn.classList.remove("listening");
        if (micStatus) micStatus.textContent = "Could not capture voice";
      };

      recognition.onend = () => {
        isRecording = false;
        micBtn.classList.remove("listening");
        if (micStatus) micStatus.textContent = "Voice dictation ready";
      };
    } else {
      micBtn.addEventListener("click", () => {
        alert("Speech Recognition is not supported on this browser. Try Google Chrome or Microsoft Edge.");
      });
    }
  }
});
