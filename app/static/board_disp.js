/*
 * TODO:
 * -   Server error handling within submitModal and loadAllPosts
 * -   Calling loadAllPosts each time we want to update might not be good. We might need to change it.
 */

// fetch board data from API
let boardId = "";
let boardName = null;
let boardContent = null;
let currentUserRole = null;
let currentUsername = null;
const postTemplate = document.getElementById("task-template");
const title = document.querySelector("#board-name");
let boardNameBound = false;
let boardUsers = [];

async function loadAllPosts() {
  const currentPath = window.location.pathname.split("/");
  boardId = currentPath[currentPath.length - 1];

  try {
    const boardResp = await fetchWithAuth(`/api/boards/${boardId}`);

    if (boardResp.status === 404) {
      window.location.pathname = "/boards";
      return;
    }

    if (boardResp.ok) {
      const boardInfo = await boardResp.json();
      currentUserRole = boardInfo.board.role;
      currentUsername = boardInfo.user.username;
      boardName = boardInfo.board.name;
      displayUsername(currentUsername);
      title.value = boardName;
      title.dataset.value = boardName;
      if (!boardNameBound) {
        bindBoardNameInput();
        boardNameBound = true;
      }
      const canEditBoard = parseInt(currentUserRole, 10) === 1;
      title.readOnly = !canEditBoard;
      title.classList.toggle("is-readonly", !canEditBoard);
    }

    // clear every row first
    document.querySelectorAll(".status-tasks").forEach((row) => {
      row.innerHTML = "";
    });

    boardContent = await fetchWithAuth(`/api/boards/${boardId}/tasks`).then(
      (r) => r.json(),
    );
    boardContent.forEach((post) => {
      // console.log(post);

      // update fields which are supposed to have post id
      const postClone = document.importNode(postTemplate.content, true);
      postClone.querySelector(".task").id = "task_" + post.task_id;
      for (child of postClone
        .querySelector(".task")
        .getElementsByTagName("*")) {
        if (child.dataset.handler) {
          child.dataset.handler = child.dataset.handler + "_" + post.task_id;
        }
      }

      // update textual content
      postClone.querySelector(".task-header > h3").textContent = post.title;
      postClone.querySelector(".task-desc").textContent = post.content;

      const footer = postClone.querySelector(".task-footer");
      if (footer) {
        footer.textContent = `Created by ${post.created_by}`;
      }

      const bar = postClone.querySelector(".importance-bar");
      if (bar) {
        const importance = Math.max(
          1,
          Math.min(3, parseInt(post.importance, 10) || 1),
        );
        bar.style.width = `${(importance / 3) * 100}%`;
        bar.classList.add(`level-${importance}`);
      }

      document
        .querySelector(`#status_${post.status} .status-tasks`)
        .appendChild(postClone);
    });
  } catch (err) {
    console.log(err);
    return;
  }
}

function bindBoardNameInput() {
  title.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      title.blur();
    }
    if (event.key === "Escape") {
      event.preventDefault();
      title.value = title.dataset.value || "";
      title.blur();
    }
  });

  title.addEventListener("blur", async () => {
    if (title.readOnly) return;

    const nextName = title.value.trim();
    const prevName = title.dataset.value || "";

    if (!nextName) {
      title.value = prevName;
      return;
    }

    if (nextName === prevName) return;

    try {
      const res = await fetchWithAuth(`/api/boards/${boardId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: nextName }),
      });

      if (!res.ok) {
        throw new Error("Failed to update board name");
      }

      boardName = nextName;
      title.dataset.value = nextName;
    } catch (err) {
      console.log(err);
      title.value = prevName;
    }
  });
}

async function fetchBoardUsers() {
  try {
    const usersResp = await fetchWithAuth(`/api/boards/${boardId}/users`);
    if (!usersResp.ok) return null;
    const users = await usersResp.json();
    boardUsers = users;
    return users;
  } catch (err) {
    console.log(err);
    return null;
  }
}

function populateAssigneeSelect(container, selectedId) {
  if (!container || typeof container.querySelector !== "function") return;

  const select = container.querySelector("#assigned-to-input");
  if (!select) return;

  const currentValue =
    selectedId !== undefined && selectedId !== null
      ? String(selectedId)
      : select.value;

  select.replaceChildren();

  const unassignedOption = document.createElement("option");
  unassignedOption.value = "";
  unassignedOption.textContent = "Unassigned";
  select.appendChild(unassignedOption);

  boardUsers.forEach((u) => {
    const option = document.createElement("option");
    option.value = u.user_id;
    option.textContent = u.username;
    select.appendChild(option);
  });

  select.value = currentValue || "";
}

function refreshAssigneeSelects(selectedId) {
  const container = document.getElementById("modal-container");
  if (!container) return;
  populateAssigneeSelect(container, selectedId);
}

async function fetchAndPopulateCollaborators(modalFragment) {
  try {
    const users = await fetchBoardUsers();
    if (!users) return;

    let container = null;
    if (modalFragment && typeof modalFragment.querySelector === "function") {
      container = modalFragment.querySelector("#collaborators-list");
    }
    if (!container) container = document.getElementById("collaborators-list");
    if (!container) return;

    container.replaceChildren();

    users.forEach((u) => {
      const userDiv = document.createElement("div");
      userDiv.className = "user-details";

      const usernameGroup = document.createElement("div");
      usernameGroup.className = "username-group";

      const icon = document.createElement("div");
      icon.className = "user-icon";
      icon.textContent = u.username ? u.username.charAt(0).toUpperCase() : "?";

      const nameP = document.createElement("p");
      nameP.className = "text-md";
      nameP.textContent = u.username;

      usernameGroup.appendChild(icon);
      usernameGroup.appendChild(nameP);

      userDiv.appendChild(usernameGroup);

      const roleGroup = document.createElement("div");
      roleGroup.className = "user-role-group";

      const roleP = document.createElement("p");
      roleP.className = "text-md user-role";
      roleP.textContent = u.role == 1 ? "Owner" : "Editor";

      roleGroup.appendChild(roleP);

      if (currentUserRole == 1 && u.role != 1) {
        const revokeBtn = document.createElement("button");
        revokeBtn.className = "revoke-button";
        revokeBtn.textContent = "✕";
        revokeBtn.dataset.handler = "revoke_" + u.user_id;
        roleGroup.appendChild(revokeBtn);
      }

      userDiv.appendChild(roleGroup);

      container.appendChild(userDiv);
    });
    refreshAssigneeSelects();
  } catch (err) {
    console.log(err);
  }
}

/*
handle general clicking on webpage, this should cover:
*   clicking on dropdown menus (all forms)
*   modal buttons
*/

var clickMap = {
  optionbtn: optionBtnHandle,
  editbtn: editBtnHandle,
  deletebtn: deleteBtnHandle,
  submitmodal: submitModal,
  deletemodal: deleteModal,
  addpost: addPostHandle,
  shareboard: shareBoardHandle,
  sharesubmit: shareSubmit,
  revoke: revokeAccess,
  logout: handleLogout,
};

var updateStatus = { board: null, id: null };
let postModalTemp = document.getElementById("post-modal-template");
let deleteModalTemp = document.getElementById("delete-modal-template");
let shareModalTemp = document.getElementById("share-modal-template");
let pendingDeleteTaskId = null;

function shareBoardHandle() {
  showTemplateInModal(shareModalTemp, fetchAndPopulateCollaborators);
}

async function shareSubmit() {
  const input = document.getElementById("share-input");
  if (!input) return;
  const username = input.value.trim();
  if (!username) return;

  try {
    const resp = await fetchWithAuth(`/api/boards/${boardId}/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username }),
    });

    if (resp.ok) {
      showNotification(`Board shared with ${username}`, false);
      input.value = "";
      await fetchAndPopulateCollaborators();
    } else {
      const err = await resp.json();
      showNotification(err.message, true);
    }
  } catch (err) {
    console.log(err);
    showNotification("Failed to share board", true);
  }
}

async function revokeAccess(userId) {
  try {
    const resp = await fetchWithAuth(`/api/boards/${boardId}/users/${userId}`, {
      method: "DELETE",
    });

    if (resp.ok) {
      showNotification("Access revoked successfully", false);
      await fetchAndPopulateCollaborators();
    } else {
      const err = await resp.json();
      showNotification(err.message, true);
    }
  } catch (err) {
    console.log(err);
    showNotification("Failed to revoke access", true);
  }
}

function addPostHandle(status) {
  updateStatus.id = null;
  updateStatus.board = parseInt(status);
  showTemplateInModal(postModalTemp, (newPostModal) => {
    preparePostModal(newPostModal, null);
  });
}

function optionBtnHandle(id) {
  var dropdownMenu = document.querySelector(
    `#task_${id} .option-dropdown-menu`,
  );
  dropdownMenu.hidden = !dropdownMenu.hidden;
}

function editBtnHandle(id) {
  const post = boardContent.find((x) => x.task_id == id);
  if (!post) return;

  var dropdownMenu = document.querySelector(
    `#task_${id} .option-dropdown-menu`,
  );
  dropdownMenu.hidden = true;
  updateStatus.id = id;
  updateStatus.board = null;

  showTemplateInModal(postModalTemp, (newPostModal) => {
    preparePostModal(newPostModal, post);
  });
}

function preparePostModal(modalFragment, post) {
  const titleInput = modalFragment.getElementById("title-input");
  const descInput = modalFragment.getElementById("desc-textarea");
  const importanceInput = modalFragment.getElementById("importance-input");

  if (titleInput) titleInput.value = post ? post.title : "";
  if (descInput) descInput.value = post ? post.content : "";
  if (importanceInput) {
    importanceInput.value = post ? String(post.importance || 1) : "1";
  }

  populateAssigneeSelect(modalFragment, post ? post.assigned_to : "");

  fetchBoardUsers().then(() => {
    populateAssigneeSelect(modalFragment, post ? post.assigned_to : "");
  });
}

function deleteBtnHandle(id) {
  var dropdownMenu = document.querySelector(
    `#task_${id} .option-dropdown-menu`,
  );
  dropdownMenu.hidden = true;

  pendingDeleteTaskId = id;
  showTemplateInModal(deleteModalTemp);
}

function deleteModal() {
  if (!pendingDeleteTaskId) return;

  fetchWithAuth(`/api/tasks/${pendingDeleteTaskId}`, {
    method: "DELETE",
  })
    .then((resp) => {
      if (!resp.ok) {
        throw Error("Unable to delete task");
      }

      pendingDeleteTaskId = null;
      hideModal();
      loadAllPosts();
      showNotification("Task deleted successfully", false);
    })
    .catch((err) => {
      console.log(err);
      showNotification("Failed to delete task", true);
    });
}

function submitModal() {
  var title = document.querySelector(".title-input").value;
  var desc = document.querySelector(".desc-textarea").value;
  const importanceInput = document.getElementById("importance-input");
  const assignedInput = document.getElementById("assigned-to-input");
  const importance = importanceInput
    ? Math.max(1, Math.min(3, parseInt(importanceInput.value, 10) || 1))
    : 1;
  const assignedTo =
    assignedInput && assignedInput.value !== "" ? assignedInput.value : null;
  if (title == "") {
    showNotification("Missing title", true);
    return
  };

  // only clear and close if went through
  // update importance
  if (updateStatus.board) {
    fetchWithAuth(`/api/boards/${boardId}/tasks`, {
      method: "POST",
      body: JSON.stringify({
        title: title,
        status: updateStatus.board,
        content: desc,
        importance: importance,
        assigned_to: assignedTo,
      }),
      headers: { "Content-Type": "application/json" },
    }).then((resp) => {
      // console.log(resp.json());
      submitModalSuccess();
      loadAllPosts();
      showNotification("Task created successfully", false);
    });
  } else if (updateStatus.id) {
    const post = boardContent.find((x) => x.task_id == updateStatus.id);
    if (!post) throw Error(`Unable to find post with id ${updateStatus.id}`);

    fetchWithAuth(`/api/tasks/${updateStatus.id}`, {
      method: "PATCH",
      body: JSON.stringify({
        title: title,
        status: post.status,
        content: desc,
        importance: importance,
        assigned_to: assignedTo,
      }),
      headers: { "Content-Type": "application/json" },
    }).then((resp) => {
      submitModalSuccess();
      loadAllPosts();
      showNotification("Task updated successfully", false);
    });
  } else return;
}

function submitModalSuccess() {
  document.querySelector(".title-input").value = "";
  document.querySelector(".desc-textarea").value = "";
  const importanceInput = document.getElementById("importance-input");
  const assignedInput = document.getElementById("assigned-to-input");
  if (importanceInput) importanceInput.value = "1";
  if (assignedInput) assignedInput.value = "";
  hideModal();
}

function clickHandle(e) {
  // https://stackoverflow.com/questions/46732637/best-way-to-handle-clicks-on-buttons-in-javascript-vanilla
  // do something similar to this for edit, dropdowns and shit
  if (!e.target.dataset.handler) return;
  handlerArgs = e.target.dataset.handler.split("_");
  if (!clickMap[handlerArgs[0]]) return;
  if (handlerArgs.length == 1) clickMap[handlerArgs[0]]();
  else if (handlerArgs.length == 2) clickMap[handlerArgs[0]](handlerArgs[1]);
}

// handle dragging on webpage

let preview = document.querySelector(".hover-preview");
let previewOffset = { x: null, y: null, originalStatus: null };
let draggingTask = false;

const emptyImg = document.createElement("img");
emptyImg.src =
  "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==";

function dragStartHandle(e) {
  console.log(e);

  // check if task element is being selected
  draggingTask = e.target.classList && e.target.classList.contains("task");
  if (!draggingTask) return;

  // exclude selecting option button or dropdown menu
  var elementsAtPos = document.elementsFromPoint(e.clientX, e.clientY);
  var shouldBeIgnored = elementsAtPos.find(
    (x) =>
      x.classList.contains("option-dropdown-comp") ||
      x.classList.contains("option-dropdown-menu"),
  );
  if (shouldBeIgnored) {
    draggingTask = false;
    return;
  }

  var parentStatusBox = elementsAtPos.find((x) =>
    x.classList.contains("flex-status"),
  );
  if (parentStatusBox) {
    const statusName =
      parentStatusBox.querySelector(".status-head > p").textContent;
    preview.querySelector("h3").textContent =
      'Set status to "' + statusName + '"';
    previewOffset.originalStatus = statusName;
  }

  const elementRect = e.target.getBoundingClientRect();
  preview.style.width = elementRect.width - 4 + "px";
  preview.style.height = elementRect.height - 4 + "px";

  previewOffset.x = e.clientX - elementRect.left;
  previewOffset.y = e.clientY - elementRect.top; // hack to make sure y of the offset meets
  // can't tell if this is intended behaviour

  document.body.appendChild(preview);
  e.dataTransfer.effectAllowed = "move";
  e.dataTransfer.setDragImage(emptyImg, 0, 0);
}

function dragOverHandle(e) {
  if (!draggingTask) return;

  preview.style.transform =
    "translate(" +
    (e.clientX - previewOffset.x + 9999) +
    "px, " +
    (e.clientY - previewOffset.y + 9999) +
    "px)";

  var parentStatusBox = document
    .elementsFromPoint(e.clientX, e.clientY)
    .find((x) => x.classList.contains("flex-status"));

  if (parentStatusBox) {
    const statusName =
      parentStatusBox.querySelector(".status-head > p").textContent;
    preview.querySelector("h3").textContent =
      'Set status to "' + statusName + '"';
    if (statusName == previewOffset.originalStatus)
      preview.style.opacity = "0.5";
    else preview.style.opacity = "1";
  } else {
    preview.querySelector("h3").textContent =
      'Set status to "' + previewOffset.originalStatus + '"';
    preview.style.opacity = "0.5";
  }

  e.preventDefault();
  e.dataTransfer.dropEffect = "move";
}

function dragEndHandle(e) {
  if (!draggingTask) return;

  e.target.classList.remove("dragging");
  var parentStatusBox = document
    .elementsFromPoint(e.clientX, e.clientY)
    .find((x) => x.classList.contains("flex-status"));

  // if parent status box exists and is not the same as original:
  if (
    parentStatusBox &&
    !parentStatusBox
      .querySelector(".status-tasks")
      .childNodes.values()
      .find((x) => x == e.target)
  ) {
    // we don't need to update it now since it will be updated once we refresh
    // parentStatusBox.querySelector('.status-list').appendChild(e.target);

    // update dragging server-side
    const postId = e.target.id.slice(-10);
    const post = boardContent.find((x) => x.task_id == postId);
    const statusId = parseInt(parentStatusBox.parentElement.id.slice(-1));

    fetchWithAuth(`/api/tasks/${postId}`, {
      method: "PATCH",
      body: JSON.stringify({
        title: post.title,
        status: statusId,
        content: post.content,
        importance: post.importance,
        assigned_to: post.assigned_to,
      }),
      headers: { "Content-Type": "application/json" },
    }).then((resp) => {
      // console.log(resp.json());
      loadAllPosts();
    });
  }
  // console.log(e.target);
  // console.log(parentStatusBox);

  preview.style.left = "-9999px";
  preview.style.top = "-9999px";
  preview.style.transform = "";
}

// connect handles

document.addEventListener("DOMContentLoaded", loadAllPosts);
document.addEventListener("dragstart", dragStartHandle);
document.addEventListener("dragover", dragOverHandle);
document.addEventListener("dragend", dragEndHandle);
document.addEventListener("click", clickHandle);
