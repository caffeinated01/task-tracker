function showNotification(message, isError) {
  const container = document.getElementById("notification-container");

  const toast = document.createElement("div");
  toast.className = `toast toast-${isError ? "error" : "success"}`;

  const closeBtn = document.createElement("div");
  closeBtn.className = "toast-close";
  closeBtn.textContent = "✕";
  closeBtn.addEventListener("click", () => removeToast(toast));

  const messageDiv = document.createElement("div");
  messageDiv.className = "toast-message";
  messageDiv.textContent = message;

  toast.appendChild(messageDiv);
  toast.appendChild(closeBtn);
  container.appendChild(toast);

  setTimeout(() => removeToast(toast), 3 * 1000);
}

function removeToast(toast) {
  toast.classList.add("toast-fade-out");
  toast.addEventListener(
    "transitionend",
    () => {
      toast.remove();
    },
    { once: true }, // ensure listener only called ONCE
  );
}
