
const API_BASE = '/api';

const API = {
    
    async login(userData) {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        return await res.json();
    },

    
    async getSchedule(dayId) {
        const res = await fetch(`${API_BASE}/schedule/${dayId}`);
        return await res.json();
    },

   
    async getTasks() {
        const res = await fetch(`${API_BASE}/tasks`);
        return await res.json();
    },

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

   
    async toggleTask(taskId) {
        const res = await fetch(`${API_BASE}/tasks/${taskId}/toggle`, {
            method: 'PATCH'
        });
        return await res.json();
    },

    
    async getMenu(dateStr) {
        const res = await fetch(`${API_BASE}/menu/day/${dateStr}`);
        return await res.json();
    },

    
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
