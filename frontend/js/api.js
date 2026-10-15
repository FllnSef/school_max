// Базовый URL нашего бэкенда
const API_BASE = '/api';

const API = {
    // 1. АВТОРИЗАЦИЯ / ВХОД
    async login(userData) {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        return await res.json();
    },

    // 2. ПОЛУЧЕНИЕ РАСПИСАНИЯ НА ДЕНЬ (1-7)
    async getSchedule(dayId) {
        const res = await fetch(`${API_BASE}/schedule/${dayId}`);
        return await res.json();
    },

    // 3. ПОЛУЧЕНИЕ ВСЕХ ЗАДАЧ И ДЕДЛАЙНОВ
    async getTasks() {
        const res = await fetch(`${API_BASE}/tasks`);
        return await res.json();
    },

    // 4. СОЗДАНИЕ НОВОЙ ЗАДАЧИ (Учителем)
    async createTask(taskData) {
        const res = await fetch(`${API_BASE}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskData)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Ошибка создания задачи');
        }
        return await res.json();
    },

    // 5. ИЗМЕНЕНИЕ СТАТУСА ЗАДАЧИ (Выполнено/Не выполнено)
    async toggleTask(taskId) {
        const res = await fetch(`${API_BASE}/tasks/${taskId}/toggle`, {
            method: 'PATCH'
        });
        return await res.json();
    },

    // 6. ПОЛУЧЕНИЕ МЕНЮ СТОЛОВОЙ НА ДАТУ (YYYY-MM-DD)
    async getMenu(dateStr) {
        const res = await fetch(`${API_BASE}/menu/day/${dateStr}`);
        return await res.json();
    },

    // 7. ЗАПИСЬ НА ПИТАНИЕ
    async bookMeal(bookingData) {
        const res = await fetch(`${API_BASE}/menu/book`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bookingData)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Ошибка записи на питание');
        }
        return await res.json();
    }
};
