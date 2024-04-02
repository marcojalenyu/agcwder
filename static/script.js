var inputImg = document.getElementById('imgPreview');
inputImg.onload = function() {
    resizeImg();
}

var outputImg = document.getElementById('outputImage');
if (outputImg != null) {
    outputImg.onload = function() {
        resizeImg();
    }
}

window.onload = function() {
    resizeImg();
}

function resizeImg() {
    console.log("Resizing image");
    var inputImg = document.getElementById('imgPreview');
    var outputImg = document.getElementById('outputImage');
    // Get ratio of image and set width and height accordingly
    if (inputImg.width > inputImg.height) {
        inputImg.style.width = "100%";
        inputImg.style.height = "auto";
        if (outputImg != null) {
            outputImg.style.width = "100%";
            outputImg.style.height = "auto";
        }
    } else {
        inputImg.style.width = "auto";
        inputImg.style.height = "350px";
        if (outputImg != null) {
            outputImg.style.width = "auto";
            outputImg.style.height = "350px";
        }
    }

}

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
        var outputImg = document.getElementById('outputImage')
        if (outputImg != null) {
            outputImg.remove();
            document.getElementById('download-btn').remove();
        }
    };
    reader.readAsDataURL(file);
});