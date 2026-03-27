const navbarRightHtml = `
        <div class="nav-right" style="display: flex; gap: 15px; align-items: center; position: relative;">
            <div class="search-container d-none d-md-block" style="position: relative;">
                <i class="fa-solid fa-search" style="position: absolute; left: 12px; top: 12px; font-size: 12px; color: #999;"></i>
                <input type="text" placeholder="Search..." id="globalSearch" style="padding-left: 30px;">
                <span class="short-key" style="position: absolute; right: 12px; top: 10px; font-size: 10px; color: #999;">⌘K</span>
            </div>

            <div class="nav-btn" onclick="window.location.href='profile.html'"><i class="fa-solid fa-gear"></i></div>
            <div class="nav-btn position-relative" onclick="toggleMessagesDropdown()">
                <i class="fa-solid fa-comment-dots"></i>
                <span class="badge-notify" id="msg-badge" style="display: none; position: absolute; top: -5px; right: -5px; background: red; color: white; border-radius: 50%; padding: 2px 6px; font-size: 10px;">0</span>
            </div>
            <div class="nav-btn position-relative" onclick="toggleNotificationsDropdown()">
                <i class="fa-solid fa-bell"></i>
                <span class="badge-notify" id="notify-badge" style="display: none; position: absolute; top: -5px; right: -5px; background: red; color: white; border-radius: 50%; padding: 2px 6px; font-size: 10px;">0</span>
            </div>

            <div class="avatar-circle" id="userInitials" onclick="toggleDropdown()" style="width: 40px; height: 40px; border-radius: 50%; background: var(--primary); color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; cursor: pointer;"></div>
        </div>

        <div class="profile-dropdown shadow-lg rounded-4 p-0" id="profileDropdown" style="display: none; position: absolute; top: 80px; right: 30px; background: white; width: 220px; z-index: 2000; overflow: hidden; border: 1px solid #eee;">
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

        <div class="profile-dropdown shadow-lg rounded-4 p-0" id="messagesDropdown" style="display: none; position: absolute; top: 80px; right: 110px; background: white; width: 300px; z-index: 2000; overflow: hidden; border: 1px solid #eee;">
            <div class="p-3 border-bottom bg-light d-flex justify-content-between align-items-center">
                <div class="fw-bold text-dark" style="font-size: 14px;">Messages</div>
                <span class="badge bg-primary rounded-pill small" id="msg-unread-count" style="display: none;">0</span>
            </div>
            <div class="list-group list-group-flush text-start" id="messagesList" style="max-height: 350px; overflow-y: auto;">
                <div class="p-4 text-center text-muted small">No messages yet.</div>
            </div>
            <div class="p-2 border-top text-center">
                <a href="#" class="small text-primary text-decoration-none fw-bold">View All in Inbox</a>
            </div>
        </div>

        <div class="profile-dropdown shadow-lg rounded-4 p-0" id="notificationsDropdown" style="display: none; position: absolute; top: 80px; right: 70px; background: white; width: 320px; z-index: 2000; overflow: hidden; border: 1px solid #eee;">
            <div class="p-3 border-bottom bg-light d-flex justify-content-between align-items-center">
                <div class="fw-bold text-dark" style="font-size: 14px;">Notifications</div>
                <button class="btn btn-sm text-primary p-0 small fw-bold" id="mark-notifications-all" style="font-size: 11px;" onclick="markAllNotificationsRead()">Mark all as read</button>
            </div>
            <div class="list-group list-group-flush text-start" id="notificationsList" style="max-height: 350px; overflow-y: auto;">
                <div class="p-4 text-center text-muted small">No notifications found.</div>
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

function toggleDropdown() {
    closeOtherDropdowns('profileDropdown');
    const dd = document.getElementById('profileDropdown');
    if (dd) dd.style.display = dd.style.display === 'block' ? 'none' : 'block';
}

function toggleMessagesDropdown() {
    closeOtherDropdowns('messagesDropdown');
    const dd = document.getElementById('messagesDropdown');
    if (dd) {
        dd.style.display = dd.style.display === 'block' ? 'none' : 'block';
        if (dd.style.display === 'block') fetchMessages();
    }
}

function toggleNotificationsDropdown() {
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
    alert("This feature marks all notifications as read.");
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
    try {
        const res = await fetch('http://localhost:5000/api/notifications/', { headers: { 'Authorization': `Bearer ${token}` } });
        const data = await res.json();
        const list = document.getElementById('notificationsList'); if (!list) return;
        list.innerHTML = '';
        if (data.length === 0) { list.innerHTML = '<div class="p-4 text-center text-muted small">No notifications found.</div>'; return; }
        data.forEach(n => {
            const item = document.createElement('div');
            item.className = `list-group-item list-group-item-action border-0 py-3 ${n.is_read ? '' : 'bg-light'}`;
            item.style.cursor = 'pointer';
            item.onclick = async () => { await fetch(`http://localhost:5000/api/notifications/read/${n.id}`, { method: 'PUT', headers: { 'Authorization': `Bearer ${token}` } }); fetchNotifications(); updateBadges(); };
            item.innerHTML = `<div class="d-flex gap-3"><div class="rounded-circle bg-primary bg-opacity-10 p-2 text-primary" style="height:fit-content"><i class="fa-solid fa-bell"></i></div><div><h6 class="mb-1 fw-bold" style="font-size:13px">${n.title} ${n.is_read ? '' : '<span class="badge bg-danger p-1 ms-1">New</span>'}</h6><p class="mb-1 text-muted small">${n.message}</p></div></div>`;
            list.appendChild(item);
        });
    } catch (e) { }
}

async function fetchMessages() {
    const token = localStorage.getItem('token');
    try {
        const res = await fetch('http://localhost:5000/api/messages/', { headers: { 'Authorization': `Bearer ${token}` } });
        const data = await res.json();
        const list = document.getElementById('messagesList'); if (!list) return;
        list.innerHTML = '';
        if (data.length === 0) { list.innerHTML = '<div class="p-4 text-center text-muted small">No messages yet.</div>'; return; }
        data.forEach(c => {
            const item = document.createElement('div');
            item.className = 'list-group-item list-group-item-action border-0 py-3 d-flex align-items-center gap-3';
            item.innerHTML = `<div class="avatar-circle small" style="width:35px;height:35px;flex-shrink:0;border-radius:50%;background:var(--primary);color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;">${c.other_name[0].toUpperCase()}</div><div class="flex-grow-1 overflow-hidden"><h6 class="mb-0 fw-bold" style="font-size:13px">${c.other_name}</h6><p class="mb-0 text-muted small text-truncate">${c.last_message}</p></div>${c.unread_count > 0 ? `<span class="badge bg-primary rounded-pill small">${c.unread_count}</span>` : ''}`;
            list.appendChild(item);
        });
    } catch (e) { }
}
