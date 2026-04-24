/*
handle general clicking on webpage, this should cover:
*   clicking on dropdown menus (all forms)
*/

function optionBtnHandle(id) {
  var dropdownMenu = document.querySelector(
    `#task_${id} .option-dropdown-menu`,
  );
  dropdownMenu.hidden = !dropdownMenu.hidden;
}

function editBtnHandle(id) {
  var dropdownMenu = document.querySelector(
    `#task_${id} .option-dropdown-menu`,
  );
  dropdownMenu.hidden = true;

  document.querySelector(".modal-base").classList.remove("hidden");
}

function deleteBtnHandle(id) {
  var dropdownMenu = document.querySelector(
    `#task_${id} .option-dropdown-menu`,
  );
  dropdownMenu.hidden = true;
}

function closeModal() {
  document.querySelector(".modal-base").classList.add("hidden");
}

var clickMap = {
  optionbtn: optionBtnHandle,
  editbtn: editBtnHandle,
  deletebtn: deleteBtnHandle,
  closemodal: closeModal,
};

function clickHandle(e) {
  // https://stackoverflow.com/questions/46732637/best-way-to-handle-clicks-on-buttons-in-javascript-vanilla
  // do something similar to this for edit, dropdowns and shit
  if (!e.target.dataset.handler) return;
  handlerArgs = e.target.dataset.handler.split("_");
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
      parentStatusBox.querySelector(".status-head > h2").textContent;
    preview.querySelector("h3").textContent =
      'Set status to "' + statusName + '"';
    previewOffset.originalStatus = statusName;
  }

  const elementRect = e.target.getBoundingClientRect();
  preview.style.width = elementRect.width + "px";
  preview.style.height = elementRect.height + "px";

  previewOffset.x = e.layerX;
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
      parentStatusBox.querySelector(".status-head > h2").textContent;
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

  if (
    parentStatusBox &&
    !parentStatusBox
      .querySelector(".status-list")
      .childNodes.values()
      .find((x) => x == e.target)
  ) {
    parentStatusBox.querySelector(".status-list").appendChild(e.target);
  }
  // console.log(e.target);
  // console.log(parentStatusBox);

  preview.style.left = "-9999px";
  preview.style.top = "-9999px";
  preview.style.transform = "";

  // add stuff to update main page
}

// connect handles

document.addEventListener("dragstart", dragStartHandle);
document.addEventListener("dragover", dragOverHandle);
document.addEventListener("dragend", dragEndHandle);
document.addEventListener("click", clickHandle);
