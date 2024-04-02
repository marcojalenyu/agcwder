function downloadEnhancedImage(image) {
    const blob = base64ToBlob(image);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'enhanced_image.png';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function base64ToBlob(base64) {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: 'image/png' });
}

document.getElementById('imgInput').addEventListener('change', function() {
    var image = document.getElementById('imgPreview');
    var file = this.files[0];
    var reader = new FileReader();
    reader.onload = function(e) {
        image.src = e.target.result;
        // Clear the previous enhanced image and download button
        document.getElementById('outputImage').src = '';
        document.getElementById('download-btn').style.display = 'none';
    };
    reader.readAsDataURL(file);
});