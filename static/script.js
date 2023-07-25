const iptPhoto = document.getElementById('photo');
const preview = document.getElementById('preview');
const error = document.getElementById('error');
const btnFile = document.getElementById('btnFile');
const form = document.getElementById('form');

iptPhoto.addEventListener('change', handleFileSelect);
btnFile.addEventListener('dragenter', highlight);
btnFile.addEventListener('dragover', highlight);
btnFile.addEventListener('dragleave', unhighlight);
btnFile.addEventListener('drop', handleDrop);

function handleFileSelect() {
    if (iptPhoto.files.length > 0) {
        const fileName = iptPhoto.files[0].name;
        updatePreview(fileName);
    } else {
        preview.textContent = 'Nenhuma imagem enviada.';
    }
}

function highlight(e) {
    e.preventDefault();
    btnFile.classList.add('highlight');
}

function unhighlight(e) {
    e.preventDefault();
    btnFile.classList.remove('highlight');
}

function handleDrop(e) {
    e.preventDefault();
    btnFile.classList.remove('highlight');

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
        iptPhoto.files = files;
        const fileName = files[0].name;
        updatePreview(fileName);
    }
}

function updatePreview(fileName) {  
    preview.textContent = fileName;
    preview.style.color = '#7203FF';
    error.style.display = 'none';
}
