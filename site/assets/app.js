const state = {
  data: null,
  group: "",
  status: "",
  search: ""
};

const fmt = new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 2 });

function statusClass(status) {
  if (status === "Trả lời được") return "ok";
  if (status === "Một phần") return "partial";
  return "missing";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderKpis(data) {
  const items = [
    ["10,865,001", "Dòng THPT canonical 2016-2026"],
    ["2,412,155", "Dòng legacy có tên/ngày sinh 2013-2014"],
    [String(data.questions.length), "Câu hỏi đã trả lời và gắn trạng thái"],
    [String(data.story.latest_year), "Năm mới nhất trong bộ phân tích"]
  ];
  document.querySelector("#kpis").innerHTML = items.map(([value, label]) => `
    <article class="kpi"><strong>${value}</strong><span>${label}</span></article>
  `).join("");
}

function lineChart(el, rows) {
  const width = 640, height = 280, pad = 34;
  const xs = rows.map(d => d.year);
  const ys = rows.map(d => d.weighted_mean);
  const minX = Math.min(...xs), maxX = Math.max(...xs);
  const minY = Math.min(...ys) - 0.15, maxY = Math.max(...ys) + 0.15;
  const x = year => pad + ((year - minX) / Math.max(maxX - minX, 1)) * (width - pad * 2);
  const y = value => height - pad - ((value - minY) / Math.max(maxY - minY, 1)) * (height - pad * 2);
  const points = rows.map(d => `${x(d.year)},${y(d.weighted_mean)}`).join(" ");
  const labels = rows.map(d => `<text x="${x(d.year)}" y="${height - 10}" text-anchor="middle" font-size="10" fill="#5b6573">${d.year}</text>`).join("");
  const dots = rows.map(d => `<circle cx="${x(d.year)}" cy="${y(d.weighted_mean)}" r="3.5"><title>${d.year}: ${fmt.format(d.weighted_mean)}</title></circle>`).join("");
  el.innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Mean theo năm">
    <line x1="${pad}" y1="${height-pad}" x2="${width-pad}" y2="${height-pad}" stroke="#d9dee7"/>
    <line x1="${pad}" y1="${pad}" x2="${pad}" y2="${height-pad}" stroke="#d9dee7"/>
    <polyline points="${points}" fill="none" stroke="#0e7c86" stroke-width="3"/>
    <g fill="#0e7c86">${dots}</g>
    ${labels}
  </svg>`;
}

function barChart(el, rows) {
  const data = rows.slice().sort((a, b) => b.mean - a.mean);
  const width = 640, height = 280, pad = 34;
  const max = Math.max(...data.map(d => d.mean));
  const barW = (width - pad * 2) / data.length - 5;
  const bars = data.map((d, i) => {
    const x = pad + i * ((width - pad * 2) / data.length);
    const h = (d.mean / max) * (height - pad * 2);
    const y = height - pad - h;
    const label = d.subject_label.length > 11 ? d.subject_label.slice(0, 10) + "." : d.subject_label;
    return `<g>
      <rect x="${x}" y="${y}" width="${barW}" height="${h}" rx="3" fill="#bc5b33"><title>${escapeHtml(d.subject_label)}: ${fmt.format(d.mean)}</title></rect>
      <text transform="translate(${x + barW / 2},${height - 8}) rotate(-35)" text-anchor="end" font-size="10" fill="#5b6573">${escapeHtml(label)}</text>
    </g>`;
  }).join("");
  el.innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Mean theo môn năm gần nhất">
    <line x1="${pad}" y1="${height-pad}" x2="${width-pad}" y2="${height-pad}" stroke="#d9dee7"/>
    ${bars}
  </svg>`;
}

function renderFilters(data) {
  const groups = [...new Set(data.questions.map(q => q.group))];
  const statuses = [...new Set(data.questions.map(q => q.status))];
  document.querySelector("#groupFilter").innerHTML += groups.map(g => `<option value="${escapeHtml(g)}">${escapeHtml(g)}</option>`).join("");
  document.querySelector("#statusFilter").innerHTML += statuses.map(s => `<option value="${escapeHtml(s)}">${escapeHtml(s)}</option>`).join("");
}

function renderHighlights(data) {
  document.querySelector("#highlights").innerHTML = data.highlights.map(item => `<li>${escapeHtml(item)}</li>`).join("");
}

function renderQuestions() {
  const query = state.search.trim().toLowerCase();
  const rows = state.data.questions.filter(q => {
    const matchesGroup = !state.group || q.group === state.group;
    const matchesStatus = !state.status || q.status === state.status;
    const haystack = `${q.question} ${q.answer} ${q.evidence} ${q.group}`.toLowerCase();
    const matchesSearch = !query || haystack.includes(query);
    return matchesGroup && matchesStatus && matchesSearch;
  });
  document.querySelector("#resultCount").textContent = `${rows.length} câu đang hiển thị`;
  document.querySelector("#questionList").innerHTML = rows.map(q => `
    <article class="question-card">
      <div class="question-meta">
        <span class="pill">#${q.id}</span>
        <span class="pill">${escapeHtml(q.group)}</span>
        <span class="pill ${statusClass(q.status)}">${escapeHtml(q.status)}</span>
      </div>
      <h3>${escapeHtml(q.question)}</h3>
      <p class="answer">${escapeHtml(q.answer)}</p>
      <p class="evidence">${escapeHtml(q.evidence)}</p>
    </article>
  `).join("");
}

fetch("data/answers.json")
  .then(response => response.json())
  .then(data => {
    state.data = data;
    renderKpis(data);
    renderFilters(data);
    renderHighlights(data);
    lineChart(document.querySelector("#annualChart"), data.charts.annual);
    barChart(document.querySelector("#subjectChart"), data.charts.latest_subjects);
    renderQuestions();
  });

document.querySelector("#searchBox").addEventListener("input", event => {
  state.search = event.target.value;
  renderQuestions();
});
document.querySelector("#groupFilter").addEventListener("change", event => {
  state.group = event.target.value;
  renderQuestions();
});
document.querySelector("#statusFilter").addEventListener("change", event => {
  state.status = event.target.value;
  renderQuestions();
});
