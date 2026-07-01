import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

with open('e:/作业2/计算机前沿技术/huashang_grade_system/data.json', encoding='utf-8') as f:
    data = json.load(f)

# ===== 图1: 成绩分布柱状图 (精美版) =====
fig1, ax1 = plt.subplots(figsize=(9, 5.5))
fig1.patch.set_facecolor('#0f172a')
ax1.set_facecolor('#0f172a')
bins = [0, 60, 70, 80, 90, 100]
labels = ['< 60 分', '60 - 69 分', '70 - 79 分', '80 - 89 分', '≥ 90 分']
counts = []
for i in range(len(bins)-1):
    lo, hi = bins[i], bins[i+1]
    cnt = sum(1 for d in data if lo <= d['综合成绩'] < hi) if i < len(bins)-2 else sum(1 for d in data if d['综合成绩'] >= lo)
    counts.append(cnt)

gradients = ['#ef4444', '#f59e0b', '#eab308', '#3b82f6', '#10b981']
bars = ax1.bar(labels, counts, color=gradients, edgecolor='#1e293b', linewidth=1.2, width=0.6)
for bar, c in zip(bars, counts):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.6, str(c),
             ha='center', fontsize=15, fontweight='bold', color='#e2e8f0')
ax1.set_title('全班综合成绩分布', fontsize=20, fontweight='bold', pad=20, color='#f1f5f9')
ax1.set_ylabel('人数', fontsize=14, color='#94a3b8')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#334155')
ax1.spines['bottom'].set_color('#334155')
ax1.tick_params(labelsize=13, colors='#94a3b8')
ax1.yaxis.grid(True, color='#1e293b', linewidth=0.5)
ax1.set_axisbelow(True)
fig1.tight_layout()
buf1 = io.BytesIO()
fig1.savefig(buf1, format='png', dpi=180, bbox_inches='tight', facecolor='#0f172a')
buf1.seek(0)
img_dist = base64.b64encode(buf1.read()).decode()
plt.close(fig1)

# ===== 图2: TOP 10 =====
top10 = data[:10]
fig2, ax2 = plt.subplots(figsize=(10, 5.5))
fig2.patch.set_facecolor('#0f172a')
ax2.set_facecolor('#0f172a')
names = [d['学生姓名'] for d in reversed(top10)]
scores = [d['综合成绩'] for d in reversed(top10)]
colors2 = []
for s in reversed(scores):
    if s >= 95: colors2.append('#fbbf24')
    elif s >= 90: colors2.append('#10b981')
    elif s >= 80: colors2.append('#60a5fa')
    else: colors2.append('#f59e0b')

bars2 = ax2.barh(names, scores, color=colors2, edgecolor='#1e293b', linewidth=0.8, height=0.65)
for bar, s in zip(bars2, scores):
    ax2.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2, f'{s} 分',
             va='center', fontsize=12, fontweight='bold', color='#e2e8f0')
ax2.set_title('综合成绩 TOP 10', fontsize=20, fontweight='bold', pad=20, color='#f1f5f9')
ax2.set_xlabel('综合成绩', fontsize=14, color='#94a3b8')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#334155')
ax2.spines['bottom'].set_color('#334155')
ax2.tick_params(labelsize=13, colors='#94a3b8')
ax2.set_xlim(0, max(scores)+7)
ax2.xaxis.grid(True, color='#1e293b', linewidth=0.5)
ax2.set_axisbelow(True)
fig2.tight_layout()
buf2 = io.BytesIO()
fig2.savefig(buf2, format='png', dpi=180, bbox_inches='tight', facecolor='#0f172a')
buf2.seek(0)
img_top10 = base64.b64encode(buf2.read()).decode()
plt.close(fig2)

# ===== 图3: 满分达成率 =====
items = ['讨论', '作业', '签到', '课程积分', 'PBL']
max_vals = {'讨论': 20, '作业': 30, '签到': 10, '课程积分': 20, 'PBL': 20}
full_rates = []
for k in items:
    cnt = sum(1 for d in data if d[k] is not None and d[k] >= max_vals[k]*0.99)
    full_rates.append(round(cnt/len(data)*100, 1))

fig3, ax3 = plt.subplots(figsize=(9, 5.5))
fig3.patch.set_facecolor('#0f172a')
ax3.set_facecolor('#0f172a')
colors3 = ['#60a5fa', '#34d399', '#f472b6', '#fbbf24', '#a78bfa']
bars3 = ax3.bar(items, full_rates, color=colors3, edgecolor='#1e293b', linewidth=1.2, width=0.55)
for bar, r in zip(bars3, full_rates):
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1, f'{r}%',
             ha='center', fontsize=14, fontweight='bold', color='#e2e8f0')
ax3.set_title('各项满分达成率', fontsize=20, fontweight='bold', pad=20, color='#f1f5f9')
ax3.set_ylabel('占比 (%)', fontsize=14, color='#94a3b8')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_color('#334155')
ax3.spines['bottom'].set_color('#334155')
ax3.tick_params(labelsize=13, colors='#94a3b8')
ax3.set_ylim(0, 105)
ax3.yaxis.grid(True, color='#1e293b', linewidth=0.5)
ax3.set_axisbelow(True)
fig3.tight_layout()
buf3 = io.BytesIO()
fig3.savefig(buf3, format='png', dpi=180, bbox_inches='tight', facecolor='#0f172a')
buf3.seek(0)
img_full = base64.b64encode(buf3.read()).decode()
plt.close(fig3)

avg = round(sum(d['综合成绩'] for d in data) / len(data), 1)
mx = max(d['综合成绩'] for d in data)
mn = min(d['综合成绩'] for d in data)
excellent = sum(1 for d in data if d['综合成绩'] >= 90)
fail = sum(1 for d in data if d['综合成绩'] < 60)
top3_names = '、'.join(d['学生姓名'] for d in data[:3])
top1 = data[0]
top2 = data[1]
top3 = data[2]

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>华商创新班综合成绩排名系统 · 项目分享</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --ink: #0f172a;
    --paper: #f8fafc;
    --accent: #6366f1;
    --accent2: #a855f7;
    --gold: #f59e0b;
    --muted: #64748b;
  }

  body {
    font-family: "Noto Serif SC", "Source Han Serif SC", "Songti SC", Georgia, "Times New Roman", "PingFang SC", "Microsoft YaHei", serif;
    background: #020617;
    color: #e2e8f0;
    line-height: 1.9;
    -webkit-font-smoothing: antialiased;
  }

  /* ---- HERO ---- */
  .hero {
    position: relative;
    background: linear-gradient(160deg, #0f172a 0%, #1e1b4b 40%, #312e81 70%, #4c1d95 100%);
    padding: 8rem 2rem 6rem;
    text-align: center;
    overflow: hidden;
  }
  .hero::after {
    content: "";
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 120%, rgba(99,102,241,0.25) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(168,85,247,0.15) 0%, transparent 50%);
  }
  .hero-content { position: relative; z-index: 1; max-width: 720px; margin: 0 auto; }
  .hero-tag {
    display: inline-block; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 0.8rem; letter-spacing: 0.25em; text-transform: uppercase;
    color: var(--gold); border: 1px solid rgba(245,158,11,0.3);
    border-radius: 3rem; padding: 0.4rem 1.6rem; margin-bottom: 2rem;
    font-weight: 600;
  }
  .hero h1 { font-size: 3.2rem; font-weight: 900; letter-spacing: 0.04em; line-height: 1.3; margin-bottom: 1rem; color: #fff; }
  .hero h1 span { background: linear-gradient(135deg, #c4b5fd, #a78bfa, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .hero .subtitle { font-size: 1.15rem; color: #a5b4fc; font-weight: 400; margin-bottom: 3rem; opacity: 0.9; }

  .hero-stats { display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; }
  .hero-stat {
    background: rgba(255,255,255,0.06); backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1); border-radius: 1rem;
    padding: 1.2rem 1.8rem; text-align: center; min-width: 120px; transition: transform 0.3s;
  }
  .hero-stat:hover { transform: translateY(-4px); }
  .hero-stat .val { display: block; font-size: 2.4rem; font-weight: 900; color: #fbbf24; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
  .hero-stat .lbl { display: block; font-size: 0.8rem; color: #94a3b8; margin-top: 0.3rem; letter-spacing: 0.05em; }

  /* ---- SECTION ---- */
  .section { max-width: 860px; margin: 0 auto; padding: 5rem 2rem; }
  .section + .section { padding-top: 0; }

  .section-intro { text-align: center; }
  .section-number {
    display: inline-block; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 0.75rem; letter-spacing: 0.2em; color: var(--accent); font-weight: 700;
    margin-bottom: 0.8rem; text-transform: uppercase;
  }
  .section-heading {
    font-size: 2rem; font-weight: 800; color: #f1f5f9; margin-bottom: 1.2rem; letter-spacing: 0.02em;
  }
  .section-heading em { font-style: normal; color: var(--accent2); }

  .prose { margin: 0 auto; }
  .prose p { font-size: 1.05rem; color: #cbd5e1; margin-bottom: 1.5rem; text-align: justify; }
  .prose p.lead { font-size: 1.2rem; line-height: 2; color: #e2e8f0; }

  /* ---- DIVIDER ---- */
  .divider { width: 60px; height: 3px; background: linear-gradient(90deg, var(--accent), var(--accent2)); margin: 3rem auto; border-radius: 1px; }

  /* ---- PULL QUOTE ---- */
  .pullquote {
    border-left: 4px solid var(--accent); padding: 1.2rem 0 1.2rem 2rem;
    margin: 2.5rem 0; background: rgba(99,102,241,0.05); border-radius: 0 0.75rem 0.75rem 0;
  }
  .pullquote p { font-size: 1.2rem; font-style: italic; color: #e2e8f0; margin: 0; }

  /* ---- IMAGE ---- */
  .figure { margin: 3rem 0; text-align: center; }
  .figure img { max-width: 100%; border-radius: 1rem; box-shadow: 0 8px 40px rgba(0,0,0,0.5); border: 1px solid #1e293b; }
  .figure .figcaption { font-size: 0.85rem; color: #64748b; margin-top: 1rem; font-style: italic; letter-spacing: 0.02em; }

  /* ---- PODIUM ---- */
  .podium { display: flex; justify-content: center; align-items: flex-end; gap: 1.5rem; padding: 2rem 0; flex-wrap: wrap; }
  .podium-card {
    background: rgba(30,41,59,0.8); border: 1px solid #1e293b; border-radius: 1.25rem;
    padding: 2rem 1.5rem; text-align: center; position: relative; transition: all 0.3s;
    min-width: 170px; backdrop-filter: blur(8px);
  }
  .podium-card:hover { transform: translateY(-6px); border-color: #334155; }
  .podium-card.gold { border-color: rgba(245,158,11,0.4); padding-top: 3rem; min-width: 200px; }
  .podium-card.silver { padding-top: 2.5rem; }
  .podium-card.bronze { padding-top: 2.2rem; }
  .podium-medal {
    position: absolute; top: -1.2rem; left: 50%; transform: translateX(-50%);
    width: 3rem; height: 3rem; border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; font-weight: 900; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }
  .podium-card.gold .podium-medal { background: linear-gradient(135deg, #fbbf24, #d97706); color: #451a03; }
  .podium-card.silver .podium-medal { background: linear-gradient(135deg, #cbd5e1, #94a3b8); color: #1e293b; }
  .podium-card.bronze .podium-medal { background: linear-gradient(135deg, #d97706, #92400e); color: #fef3c7; }
  .podium-name { font-size: 1.2rem; font-weight: 700; color: #f1f5f9; margin: 0.8rem 0 0.2rem; }
  .podium-score { font-size: 2.2rem; font-weight: 900; color: #fbbf24; }
  .podium-score small { font-size: 0.85rem; font-weight: 500; color: #94a3b8; }
  .podium-detail { font-size: 0.78rem; color: #64748b; margin-top: 0.5rem; line-height: 1.6; }
  .podium-detail span { display: inline-block; margin: 0 0.3rem; }

  /* ---- HIGHLIGHT BOX ---- */
  .highlight-box {
    background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(168,85,247,0.1));
    border: 1px solid rgba(99,102,241,0.25); border-radius: 1rem; padding: 2rem;
    margin: 2rem 0;
  }
  .highlight-box p { margin: 0; color: #e2e8f0; font-size: 1.05rem; text-align: center; }
  .highlight-box p strong { color: #fbbf24; }

  /* ---- LINKS ---- */
  .cta {
    max-width: 860px; margin: 0 auto; padding: 3rem 2rem 6rem; text-align: center;
  }
  .cta-heading { font-size: 1.4rem; font-weight: 700; color: #f1f5f9; margin-bottom: 2rem; }
  .cta-links { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }
  .cta-btn {
    display: inline-flex; align-items: center; gap: 0.5rem; padding: 1rem 2rem;
    border-radius: 0.75rem; font-size: 1rem; font-weight: 700; text-decoration: none;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    transition: all 0.3s; border: 1px solid transparent;
  }
  .cta-btn.primary {
    background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4);
  }
  .cta-btn.primary:hover { box-shadow: 0 6px 30px rgba(99,102,241,0.6); transform: translateY(-2px); }
  .cta-btn.secondary { background: rgba(255,255,255,0.06); color: #e2e8f0; border-color: #334155; }
  .cta-btn.secondary:hover { background: rgba(255,255,255,0.12); border-color: #475569; transform: translateY(-2px); }
  .cta-url { display: block; font-size: 0.85rem; color: #475569; margin-top: 1.2rem; word-break: break-all; }

  /* ---- FOOTER ---- */
  .footer { text-align: center; padding: 2rem; border-top: 1px solid #1e293b; color: #475569; font-size: 0.85rem; }
  .footer a { color: #6366f1; text-decoration: none; }
  .footer a:hover { text-decoration: underline; }

  @media (max-width: 640px) {
    .hero h1 { font-size: 2rem; }
    .hero-stats { gap: 0.8rem; }
    .hero-stat { padding: 0.8rem 1.2rem; min-width: 100px; }
    .hero-stat .val { font-size: 1.8rem; }
    .podium { flex-direction: column; align-items: center; }
    .section { padding: 3rem 1.2rem; }
    .section-heading { font-size: 1.5rem; }
    .prose p { text-align: left; }
  }
</style>
</head>
<body>

<!-- ====== HERO ====== -->
<div class="hero">
  <div class="hero-content">
    <div class="hero-tag">项目分享 · 计算机前沿技术</div>
    <h1>用 <span>代码</span> 点亮排行榜</h1>
    <p class="subtitle">华商创新班 · 综合成绩排名系统</p>
    <div class="hero-stats">
      <div class="hero-stat"><span class="val">56</span><span class="lbl">同学</span></div>
      <div class="hero-stat"><span class="val">''' + str(avg) + '''</span><span class="lbl">平均分</span></div>
      <div class="hero-stat"><span class="val">''' + str(mx) + '''</span><span class="lbl">最高分</span></div>
      <div class="hero-stat"><span class="val">''' + str(excellent) + ''' 人</span><span class="lbl">90 分以上</span></div>
    </div>
  </div>
</div>

<!-- ====== 01 项目缘起 ====== -->
<div class="section">
  <div class="section-intro">
    <div class="section-number">一</div>
    <h2 class="section-heading">从 Excel 到<em>排行榜</em>的诞生</h2>
  </div>
  <div class="divider"></div>
  <div class="prose">
    <p class="lead">作为计算机科学与技术创新实验班的学生，这学期《计算机前沿技术》课程的综合成绩由讨论、作业、签到、课程积分和 PBL 五大模块组成，满分一百分。数据躺在 Excel 表格里的时候，它只是一串数字。但用代码把它变成网页上的排行榜后，数字有了温度、有了对比、有了故事。</p>
    <p>系统覆盖了人工智能学院创新实验班两个班级的全部同学。讨论占百分之二十、作业占百分之三十、签到占百分之十、课程积分占百分之二十、PBL 占百分之二十——这五个维度构成了一个学生的完整课堂画像。做这个项目的初衷很简单：把成绩从教务系统干瘪的数字变成一个有交互、能排序、可互动的视觉工具，顺便交一份漂亮的期末设计报告。</p>
  </div>

  <div class="pullquote">
    <p>"代码不应该只是考试工具，它应该能把你身边真实的数据变成有用的东西。"</p>
  </div>
</div>

<!-- ====== 02 三甲领奖台 ====== -->
<div class="section">
  <div class="section-intro">
    <div class="section-number">二</div>
    <h2 class="section-heading">三甲<em>领奖台</em></h2>
  </div>
  <div class="divider"></div>

  <div class="podium">
    <div class="podium-card silver">
      <div class="podium-medal">2</div>
      <div class="podium-name">''' + top2['学生姓名'] + '''</div>
      <div class="podium-score">''' + str(top2['综合成绩']) + ''' <small>分</small></div>
      <div class="podium-detail">
        <span>讨论 ''' + str(top2['讨论']) + '''</span><span>作业 ''' + str(top2['作业']) + '''</span>
        <span>签到 ''' + str(top2['签到']) + '''</span><span>积分 ''' + str(top2['课程积分']) + '''</span><span>PBL ''' + str(top2['PBL']) + '''</span>
      </div>
    </div>
    <div class="podium-card gold">
      <div class="podium-medal">1</div>
      <div class="podium-name">''' + top1['学生姓名'] + '''</div>
      <div class="podium-score">''' + str(top1['综合成绩']) + ''' <small>分</small></div>
      <div class="podium-detail">
        <span>讨论 ''' + str(top1['讨论']) + '''</span><span>作业 ''' + str(top1['作业']) + '''</span>
        <span>签到 ''' + str(top1['签到']) + '''</span><span>积分 ''' + str(top1['课程积分']) + '''</span><span>PBL ''' + str(top1['PBL']) + '''</span>
      </div>
    </div>
    <div class="podium-card bronze">
      <div class="podium-medal">3</div>
      <div class="podium-name">''' + top3['学生姓名'] + '''</div>
      <div class="podium-score">''' + str(top3['综合成绩']) + ''' <small>分</small></div>
      <div class="podium-detail">
        <span>讨论 ''' + str(top3['讨论']) + '''</span><span>作业 ''' + str(top3['作业']) + '''</span>
        <span>签到 ''' + str(top3['签到']) + '''</span><span>积分 ''' + str(top3['课程积分']) + '''</span><span>PBL ''' + str(top3['PBL']) + '''</span>
      </div>
    </div>
  </div>

  <div class="highlight-box">
    <p>全班共 ''' + str(len(data)) + ''' 名同学，<strong>平均分 ''' + str(avg) + '''</strong>，最高分 ''' + str(mx) + '''，超过半数同学达到 90 分以上，整体成绩水平优良。</p>
  </div>
</div>

<!-- ====== 03 成绩分布 ====== -->
<div class="section">
  <div class="section-intro">
    <div class="section-number">三</div>
    <h2 class="section-heading">成绩<em>分布</em></h2>
  </div>
  <div class="divider"></div>
  <div class="prose">
    <p>把全班 56 名同学的综合成绩按照不及格、六十分段、七十分段、八十分段和九十分以上五个区间统计，可以清晰地看到全班成绩的整体结构。大多数同学集中在优秀线附近，峰值落在 90 分以上区间，说明创新班整体学风优良。</p>
  </div>
  <div class="figure">
    <img src="data:image/png;base64,''' + img_dist + '''" alt="成绩分布图">
    <div class="figcaption">图一：全班综合成绩五区间分布统计</div>
  </div>
</div>

<!-- ====== 04 TOP 10 ====== -->
<div class="section">
  <div class="section-intro">
    <div class="section-number">四</div>
    <h2 class="section-heading">TOP <em>10</em> 排行榜</h2>
  </div>
  <div class="divider"></div>
  <div class="prose">
    <p>下面是综合成绩排名前十的同学。金色柱子代表 95 分以上的顶尖选手，绿色代表 90 分以上的优秀选手。可以看到头部竞争非常激烈，前三名之间的分差不到两分，前五名之间的分差也在五分之內。</p>
  </div>
  <div class="figure">
    <img src="data:image/png;base64,''' + img_top10 + '''" alt="TOP10排名">
    <div class="figcaption">图二：综合成绩前十排名</div>
  </div>
</div>

<!-- ====== 05 满分达成率 ====== -->
<div class="section">
  <div class="section-intro">
    <div class="section-number">五</div>
    <h2 class="section-heading">五项<em>满分率</em></h2>
  </div>
  <div class="divider"></div>
  <div class="prose">
    <p>下面这张图展示了讨论、作业、签到、课程积分和 PBL 五个模块各自的满分达成率。从数据可以看出，签到是全班表现最均匀的模块，几乎所有人拿到了满分；作业和 PBL 也保持了较高的满分比例；讨论和课程积分则呈现出更大的区分度，是拉开总分差距的关键环节。</p>
  </div>
  <div class="figure">
    <img src="data:image/png;base64,''' + img_full + '''" alt="满分达成率">
    <div class="figcaption">图三：五项成绩满分达成率对比</div>
  </div>
</div>

<!-- ====== 06 系统功能 ====== -->
<div class="section">
  <div class="section-intro">
    <div class="section-number">六</div>
    <h2 class="section-heading">系统功能<em>一览</em></h2>
  </div>
  <div class="divider"></div>
  <div class="prose">
    <p>打开系统首页，你会发现五个核心数据指标被放在了醒目的位置——平均分、最高分、90 分以上人数、不及格人数和接近满分人数。紧接着是三甲领奖台，以领奖台的方式展示了金银铜三位的姓名、分数和所有小分。再往下是两张可视化图表：一张是按成绩分段的分布柱状图，另一张是讨论、作业、签到、课程积分和 PBL 五项各自满分率的横向柱状图。</p>
    <p>排名表格是整个系统的信息核心。56 名同学按综合成绩降序排列，每一列都可以点击排序——你想看谁签到最好，点一下签到列；想看 PBL 排名，点一下 PBL 列。搜索框支持按姓名或学号实时过滤。点击任意一行，该同学的详细成绩卡片会展开，用五条彩色进度条分别展示对应项的得分进度。</p>
  </div>

  <div class="pullquote">
    <p>"完全使用原生 HTML、CSS 和 JavaScript 构建，无 React、无 Vue、无 Webpack，连 npm install 都省了。"</p>
  </div>
</div>

<!-- ====== 07 技术小结 ====== -->
<div class="section">
  <div class="section-intro">
    <div class="section-number">七</div>
    <h2 class="section-heading">技术<em>小结</em></h2>
  </div>
  <div class="divider"></div>
  <div class="prose">
    <p>整个项目遵循了极简主义的工程原则。HTML 负责骨架，CSS 用原生变量实现了一套暗色主题的视觉体系，JS 完成了从数据加载、统计计算、图表渲染到搜索排序的全部交互逻辑。图表部分借用了 Chart.js 的 CDN 资源，所有样式通过 CSS Grid 和 Flexbox 实现响应式布局，手机端也能流畅访问。</p>
    <p>部署方面选择 GitHub Pages，完全免费。把代码推送到仓库之后，在 Settings 中开启 Pages 功能，选择 main 分支，等待一两分钟就能获得一个公网可访问的链接。不需要服务器、不需要域名、不需要任何费用。对于课程作业展示来说，这几乎是最理想的交付方式。</p>
  </div>
</div>

<!-- ====== CTA ====== -->
<div class="cta">
  <div class="cta-heading">项目链接</div>
  <div class="cta-links">
    <a class="cta-btn primary" href="https://github.com/MDgua-ui/huashang_grade_system" target="_blank">
      GitHub 仓库
    </a>
    <a class="cta-btn secondary" href="https://MDgua-ui.github.io/huashang_grade_system" target="_blank">
      在线演示
    </a>
  </div>
  <span class="cta-url">https://github.com/MDgua-ui/huashang_grade_system</span>
  <span class="cta-url">https://MDgua-ui.github.io/huashang_grade_system</span>
</div>

<div class="footer">
  <p>广州华商学院 · 23 本计算机科学与技术（创新实验班） · 2026 年 7 月</p>
</div>

</body>
</html>'''

with open('e:/作业2/计算机前沿技术/huashang_grade_system/推文.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'推文已生成: 推文.html, 大小约 {len(html)//1024} KB')
