chrome.runtime.onInstalled.addListener(() => {
  console.log('YT-DLP Extension installed');
});

chrome.action.onClicked.addListener((tab) => {
  chrome.tabs.sendMessage(tab.id, {action: "download"});
});
