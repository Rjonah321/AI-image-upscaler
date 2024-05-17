document.addEventListener("DOMContentLoaded", function() {
    const uploadButton = document.getElementById("upload-button");
    const imageInput = document.getElementById("image-input");
    const uploadForm = document.getElementById("upload-form");
    const enhanceOptions = document.getElementById("enhance-options");
    const enhanceButton = document.getElementById("enhance-button");
    const loadingBar = document.getElementById("loading-bar");
    const imageContainer = document.getElementById("image-container");
    const uploadText = document.getElementById("upload-text");
    const imageModal = document.getElementById("image-modal");
    const modalClose = document.getElementById("modal-close");
    const beforeImage = document.getElementById("before-image");
    const afterImage = document.getElementById("after-image");
    const downloadButton = document.getElementById("download-button");

    uploadButton.addEventListener("click", function() {
        imageInput.click();
    });

    imageInput.addEventListener("change", function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement("img");
                img.src = e.target.result;
                img.id = "uploaded-image";
                img.alt = "Uploaded Image";

                imageContainer.innerHTML = "";
                imageContainer.appendChild(img);
                enhanceOptions.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });

    uploadForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const formData = new FormData(uploadForm);
        loadingBar.style.display = "block";

        fetch("/", {
            method: "POST",
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            loadingBar.style.display = "none";
            const url = URL.createObjectURL(blob);
            afterImage.src = url;
            downloadButton.href = url;

            const uploadedImage = document.getElementById("uploaded-image");
            if (uploadedImage) {
                beforeImage.src = uploadedImage.src;
            }

            imageModal.style.display = "block";
        })
        .catch(error => {
            loadingBar.style.display = "none";
            console.error("Error enhancing image:", error);
        });
    });

    modalClose.addEventListener("click", function() {
        imageModal.style.display = "none";
    });

    window.addEventListener("click", function(event) {
        if (event.target === imageModal) {
            imageModal.style.display = "none";
        }
    });
});