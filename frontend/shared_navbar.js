const navbarRightHtml = `
    <style>
        .nav-btn {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            color: #6b7280;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            background: transparent;
        }
        .nav-btn:hover {
            background: #f3f4f6;
            color: #2563eb;
            transform: translateY(-1px);
        }
        .nav-btn i { font-size: 18px; }
        .short-key {
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            letter-spacing: 0.5px;
        }
        .avatar-circle {
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
        }
        .avatar-circle:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 15px rgba(37, 99, 235, 0.3);
        }
        #globalSearch:focus {
            outline: none;
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
        .profile-dropdown {
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.95) !important;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
        }
        .list-group::-webkit-scrollbar {
            width: 4px;
        }
        .list-group::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        .list-group::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 10px;
        }
        .list-group::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        .list-group-item {
            transition: background 0.2s ease;
        }
        .list-group-item:hover {
            background: #f8fafc !important;
        }
    </style>
        <div class="nav-right" style="display: flex; gap: 8px; align-items: center; position: relative;">
            <div class="search-container d-none d-md-block" style="position: relative; width: 220px;">
                <i class="fa-solid fa-search" style="position: absolute; left: 15px; top: 50%; transform: translateY(-50%); font-size: 13px; color: #94a3b8;"></i>
                <input type="text" placeholder="Search..." id="globalSearch" style="width: 100%; padding: 10px 45px 10px 40px; border-radius: 12px; border: 1.5px solid #f1f5f9; transition: all 0.3s ease; font-size: 13px; background: #f8fafc; color: #1e293b;">
                <span class="short-key" style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); font-size: 10px; color: #64748b; background: #ffffff; padding: 2px 6px; border-radius: 6px; border: 1px solid #e2e8f0; pointer-events: none; font-weight: 800; font-family: system-ui, -apple-system, sans-serif;">Ctrl K</span>
            </div>

            <div class="nav-btn" onclick="window.location.href='profile.html'"><i class="fa-solid fa-gear"></i></div>
            <div class="nav-btn position-relative" onclick="toggleMessagesDropdown(event)">
                <i class="fa-solid fa-comment-dots"></i>
                <span class="badge-notify" id="msg-badge" style="display: none; position: absolute; top: -5px; right: -5px; background: red; color: white; border-radius: 50%; padding: 2px 6px; font-size: 10px;">0</span>
            </div>
            <div class="nav-btn position-relative" onclick="toggleNotificationsDropdown(event)">
                <i class="fa-solid fa-bell"></i>
                <span class="badge-notify" id="notify-badge" style="display: none; position: absolute; top: -5px; right: -5px; background: red; color: white; border-radius: 50%; padding: 2px 6px; font-size: 10px;">0</span>
            </div>

        <div class="avatar-circle" id="userInitials" onclick="toggleDropdown(event)" style="width: 40px; height: 40px; border-radius: 50%; background: var(--primary); color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; cursor: pointer;"></div>
        </div>

        <div class="profile-dropdown shadow-lg rounded-4 p-0" id="profileDropdown" style="display: none; position: absolute; top: 70px; right: 20px; background: white; width: 220px; z-index: 2000; overflow: hidden; border: 1px solid #eee;" onclick="event.stopPropagation()">
            <div class="p-3 border-bottom bg-light">
                <div class="fw-bold profile-name text-dark" style="font-size: 14px;">...</div>
                <div class="text-muted profile-email" style="font-size: 11px;">...</div>
            </div>
            <div class="list-group list-group-flush">
                <a href="profile.html" class="list-group-item list-group-item-action border-0 py-2 d-flex align-items-center gap-2">
                    <i class="fa-solid fa-user text-muted" style="width: 20px;"></i>
                    <span style="font-size: 13px; font-weight: 500;">My Profile</span>
                </a>
                <a href="profile.html" class="list-group-item list-group-item-action border-0 py-2 d-flex align-items-center gap-2">
                    <i class="fa-solid fa-gear text-muted" style="width: 20px;"></i>
                    <span style="font-size: 13px; font-weight: 500;">Settings</span>
                </a>
                <a href="#" onclick="logout()" class="list-group-item list-group-item-action border-0 py-2 d-flex align-items-center gap-2 text-danger">
                    <i class="fa-solid fa-right-from-bracket" style="width: 20px;"></i>
                    <span style="font-size: 13px; font-weight: 600;">Logout</span>
                </a>
            </div>
        </div>

        <div class="profile-dropdown shadow-lg rounded-4 p-0" id="messagesDropdown" style="display: none; position: absolute; top: 70px; right: 100px; background: white; width: 320px; z-index: 2000; overflow: hidden; border: 1px solid #eee;" onclick="event.stopPropagation()">
            <div class="p-3 border-bottom bg-light d-flex justify-content-between align-items-center">
                <div class="fw-bold text-dark" style="font-size: 14px;">Messages</div>
                <span class="badge bg-primary rounded-pill small" id="msg-unread-count" style="display: none;">0</span>
            </div>
            <div class="list-group list-group-flush text-start" id="messagesList" style="max-height: 350px; overflow-y: auto;">
                <div class="p-5 text-center text-muted">
                    <i class="fa-solid fa-comment-slash d-block mb-3 opacity-20" style="font-size: 40px;"></i>
                    <p class="mb-0 small fw-medium">No messages yet</p>
                </div>
            </div>
            <div class="p-2 border-top d-flex justify-content-between px-3">
                <button class="btn btn-link btn-sm text-decoration-none p-0 extra-small fw-bold" onclick="markAllMessagesRead()" style="font-size: 11px;">Mark all as read</button>
                <a href="#" class="extra-small text-primary text-decoration-none fw-bold" style="font-size: 11px;">View Inbox</a>
            </div>
        </div>

        <div class="profile-dropdown shadow-lg rounded-4 p-0" id="notificationsDropdown" style="display: none; position: absolute; top: 70px; right: 60px; background: white; width: 340px; z-index: 2000; overflow: hidden; border: 1px solid #eee;" onclick="event.stopPropagation()">
            <div class="p-3 border-bottom bg-light d-flex justify-content-between align-items-center">
                <div class="fw-bold text-dark" style="font-size: 14px;">Notifications</div>
                <button class="btn btn-sm text-primary p-0 small fw-bold" id="mark-notifications-all" style="font-size: 11px;" onclick="markAllNotificationsRead()">Mark all as read</button>
            </div>
            <div class="list-group list-group-flush text-start" id="notificationsList" style="max-height: 350px; overflow-y: auto;">
                <div class="p-5 text-center text-muted">
                    <i class="fa-solid fa-bell-slash d-block mb-3 opacity-20" style="font-size: 40px;"></i>
                    <p class="mb-0 small fw-medium">All caught up!</p>
                </div>
            </div>
        </div>
    `;

const container = document.getElementById('shared-navbar-right');
if (container) {
    container.innerHTML = navbarRightHtml;
}

// Assign initialization
initNavbarLogic();

function initNavbarLogic() {
    const user = JSON.parse(localStorage.getItem('user'));

    // Initialize user initials
    if (user) {
        const initials = user.full_name.split(' ').map(n => n[0]).join('').toUpperCase();
        const navAvatar = document.getElementById('userInitials');
        if (user.avatar_url) {
            navAvatar.innerHTML = `<img src="${user.avatar_url}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`;
        } else {
            navAvatar.innerText = initials;
        }

        const profileName = document.querySelector('.profile-name');
        const profileEmail = document.querySelector('.profile-email');
        if (profileName) profileName.innerText = user.full_name;
        if (profileEmail) profileEmail.innerText = user.email;
    }

    // ⌨️ Shortcut
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const sb = document.getElementById('globalSearch');
            if (sb) sb.focus();
        }
    });

    updateBadges();
}

function toggleDropdown(e) {
    if (e) e.stopPropagation();
    closeOtherDropdowns('profileDropdown');
    const dd = document.getElementById('profileDropdown');
    if (dd) dd.style.display = dd.style.display === 'block' ? 'none' : 'block';
}

function toggleMessagesDropdown(e) {
    if (e) e.stopPropagation();
    closeOtherDropdowns('messagesDropdown');
    const dd = document.getElementById('messagesDropdown');
    if (dd) {
        dd.style.display = dd.style.display === 'block' ? 'none' : 'block';
        if (dd.style.display === 'block') fetchMessages();
    }
}

function toggleNotificationsDropdown(e) {
    if (e) e.stopPropagation();
    closeOtherDropdowns('notificationsDropdown');
    const dd = document.getElementById('notificationsDropdown');
    if (dd) {
        dd.style.display = dd.style.display === 'block' ? 'none' : 'block';
        if (dd.style.display === 'block') fetchNotifications();
    }
}

function closeOtherDropdowns(current) {
    ['profileDropdown', 'messagesDropdown', 'notificationsDropdown'].forEach(id => {
        const el = document.getElementById(id);
        if (id !== current && el) el.style.display = 'none';
    });
}

document.addEventListener('click', function (event) {
    const avatar = document.getElementById('userInitials');
    const navBtns = document.querySelectorAll('.nav-btn');
    const dropdowns = document.querySelectorAll('.profile-dropdown');
    let isInside = avatar && avatar.contains(event.target);
    navBtns.forEach(btn => { if (btn.contains(event.target)) isInside = true; });
    dropdowns.forEach(dd => { if (dd.contains(event.target)) isInside = true; });

    // Exception for the mark read button inside dropdown
    if (event.target.id === 'mark-notifications-all') isInside = true;

    if (!isInside) dropdowns.forEach(dd => dd.style.display = 'none');
});

function logout() {
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

async function markAllNotificationsRead() {
    const token = localStorage.getItem('token');
    try {
        await fetch('http://localhost:5000/api/notifications/read-all', { method: 'PUT', headers: { 'Authorization': `Bearer ${token}` } });
        fetchNotifications();
        updateBadges();
    } catch (e) { }
}

async function markAllMessagesRead() {
    const token = localStorage.getItem('token');
    try {
        await fetch('http://localhost:5000/api/messages/read-all', { method: 'PUT', headers: { 'Authorization': `Bearer ${token}` } });
        fetchMessages();
        updateBadges();
    } catch (e) { }
}

async function updateBadges() {
    const token = localStorage.getItem('token');
    if (!token) return;
    try {
        const nRes = await fetch('http://localhost:5000/api/notifications/unread-count', { headers: { 'Authorization': `Bearer ${token}` } });
        const nData = await nRes.json();
        const nBadge = document.getElementById('notify-badge');
        if (nBadge) { if (nData.unread_count > 0) { nBadge.innerText = nData.unread_count; nBadge.style.display = 'flex'; } else nBadge.style.display = 'none'; }

        const mRes = await fetch('http://localhost:5000/api/messages/', { headers: { 'Authorization': `Bearer ${token}` } });
        const mData = await mRes.json();
        let totalUnread = 0; mData.forEach(c => totalUnread += c.unread_count);
        const mBadge = document.getElementById('msg-badge');
        if (mBadge) { if (totalUnread > 0) { mBadge.innerText = totalUnread; mBadge.style.display = 'flex'; } else mBadge.style.display = 'none'; }
        const mUnreadText = document.getElementById('msg-unread-count');
        if (mUnreadText) {
            mUnreadText.innerText = totalUnread;
            mUnreadText.style.display = totalUnread > 0 ? 'inline-block' : 'none';
        }
    } catch (e) { }
}

setInterval(updateBadges, 30000);

async function fetchNotifications() {
    const token = localStorage.getItem('token');
    const list = document.getElementById('notificationsList'); if (!list) return;
    list.innerHTML = `
        <div class="p-5 text-center text-muted">
            <div class="spinner-border spinner-border-sm text-primary mb-2" role="status"></div>
            <p class="mb-0 small fw-medium">Loading notifications...</p>
        </div>`;

    try {
        const res = await fetch('http://localhost:5000/api/notifications/', { headers: { 'Authorization': `Bearer ${token}` } });
        if (!res.ok) throw new Error('Failed to fetch');
        const data = await res.json();
        const list = document.getElementById('notificationsList'); if (!list) return;
        list.innerHTML = '';
        if (data.length === 0) {
            list.innerHTML = `
                <div class="p-5 text-center text-muted">
                    <i class="fa-solid fa-bell-slash d-block mb-3 opacity-20" style="font-size: 40px;"></i>
                    <p class="mb-0 small fw-medium text-uppercase tracking-wider">All caught up!</p>
                </div>
            `;
            return;
        }
        data.forEach(n => {
            const item = document.createElement('div');
            item.className = `list-group-item list-group-item-action border-0 py-3 px-4 position-relative ${n.is_read ? 'opacity-75' : 'bg-primary-subtle border-start border-primary border-4'}`;
            item.style.cursor = 'pointer';
            item.onclick = async () => {
                await fetch(`http://localhost:5000/api/notifications/read/${n.id}`, { method: 'PUT', headers: { 'Authorization': `Bearer ${token}` } });
                fetchNotifications();
                updateBadges();
            };
            item.innerHTML = `
                <div class="d-flex gap-3 align-items-start">
                    <div class="rounded-circle bg-primary bg-opacity-10 p-2 text-primary" style="width:38px;height:38px;display:flex;align-items:center;justify-content:center;flex-shrink:0">
                        <i class="fa-solid ${getNotifyIcon(n.type)}"></i>
                    </div>
                    <div class="flex-grow-1">
                        <div class="d-flex justify-content-between">
                            <h6 class="mb-1 fw-bold text-dark" style="font-size:13px">${n.title}</h6>
                            <span class="text-muted" style="font-size:10px">${n.created_at.split(' ')[1]}</span>
                        </div>
                        <p class="mb-0 text-muted small" style="line-height:1.4">${n.message}</p>
                    </div>
                </div>`;
            list.appendChild(item);
        });
    } catch (e) {
        const list = document.getElementById('notificationsList');
        if (list) {
            list.innerHTML = `
                <div class="p-5 text-center text-muted">
                    <i class="fa-solid fa-circle-exclamation d-block mb-3 text-warning opacity-50" style="font-size: 40px;"></i>
                    <p class="mb-0 small fw-medium">Unable to load notifications</p>
                    <button class="btn btn-sm btn-outline-primary mt-3" onclick="fetchNotifications()">Retry</button>
                </div>`;
        }
    }
}

function getNotifyIcon(type) {
    if (type === 'appointment_confirmed') return 'fa-calendar-check';
    if (type === 'appointment_cancelled') return 'fa-calendar-xmark';
    if (type === 'prescription_uploaded') return 'fa-file-medical';
    if (type === 'medicine_reminder') return 'fa-pills';
    return 'fa-message';
}

async function fetchMessages() {
    const token = localStorage.getItem('token');
    const list = document.getElementById('messagesList'); if (!list) return;
    list.innerHTML = `
        <div class="p-5 text-center text-muted">
            <div class="spinner-border spinner-border-sm text-primary mb-2" role="status"></div>
            <p class="mb-0 small fw-medium">Syncing inbox...</p>
        </div>`;

    try {
        const res = await fetch('http://localhost:5000/api/messages/', { headers: { 'Authorization': `Bearer ${token}` } });
        if (!res.ok) throw new Error('Failed to fetch');
        const data = await res.json();
        list.innerHTML = '';
        if (data.length === 0) {
            list.innerHTML = `
                <div class="p-5 text-center text-muted">
                    <i class="fa-solid fa-comment-slash d-block mb-3 opacity-20" style="font-size: 40px;"></i>
                    <p class="mb-0 small fw-medium text-uppercase tracking-wider">No conversations yet</p>
                </div>
            `;
            return;
        }
        data.forEach(c => {
            const item = document.createElement('div');
            item.className = 'list-group-item list-group-item-action border-0 py-3 px-4 d-flex align-items-center gap-3';
            item.style.cursor = 'pointer';
            item.innerHTML = `
                <div class="position-relative">
                    <div class="avatar-circle small" style="width:40px;height:40px;flex-shrink:0;border-radius:50%;background:linear-gradient(45deg, var(--primary), #4f46e5);color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1)">
                        ${c.other_name[0].toUpperCase()}
                    </div>
                </div>
                <div class="flex-grow-1 overflow-hidden">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                        <h6 class="mb-0 fw-bold text-dark" style="font-size:13px">${c.other_name}</h6>
                        <span class="text-muted" style="font-size:10px">${c.timestamp.split(' ')[1]}</span>
                    </div>
                    <p class="mb-0 text-muted small text-truncate" style="max-width: 180px;">${c.last_message}</p>
                </div>
                ${c.unread_count > 0 ? `<div class="bg-primary rounded-circle" style="width:8px;height:8px"></div>` : ''}
            `;
            list.appendChild(item);
        });
    } catch (e) {
        if (list) {
            list.innerHTML = `
                <div class="p-5 text-center text-muted">
                    <i class="fa-solid fa-circle-exclamation d-block mb-3 text-warning opacity-50" style="font-size: 40px;"></i>
                    <p class="mb-0 small fw-medium">Unable to load messages</p>
                    <button class="btn btn-sm btn-outline-primary mt-3" onclick="fetchMessages()">Retry</button>
                </div>`;
        }
    }
}
