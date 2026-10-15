document.addEventListener('DOMContentLoaded', loadCanteenMenu);

async function loadCanteenMenu() {
    const listEl = document.getElementById('canteenMenuList');
    const todayStr = new Date().toISOString().split('T')[0];

    try {
        const menu = await API.getMenu(todayStr);

        if (!menu || menu.length === 0) {
            listEl.innerHTML = `
                <div class="card">
                    <h4>🥣 Комплексный обед</h4>
                    <p style="color: var(--text-muted); margin-top:4px;">Суп куриный с лапшой, котлета мясная с пюре, компот из сухофруктов.</p>
                    <button class="btn-primary" style="margin-top:12px;" onclick="bookMealDemo('обед')">Записаться на обед (Демо)</button>
                </div>`;
            return;
        }

        listEl.innerHTML = menu.map(item => `
            <div class="card">
                <span class="tag" style="color:#38bdf8">${item.meal_type.toUpperCase()}</span>
                <h4 style="margin-top:6px;">${item.dish_name}</h4>
                <p style="font-size:0.8rem; color:var(--text-muted); margin-top:4px;">${item.description || ''}</p>
                <button class="btn-primary" style="margin-top:10px;" onclick="bookMealDemo('${item.meal_type}')">Записаться</button>
            </div>
        `).join('');

    } catch (err) {
        listEl.innerHTML = '<div class="card"><p style="color:var(--red)">Ошибка загрузки меню</p></div>';
    }
}

async function bookMealDemo(mealType) {
    if (!currentUser) return;
    const todayStr = new Date().toISOString().split('T')[0];

    try {
        await API.bookMeal({
            user_id: currentUser.id,
            booking_date: todayStr,
            meal_type: mealType
        });
        alert(`Вы успешно записались на ${mealType}! 🍏`);
    } catch (err) {
        alert(err.message);
    }
}
