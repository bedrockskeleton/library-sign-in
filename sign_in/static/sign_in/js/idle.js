(function() {
    const IDLE_TIMEOUT_MS = 5000; // 5 seconds
    const inputSelector = '#id_student_id'; // Django auto-generates this from the form

    let timeout;

    function resetTimer() {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            focus();
        }, IDLE_TIMEOUT_MS);
    }
    
    function focus() {
        const input = document.querySelector(inputSelector);
            if (input) {
                input.value = "";
                input.focus();
            }
    }

    // Monitor user activity
    ['mousemove', 'keydown', 'touchstart'].forEach(event =>
        document.addEventListener(event, resetTimer, false)
    );

    // Initial trigger
    window.onload = resetTimer;
    focus();
})();