const BoardRole = {
  OWNER: 1,
  EDITOR: 2,
};

const BoardRoleNames = {
  [BoardRole.OWNER]: "Owner",
  [BoardRole.EDITOR]: "Editor",
};

const boardsList = document.getElementById("boards-list");
const template = document.getElementById("board-card-template");
const createBoardModalTemplate = document.getElementById(
  "create-board-modal-template",
);

const fetchAndDisplayBoards = async () => {
  const response = await fetchWithAuth("/api/boards");
  const boards = await response.json();

  boardsList.innerHTML = "";

  const fragment = document.createDocumentFragment();

  for (const board of boards) {
    const clone = template.content.cloneNode(true);

    const card = clone.querySelector("a.board-card");
    const title = clone.querySelector(".title");
    const username = clone.querySelector(".username");
    const icon = clone.querySelector(".board-card-icon");

    card.href = `/boards/${board.board_id}`;
    title.textContent = board.name;
    username.textContent = BoardRoleNames[board.role];
    icon.textContent = board.name.charAt(0).toUpperCase();

    fragment.appendChild(clone);
  }

  boardsList.appendChild(fragment);
};

const createBoardButton = document.getElementById("create-board-btn");

const clickMap = {
  createboard: createBoardFromModal,
};

createBoardButton.addEventListener("click", () => {
  showTemplateInModal(createBoardModalTemplate);
});

async function createBoardFromModal() {
  const boardNameInput = document.getElementById("board-name-input");
  if (!boardNameInput) return;

  const boardName = boardNameInput.value.trim();

  if (!boardName) {
    showNotification("Board name is required", true);
    return;
  }

  try {
    const response = await fetchWithAuth("/api/boards", {
      method: "POST",
      body: JSON.stringify({ name: boardName }),
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      const data = await response.json()
      const message = data.message
      throw Error(message);
    }

    hideModal();
    showNotification("Board created successfully", false);
    document.dispatchEvent(new Event("boardCreated"));
  } catch (err) {
    showNotification(err, true);
  }
}

function clickHandle(event) {
  if (!event.target.dataset.handler) return;

  const handlerName = event.target.dataset.handler.split("_")[0];
  if (!clickMap[handlerName]) return;

  clickMap[handlerName]();
}

document.addEventListener("DOMContentLoaded", fetchAndDisplayBoards);
document.addEventListener("boardCreated", fetchAndDisplayBoards);
document.addEventListener("click", clickHandle);
