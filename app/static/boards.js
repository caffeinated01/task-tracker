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
    boards.forEach((board) => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = `/boards/${board.id}`;
      a.textContent = board.name;
      li.appendChild(a);

      if (board.role === "owner") {
        const shareForm = document.createElement("form");
        shareForm.classList.add("share-form");
        shareForm.dataset.boardId = board.id;

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

      ul.appendChild(li);
    });
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
            alert(result.message);
            e.target.querySelector("input").value = "";
          } else {
            alert(`Error sharing board: ${result.message}`);
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
