// Immediate Theme Initialization (prevents FOUC & localStorage exceptions)
function initTheme() {
  try {
    const saved = localStorage.getItem('nb_theme') || (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeIcon(saved);
  } catch (e) {
    document.documentElement.setAttribute('data-theme', 'dark');
  }
}
function toggleTheme() {
  try {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('nb_theme', next);
    updateThemeIcon(next);
  } catch (e) {}
}
function updateThemeIcon(theme) {
  const btn = document.getElementById('portalThemeBtn');
  if (btn) btn.innerText = theme === 'dark' ? '🌙 Dark' : '☀️ Light';
}
initTheme();

// Global session state initialized safely before DOM rendering
var clientSessionToken = null;
try {
  clientSessionToken = localStorage.getItem('nb_client_token') || null;
} catch (e) {}
window.clientSessionToken = clientSessionToken;

// View switcher for Enterprise Client Space Admin Views
function switchAdminView(viewId) {
  const viewMap = {
    'client-overview': 'adminViewOverview',
    'governance': 'governance',
    'commercial-provisioner': 'commercial-provisioner',
    'swarm-governance': 'swarm-governance',
    'fleet-monitor': 'fleet-monitor'
  };

  // Update admin navigation buttons
  document.querySelectorAll('.admin-nav-btn').forEach(btn => btn.classList.remove('active'));
  if (viewId === 'client-overview') {
    document.getElementById('adminTabOverviewBtn')?.classList.add('active');
  } else if (viewId === 'governance') {
    document.getElementById('govNavBtn')?.classList.add('active');
  } else if (viewId === 'commercial-provisioner') {
    document.getElementById('commercialNavBtn')?.classList.add('active');
  } else if (viewId === 'swarm-governance') {
    document.getElementById('swarmNavBtn')?.classList.add('active');
  } else if (viewId === 'fleet-monitor') {
    document.getElementById('fleetNavBtn')?.classList.add('active');
  }

  // Hide all admin panes and show target
  document.querySelectorAll('.admin-view-pane').forEach(el => el.classList.remove('active'));
  const targetId = viewMap[viewId] || viewId;
  const target = document.getElementById(targetId);
  if (target) {
    target.classList.add('active');
  }

  // Trigger loaders if available
  if (viewId === 'governance') {
    if (typeof loadGovernanceTab === 'function') loadGovernanceTab();
  } else if (viewId === 'commercial-provisioner') {
    if (typeof loadCommercialTab === 'function') loadCommercialTab();
  } else if (viewId === 'swarm-governance') {
    if (typeof loadSwarmTab === 'function') loadSwarmTab();
  } else if (viewId === 'fleet-monitor') {
    if (typeof loadFleetTab === 'function') loadFleetTab();
  } else if (viewId === 'client-overview') {
    if (typeof loadClientData === 'function') loadClientData();
  }
}
window.switchAdminView = switchAdminView;

// Sub-tab switcher for Economics section
window.showEconomicsSubtab = function(subtabId) {
  const container = document.getElementById('economics');
  if (!container) return;
  container.querySelectorAll('.econ-subtab-pane').forEach(el => { el.style.display = 'none'; el.classList.remove('active'); });
  container.querySelectorAll('.econ-subtab-btn').forEach(btn => btn.classList.remove('active'));
  const target = container.querySelector(`[data-econ-subtab="${subtabId}"]`);
  if (target) {
    target.style.display = 'block';
    target.classList.add('active');
    container.querySelector(`[data-econ-btn="${subtabId}"]`)?.classList.add('active');
  }
  if (subtabId === 'econ-roi' && typeof recalcRoi === 'function') recalcRoi();
  if (subtabId === 'econ-pricing' && typeof calculateCeilings === 'function') calculateCeilings();
};

// Sub-tab switcher for Interactive Lab section
window.showLabSubtab = function(subtabId) {
  const container = document.getElementById('lab');
  if (!container) return;
  container.querySelectorAll('.lab-subtab-pane').forEach(el => { el.style.display = 'none'; el.classList.remove('active'); });
  container.querySelectorAll('.lab-subtab-btn').forEach(btn => btn.classList.remove('active'));
  const target = container.querySelector(`[data-lab-subtab="${subtabId}"]`);
  if (target) {
    target.style.display = 'block';
    target.classList.add('active');
    container.querySelector(`[data-lab-btn="${subtabId}"]`)?.classList.add('active');
  }
};

// Sub-tab switcher for Resources section
window.showResourceSubtab = function(subtabId) {
  const container = document.getElementById('resources');
  if (!container) return;
  container.querySelectorAll('.res-subtab-pane').forEach(el => { el.style.display = 'none'; el.classList.remove('active'); });
  container.querySelectorAll('.res-subtab-btn').forEach(btn => btn.classList.remove('active'));
  const target = container.querySelector(`[data-res-subtab="${subtabId}"]`);
  if (target) {
    target.style.display = 'block';
    target.classList.add('active');
    container.querySelector(`[data-res-btn="${subtabId}"]`)?.classList.add('active');
  }
  if (subtabId === 'res-reports' && typeof fetchPortalTokenSavings === 'function') fetchPortalTokenSavings();
  if (subtabId === 'res-observability' && typeof fetchOtelSpans === 'function') fetchOtelSpans();
  if (subtabId === 'res-swarm' && typeof loadSwarmFleetTelemetry === 'function') loadSwarmFleetTelemetry();
};

// Main Tab Routing - hoisted and attached to window so header buttons never fail with ReferenceError
function showTab(id) {
  if (!id) return;

  // 1. Enterprise Client Space subviews
  const adminTabs = ['governance', 'commercial-provisioner', 'swarm-governance', 'fleet-monitor', 'client-overview'];
  if (adminTabs.includes(id)) {
    showTab('client');
    if (!window.clientSessionToken) {
      if (typeof loginClient === 'function') loginClient(true);
    }
    switchAdminView(id);
    return;
  }

  // 2. Interactive Lab subtabs
  if (id === 'gateway' || id === 'sandboxes') {
    showTab('lab');
    window.showLabSubtab(id === 'gateway' ? 'lab-gateway' : 'lab-sandbox');
    return;
  }

  // 3. Economics subtabs
  if (id === 'roi-calculator') {
    showTab('economics');
    window.showEconomicsSubtab('econ-roi');
    if (typeof recalcRoi === 'function') recalcRoi();
    return;
  }
  if (id === 'tier-matrix' || id === 'pricing') {
    showTab('economics');
    window.showEconomicsSubtab('econ-pricing');
    if (typeof calculateCeilings === 'function') calculateCeilings();
    return;
  }
  if (id === 'infrastructure') {
    showTab('economics');
    window.showEconomicsSubtab('econ-infra');
    return;
  }

  // 4. Resources subtabs
  const resTabs = {
    'docs': 'res-docs',
    'reports': 'res-reports',
    'observability': 'res-observability',
    'swarm-fleet': 'res-swarm'
  };
  if (resTabs[id]) {
    showTab('resources');
    window.showResourceSubtab(resTabs[id]);
    return;
  }

  // Top-level tab switching
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
  const target = document.getElementById(id);
  if (target) {
    target.classList.add('active');
  }

  // Highlight matching nav button
  document.querySelectorAll('.nav-btn').forEach(btn => {
    const oc = btn.getAttribute('onclick') || '';
    if (oc.includes("'" + id + "'") || oc.includes('"' + id + '"')) {
      btn.classList.add('active');
    }
  });

  // Update URL hash for deep linking and back/forward browser navigation
  if (window.location.hash !== '#' + id) {
    try {
      history.replaceState ? history.replaceState(null, null, '#' + id) : location.hash = '#' + id;
    } catch (e) {}
  }

  // Smooth scroll to top on tab switch
  try {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } catch (e) {}

  // Tab-specific live data activations
  if (id === 'economics') {
    if (typeof recalcRoi === 'function') recalcRoi();
    if (typeof calculateCeilings === 'function') calculateCeilings();
  } else if (id === 'client') {
    if (typeof checkClientSession === 'function') checkClientSession();
  }
}
window.showTab = showTab;

// Auto-navigate on initial page load if hash exists
if (typeof window !== 'undefined') {
  window.addEventListener('DOMContentLoaded', function() {
    const hash = (window.location.hash || '').replace('#', '');
    if (hash) {
      showTab(hash);
    }
  });
}
