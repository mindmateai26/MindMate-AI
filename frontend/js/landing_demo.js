// MindMate AI - Landing Page Interactive Mock Demo Controller
document.addEventListener("DOMContentLoaded", () => {
  const chatMessages = document.getElementById("demo-chat-messages");
  const chatForm = document.getElementById("demo-chat-form");
  const chatInput = document.getElementById("demo-chat-input");
  const moodPill = document.getElementById("demo-mood-pill");
  const promptButtons = document.querySelectorAll(".demo-prompt");

  // Mood Overview elements
  const moodButtons = document.querySelectorAll(".mood-btn");
  const moodFeedbackNote = document.getElementById("mood-feedback-note");
  const riskBadge = document.getElementById("demo-risk-badge");
  const scoreText = document.getElementById("demo-score-text");
  const riskSummary = document.getElementById("demo-risk-summary");

  // Mock responses for interactive showcase
  const mockResponses = {
    "exam": {
      text: "I completely understand. Exam pressure can feel so heavy on your shoulders. First, take a slow breath in... and out. Try chunking your revision into 25-minute sprints with a 5-minute breather. Would you like a quick grounding exercise or advice on organizing your study topics?",
      mood: "Exam Strain"
    },
    "thanglish": {
      text: "Ayyoo tension aagathinga bro! Exam/work pressure iruntha manasula romba load aagum, athu romba normal thaan. Mudhala oru glass thanni kudichitu konjam deep breath edunga. Enna aachu nu share panreengala, naan kekkuran!",
      mood: "Stress (தங்கிலிஷ்)"
    },
    "breath": {
      text: "Let's do this together right now:\n\n1. Inhale gently through your nose (4 seconds)...\n2. Hold your breath gently (4 seconds)...\n3. Release slowly through your mouth (4 seconds)...\n\nNotice the tension melting away from your shoulders. Repeat this 3 times.",
      mood: "Grounding"
    },
    "energy": {
      text: "Honoring your low energy is actually a sign of emotional wisdom. It is okay not to be productive every minute. Drink a tall glass of water, stretch gently, or rest for 15 minutes without looking at screens.",
      mood: "Low Energy"
    },
    "default": {
      text: "Thank you for sharing that with me. Your feelings are valid and acknowledged. Remember to pace yourself today, stay hydrated, and take small pauses whenever you need to recharge.",
      mood: "Supportive"
    }
  };

  function appendDemoMessage(sender, text) {
    if (!chatMessages) return;
    const row = document.createElement("div");
    row.className = `message-row ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.textContent = text;

    const meta = document.createElement("div");
    meta.className = "bubble-meta";
    meta.innerHTML = `<span>${sender === "user" ? "You" : "MindMate AI"}</span> &bull; <span>Just now</span>`;

    bubble.appendChild(meta);
    row.appendChild(bubble);
    chatMessages.appendChild(row);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function handleDemoUserMessage(userText) {
    appendDemoMessage("user", userText);

    // Simulate AI thinking and responsive reply
    setTimeout(() => {
      const lower = userText.toLowerCase();
      let match = mockResponses.default;

      if (lower.includes("exam") || lower.includes("anxious") || lower.includes("study")) {
        match = mockResponses.exam;
      } else if (lower.includes("stress") || lower.includes("bro") || lower.includes("enaku")) {
        match = mockResponses.thanglish;
      } else if (lower.includes("breath") || lower.includes("exercise") || lower.includes("grounding")) {
        match = mockResponses.breath;
      } else if (lower.includes("tired") || lower.includes("unmotivated") || lower.includes("energy")) {
        match = mockResponses.energy;
      }

      appendDemoMessage("ai", match.text);
      if (moodPill) {
        moodPill.textContent = match.mood;
      }
    }, 550);
  }

  // Handle Form Submission
  if (chatForm && chatInput) {
    chatForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const val = chatInput.value.trim();
      if (!val) return;
      chatInput.value = "";
      handleDemoUserMessage(val);
    });
  }

  // Handle Quick Prompts
  promptButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const msg = btn.getAttribute("data-msg");
      if (msg) {
        handleDemoUserMessage(msg);
      }
    });
  });

  // Handle Mood Selection Interactions
  moodButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      moodButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const mood = btn.getAttribute("data-mood");
      const score = btn.getAttribute("data-score");
      const tier = btn.getAttribute("data-tier");
      const feedback = btn.getAttribute("data-feedback");

      if (scoreText) scoreText.textContent = score;
      if (moodFeedbackNote) {
        moodFeedbackNote.innerHTML = `<strong>Selected (${mood}):</strong> ${feedback}`;
      }

      if (riskBadge) {
        riskBadge.textContent = `${tier} Risk`;
        riskBadge.className = `risk-badge risk-${tier.toLowerCase()}`;
      }

      if (riskSummary) {
        if (tier === "Low") {
          riskSummary.textContent = "Minimal distress reported. Emotional indicators reflect positive coping and consistent vitality.";
        } else if (tier === "Mild") {
          riskSummary.textContent = "Manageable stress observed. Balanced pacing, routine sleep, and micro-breaks are sufficient.";
        } else if (tier === "Moderate") {
          riskSummary.textContent = "Elevated emotional strain detected. Consider discussing workload with friends or a counselor.";
        } else {
          riskSummary.textContent = "High acute fatigue and burden reported. Prioritize rest and explore available student counseling support.";
        }
      }
    });
  });
});
