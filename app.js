// Minimal landing page behavior using localStorage (works in any browser)
// Keys: 'quickLinks' and 'theme' (values: 'dark'|'light')

const DEFAULT_LINKS = [
  { title: 'GitHub', url: 'https://github.com' },
  { title: 'Mail', url: 'https://mail.google.com' },
  { title: 'Docs', url: 'https://developer.mozilla.org' }
];

const LS_LINKS = 'quickLinks';
const LS_THEME = 'theme';

function $(id){return document.getElementById(id)}

// THEME
function applyTheme(theme){
  if(theme === 'light'){
    document.documentElement.classList.add('light');
    $('themeSwitch').checked = true;
    $('themeLabel').textContent = 'Light';
  } else {
    document.documentElement.classList.remove('light');
    $('themeSwitch').checked = false;
    $('themeLabel').textContent = 'Dark';
  }
  localStorage.setItem(LS_THEME, theme);
}

// default to dark unless user previously chose
const storedTheme = localStorage.getItem(LS_THEME) || 'dark';
applyTheme(storedTheme);

$('themeSwitch').addEventListener('change', (e) => {
  applyTheme(e.target.checked ? 'light' : 'dark');
});

// CLOCK
function updateClock(){
  const now = new Date();
  const hh = String(now.getHours()).padStart(2,'0');
  const mm = String(now.getMinutes()).padStart(2,'0');
  const ss = String(now.getSeconds()).padStart(2,'0');
  $('clock').textContent = `${hh}:${mm}:${ss}`;
}
updateClock();
setInterval(updateClock, 1000);

// QUICK LINKS
function loadLinks(){
  try{
    const raw = localStorage.getItem(LS_LINKS);
    return raw ? JSON.parse(raw) : DEFAULT_LINKS;
  }catch(e){
    return DEFAULT_LINKS;
  }
}

function saveLinks(arr){
  localStorage.setItem(LS_LINKS, JSON.stringify(arr));
  renderLinks();
}

function sanitizeUrl(u){
  u = u.trim();
  if(!/^https?:\/\//i.test(u)) u = 'https://' + u;
  return u;
}

function renderLinks(){
  const container = $('links');
  container.innerHTML = '';
  const links = loadLinks();
  links.forEach((l, idx) => {
    const a = document.createElement('a');
    a.className = 'link-card';
    a.href = l.url;
    a.target = '_blank';
    a.rel = 'noreferrer noopener';
    a.innerHTML = `
      <div class="meta">
        <span class="title">${escapeHtml(l.title)}</span>
        <span class="url">${escapeHtml(stripProtocol(l.url))}</span>
      </div>
    `;
    // action buttons
    const actions = document.createElement('div');
    actions.className = 'link-actions';
    const edit = document.createElement('button');
    edit.className = 'icon-btn';
    edit.textContent = 'Edit';
    edit.onclick = (ev) => { ev.preventDefault(); editLink(idx); };
    const del = document.createElement('button');
    del.className = 'icon-btn';
    del.textContent = 'Remove';
    del.onclick = (ev) => { ev.preventDefault(); removeLink(idx); };
    actions.appendChild(edit);
    actions.appendChild(del);
    a.appendChild(actions);
    container.appendChild(a);
  });
}

function editLink(i){
  const links = loadLinks();
  const cur = links[i];
  const newTitle = prompt('Edit link title', cur.title);
  if (newTitle === null) return;
  const newUrl = prompt('Edit link URL', cur.url);
  if (newUrl === null) return;
  links[i] = { title: newTitle.trim() || cur.title, url: sanitizeUrl(newUrl) };
  saveLinks(links);
}

function removeLink(i){
  const links = loadLinks();
  links.splice(i,1);
  saveLinks(links);
}

function stripProtocol(u){
  return u.replace(/^https?:\/\//,'').replace(/\/$/,'');
}

function escapeHtml(s){
  return String(s).replace(/[&<>"']/g, (m)=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[m]));
}

document.addEventListener('DOMContentLoaded', () => {
  renderLinks();

  $('addForm').addEventListener('submit', (ev) => {
    ev.preventDefault();
    const title = $('linkTitle').value.trim();
    let url = $('linkUrl').value.trim();
    if(!title || !url) return;
    url = sanitizeUrl(url);
    const links = loadLinks();
    links.push({ title, url });
    saveLinks(links);
    $('linkTitle').value = '';
    $('linkUrl').value = '';
  });

  // SEARCH: if looks like a URL, navigate; else use chosen search engine
  $('searchForm').addEventListener('submit', (ev) => {
    ev.preventDefault();
    const q = $('q').value.trim();
    if(!q) return;
    const engine = $('engine').value;
    const looksLikeUrl = /^[a-zA-Z]+:\/\//.test(q) || /^[\w-]+(\.[\w.-]+)+/.test(q);
    const target = looksLikeUrl ? (q.startsWith('http') ? q : ('https://' + q)) : (engine + encodeURIComponent(q));
    // navigate in current window/tab
    window.location.href = target;
  });

  // keyboard focus: press "/" to focus search (like many landing pages)
  document.addEventListener('keydown', (e) => {
    if(e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA'){
      e.preventDefault();
      $('q').focus();
    }
  });
});