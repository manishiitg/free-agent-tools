/* Catalog text is rendered as data, never as HTML. No account credentials are used. */
'use strict';
const $ = id => document.getElementById(id);
const names = {recurring: 'Recurring free tier', trial: 'One-time trial', grant: 'Conditional grant', open_source: 'Open source', paid: 'Paid API', unconfirmed: 'Unconfirmed offer'};
const state = {category: '', page: 0, data: null};
const pageSize = 20;
function node(tag, text, className) {
  const el = document.createElement(tag);
  if (text !== undefined) el.textContent = text;
  if (className) el.className = className;
  return el;
}
function link(text, href) {
  const a = node('a', text);
  if (new URL(href, location.href).protocol !== 'https:') throw new Error('Invalid source URL');
  a.href = href; a.target = '_blank'; a.rel = 'noopener noreferrer'; return a;
}
function status(p) {
  const age = p.last_verified ? Math.floor((Date.now() - Date.parse(p.last_verified + 'T00:00:00Z')) / 86400000) : null;
  return p.status === 'verified' && age > state.data.freshness_days ? 'stale' : p.status;
}
function categoryName(id) { return state.data.categories.find(c => c.id === id)?.name || id; }
function card(p) {
  const article = node('article', undefined, 'provider'); article.dataset.provider = p.id;
  const top = node('div', undefined, 'card-top'); const title = node('div');
  title.append(node('h3', p.name), node('p', p.categories.map(categoryName).join(' · '), 'category-names'));
  const badges = node('div', undefined, 'badges'); badges.append(node('span', names[p.offer.kind], 'badge ' + p.offer.kind));
  const effective = status(p);
  if (effective !== 'verified') badges.append(node('span', effective === 'stale' ? 'Review overdue' : 'Needs review', 'badge ' + effective));
  if (p.mcp.support === 'official' || p.mcp.support === 'community') badges.append(node('span', p.mcp.support === 'official' ? 'Official MCP' : 'Community MCP', 'badge mcp'));
  top.append(title, badges); article.append(top, node('p', p.offer.summary, 'allowance'));
  const details = node('details'); details.append(node('summary', 'Conditions & eligibility'));
  const ul = node('ul'); p.offer.conditions.forEach(c => ul.append(node('li', c))); details.append(ul); article.append(details);
  const bottom = node('div', undefined, 'card-bottom'); const sources = node('div', undefined, 'source-links');
  p.sources.forEach((source, i) => sources.append(link(i === 0 ? 'Official source ↗' : 'More evidence ↗', source.url)));
  if (p.mcp.setup_url) sources.append(link('MCP setup ↗', p.mcp.setup_url));
  bottom.append(sources, node('span', p.last_verified ? 'Verified ' + p.last_verified : 'Reviewed ' + p.last_reviewed, 'date')); article.append(bottom);
  if (p.mcp.agentworks_connector) article.append(node('p', 'AgentWorks catalog name: ' + p.mcp.agentworks_connector + ' · Requires separate setup', 'integration'));
  return article;
}
function render() {
  if (!state.data) return;
  const terms = ($('search').value.toLowerCase().match(/[a-z0-9]+/g) || []);
  const matches = state.data.providers.filter(p => {
    const haystack = [p.name, p.description, ...p.categories, ...p.capabilities, p.offer.summary].join(' ').toLowerCase();
    return (!state.category || p.categories.includes(state.category)) && (!$('offer').value || p.offer.kind === $('offer').value) &&
      (!$('free-only').checked || ['recurring','trial','grant','open_source'].includes(p.offer.kind)) &&
      (!$('mcp-only').checked || ['official','community'].includes(p.mcp.support)) &&
      (!$('verified-only').checked || status(p) === 'verified') && terms.every(t => haystack.includes(t));
  }).sort((a,b) => (status(a) !== 'verified') - (status(b) !== 'verified') || a.name.localeCompare(b.name));
  state.page = Math.min(state.page, Math.max(0, Math.ceil(matches.length / pageSize) - 1));
  $('providers').replaceChildren(...matches.slice(state.page * pageSize, (state.page + 1) * pageSize).map(card));
  if (!matches.length) {
    const empty = node('div', undefined, 'empty'); empty.append(node('h3', 'No matching tools'), node('p', 'Try a broader capability or reset the filters.')); $('providers').append(empty);
  }
  $('result-title').textContent = state.category ? categoryName(state.category) : 'All capabilities';
  $('result-count').textContent = matches.length + ' provider' + (matches.length === 1 ? '' : 's');
  $('previous').disabled = state.page === 0; $('next').disabled = (state.page + 1) * pageSize >= matches.length;
  $('pagination').hidden = matches.length <= pageSize;
  $('page-number').textContent = 'Page ' + (state.page + 1) + ' of ' + Math.max(1, Math.ceil(matches.length / pageSize));
  document.querySelectorAll('.category').forEach(b => { const selected = b.dataset.id === state.category; b.classList.toggle('active', selected); b.setAttribute('aria-pressed', String(selected)); });
  $('category-mobile').value = state.category;
  const params = new URLSearchParams(); if (state.category) params.set('category', state.category); if ($('search').value) params.set('q', $('search').value);
  if ($('offer').value) params.set('offer', $('offer').value);
  ['free-only', 'mcp-only', 'verified-only'].forEach(id => { if ($(id).checked) params.set(id, '1'); });
  history.replaceState(null, '', location.pathname + (params.size ? '?' + params : '') + location.hash);
}
function filter() { state.page = 0; render(); }
function restore() {
  const params = new URLSearchParams(location.search);
  state.category = state.data.categories.some(c => c.id === params.get('category')) ? params.get('category') : '';
  $('search').value = params.get('q') || '';
  $('offer').value = Object.hasOwn(names, params.get('offer')) ? params.get('offer') : '';
  ['free-only', 'mcp-only', 'verified-only'].forEach(id => { $(id).checked = params.get(id) === '1'; });
  filter();
}
async function main() {
  const response = await fetch('catalog.json'); if (!response.ok) throw new Error('Catalog unavailable'); state.data = await response.json();
  $('provider-count').textContent = state.data.providers.length; $('category-count').textContent = state.data.categories.length; $('snapshot-date').textContent = state.data.updated_at;
  [{id: '', name: 'All capabilities'}, ...state.data.categories].forEach(c => {
    const button = node('button', undefined, 'category'); button.type = 'button'; button.dataset.id = c.id;
    button.append(node('span', c.name), node('span', c.id ? state.data.providers.filter(p => p.categories.includes(c.id)).length : state.data.providers.length));
    button.addEventListener('click', () => { state.category = c.id; filter(); }); $('categories').append(button);
    if (c.id) { const option = node('option', c.name); option.value = c.id; $('category-mobile').append(option); }
  });
  $('category-mobile').addEventListener('change', () => { state.category = $('category-mobile').value; filter(); });
  $('search').addEventListener('input', filter); ['offer','free-only','mcp-only','verified-only'].forEach(id => $(id).addEventListener('change', filter));
  $('reset').addEventListener('click', () => { state.category = ''; $('search').value = ''; $('offer').value = ''; ['free-only','mcp-only','verified-only'].forEach(id => { $(id).checked = false; }); filter(); });
  $('previous').addEventListener('click', () => { state.page--; render(); $('result-title').scrollIntoView({block:'start'}); });
  $('next').addEventListener('click', () => { state.page++; render(); $('result-title').scrollIntoView({block:'start'}); });
  document.addEventListener('keydown', e => { if (e.key === '/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)) { e.preventDefault(); $('search').focus(); } });
  window.addEventListener('popstate', restore); restore();
}
main().catch(() => { $('result-count').textContent = 'Could not load the catalog. Use the GitHub catalog or try again.'; $('pagination').hidden = true; });
