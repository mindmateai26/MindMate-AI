// MindMate AI - Enhanced Dashboard Controller with 7/30-Day Analytics & Personalized Plan

document.addEventListener("DOMContentLoaded", async () => {
  const dashScore = document.getElementById("dash-score");
  const dashDate = document.getElementById("dash-date");
  const dashCategory = document.getElementById("dash-category");
  const dashFactor = document.getElementById("dash-factor");
  const dashTotal = document.getElementById("dash-total");
  const factorsList = document.getElementById("dash-factors-list");
  const tableBody = document.getElementById("history-table-body");

  const analyticsBarsContainer = document.getElementById("analytics-bars-container");
  const btnFilter7d = document.getElementById("btn-filter-7d");
  const btnFilter30d = document.getElementById("btn-filter-30d");
  const chartDescText = document.getElementById("chart-desc-text");

  const planTasksContainer = document.getElementById("plan-tasks-container");
  const planProgressText = document.getElementById("plan-progress-text");

  let historyRecords = [];

  // 1. Fetch from backend
  try {
    const res = await fetch(`${API_BASE}/assessment/history`);
    if (res.ok) {
      const data = await res.json();
      if (data.history && data.history.length > 0) {
        historyRecords = data.history;
      }
    }
  } catch (e) {
    console.warn("Could not fetch history from API, checking local storage:", e);
  }

  // 2. Merge with localStorage
  if (historyRecords.length === 0) {
    historyRecords = Storage.getHistory();
  }

  const latest = historyRecords.length > 0 ? historyRecords[0] : Storage.getLatestAssessment();

  // 3. Populate Summary Cards
  const currentRisk = latest ? (latest.riskCategory || "Mild") : "Mild";
  const currentScore = latest ? (latest.score || 38) : 38;

  if (latest) {
    dashScore.textContent = `${latest.score || '--'} / 100`;
    dashDate.textContent = latest.dateFormatted || (latest.timestamp ? new Date(latest.timestamp).toLocaleDateString() : "Recent");
    dashCategory.innerHTML = `<span class="risk-badge risk-${currentRisk.toLowerCase()}" style="font-size: 1.1rem; padding: 4px 14px;">${currentRisk}</span>`;

    const topFactor = latest.contributingFactors && latest.contributingFactors.length > 0
      ? latest.contributingFactors[0]
      : null;

    dashFactor.textContent = topFactor ? (topFactor.label || topFactor.feature) : "Balanced";
    dashTotal.textContent = historyRecords.length || 1;

    // Populate Factors Breakdown
    if (latest.contributingFactors && latest.contributingFactors.length > 0) {
      factorsList.innerHTML = latest.contributingFactors.map(f => {
        let pillClass = "status-low";
        if (f.rating >= 4) pillClass = "status-high";
        else if (f.rating === 3) pillClass = "status-moderate";
        return `
          <div class="factor-item">
            <div>
              <strong>${f.label || f.feature}</strong>
              <div style="font-size: 0.8rem; color: var(--text-muted);">Impact rating: ${f.rating} / 5</div>
            </div>
            <span class="factor-status-pill ${pillClass}">${f.status || 'Active'}</span>
          </div>
        `;
      }).join("");
    }
  } else {
    dashScore.textContent = "38 / 100";
    dashCategory.innerHTML = `<span class="risk-badge risk-mild" style="font-size: 1.1rem; padding: 4px 14px;">Mild</span>`;
    dashFactor.textContent = "Balanced";
    dashTotal.textContent = "1 (Demo)";
  }

  // 4. Populate Table
  if (historyRecords.length > 0) {
    tableBody.innerHTML = historyRecords.map(item => {
      const topF = item.contributingFactors && item.contributingFactors.length > 0
        ? (item.contributingFactors[0].label || item.contributingFactors[0].feature)
        : "General";
      const cat = item.riskCategory || "Low";

      return `
        <tr>
          <td>${item.dateFormatted || (item.timestamp ? new Date(item.timestamp).toLocaleString() : 'Recent')}</td>
          <td><strong>${item.score || '--'} / 100</strong></td>
          <td><span class="risk-badge risk-${cat.toLowerCase()}" style="font-size: 0.85rem; padding: 2px 10px;">${cat}</span></td>
          <td>${topF}</td>
          <td>
            <a href="companion.html" class="btn btn-outline btn-sm" style="padding: 4px 8px;">Talk to AI</a>
          </td>
        </tr>
      `;
    }).join("");
  }

  // 5. Render 7-day / 30-day Analytics Chart
  const sample7Days = [
    { day: "Mon", score: 48 },
    { day: "Tue", score: 54 },
    { day: "Wed", score: 42 },
    { day: "Thu", score: 60 },
    { day: "Fri", score: 38 },
    { day: "Sat", score: 32 },
    { day: "Sun", score: currentScore }
  ];

  const sample30Days = [
    { day: "W1-M", score: 58 }, { day: "W1-W", score: 55 }, { day: "W1-F", score: 52 },
    { day: "W2-M", score: 62 }, { day: "W2-W", score: 58 }, { day: "W2-F", score: 49 },
    { day: "W3-M", score: 45 }, { day: "W3-W", score: 40 }, { day: "W3-F", score: 44 },
    { day: "W4-M", score: 38 }, { day: "W4-W", score: 35 }, { day: "W4-F", score: currentScore }
  ];

  function renderAnalyticsChart(dataList, is30d = false) {
    if (!analyticsBarsContainer) return;
    analyticsBarsContainer.innerHTML = "";

    dataList.forEach(item => {
      const col = document.createElement("div");
      col.style.display = "flex";
      col.style.flexDirection = "column";
      col.style.alignItems = "center";
      col.style.gap = "4px";
      col.style.flex = "1";
      col.style.minWidth = is30d ? "22px" : "32px";

      // Height percentage mapped to score (max 100)
      const barHeight = Math.max(15, Math.round((item.score / 100) * 120));
      let barBg = "var(--primary)";
      if (item.score >= 70) barBg = "var(--danger)";
      else if (item.score >= 50) barBg = "var(--warning)";
      else if (item.score >= 35) barBg = "var(--secondary)";

      col.innerHTML = `
        <span style="font-size: 0.7rem; font-weight: 700; color: var(--text-muted);">${item.score}</span>
        <div style="width: ${is30d ? '14px' : '22px'}; height: ${barHeight}px; background: ${barBg}; border-radius: 4px 4px 0 0; opacity: 0.88; transition: height 0.4s ease;"></div>
        <span style="font-size: 0.72rem; color: var(--text-muted); margin-top: 4px;">${item.day}</span>
      `;
      analyticsBarsContainer.appendChild(col);
    });
  }

  renderAnalyticsChart(sample7Days, false);

  if (btnFilter7d && btnFilter30d) {
    btnFilter7d.addEventListener("click", () => {
      btnFilter7d.classList.add("active");
      btnFilter30d.classList.remove("active");
      if (chartDescText) chartDescText.textContent = "Distress score trajectory for the past 7 days (lower score indicates higher wellness):";
      renderAnalyticsChart(sample7Days, false);
    });

    btnFilter30d.addEventListener("click", () => {
      btnFilter30d.classList.add("active");
      btnFilter7d.classList.remove("active");
      if (chartDescText) chartDescText.textContent = "Multi-week distress trend over the past 30 days:";
      renderAnalyticsChart(sample30Days, true);
    });
  }

  // 6. Personalized Wellness Plan Checklist
  const plansByTier = {
    "Low": [
      { id: "p1", title: "Morning Gratitude & Hydration", desc: "Drink 500ml water and jot down 2 positive moments.", category: "Routine" },
      { id: "p2", title: "Active Movement", desc: "20-minute brisk walk or gentle yoga stretch outdoors.", category: "Physical" },
      { id: "p3", title: "Study-Life Balance", desc: "Clock off books/work by 8:30 PM for social rest.", category: "Boundaries" },
      { id: "p4", title: "Evening Journaling", desc: "Write 3 lines in the MindMate AI Journal.", category: "Mindfulness" }
    ],
    "Mild": [
      { id: "p1", title: "Box Breathing (4-4-4)", desc: "Perform 3 cycles of 4s box breathing before study sessions.", category: "Grounding" },
      { id: "p2", title: "Pomodoro Micro-Breaks", desc: "Take mandatory 5-min detachments every 25 minutes.", category: "Focus" },
      { id: "p3", title: "Blue-Light Cutoff", desc: "Turn off mobile screens 45 minutes before sleep.", category: "Sleep Hygiene" },
      { id: "p4", title: "AI Companion Reflection", desc: "Share any stress build-up with MindMate AI.", category: "Support" }
    ],
    "Moderate": [
      { id: "p1", title: "Stress De-escalation", desc: "5-minute progressive muscle relaxation to relieve neck tension.", category: "Somatic" },
      { id: "p2", title: "Task De-clustering", desc: "Pick only top 2 essential priorities today; defer non-urgent tasks.", category: "Workload" },
      { id: "p3", title: "Peer/Mentor Touchpoint", desc: "Have a brief honest conversation with a friend or counselor.", category: "Connection" },
      { id: "p4", title: "Hydration & Rest Window", desc: "Ensure 8 full hours of uninterrupted sleep.", category: "Rest" }
    ],
    "High": [
      { id: "p1", title: "Immediate Grounding Check", desc: "Name 5 things you see, 4 you feel, 3 you hear.", category: "Safety" },
      { id: "p2", title: "Confide in a Trusted Contact", desc: "Reach out to family or use confidential Tele-MANAS (14416).", category: "Support" },
      { id: "p3", title: "Complete Pressure Stand-down", desc: "Pause academic work for the next 2 hours for nervous reset.", category: "Care" },
      { id: "p4", title: "Counselor Consultation", desc: "Schedule an appointment with a college mental health counselor.", category: "Professional" }
    ]
  };

  const currentPlan = plansByTier[currentRisk] || plansByTier["Mild"];
  let savedCompleted = JSON.parse(localStorage.getItem(`mindmate_plan_${currentRisk}`) || "[]");

  function updatePlanUI() {
    if (!planTasksContainer) return;
    planTasksContainer.innerHTML = currentPlan.map(task => {
      const isDone = savedCompleted.includes(task.id);
      return `
        <div class="plan-category-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span class="saas-badge" style="background: #e0f2fe; color: #0284c7; font-size: 0.72rem;">${task.category}</span>
            <span style="font-size: 0.8rem; color: ${isDone ? 'var(--success)' : 'var(--text-muted)'}; font-weight: 600;">
              ${isDone ? '✓ Completed' : 'Pending'}
            </span>
          </div>
          <strong style="font-size: 0.95rem; color: var(--text-main);">${task.title}</strong>
          <p style="font-size: 0.83rem; color: var(--text-muted); margin: 6px 0 10px;">${task.desc}</p>
          <div class="plan-task-item ${isDone ? 'completed' : ''}" data-id="${task.id}">
            <input type="checkbox" ${isDone ? 'checked' : ''} style="cursor: pointer; width: 16px; height: 16px;" />
            <span style="font-size: 0.86rem; font-weight: 500;">${isDone ? 'Task Finished' : 'Mark as Done'}</span>
          </div>
        </div>
      `;
    }).join("");

    if (planProgressText) {
      planProgressText.textContent = `${savedCompleted.length} / ${currentPlan.length} completed`;
    }

    // Attach click listeners to task checkboxes
    planTasksContainer.querySelectorAll(".plan-task-item").forEach(item => {
      item.addEventListener("click", () => {
        const id = item.getAttribute("data-id");
        if (savedCompleted.includes(id)) {
          savedCompleted = savedCompleted.filter(x => x !== id);
        } else {
          savedCompleted.push(id);
        }
        localStorage.setItem(`mindmate_plan_${currentRisk}`, JSON.stringify(savedCompleted));
        updatePlanUI();
      });
    });
  }

  updatePlanUI();
});
