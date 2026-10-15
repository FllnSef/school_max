
let currentAuthMode = 'login';
let pendingEmail = '';


function toggleElement(id, show) {
    const el = document.getElementById(id);
    if (el) {
        if (show) el.classList.remove('hidden');
        else el.classList.add('hidden');
    }
}

function switchAuthMode(mode) {
    currentAuthMode = mode;
    
   
    toggleElement('authMainForm', true);
    toggleElement('verifyCodeGroup', false);

    const btnLogin = document.getElementById('btnModeLogin');
    const btnReg = document.getElementById('btnModeRegister');
    const regGroup = document.getElementById('registerFieldsGroup');
    const submitBtn = document.getElementById('btnAuthSubmit');
    const lblEmail = document.getElementById('lblEmailUsername');

    if (mode === 'register') {
        if (btnLogin) btnLogin.classList.remove('active');
        if (btnReg) btnReg.classList.add('active');
        if (regGroup) regGroup.classList.remove('hidden');
        if (submitBtn) submitBtn.textContent = 'Зарегистрироваться';
        if (lblEmail) lblEmail.textContent = 'Электронная почта';
    } else {
        if (btnReg) btnReg.classList.remove('active');
        if (btnLogin) btnLogin.classList.add('active');
        if (regGroup) regGroup.classList.add('hidden');
        if (submitBtn) submitBtn.textContent = 'Войти';
        if (lblEmail) lblEmail.textContent = 'Почта или логин';
    }
}

async function handleAuthSubmit(e) {
    if (e) e.preventDefault();

    const email = document.getElementById('authEmailInput').value.trim();
    const password = document.getElementById('authPasswordInput').value;
    const btn = document.getElementById('btnAuthSubmit');

    if (!email || !password) {
        alert('Заполните почту и пароль');
        return;
    }

    btn.disabled = true;
    btn.textContent = currentAuthMode === 'register' ? 'Отправка...' : 'Вход...';

    try {
        if (currentAuthMode === 'register') {
            const firstName = document.getElementById('regFirstName').value.trim();
            const lastName = document.getElementById('regLastName').value.trim();
            const grade = document.getElementById('regGrade').value;

            const res = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email, password, first_name: firstName, last_name: lastName, grade
                })
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || 'Ошибка регистрации');

            
            pendingEmail = email;
            toggleElement('authMainForm', false);
            toggleElement('verifyCodeGroup', true);
            
            const notice = document.getElementById('verifyNoticeText');
            if (notice) notice.textContent = `Код отправлен на ${email}. Проверьте почту или консоль сервера.`;

        } else {
            
            const res = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || 'Неверные данные');

            applyUserSession(data.user);
        }
    } catch (err) {
        alert(err.message);
    } finally {
        btn.disabled = false;
        btn.textContent = currentAuthMode === 'register' ? 'Зарегистрироваться' : 'Войти';
    }
}

async function handleVerifyCodeSubmit() {
    const code = document.getElementById('inputVerifyCode').value.trim();
    const btn = document.querySelector('#verifyCodeGroup button');

    if (!code || code.length !== 6) {
        alert('Введите 6 цифр кода');
        return;
    }

    try {
        const res = await fetch('/api/auth/verify-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: pendingEmail, code: code })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Неверный код');

        alert('Почта подтверждена! Теперь войдите.');
        switchAuthMode('login');
    } catch (err) {
        alert(err.message);
    }
}

function applyUserSession(user) {
    localStorage.setItem('sferum_user', JSON.stringify(user));
    location.reload(); // Перезагружаем для обновления интерфейса
}

function handleLogout() {
    localStorage.removeItem('sferum_user');
    location.reload();
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('authMainForm');
    if (form) form.onsubmit = handleAuthSubmit;

    const user = localStorage.getItem('sferum_user');
    if (user) {
        const u = JSON.parse(user);
        document.getElementById('authBox')?.classList.add('hidden');
        document.getElementById('userProfileBox')?.classList.remove('hidden');
        document.getElementById('profileDashboardName').textContent = `${u.last_name} ${u.first_name}`;
    }
});
