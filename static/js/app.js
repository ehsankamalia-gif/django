document.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('app');
    if (!el || typeof Vue === 'undefined') return;

    Vue.createApp({
        data() {
            return { count: 0 };
        },
    }).mount('#app');
});
