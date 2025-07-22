// State
let selectedImage = null;

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded fired');
    // DOM elements (now inside DOMContentLoaded)
    const imageInput = document.getElementById('imageInput');
    const scanBtn = document.getElementById('scanBtn');
    const ocrText = document.getElementById('ocrText');
    const result = document.getElementById('result');
    const uploadBtn = document.getElementById('uploadBtn');
    console.log('imageInput:', imageInput);
    console.log('scanBtn:', scanBtn);
    console.log('ocrText:', ocrText);
    console.log('result:', result);
    console.log('uploadBtn:', uploadBtn);

    // Add event listeners
    if (uploadBtn && imageInput) {
        uploadBtn.addEventListener('click', function() {
            imageInput.click();
            console.log('Upload Receipt button clicked, file input triggered');
        });
    }
    if (imageInput) {
        imageInput.addEventListener('change', handleImageSelect);
        console.log('imageInput event listener attached');
    } else {
        console.log('imageInput not found');
    }
    if (scanBtn) {
        scanBtn.addEventListener('click', scanReceipt);
        console.log('scanBtn event listener attached');
    } else {
        console.log('scanBtn not found');
    }
    // Initially disable scan button
    if (scanBtn) scanBtn.disabled = true;

    function handleImageSelect(event) {
        console.log('handleImageSelect called');
        const file = event.target.files[0];
        if (file) {
            console.log('File selected:', file);
            // Validate file type
            if (!file.type.startsWith('image/')) {
                alert('Please select an image file.');
                return;
            }
            // Create preview
            const reader = new FileReader();
            reader.onload = function(e) {
                selectedImage = e.target.result;
                showImagePreview(selectedImage);
                if (scanBtn) scanBtn.disabled = false;
                console.log('Image loaded and preview shown');
            };
            reader.readAsDataURL(file);
        } else {
            console.log('No file selected');
        }
    }

    function showImagePreview(imageSrc) {
        console.log('showImagePreview called');
        // Remove existing preview
        const existingPreview = document.querySelector('.preview-image');
        if (existingPreview) {
            existingPreview.remove();
            console.log('Existing preview removed');
        }
        // Create new preview
        const preview = document.createElement('img');
        preview.className = 'preview-image';
        preview.src = imageSrc;
        preview.alt = 'Receipt Preview';
        // Insert after file input
        const previewContainer = document.getElementById('image-preview-container');
        previewContainer.innerHTML = '';  // Clear previous previews
        previewContainer.appendChild(preview);
        console.log('Preview image inserted');
    }

    function scanReceipt() {
        console.log('scanReceipt called');
        if (!selectedImage) {
            alert('Please select an image first.');
            console.log('No image selected');
            return;
        }
        // Show loading state
        showLoading(true);
        if (scanBtn) scanBtn.disabled = true;
        ocrText.textContent = 'Scanning receipt...';
        // Perform OCR using Tesseract.js
        Tesseract.recognize(
            selectedImage,
            'eng',
            {
                logger: m => console.log(m)
            }
        ).then(({ data: { text } }) => {
            // Display results
            ocrText.textContent = text;
            showLoading(false);
            if (scanBtn) scanBtn.disabled = false;
            // Parse and extract receipt data
            const extractedData = parseReceiptData(text);
            displayExtractedData(extractedData);
            console.log('OCR complete, text extracted');
        }).catch(error => {
            console.error('OCR Error:', error);
            ocrText.textContent = 'Error scanning receipt. Please try again.';
            showLoading(false);
            if (scanBtn) scanBtn.disabled = false;
        });
    }

    function showLoading(show) {
        console.log('showLoading called, show:', show);
        // Remove existing loading spinner
        const existingSpinner = document.querySelector('.loading');
        if (existingSpinner) {
            existingSpinner.remove();
            console.log('Existing spinner removed');
        }
        if (show) {
            const loading = document.createElement('div');
            loading.className = 'loading show';
            loading.innerHTML = '<div class="spinner"></div><p>Processing receipt...</p>';
            // Place loading spinner after scan button
            scanBtn.parentNode.insertBefore(loading, scanBtn.nextSibling);
            console.log('Loading spinner inserted');
        }
    }

    function parseReceiptData(text) {
        console.log('parseReceiptData called');
        const lines = text.split('\n').filter(line => line.trim());
        const data = {
            total: null,
            date: null,
            items: [],
            store: null
        };
        // Extract total (look for patterns like $XX.XX or TOTAL: $XX.XX)
        const totalPattern = /(?:total|amount|sum)[:\s]*\$?(\d+\.\d{2})/i;
        const totalMatch = text.match(totalPattern);
        if (totalMatch) {
            data.total = parseFloat(totalMatch[1]);
            console.log('Total found:', data.total);
        }
        // Extract date (look for common date patterns)
        const datePattern = /(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})|(\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2})/;
        const dateMatch = text.match(datePattern);
        if (dateMatch) {
            data.date = dateMatch[0];
            console.log('Date found:', data.date);
        }
        // Extract store name (usually in first few lines)
        if (lines.length > 0) {
            data.store = lines[0].trim();
            console.log('Store found:', data.store);
        }
        // Extract items (lines with prices)
        const itemPattern = /(.+?)\s+\$(\d+\.\d{2})/;
        lines.forEach(line => {
            const itemMatch = line.match(itemPattern);
            if (itemMatch) {
                data.items.push({
                    name: itemMatch[1].trim(),
                    price: parseFloat(itemMatch[2])
                });
                console.log('Item found:', itemMatch[1].trim(), itemMatch[2]);
            }
        });
        return data;
    }

    function displayExtractedData(data) {
        console.log('displayExtractedData called');
        // Create a structured display of extracted data
        let structuredText = '=== EXTRACTED RECEIPT DATA ===\n\n';
        if (data.store) {
            structuredText += `Store: ${data.store}\n`;
        }
        if (data.date) {
            structuredText += `Date: ${data.date}\n`;
        }
        if (data.items.length > 0) {
            structuredText += '\nItems:\n';
            data.items.forEach(item => {
                structuredText += `  ${item.name}: $${item.price.toFixed(2)}\n`;
            });
        }
        if (data.total) {
            structuredText += `\nTotal: $${data.total.toFixed(2)}\n`;
        }
        // Add the structured data to the display
        ocrText.textContent = structuredText + '\n\n=== RAW OCR TEXT ===\n' + ocrText.textContent;
        console.log('displayExtractedData finished');
    }
}); 