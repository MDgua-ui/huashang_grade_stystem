// 全局状态
let students = [];
let filteredStudents = [];
let currentSort = { key: '综合成绩', dir: 'desc' };

// 满分标准
const FULL_SCORES = { '讨论': 20, '作业': 30, '签到': 10, '课程积分': 20, 'PBL': 20 };

async function init() {
  const res = await fetch('data.json');
  students = await res.json();
  filteredStudents = [...students];
  renderAll();
  setupEvents();
}

function renderAll() {
  renderHeroStats();
  renderPodium();
  renderCharts();
  renderTable();
  document.getElementById('totalCount').textContent = students.length;
}

function renderHeroStats() {
  const all = students;
  const avg = (all.reduce((s, x) => s + x.综合成绩, 0) / all.length).toFixed(1);
  const max = Math.max(...all.map(x => x.综合成绩));
  const excellent = all.filter(x => x.综合成绩 >= 90).length;
  const fail = all.filter(x => x.综合成绩 < 60).length;
  const fullMark = all.filter(x => x.综合成绩 >= 99).length;

  document.getElementById('heroStats').innerHTML = `
    <div class="hero-stat"><span class="val">${avg}</span><span class="lbl">平均分</span></div>
    <div class="hero-stat"><span class="val">${max}</span><span class="lbl">最高分</span></div>
    <div class="hero-stat"><span class="val">${excellent}</span><span class="lbl">90分以上</span></div>
    <div class="hero-stat"><span class="val">${fail}</span><span class="lbl">不及格</span></div>
    <div class="hero-stat"><span class="val">${fullMark}</span><span class="lbl">接近满分</span></div>
  `;
}

function renderPodium() {
  const top3 = students.slice(0, 3);
  const podium = document.getElementById('podium');
  if (top3.length < 3) return;

  const classes = ['rank1', 'rank2', 'rank3'];
  podium.innerHTML = top3.map((s, i) => `
    <div class="podium-item ${classes[i]}">
      <div class="rank-name">${s.学生姓名}</div>
      <div class="rank-score">${s.综合成绩}<small>分</small></div>
      <div class="rank-details">
        <span>讨论 ${s.讨论}</span><span>作业 ${s.作业}</span>
        <span>签到 ${s.签到}</span><span>积分 ${s.课程积分}</span><span>PBL ${s.PBL}</span>
      </div>
    </div>
  `).join('');
}

let distChartInst = null;
let fullScoreChartInst = null;

function renderCharts() {
  // 成绩分布
  const bins = [
    { label: '<60', min: 0, max: 59.99 },
    { label: '60-69', min: 60, max: 69.99 },
    { label: '70-79', min: 70, max: 79.99 },
    { label: '80-89', min: 80, max: 89.99 },
    { label: '≥90', min: 90, max: 100 },
  ];
  const counts = bins.map(b => students.filter(s => s.综合成绩 >= b.min && s.综合成绩 <= b.max).length);

  if (distChartInst) distChartInst.destroy();
  const ctx1 = document.getElementById('distChart').getContext('2d');
  distChartInst = new Chart(ctx1, {
    type: 'bar',
    data: {
      labels: bins.map(b => b.label),
      datasets: [{
        label: '人数',
        data: counts,
        backgroundColor: [
          '#ef4444', '#f59e0b', '#eab308', '#3b82f6', '#22c55e'
        ],
        borderRadius: 6,
        borderWidth: 0,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ctx.raw + ' 人' } }
      },
      scales: {
        y: { beginAtZero: true, ticks: { stepSize: 5 }, grid: { color: '#f0ece4' }, title: { display: true, text: '人数' } },
        x: { grid: { display: false } }
      }
    }
  });

  // 满分达成率
  const items = ['讨论', '作业', '签到', '课程积分', 'PBL'];
  const fullRate = items.map(k => {
    const max = FULL_SCORES[k];
    const count = students.filter(s => s[k] >= max * 0.99).length;
    return ((count / students.length) * 100).toFixed(1);
  });

  if (fullScoreChartInst) fullScoreChartInst.destroy();
  const ctx2 = document.getElementById('fullScoreChart').getContext('2d');
  fullScoreChartInst = new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: items,
      datasets: [{
        label: '满分率 %',
        data: fullRate.map(Number),
        backgroundColor: ['#60a5fa', '#34d399', '#f472b6', '#fbbf24', '#a78bfa'],
        borderRadius: 6,
        borderWidth: 0,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ctx.raw + '%' } }
      },
      scales: {
        x: { beginAtZero: true, max: 100, ticks: { callback: v => v + '%' }, grid: { color: '#f0ece4' } },
        y: { grid: { display: false } }
      }
    }
  });
}

function renderTable() {
  const tbody = document.getElementById('tableBody');
  tbody.innerHTML = filteredStudents.map(s => {
    const rankClass = s.排名 <= 3 ? `rank-${s.排名}-row top3` : '';
    const badgeClass = s.排名 === 1 ? 'gold' : s.排名 === 2 ? 'silver' : s.排名 === 3 ? 'bronze' : 'normal';
    const scoreClass = s.综合成绩 >= 90 ? 'score-high' : s.综合成绩 >= 60 ? 'score-mid' : 'score-low';
    return `
      <tr class="${rankClass}" data-index="${students.indexOf(s)}">
        <td><span class="rank-badge ${badgeClass}">${s.排名}</span></td>
        <td class="name-cell">${s.学生姓名}</td>
        <td>${s.学号}</td>
        <td>${s.讨论 ?? '-'}</td>
        <td>${s.作业 ?? '-'}</td>
        <td>${s.签到 ?? '-'}</td>
        <td>${s.课程积分 ?? '-'}</td>
        <td>${s.PBL ?? '-'}</td>
        <td class="${scoreClass}">${s.综合成绩}</td>
      </tr>
    `;
  }).join('');

  // 点击行查看详情
  tbody.querySelectorAll('tr').forEach(tr => {
    tr.addEventListener('click', () => {
      const idx = parseInt(tr.dataset.index);
      showDetail(students[idx]);
    });
  });

  // 排序表头
  document.querySelectorAll('th.sortable').forEach(th => {
    th.className = 'sortable';
    if (th.dataset.key === currentSort.key) {
      th.classList.add('active');
      th.textContent = th.textContent.replace(/[▼▲]/g, '').trim() + (currentSort.dir === 'desc' ? ' ▼' : ' ▲');
    }
  });
}

function showDetail(student) {
  const section = document.getElementById('detailSection');
  const card = document.getElementById('detailCard');

  const totalMax = 100;
  const pct = (student.综合成绩 / totalMax * 100).toFixed(1);
  const rankClass = student.排名 <= 3 ? 'top' : student.综合成绩 < 60 ? 'low' : 'mid';
  const items = [
    { k: '讨论', v: student.讨论, max: 20, cls: 'discuss' },
    { k: '作业', v: student.作业, max: 30, cls: 'homework' },
    { k: '签到', v: student.签到, max: 10, cls: 'checkin' },
    { k: '课程积分', v: student.课程积分, max: 20, cls: 'points' },
    { k: 'PBL', v: student.PBL, max: 20, cls: 'pbl' },
  ];

  card.innerHTML = `
    <div class="detail-header">
      <div class="detail-rank ${rankClass}">${student.排名}</div>
      <div>
        <div class="detail-name">${student.学生姓名}</div>
        <div class="detail-id">${student.学号} · ${student.班级}</div>
      </div>
      <div class="detail-score">${student.综合成绩} 分</div>
    </div>
    <div class="detail-bars">
      ${items.map(it => `
        <div class="detail-bar-item">
          <span class="bar-label">${it.k}</span>
          <div class="bar-track">
            <div class="bar-fill ${it.cls}" style="width:${(it.v / it.max * 100).toFixed(1)}%"></div>
          </div>
          <span class="bar-val">${it.v}/${it.max}</span>
        </div>
      `).join('')}
    </div>
    <button class="detail-close" onclick="closeDetail()">收起明细</button>
  `;

  section.style.display = 'block';
  section.scrollIntoView({ behavior: 'smooth' });
}

function closeDetail() {
  document.getElementById('detailSection').style.display = 'none';
}

function setupEvents() {
  // 搜索
  document.getElementById('searchBtn').addEventListener('click', doSearch);
  document.getElementById('searchInput').addEventListener('keydown', e => {
    if (e.key === 'Enter') doSearch();
  });

  // 排序
  document.querySelectorAll('th.sortable').forEach(th => {
    th.addEventListener('click', () => {
      const key = th.dataset.key;
      if (currentSort.key === key) {
        currentSort.dir = currentSort.dir === 'desc' ? 'asc' : 'desc';
      } else {
        currentSort.key = key;
        currentSort.dir = 'desc';
      }
      // 排名特殊处理：按综合成绩排序后重新编号
      if (key === '排名') {
        // 排名实际上是综合成绩的降序
        currentSort.key = '综合成绩';
        currentSort.dir = 'desc';
      }
      sortData();
      reRank();
      renderTable();
    });
  });
}

function doSearch() {
  const q = document.getElementById('searchInput').value.trim();
  if (!q) {
    filteredStudents = [...students];
  } else {
    const lower = q.toLowerCase();
    filteredStudents = students.filter(s =>
      s.学生姓名.toLowerCase().includes(lower) ||
      String(s.学号).includes(q)
    );
  }
  sortData();
  renderTable();
}

function sortData() {
  const key = currentSort.key;
  const dir = currentSort.dir === 'desc' ? -1 : 1;
  filteredStudents.sort((a, b) => {
    const va = a[key] ?? 0;
    const vb = b[key] ?? 0;
    if (typeof va === 'string') return dir * va.localeCompare(vb);
    return dir * (va - vb);
  });
}

function reRank() {
  // 仅当没有搜索过滤时重新排名
  if (filteredStudents.length === students.length) {
    const sorted = [...students].sort((a, b) => b.综合成绩 - a.综合成绩);
    sorted.forEach((s, i) => s.排名 = i + 1);
  }
}

init();
