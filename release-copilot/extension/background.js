// Clicking the toolbar icon opens the side panel with the release package.
chrome.runtime.onInstalled.addListener(() => {
  chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true }).catch(() => {});
});
chrome.runtime.onStartup.addListener(() => {
  chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true }).catch(() => {});
});
// The on-page button can ask to open the panel
chrome.runtime.onMessage.addListener((msg, sender) => {
  if (msg && msg.type === 'openPanel' && sender.tab) chrome.sidePanel.open({ tabId: sender.tab.id }).catch(() => {});
});
