function displayUsername(username) {
  const usernameSpan = document.querySelector("#user-username");
  const avatarSpan = document.querySelector("#user-avatar");

  if (usernameSpan) {
    usernameSpan.textContent = username;
  }

  if (avatarSpan) {
    avatarSpan.textContent = username.charAt(0).toUpperCase();
  }
}

function setupNavbarDropdown() {
  const userMenuBtn = document.querySelector('[data-handler="usermenubtn"]');
  const userMenu = document.querySelector(".navbar-user-menu");

  if (userMenuBtn && userMenu) {
    userMenuBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      userMenu.hidden = !userMenu.hidden;
    });

    document.addEventListener("click", function (e) {
      if (!userMenu.hidden && !userMenu.contains(e.target)) {
        userMenu.hidden = true;
      }
    });
  }
}

async function handleLogout() {
  try {
    const response = await fetchWithAuth("/api/auth/logout", {
      method: "GET",
    });

    if (response.ok) {
      window.location.href = "/login";
    } else {
      showNotification("Logout failed", true);
    }
  } catch (err) {
    showNotification("Logout failed", true);
  }
}

document.addEventListener("DOMContentLoaded", setupNavbarDropdown());
