function showModal(content) {
  const container = document.getElementById("modal-container");
  if (!container) return;

  container.replaceChildren();

  if (typeof content === "string") {
    container.innerHTML = content;
  } else if (content) {
    container.appendChild(content);
  }

  container.classList.remove("hidden");
}

function hideModal() {
  const container = document.getElementById("modal-container");
  if (!container) return;

  container.classList.add("hidden");
  container.replaceChildren();
}

function isModalOpen() {
  const container = document.getElementById("modal-container");
  if (!container) return false;

  return !container.classList.contains("hidden");
}

function showTemplateInModal(template, beforeShow) {
  const modalContent = document.importNode(template.content, true);

  if (typeof beforeShow === "function") {
    beforeShow(modalContent);
  }

  showModal(modalContent);
}

document.addEventListener("click", (event) => {
  const container = document.getElementById("modal-container");
  if (!container || container.classList.contains("hidden")) return;

  if (event.target === container) {
    hideModal();
    return;
  }

  if (event.target.closest("[data-modal-action='close']")) {
    hideModal();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && isModalOpen()) {
    hideModal();
  }
});

window.showModal = showModal;
window.hideModal = hideModal;
window.isModalOpen = isModalOpen;
window.showTemplateInModal = showTemplateInModal;
