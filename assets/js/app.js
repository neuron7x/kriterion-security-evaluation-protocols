function qs(sel, root=document){ return root.querySelector(sel); }
function qsa(sel, root=document){ return Array.from(root.querySelectorAll(sel)); }

function renderBadgeRow(targetId){
  const host = document.getElementById(targetId);
  if (!host || !window.REPO_DATA) return;
  host.innerHTML = window.REPO_DATA.badges.map(b => `<span class="pill">${b}</span>`).join("");
}

function renderFlow(targetId){
  const host = document.getElementById(targetId);
  if (!host || !window.REPO_DATA) return;
  host.innerHTML = window.REPO_DATA.architectureFlow.map((step, idx) => `
    <div class="node reveal">
      <span>${String(idx + 1).padStart(2, "0")} · ${step}</span>
      <span>phase</span>
    </div>
  `).join("");
}

function renderProtocols(targetId, filter=""){
  const host = document.getElementById(targetId);
  if (!host || !window.REPO_DATA) return;
  const q = filter.trim().toLowerCase();
  const list = window.REPO_DATA.protocols.filter(item => {
    const text = `${item.title} ${item.level} ${item.focus}`.toLowerCase();
    return !q || text.includes(q);
  });
  host.innerHTML = list.map(item => `
    <article class="protocol-item reveal">
      <div class="top">
        <div>
          <div class="id">${item.id}</div>
          <h3>${item.title}</h3>
          <p class="meta">${item.level}</p>
        </div>
        <a class="btn" href="${item.file}">Open file</a>
      </div>
      <p>${item.focus}</p>
    </article>
  `).join("") || `<div class="protocol-item"><p>No matching protocols.</p></div>`;
  attachReveal();
}

function renderDoctrine(targetId){
  const host = document.getElementById(targetId);
  if (!host || !window.REPO_DATA) return;
  host.innerHTML = window.REPO_DATA.doctrine.map(item => `
    <article class="card reveal">
      <span class="tag">Doctrine</span>
      <h3>${item.title}</h3>
      <p>${item.note}</p>
      <div class="actions" style="margin-top:18px">
        <a class="btn" href="${item.file}">Open document</a>
      </div>
    </article>
  `).join("");
  attachReveal();
}

function renderBars(targetId){
  const host = document.getElementById(targetId);
  if (!host || !window.REPO_DATA) return;
  host.innerHTML = window.REPO_DATA.benchmarkSummary.highlights.map(item => `
    <div class="bar reveal">
      <div class="head"><span>${item.label}</span><span>${item.value}</span></div>
      <div class="bar-track"><div class="bar-fill" style="width:${item.width}%"></div></div>
    </div>
  `).join("");
  const status = document.getElementById("benchmark-status");
  if (status) status.textContent = window.REPO_DATA.benchmarkSummary.status;
  attachReveal();
}

function attachReveal(){
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const items = qsa('.reveal');
  if (reduce){
    items.forEach(el => el.classList.add('in'));
    return;
  }
  const io = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting){
        entry.target.classList.add('in');
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  items.forEach(el => {
    if (!el.classList.contains('in')) io.observe(el);
  });
}

function markActiveNav(){
  const page = location.pathname.split('/').pop() || 'index.html';
  qsa('.nav a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === page) a.setAttribute('aria-current', 'page');
  });
}

document.addEventListener("DOMContentLoaded", () => {
  renderBadgeRow("badge-row");
  renderFlow("flow");
  renderDoctrine("doctrine-grid");
  renderProtocols("protocols");
  renderBars("bars");
  const search = document.getElementById("protocol-search");
  if (search) search.addEventListener("input", e => renderProtocols("protocols", e.target.value));
  markActiveNav();
  attachReveal();
});
