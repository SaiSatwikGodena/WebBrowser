// Minimal behavior: clock, search, quick links stored in chrome.storage
function updateClock() {
  const el = document.getElementById('clock');
  const now = new Date();
  const hh = String(now.getHours()).padStart(2,'0');
  const mm = String(now.getMinutes()).padStart(2,'0');
  el.textContent = `${hh}:${mm}`;
}
setInterval(updateClock, 1000);
updateClock();

const defaultLinks = [
  {title:'GitHub', url:'https://github.com'},
  {title:'Mail', url:'https://mail.google.com'}
];

function renderLinks(links){
  const container = document.getElementById('links');
  container.innerHTML = '';
  (links || []).forEach(l=>{
    const a = document.createElement('a');
    a.className='link';
    a.href = l.url;
    a.textContent = l.title;
    a.target = '_blank';
    container.appendChild(a);
  });
}

// Load saved links (chrome.storage.sync where available)
const storage = (chrome && chrome.storage) ? chrome.storage : null;
if (storage && storage.sync) {
  storage.sync.get({quickLinks: defaultLinks}, (res) => {
    renderLinks(res.quickLinks);
  });
} else {
  renderLinks(defaultLinks);
}

// Search handling: if input looks like URL, go directly; otherwise Google search
document.getElementById('go').addEventListener('click', () => {
  const q = document.getElementById('q').value.trim();
  if (!q) return;
  const isUrl = /^https?:\/\//i.test(q) || /^[\w-]+\.[\w.-]+/.test(q);
  const target = isUrl ? (q.startsWith('http') ? q : 'https://' + q) : 'https://www.google.com/search?q=' + encodeURIComponent(q);
  window.location.href = target;
});