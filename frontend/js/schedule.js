document.addEventListener('DOMContentLoaded', () => {
    // Навешиваем клики на кнопки дней недели (ПН-ПТ)
    const dayBtns = document.querySelectorAll('.day-btn');
    dayBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            dayBtns.forEach(b => b.classList.remove('active'));
            e.currentTarget.classList.add('active');
            
            const dayId = parseInt(e.currentTarget.dataset.day);
            loadSchedule(dayId);
        });
    });

    // По умолчанию загружаем Понедельник (1)
    loadSchedule(1);
});

async function loadSchedule(dayId) {
    const listEl = document.getElementById('scheduleList');
    listEl.innerHTML = '<div class="card"><p>Загрузка расписания...</p></div>';

    try {
        const schedule = await API.getSchedule(dayId);
        
        if (!schedule || schedule.length === 0) {
            listEl.innerHTML = `
                <div class="card">
                    <p style="color: var(--text-muted); text-align: center;">В этот день уроков и консультаций нет 🎉</p>
                </div>`;
            return;
        }

        listEl.innerHTML = schedule.map(item => `
            <div class="card item-card">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div class="item-num">${item.lesson_number || '•'}</div>
                    <div class="item-main">
                        <h4>${item.subject}</h4>
                        <div class="item-sub">${item.teacher_name} · каб. ${item.classroom}</div>
                        ${item.material_link ? `
                            <a href="${item.material_link}" target="_blank" style="font-size:0.75rem; color:#c084fc; text-decoration:none; display:inline-block; margin-top:4px;">
                                📁 ${item.material_title || 'Скачать материалы урока'}
                            </a>
                        ` : ''}
                    </div>
                </div>
                <div class="tag">${item.start_time} - ${item.end_time}</div>
            </div>
        `).join('');

    } catch (err) {
        listEl.innerHTML = '<div class="card"><p style="color:var(--red)">Ошибка загрузки расписания</p></div>';
    }
}
