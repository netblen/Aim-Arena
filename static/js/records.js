async function refreshBestRecords() {
  const recordTargets = document.querySelectorAll('[data-game-record]');
  if (!recordTargets.length) {
    return;
  }

  try {
    const response = await fetch('/best_scores');
    const data = await response.json();
    const records = data.records || {};

    recordTargets.forEach((target) => {
      const game = target.dataset.gameRecord;
      const record = records[game];
      const label = target.querySelector('[data-record-label]');
      const value = target.querySelector('[data-record-value]');
      const attempts = target.querySelector('[data-record-attempts]');

      if (!record) {
        return;
      }

      if (label) {
        label.textContent = record.label;
      }

      if (value) {
        value.textContent = record.display || 'No record yet';
      }

      if (attempts) {
        attempts.textContent = record.attempts
          ? `${record.attempts} recorded run${record.attempts === 1 ? '' : 's'}`
          : 'Play one round to set it';
      }
    });
  } catch (error) {
    console.error('Could not load best records:', error);
  }
}

window.refreshBestRecords = refreshBestRecords;
document.addEventListener('DOMContentLoaded', refreshBestRecords);
