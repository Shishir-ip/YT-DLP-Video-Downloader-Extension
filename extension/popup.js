const SERVER = 'http://127.0.0.1:8765';

document.addEventListener('DOMContentLoaded', async () => {
  const urlEl = document.getElementById('url');
  const btn = document.getElementById('download-btn');
  const progress = document.getElementById('progress');
  const status = document.getElementById('status');
  const formatSel = document.getElementById('format');
  const offlineBanner = document.getElementById('server-offline');

  let currentUrl = '';
  try {
    const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
    currentUrl = tab.url || '';
    urlEl.textContent = currentUrl;
  } catch (e) {
    urlEl.textContent = 'Unable to get page URL';
  }

  let serverAlive = false;
  try {
    const r = await fetch(SERVER + '/health', {method: 'GET', mode: 'cors'});
    if (r.ok) serverAlive = true;
  } catch (e) {
    serverAlive = false;
  }

  if (!serverAlive) {
    offlineBanner.style.display = 'block';
    btn.disabled = true;
    status.textContent = 'Waiting for server...';
    status.style.color = '#ff4757';
  }

  const saved = await chrome.storage.local.get(['defaultFormat']);
  if (saved.defaultFormat) formatSel.value = saved.defaultFormat;

  document.getElementById('settings-link').addEventListener('click', (e) => {
    e.preventDefault();
    chrome.runtime.openOptionsPage();
  });

  let pollInterval = null;

  btn.addEventListener('click', async () => {
    if (btn.disabled || !currentUrl) return;

    btn.disabled = true;
    status.textContent = 'Connecting to server...';
    status.style.color = '#aaa';
    progress.style.width = '0%';

    try {
      const resp = await fetch(SERVER + '/download', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          url: currentUrl,
          format: formatSel.value
        })
      });

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.error || 'Server error ' + resp.status);
      }

      const data = await resp.json();
      const jobId = data.job_id;

      await chrome.storage.local.set({defaultFormat: formatSel.value});

      status.textContent = 'Starting download...';

      pollInterval = setInterval(async () => {
        try {
          const r = await fetch(SERVER + '/progress/' + jobId, {mode: 'cors'});
          const p = await r.json();

          progress.style.width = Math.min(p.progress || 0, 100) + '%';

          let statusText = p.status;
          if (p.progress > 0) statusText += ' | ' + p.progress.toFixed(1) + '%';
          if (p.speed && p.speed !== '-') statusText += ' | ' + p.speed;
          if (p.eta && p.eta !== '-') statusText += ' | ETA ' + p.eta;
          status.textContent = statusText;
          status.style.color = '#aaa';

          if (p.title && p.title !== '-') {
            urlEl.textContent = p.title;
            urlEl.style.color = '#fff';
          }

          if (p.status === 'Completed' || p.status === 'Error') {
            clearInterval(pollInterval);
            btn.disabled = false;
            if (p.status === 'Error') {
              status.textContent = 'Error: ' + (p.error || 'Unknown error');
              status.style.color = '#ff4757';
              progress.style.width = '0%';
            } else {
              status.textContent = 'Done! Download Complete!';
              status.style.color = '#4caf50';
              progress.style.width = '100%';
            }
          }
        } catch (pollErr) {
          console.error('Poll error', pollErr);
        }
      }, 500);

    } catch (err) {
      btn.disabled = false;
      status.textContent = 'Error: ' + err.message;
      status.style.color = '#ff4757';
      progress.style.width = '0%';
      console.error(err);
    }
  });
});
