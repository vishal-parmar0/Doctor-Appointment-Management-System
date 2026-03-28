const navbarRightHtml = `
    <style>
        .nav-btn {
            width: 42px;
            height: 42px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 14px;
            color: #64748b;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: #f8fafc;
            border: 1px solid #f1f5f9;
        }
        .nav-btn:hover {
            background: #eff6ff;
            color: #2563eb;
            border-color: #dbeafe;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.1);
        }
        .nav-btn i { font-size: 19px; }
        .short-key {
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            letter-spacing: 0.5px;
        }
        .avatar-circle {
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
            border: 2px solid white;
        }
        .avatar-circle:hover {
            transform: scale(1.05) rotate(5deg);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
        }
        #globalSearch:focus {
            outline: none;
            border-color: #2563eb;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
            background: white;
        }
        .profile-dropdown {
            backdrop-filter: blur(12px);
            background: rgba(255, 255, 255, 0.98) !important;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15) !important;
            border: 1px solid rgba(241, 245, 249, 0.8) !important;
            animation: dropdownFade 0.2s ease-out;
        }
        @keyframes dropdownFade {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .list-group::-webkit-scrollbar { width: 4px; }
        .list-group::-webkit-scrollbar-track { background: transparent; }
        .list-group::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
        .list-group-item { border: none !important; transition: all 0.2s ease; margin: 4px 8px; border-radius: 10px !important; }
        .list-group-item:hover { background: #f8fafc !important; transform: translateX(4px); }
        .badge-notify {
            position: absolute;
            top: -2px;
            right: -2px;
            background: #ef4444;
            color: white;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            font-size: 10px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid white;
            box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
        }
        .dropdown-header-custom {
            padding: 16px 20px;
            border-bottom: 1px solid #f1f5f9;
            background: #fcfdfe;
        }
        .dropdown-footer-custom {
            padding: 12px 20px;
            border-top: 1px solid #f1f5f9;
            background: #fcfdfe;
        }
        .empty-state {
            padding: 40px 20px;
            text-align: center;
        }
        .empty-state i {
            font-size: 48px;
            color: #e2e8f0;
            margin-bottom: 16px;
        }
        .notification-unread {
            background: #f0f7ff !important;
            border-left: 3px solid #2563eb !important;
            border-radius: 0 10px 10px 0 !important;
        }
    </style>
        <div class="nav-right" style="display: flex; gap: 12px; align-items: center; position: relative;">
            <div class="search-container d-none d-md-block" style="position: relative; width: 240px;">
                <i class="fa-solid fa-search" style="position: absolute; left: 16px; top: 50%; transform: translateY(-50%); font-size: 14px; color: #94a3b8;"></i>
                <input type="text" placeholder="Search anything..." id="globalSearch" style="width: 100%; padding: 11px 45px 11px 42px; border-radius: 14px; border: 1.5px solid #f1f5f9; transition: all 0.3s ease; font-size: 13.5px; background: #f8fafc; color: #1e293b; font-weight: 500;">
                <span class="short-key" style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%); font-size: 9px; color: #94a3b8; background: #ffffff; padding: 3px 7px; border-radius: 7px; border: 1px solid #e2e8f0; pointer-events: none; font-weight: 800; text-transform: uppercase;">Ctrl K</span>
            </div>

            <div class="nav-btn" onclick="toggleMessagesDropdown(event)">
                <i class="fa-solid fa-comment-dots"></i>
                <span class="badge-notify" id="msg-badge" style="display: none;">0</span>
            </div>
            <div class="nav-btn" onclick="toggleNotificationsDropdown(event)">
                <i class="fa-solid fa-bell"></i>
                <span class="badge-notify" id="notify-badge" style="display: none;">0</span>
            </div>

            <div class="avatar-circle" id="userInitials" onclick="toggleDropdown(event)" style="width: 42px; height: 42px; border-radius: 14px; background: linear-gradient(135deg, #2563eb, #4f46e5); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; cursor: pointer; font-size: 15px;"></div>
        </div>

        <div class="profile-dropdown shadow-lg rounded-4 p-0" id="profileDropdown" style="display: none; position: absolute; top: 70px; right: 0; background: white; width: 240px; z-index: 2000; overflow: hidden;" onclick="event.stopPropagation()">
            <div class="dropdown-header-custom">
                <div class="fw-bold profile-name text-dark" style="font-size: 15px;">User Name</div>
                <div class="text-muted profile-email text-truncate" style="font-size: 12px;">user@example.com</div>
            </div>
            <div class="list-group list-group-flush p-1">
                <a href="profile.html" class="list-group-item list-group-item-action d-flex align-items-center gap-3 py-2 px-3">
                    <div class="bg-primary bg-opacity-10 text-primary rounded-3 p-2 d-flex align-items-center justify-content-center" style="width:34px; height:34px;"><i class="fa-solid fa-user-circle"></i></div>
                    <span style="font-size: 14px; font-weight: 500;">My Profile</span>
                </a>
                <a href="profile.html" class="list-group-item list-group-item-action d-flex align-items-center gap-3 py-2 px-3">
                    <div class="bg-secondary bg-opacity-10 text-secondary rounded-3 p-2 d-flex align-items-center justify-content-center" style="width:34px; height:34px;"><i class="fa-solid fa-sliders"></i></div>
                    <span style="font-size: 14px; font-weight: 500;">Account Settings</span>
                </a>
                <div class="dropdown-divider my-1 opacity-50"></div>
                <a href="#" onclick="logout()" class="list-group-item list-group-item-action d-flex align-items-center gap-3 py-2 px-3 text-danger">
                    <div class="bg-danger bg-opacity-10 text-danger rounded-3 p-2 d-flex align-items-center justify-content-center" style="width:34px; height:34px;"><i class="fa-solid fa-power-off"></i></div>
                    <span style="font-size: 14px; font-weight: 600;">Sign Out</span>
                </a>
            </div>
        </div>

        <div class="profile-dropdown shadow-lg rounded-4 p-0" id="messagesDropdown" style="display: none; position: absolute; top: 70px; right: 0; background: white; width: 340px; z-index: 2000; overflow: hidden;" onclick="event.stopPropagation()">
            <div class="dropdown-header-custom d-flex justify-content-between align-items-center">
                <div class="fw-bold text-dark" style="font-size: 15px;">Direct Messages</div>
                <button class="btn btn-link btn-sm text-decoration-none p-0 fw-bold" onclick="markAllMessagesRead()" style="font-size: 11px; color: #2563eb;">Mark read</button>
            </div>
            <div class="list-group list-group-flush text-start py-1" id="messagesList" style="max-height: 400px; overflow-y: auto;">
                <div class="empty-state">
                    <i class="fa-solid fa-comments"></i>
                    <p class="mb-0 text-muted small fw-medium">No messages found</p>
                </div>
            </div>
            <div class="dropdown-footer-custom text-center">
                <a href="#" class="small text-primary text-decoration-none fw-bold" style="font-size: 12px;">Open Full Inbox</a>
            </div>
        </div>

        <div class="profile-dropdown shadow-lg rounded-4 p-0" id="notificationsDropdown" style="display: none; position: absolute; top: 70px; right: 0; background: white; width: 360px; z-index: 2000; overflow: hidden;" onclick="event.stopPropagation()">
            <div class="dropdown-header-custom d-flex justify-content-between align-items-center">
                <div class="fw-bold text-dark" style="font-size: 15px;">Notifications</div>
                <button class="btn btn-link btn-sm text-decoration-none p-0 fw-bold" id="mark-notifications-all" style="font-size: 11px; color: #2563eb;" onclick="markAllNotificationsRead()">Mark all read</button>
            </div>
            <div class="list-group list-group-flush text-start py-1" id="notificationsList" style="max-height: 400px; overflow-y: auto;">
                <div class="empty-state">
                    <i class="fa-solid fa-bell-slash"></i>
                    <p class="mb-0 text-muted small fw-medium">No new notifications</p>
                </div>
            </div>
            <div class="dropdown-footer-custom text-center">
                <a href="#" class="small text-muted text-decoration-none fw-medium" style="font-size: 12px;">Showing recent activity</a>
            </div>
        </div>
    `;

const container = document.getElementById('shared-navbar-right');
if (container) {
    container.innerHTML = navbarRightHtml;
}

initNavbarLogic();

function initNavbarLogic() {
    const user = JSON.parse(sessionStorage.getItem('user'));
    if (user) {
        const initials = user.full_name.split(' ').map(n => n[0]).join('').toUpperCase();
        const navAvatar = document.getElementById('userInitials');
        if (user.avatar_url) {
            navAvatar.innerHTML = `<img src="${user.avatar_url}" style="width:100%;height:100%;object-fit:cover;border-radius:12px;">`;
        } else {
            navAvatar.innerText = initials;
        }
        const profileName = document.querySelector('.profile-name');
        const profileEmail = document.querySelector('.profile-email');
        if (profileName) profileName.innerText = user.full_name;
        if (profileEmail) profileEmail.innerText = user.email;
    }

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
    const dd = document.getElementById('profileDropdown');
    const isVisible = dd.style.display === 'block';
    closeOtherDropdowns();
    if (!isVisible) dd.style.display = 'block';
}

function toggleMessagesDropdown(e) {
    if (e) e.stopPropagation();
    const dd = document.getElementById('messagesDropdown');
    const isVisible = dd.style.display === 'block';
    closeOtherDropdowns();
    if (!isVisible) {
        dd.style.display = 'block';
        fetchMessages();
    }
}

function toggleNotificationsDropdown(e) {
    if (e) e.stopPropagation();
    const dd = document.getElementById('notificationsDropdown');
    const isVisible = dd.style.display === 'block';
    closeOtherDropdowns();
    if (!isVisible) {
        dd.style.display = 'block';
        fetchNotifications();
    }
}

function closeOtherDropdowns() {
    ['profileDropdown', 'messagesDropdown', 'notificationsDropdown'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = 'none';
    });
}

document.addEventListener('click', function (event) {
    const dropdowns = document.querySelectorAll('.profile-dropdown');
    let isClickInside = false;
    dropdowns.forEach(dd => { if (dd.contains(event.target)) isClickInside = true; });
    const navBtns = document.querySelectorAll('.nav-btn, .avatar-circle');
    navBtns.forEach(btn => { if (btn.contains(event.target)) isClickInside = true; });

    if (!isClickInside) closeOtherDropdowns();
});

function logout() {
    sessionStorage.clear();
    window.location.href = 'login.html';
}

async function markAllNotificationsRead() {
    const token = sessionStorage.getItem('token');
    const btn = document.getElementById('mark-notifications-all');
    if (btn) btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span>';

    try {
        await fetch('http://localhost:5000/api/notifications/read-all', {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        setTimeout(() => {
            fetchNotifications();
            updateBadges();
        }, 300);
    } catch (e) {
        if (btn) btn.innerText = 'Mark all read';
    }
}

async function markAllMessagesRead() {
    const token = sessionStorage.getItem('token');
    try {
        await fetch('http://localhost:5000/api/messages/read-all', {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        fetchMessages();
        updateBadges();
    } catch (e) { }
}

async function updateBadges() {
    const token = sessionStorage.getItem('token');
    if (!token) return;
    try {
        const nRes = await fetch('http://localhost:5000/api/notifications/unread-count', { headers: { 'Authorization': `Bearer ${token}` } });
        const nData = await nRes.json();
        const nBadge = document.getElementById('notify-badge');
        if (nBadge) {
            if (nData.unread_count > 0) {
                nBadge.innerText = nData.unread_count > 9 ? '9+' : nData.unread_count;
                nBadge.style.display = 'flex';
            } else nBadge.style.display = 'none';
        }

        const mRes = await fetch('http://localhost:5000/api/messages/', { headers: { 'Authorization': `Bearer ${token}` } });
        const mData = await mRes.json();
        let totalUnread = 0;
        if (Array.isArray(mData)) mData.forEach(c => totalUnread += c.unread_count);

        const mBadge = document.getElementById('msg-badge');
        if (mBadge) {
            if (totalUnread > 0) {
                mBadge.innerText = totalUnread > 9 ? '9+' : totalUnread;
                mBadge.style.display = 'flex';
            } else mBadge.style.display = 'none';
        }
    } catch (e) { }
}

setInterval(updateBadges, 15000);

async function fetchNotifications() {
    const token = sessionStorage.getItem('token');
    const list = document.getElementById('notificationsList');
    if (!list) return;

    list.innerHTML = `
        <div class="p-4 text-center">
            <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
        </div>`;

    try {
        const res = await fetch('http://localhost:5000/api/notifications/', { headers: { 'Authorization': `Bearer ${token}` } });
        const data = await res.json();
        list.innerHTML = '';
        if (!data || data.length === 0) {
            list.innerHTML = `
                <div class="empty-state">
                    <i class="fa-solid fa-bell-slash"></i>
                    <p class="mb-0 text-muted small fw-medium">All caught up!</p>
                </div>`;
            return;
        }
        data.forEach(n => {
            const item = document.createElement('div');
            item.className = `list-group-item list-group-item-action ${!n.is_read ? 'notification-unread' : ''} p-3 mb-1`;
            item.innerHTML = `
                <div class="d-flex gap-3 align-items-center">
                    <div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width:36px; height:36px; background:#f1f5f9; color:#64748b;">
                        <i class="fa-solid ${getNotifyIcon(n.type)}" style="font-size:14px"></i>
                    </div>
                    <div class="flex-grow-1 overflow-hidden">
                        <div class="d-flex justify-content-between align-items-center mb-0.5">
                            <h6 class="mb-0 fw-bold text-dark" style="font-size:13px">${n.title}</h6>
                            <span class="text-muted" style="font-size:10px">${n.created_at.split(' ')[1].substring(0, 5)}</span>
                        </div>
                        <p class="mb-0 text-muted text-truncate" style="font-size:12px">${n.message}</p>
                    </div>
                </div>`;
            item.onclick = async () => {
                if (!n.is_read) {
                    await fetch(`http://localhost:5000/api/notifications/read/${n.id}`, { method: 'PUT', headers: { 'Authorization': `Bearer ${token}` } });
                    fetchNotifications();
                    updateBadges();
                }
            };
            list.appendChild(item);
        });
    } catch (e) {
        list.innerHTML = `<div class="p-4 text-center text-danger small">Error loading notifications</div>`;
    }
}

async function fetchMessages() {
    const token = sessionStorage.getItem('token');
    const list = document.getElementById('messagesList');
    if (!list) return;

    list.innerHTML = `<div class="p-4 text-center"><div class="spinner-border spinner-border-sm text-primary" role="status"></div></div>`;

    try {
        const res = await fetch('http://localhost:5000/api/messages/', { headers: { 'Authorization': `Bearer ${token}` } });
        const data = await res.json();
        list.innerHTML = '';
        if (!data || data.length === 0) {
            list.innerHTML = `
                <div class="empty-state">
                    <i class="fa-solid fa-comments"></i>
                    <p class="mb-0 text-muted small fw-medium">No messages yet</p>
                </div>`;
            return;
        }
        data.forEach(c => {
            const item = document.createElement('div');
            item.className = 'list-group-item list-group-item-action p-3 mb-1';
            item.innerHTML = `
                <div class="d-flex align-items-center gap-3">
                    <div class="avatar-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width:40px; height:40px; border-radius:12px; background:#eff6ff; color:#2563eb; font-weight:700;">
                        ${c.other_name[0].toUpperCase()}
                    </div>
                    <div class="flex-grow-1 overflow-hidden">
                        <div class="d-flex justify-content-between align-items-center mb-0.5">
                            <h6 class="mb-0 fw-bold text-dark" style="font-size:13px">${c.other_name}</h6>
                            <span class="text-muted" style="font-size:10px">${c.timestamp.split(' ')[1].substring(0, 5)}</span>
                        </div>
                        <p class="mb-0 text-muted text-truncate" style="font-size:12px">${c.last_message}</p>
                    </div>
                    ${c.unread_count > 0 ? `<div class="bg-primary rounded-circle" style="width:6px; height:6px;"></div>` : ''}
                </div>`;
            list.appendChild(item);
        });
    } catch (e) {
        list.innerHTML = `<div class="p-4 text-center text-danger small">Unable to sync messages</div>`;
    }
}

function getNotifyIcon(type) {
    if (type === 'appointment_confirmed') return 'fa-calendar-check';
    if (type === 'appointment_cancelled') return 'fa-calendar-xmark';
    if (type === 'prescription_uploaded') return 'fa-file-medical';
    if (type === 'medicine_reminder') return 'fa-pills';
    return 'fa-bell';
}
