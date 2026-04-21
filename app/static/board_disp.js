let preview = document.querySelector('.hover-preview');
let previewOffset = {x: null, y: null};

const emptyImg = document.createElement('img'); 
emptyImg.src = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';

document.addEventListener("dragstart", (e) => {
    e.target.classList.add('dragging');

    const elementRect = e.target.getBoundingClientRect();
    preview.style.width = elementRect.width + 'px';
    preview.style.height = elementRect.height + 'px';

    previewOffset.x = e.layerX;
    previewOffset.y = e.clientY - elementRect.top;

    console.log(e);
    console.log(elementRect);
    console.log(previewOffset);

    document.body.appendChild(preview);
    e.dataTransfer.setDragImage(emptyImg, 0, 0);
})

document.addEventListener("dragover", (e) => {
    console.log(e); 

    preview.style.left = e.clientX - previewOffset.x + "px";
    preview.style.top = e.clientY - previewOffset.y + "px";
});

document.addEventListener("dragend", (e) => {
    e.target.classList.remove('dragging');
    preview.style.left = '-9999px';
    preview.style.top = '-9999px';
});