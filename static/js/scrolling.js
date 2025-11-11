document.addEventListener('DOMContentLoaded', () => {
    const statues = document.querySelectorAll('.statue');

    function animateStatues() {
        const windowHeight = window.innerHeight;

        statues.forEach((statue, index) => {
            const rect = statue.getBoundingClientRect();
            const speed = parseFloat(statue.dataset.speed);

            if (rect.top < windowHeight && rect.bottom > 0) {
                const visibleRatio = 1 - rect.top / windowHeight; // относительная видимость эл-та на экране

                const scale = 0.5 + visibleRatio * 0.5 * speed;
                const translateY = 100 - visibleRatio * 100 * speed;

                const rotate = (visibleRatio * 15 * (index % 2 === 0 ? 1 : -1)).toFixed(2); // чередование направления
                const translateX = (visibleRatio * 20 * (index % 2 === 0 ? 1 : -1)).toFixed(2);

                statue.style.transform = `scale(${scale}) translateY(${translateY}px) translateX(${translateX}px) rotate(${rotate}deg)`;
                statue.style.opacity = Math.min(1, visibleRatio + 0.2);
            } else { // обратный скролл
                statue.style.transform = 'scale(0.5) translateY(100px) translateX(0px) rotate(0deg)';
                statue.style.opacity = 0;
            }
        });

        requestAnimationFrame(animateStatues);
    }

    animateStatues();
});
