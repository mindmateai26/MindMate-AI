// MindMate AI - Screening Assessment Logic

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("screening-form");
  const blocks = document.querySelectorAll(".question-block");
  const prevBtn = document.getElementById("prev-btn");
  const nextBtn = document.getElementById("next-btn");
  const submitBtn = document.getElementById("submit-btn");
  const progressFill = document.getElementById("progress-bar-fill");
  const stepCounter = document.getElementById("step-counter");
  const progressPercent = document.getElementById("progress-percent");

  const totalQuestions = blocks.length;
  let currentStep = 1;

  // Add click handler to option cards for better mobile ergonomics
  document.querySelectorAll(".option-card").forEach(card => {
    card.addEventListener("click", () => {
      const radio = card.querySelector("input[type='radio']");
      if (radio) {
        radio.checked = true;
        // Update active class within parent group
        const group = card.closest(".options-group");
        group.querySelectorAll(".option-card").forEach(c => c.classList.remove("selected"));
        card.classList.add("selected");
      }
    });
  });

  function updateStepUI() {
    blocks.forEach((block, idx) => {
      if (idx + 1 === currentStep) {
        block.classList.add("active");
      } else {
        block.classList.remove("active");
      }
    });

    const percent = Math.round((currentStep / totalQuestions) * 100);
    progressFill.style.width = `${percent}%`;
    stepCounter.textContent = `Question ${currentStep} of ${totalQuestions}`;
    progressPercent.textContent = `${percent}% completed`;

    // Button visibility
    prevBtn.style.visibility = currentStep === 1 ? "hidden" : "visible";

    if (currentStep === totalQuestions) {
      nextBtn.style.display = "none";
      submitBtn.style.display = "inline-flex";
    } else {
      nextBtn.style.display = "inline-flex";
      submitBtn.style.display = "none";
    }
  }

  function validateCurrentStep() {
    const activeBlock = document.querySelector(`.question-block[data-index="${currentStep}"]`);
    const checked = activeBlock.querySelector("input[type='radio']:checked");
    if (!checked) {
      alert("Please select an option to continue.");
      return false;
    }
    return true;
  }

  nextBtn.addEventListener("click", () => {
    if (validateCurrentStep()) {
      if (currentStep < totalQuestions) {
        currentStep++;
        updateStepUI();
        window.scrollTo({ top: 120, behavior: "smooth" });
      }
    }
  });

  prevBtn.addEventListener("click", () => {
    if (currentStep > 1) {
      currentStep--;
      updateStepUI();
      window.scrollTo({ top: 120, behavior: "smooth" });
    }
  });

  // Handle Form Submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!validateCurrentStep()) return;

    submitBtn.disabled = true;
    submitBtn.textContent = "Analyzing Responses...";

    const formData = new FormData(form);
    const payload = {};
    for (const [key, value] of formData.entries()) {
      payload[key] = parseInt(value, 10);
    }

    try {
      const response = await fetch(`${API_BASE}/assessment/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }

      const resJson = await response.json();
      if (resJson.success && resJson.data) {
        // Save to Storage
        Storage.saveLatestAssessment(resJson.data);
        // Navigate to result page
        window.location.href = "result.html";
      } else {
        throw new Error(resJson.detail || "Prediction response malformed.");
      }
    } catch (err) {
      console.warn("API submission error, using local fallback prediction:", err);
      // Local calculation fallback if backend unavailable
      const sum = Object.values(payload).reduce((a, b) => a + b, 0);
      const score = Math.round(((sum - 9) / 36) * 100);
      let cat = "Low";
      if (score > 75) cat = "High";
      else if (score > 50) cat = "Moderate";
      else if (score > 25) cat = "Mild";

      const fallbackResult = {
        score: score,
        rawScore: sum,
        riskCategory: cat,
        probabilities: {},
        contributingFactors: [
          { label: "Daily Functioning", rating: payload.daily_functioning_impact || 2, status: "Moderate Impact" },
          { label: "Mood & Emotions", rating: payload.mood_rating || 2, status: "Moderate Impact" },
          { label: "Stress Level", rating: payload.stress_level || 2, status: "Moderate Impact" }
        ],
        suggestions: [
          "Take structured breaks between study sessions.",
          "Talk to our MindMate AI companion about what is creating tension.",
          "Ensure regular sleep and hydration."
        ],
        disclaimer: "This is a preliminary wellness screening and not a medical diagnosis."
      };
      Storage.saveLatestAssessment(fallbackResult);
      window.location.href = "result.html";
    }
  });

  updateStepUI();
});
