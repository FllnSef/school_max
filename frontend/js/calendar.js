document.addEventListener('DOMContentLoaded', loadTasks);

async function loadTasks() {
    const listEl = document.getElementById('tasksList');
    listEl.innerHTML = '<div class="card"><p>Загрузка задач...</p></div>';

    try {
        const tasks = await API.getTasks();

        if (!tasks || tasks.length === 0) {
            listEl.innerHTML = '<div class="card"><p style="color: var(--text-muted);">Активных задач и задолженностей нет 👍</p></div>';
            return;
        }

        listEl.innerHTML = tasks.map(task => {
            const deadlineDate = new Date(task.deadline).toLocaleString('ru-RU', {
                day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
            });

            return `
                <div class="card item-card" onclick="toggleTaskStatus(${task.id})">
                    <div class="item-main">
                        <span style="font-size:0.7rem; color:var(--purple); font-weight:700;">${task.subject.toUpperCase()}</span>
                        <h4>${task.title}</h4>
                        <div class="item-sub">${task.description || ''}</div>
                        <div class="item-sub" style="margin-top:4px;">⏰ Сдать до: <strong>${deadlineDate}</strong></div>
                    </div>
                    <span class="tag ${task.is_completed ? 'done' : 'pending'}">
                        ${task.is_completed ? '✓ Сдано' : 'К сдаче'}
                    </span>
                </div>
            `;
        }).join('');

    } catch (err) {
        listEl.innerHTML = '<div class="card"><p style="color:var(--red)">Ошибка загрузки задач</p></div>';
    }
}

async function toggleTaskStatus(taskId) {
    try {
        await API.toggleTask(taskId);
        loadTasks(); // Перерисовываем список
    } catch (err) {
        alert("Ошибка изменения статуса задачи");
    }
}

async function handleCreateTask() {
    if (!currentUser) return;

    const title = document.getElementById('taskTitle').value;
    const subject = document.getElementById('taskSubject').value;
    const desc = document.getElementById('taskDesc').value;
    const deadline = document.getElementById('taskDeadline').value;

    if (!title || !subject || !deadline) {
        alert("Заполните название, предмет и дедлайн!");
        return;
    }

    try {
        await API.createTask({
            title: title,
            subject: subject,
            description: desc,
            deadline: new Date(deadline).toISOString(),
            creator_id: currentUser.id
        });

        alert("Задача успешно опубликована!");
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskDesc').value = '';
        loadTasks();
    } catch (err) {
        alert(err.message);
    }
}
