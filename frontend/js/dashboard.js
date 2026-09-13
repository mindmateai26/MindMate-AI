// MindMate AI - Dashboard Controller

document.addEventListener("DOMContentLoaded", async () => {
  const dashScore = document.getElementById("dash-score");
  const dashDate = document.getElementById("dash-date");
  const dashCategory = document.getElementById("dash-category");
  const dashFactor = document.getElementById("dash-factor");
  const dashTotal = document.getElementById("dash-total");
  const factorsList = document.getElementById("dash-factors-list");
  const tableBody = document.getElementById("history-table-body");

  let historyRecords = [];

  // 1. Attempt to fetch from backend
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

  // 2. Merge with localStorage if backend history was empty
  if (historyRecords.length === 0) {
    historyRecords = Storage.getHistory();
  }

  const latest = historyRecords.length > 0 ? historyRecords[0] : Storage.getLatestAssessment();

  // 3. Populate Summary Cards
  if (latest) {
    dashScore.textContent = `${latest.score || '--'} / 100`;
    dashDate.textContent = latest.dateFormatted || (latest.timestamp ? new Date(latest.timestamp).toLocaleDateString() : "Recent");

    const cat = latest.riskCategory || "Mild";
    dashCategory.innerHTML = `<span class="risk-badge risk-${cat.toLowerCase()}" style="font-size: 1.1rem; padding: 4px 14px;">${cat}</span>`;

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
    dashScore.textContent = "No Data";
    dashCategory.textContent = "N/A";
    dashFactor.textContent = "None";
    dashTotal.textContent = "0";
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
  } else {
    tableBody.innerHTML = `
      <tr>
        <td colspan="5" style="text-align: center; color: var(--text-muted); padding: 28px;">
          No previous assessments found. <a href="assessment.html" style="color: var(--primary); font-weight: 600;">Take your first screening now</a>.
        </td>
      </tr>
    `;
  }
});
