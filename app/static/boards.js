const boardsContainer = document.getElementById("boards-container");

async function fetchAndDisplayBoards() {
  try {
    const response = await fetchWithAuth("/api/boards");
    if (!response.ok) {
      throw new Error("Failed to fetch boards");
    }

    const boards = await response.json();

    boardsContainer.innerHTML = "";
    if (boards.length === 0) {
      boardsContainer.innerHTML = "<p>No boards found. Create one!</p>";
      return;
    }

    const ul = document.createElement("ul");
    for (const board of boards) {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = `/boards/${board.board_id}`;
      a.textContent = board.name;
      li.appendChild(a);

      if (board.role === "owner") {
        const shareForm = document.createElement("form");
        shareForm.classList.add("share-form");
        shareForm.dataset.boardId = board.board_id;

        const usernameInput = document.createElement("input");
        usernameInput.type = "text";
        usernameInput.placeholder = "Username to share with";
        usernameInput.required = true;

        const shareButton = document.createElement("button");
        shareButton.type = "submit";
        shareButton.textContent = "Share";

        shareForm.appendChild(usernameInput);
        shareForm.appendChild(shareButton);
        li.appendChild(shareForm);
      }

      const userList = document.createElement("div");
      userList.classList.add("user-list");
      li.appendChild(userList);
      await fetchAndDisplayUsers(
        board.board_id,
        userList,
        board.role === "owner"
      );

      ul.appendChild(li);
    }
    boardsContainer.appendChild(ul);

    document.querySelectorAll(".share-form").forEach((form) => {
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const boardId = e.target.dataset.boardId;
        const username = e.target.querySelector("input").value;

        try {
          const response = await fetchWithAuth(`/api/boards/${boardId}/share`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ username }),
          });

          const result = await response.json();
          if (response.ok) {
            e.target.querySelector("input").value = "";
            const userListDiv = e.target
              .closest("li")
              .querySelector(".user-list");
            const boardResponse = await fetchWithAuth(`/api/boards/${boardId}`);
            const board = await boardResponse.json();
            fetchAndDisplayUsers(boardId, userListDiv, board.role === "owner");
          } else {
            console.error(`Error sharing board: ${result.message}`);
          }
        } catch (error) {
          console.error("Error sharing board:", error);
        }
      });
    });
  } catch (error) {
    console.error("Error fetching boards:", error);
    boardsContainer.innerHTML = "<p>Error loading boards</p>";
  }
}

async function fetchAndDisplayUsers(boardId, container, isOwner) {
  try {
    const response = await fetchWithAuth(`/api/boards/${boardId}/users`);
    if (!response.ok) {
      throw new Error("Failed to fetch users");
    }
    const users = await response.json();

    container.innerHTML = "Users: ";
    const userList = document.createElement("ul");
    users.forEach((user) => {
      const userItem = document.createElement("li");
      userItem.textContent = `${user.username} (${user.role})`;

      if (isOwner && user.role !== "owner") {
        const revokeButton = document.createElement("button");
        revokeButton.textContent = "Revoke";
        revokeButton.onclick = () => revokeAccess(boardId, user, container);
        userItem.appendChild(revokeButton);
      }
      userList.appendChild(userItem);
    });
    container.appendChild(userList);
  } catch (error) {
    console.error(`Error fetching users for board ${boardId}:`, error);
    container.innerHTML = "<p>Error loading users</p>";
  }
}

async function revokeAccess(boardId, user, container) {
  try {
    const response = await fetchWithAuth(
      `/api/boards/${boardId}/revoke/${user.user_id}`,
      {
        method: "POST",
      }
    );

    const result = await response.json();
    if (response.ok) {
      const boardResponse = await fetchWithAuth(`/api/boards/${boardId}`);
      const board = await boardResponse.json();
      fetchAndDisplayUsers(boardId, container, board.role === "owner");
    } else {
      console.error(`Error revoking access: ${result.message}`);
    }
  } catch (error) {
    console.error("Error revoking access:", error);
  }
}

document
  .getElementById("create-board-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const boardName = document.getElementById("board-name").value;
    try {
      const response = await fetchWithAuth("/api/boards", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: boardName }),
      });
      if (response.ok) {
        document.getElementById("board-name").value = "";
        fetchAndDisplayBoards();
      } else {
        const errorData = await response.json();
        console.error("Error creating board:", errorData.message);
      }
    } catch (error) {
      console.error("Error creating board:", error);
    }
  });

document.addEventListener("DOMContentLoaded", fetchAndDisplayBoards);
