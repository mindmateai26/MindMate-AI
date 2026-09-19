// MindMate AI - Core Client Application Utilities

const API_BASE = window.location.origin.includes("8000")
  ? `${window.location.origin}/api`
  : (window.location.protocol.startsWith("http") ? "/api" : "http://127.0.0.1:8000/api");

// Global Crisis Modal Management
function setupCrisisModal() {
  const modal = document.getElementById("crisis-modal");
  const openBtns = document.querySelectorAll(".open-crisis-btn");
  const closeBtn = document.getElementById("close-crisis-btn");

  if (!modal) return;

  openBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      modal.classList.add("show");
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      modal.classList.remove("show");
    });
  }

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.remove("show");
    }
  });
}

// Local Storage helpers for seamless student-project persistence
const Storage = {
  saveLatestAssessment: (data) => {
    try {
      localStorage.setItem("mindmate_latest_result", JSON.stringify(data));
      const history = Storage.getHistory();
      history.unshift({
        id: "rec_" + Date.now(),
        timestamp: new Date().toISOString(),
        dateFormatted: new Date().toLocaleDateString(undefined, {
          month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit'
        }),
        score: data.score,
        riskCategory: data.riskCategory,
        contributingFactors: data.contributingFactors ? data.contributingFactors.slice(0, 3) : []
      });
      localStorage.setItem("mindmate_history", JSON.stringify(history.slice(0, 30)));
    } catch (e) {
      console.warn("Storage write failed", e);
    }
  },
  getLatestAssessment: () => {
    try {
      const data = localStorage.getItem("mindmate_latest_result");
      return data ? JSON.parse(data) : null;
    } catch (e) {
      return null;
    }
  },
  getHistory: () => {
    try {
      const data = localStorage.getItem("mindmate_history");
      return data ? JSON.parse(data) : [];
    } catch (e) {
      return [];
    }
  }
};

// Theme Management (Light and Dark mode)
function initTheme() {
  const savedTheme = localStorage.getItem("mindmate_theme") || "light";
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeButtons(savedTheme);

  document.querySelectorAll(".theme-toggle-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme") || "light";
      const next = current === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("mindmate_theme", next);
      updateThemeButtons(next);
    });
  });
}

function updateThemeButtons(theme) {
  document.querySelectorAll(".theme-toggle-btn").forEach(btn => {
    btn.innerHTML = theme === "dark" ? "☀️" : "🌙";
    btn.setAttribute("title", theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode");
  });
}

// Mobile Nav Menu Drawer Toggle
function setupMobileNav() {
  const toggleBtn = document.querySelector(".mobile-nav-toggle");
  const navLinks = document.querySelector(".nav-links");
  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener("click", () => {
      navLinks.classList.toggle("show");
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  setupMobileNav();
  setupCrisisModal();
});
