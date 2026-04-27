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

document.addEventListener("DOMContentLoaded", fetchAndDisplayBoards);
