let preview = document.querySelector('.hover-preview');
let previewOffset = {x: null, y: null, originalStatus: null};

const emptyImg = document.createElement('img'); 
emptyImg.src = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';

document.addEventListener("dragstart", (e) => {
    e.target.classList.add('dragging');

    var parentStatusBox = document.elementsFromPoint(e.clientX, e.clientY)
                                  .find((x) => x.classList.contains('flex-status'));
    if (parentStatusBox) {
        const statusName = parentStatusBox.querySelector('.status-head > h2').textContent;
        preview.querySelector('h3').textContent = "Set status to \"" + statusName + "\"";
        previewOffset.originalStatus = statusName;
    }

    const elementRect = e.target.getBoundingClientRect();
    preview.style.width = elementRect.width + 'px';
    preview.style.height = elementRect.height + 'px';

    previewOffset.x = e.layerX;
    previewOffset.y = e.clientY - elementRect.top;

    document.body.appendChild(preview);
    e.dataTransfer.setDragImage(emptyImg, 0, 0);
})

document.addEventListener("dragover", (e) => {
    preview.style.transform = 'translate(' + (e.clientX - previewOffset.x + 9999) + 'px, '
                            + (e.clientY - previewOffset.y + 9999) + 'px)';

    var parentStatusBox = document.elementsFromPoint(e.clientX, e.clientY)
                                  .find((x) => x.classList.contains('flex-status'));

    if (parentStatusBox) {
        const statusName = parentStatusBox.querySelector('.status-head > h2').textContent;
        preview.querySelector('h3').textContent = "Set status to \"" + statusName + "\"";
        if (statusName == previewOffset.originalStatus)
            preview.style.opacity = '0.5';
        else
            preview.style.opacity = '1';
    } else {
        preview.querySelector('h3').textContent = "Set status to \"" + previewOffset.originalStatus + "\"";
        preview.style.opacity = '0.5';
    }
    // console.log(e.target.closest('.flex-status'));
});

document.addEventListener("dragend", (e) => {
    e.target.classList.remove('dragging');
    var parentStatusBox = document.elementsFromPoint(e.clientX, e.clientY)
                                  .find((x) => x.classList.contains('flex-status'));

    if (parentStatusBox && !parentStatusBox.querySelector('.status-list').childNodes.values().find((x) => x == e.target)) {
        parentStatusBox.querySelector('.status-list').appendChild(e.target);
    }
    console.log(e.target);
    console.log(parentStatusBox);

    preview.style.left = '-9999px';
    preview.style.top = '-9999px';
    preview.style.transform = '';
});