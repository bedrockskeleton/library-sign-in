// idle.js

(function() {
  const IDLE_TIMEOUT_MS = 20000; // Time until script refocuses cursor
  const inputSelector = '#id_student_id'; // Django auto-generates this from the form

  let timeout;

  function resetTimer() {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
          const input = document.querySelector(inputSelector);
          if (input) {
              input.focus();
          }
      }, IDLE_TIMEOUT_MS);
  }

  // Checks for user activity
  ['mousemove', 'keydown', 'touchstart'].forEach(event =>
      document.addEventListener(event, resetTimer, false)
  );
  window.onload = resetTimer;
})();
