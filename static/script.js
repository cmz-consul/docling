const fileBtn = document.getElementById('fileBtn');
const urlBtn = document.getElementById('urlBtn');
const fileInput = document.getElementById('fileInput');
const urlInput = document.getElementById('urlInput');
const markdownBtn = document.getElementById('markdownBtn');
const jsonBtn = document.getElementById('jsonBtn');
const convertBtn = document.getElementById('convertBtn');
const complete = document.getElementById('complete');
const downloadLink = document.getElementById('downloadLink');
const themeBtn = document.getElementById('themeBtn');
const themeIcon = document.getElementById('themeIcon');
const fileInputElement = document.getElementById('file');
const fileMessage = document.getElementById('fileMessage');
const fileDropArea = fileInput.querySelector('.file-drop-area');
const urlInputElement = document.getElementById('url');
const urlMessage = document.getElementById('urlMessage');

fileBtn.addEventListener('click', () => {
    fileBtn.classList.add('active');
    urlBtn.classList.remove('active');
    fileInput.classList.remove('hidden');
    urlInput.classList.add('hidden');
});

urlBtn.addEventListener('click', () => {
    urlBtn.classList.add('active');
    fileBtn.classList.remove('active');
    urlInput.classList.remove('hidden');
    fileInput.classList.add('hidden');
});

markdownBtn.addEventListener('click', () => {
    markdownBtn.classList.add('active');
    jsonBtn.classList.remove('active');
});

jsonBtn.addEventListener('click', () => {
    jsonBtn.classList.add('active');
    markdownBtn.classList.remove('active');
});

// Feedback para arquivo
fileInputElement.addEventListener('change', () => {
    if (fileInputElement.files.length > 0) {
        fileMessage.textContent = fileInputElement.files[0].name;
        fileDropArea.classList.add('selected');
    } else {
        fileMessage.textContent = 'Selecione um arquivo PDF';
        fileDropArea.classList.remove('selected');
    }
});

// Feedback para URL
urlInputElement.addEventListener('input', () => {
    if (urlInputElement.value.trim()) {
        urlInputElement.classList.add('filled');
        urlMessage.classList.remove('hidden');
    } else {
        urlInputElement.classList.remove('filled');
        urlMessage.classList.add('hidden');
    }
});

convertBtn.addEventListener('click', async () => {
    const sourceType = fileBtn.classList.contains('active') ? 'file' : 'url';
    const format = markdownBtn.classList.contains('active') ? 'markdown' : 'json';
    const formData = new FormData();

    if (sourceType === 'file') {
        const file = fileInputElement.files[0];
        if (!file) return alert('Selecione um arquivo!');
        formData.append('pdfFile', file);
    } else {
        const url = urlInputElement.value;
        if (!url) return alert('Digite uma URL!');
        formData.append('pdfUrl', url);
    }
    formData.append('format', format);

    convertBtn.disabled = true;
    convertBtn.querySelector('.loader').classList.remove('hidden');
    complete.classList.add('hidden');

    try {
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || 'Erro ao converter o arquivo');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.download = `converted_file.${format === 'json' ? 'json' : 'md'}`;
        complete.classList.remove('hidden');

        // Reseta o feedback após conversão
        if (sourceType === 'file') {
            fileMessage.textContent = 'Selecione um arquivo PDF';
            fileDropArea.classList.remove('selected');
            fileInputElement.value = '';
        } else {
            urlInputElement.value = '';
            urlInputElement.classList.remove('filled');
            urlMessage.classList.add('hidden');
        }
    } catch (error) {
        alert('Erro: ' + error.message);
    } finally {
        convertBtn.disabled = false;
        convertBtn.querySelector('.loader').classList.add('hidden');
    }
});

// Alternar tema
themeBtn.addEventListener('click', () => {
    document.body.classList.toggle('light');
    themeIcon.innerHTML = document.body.classList.contains('light') 
        ? '<path d="M12 8a4 4 0 0 0-4 4 4 4 0 0 0 4 4 4 4 0 0 0 4-4 4 4 0 0 0-4-4zm0 10a6 6 0 0 1-6-6 6 6 0 0 1 6-6 6 6 0 0 1 6 6 6 6 0 0 1-6 6zm-9-6h2m14 0h2m-9-9v2m0 14v2"/>'
        : '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>';
});