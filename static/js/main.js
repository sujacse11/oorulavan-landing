function openWhatsAppChat(phone, message) {
    const cleanPhone = phone.replace(/\D/g, '');
    const encodedMsg = encodeURIComponent(message);
    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

    let url = isMobile 
        ? `whatsapp://send?phone=${cleanPhone}&text=${encodedMsg}` 
        : `https://web.whatsapp.com/send?phone=${cleanPhone}&text=${encodedMsg}`;

    const win = window.open(url, '_blank');
    if (!win || win.closed || typeof win.closed === 'undefined') {
        window.open(`https://wa.me/${cleanPhone}?text=${encodedMsg}`, '_blank');
    }
}

document.addEventListener('DOMContentLoaded', () => {

    // 1. DELIVERY DATE: STRICTLY TODAY TILL NEXT 2 DAYS (e.g. 5th till 7th)
    const dateInput = document.querySelector('input[name="delivery_date"]');
    if (dateInput) {
        const today = new Date();
        const minDateStr = today.toISOString().split('T')[0];
        dateInput.setAttribute('min', minDateStr);

        const maxDate = new Date();
        maxDate.setDate(today.getDate() + 2);
        const maxDateStr = maxDate.toISOString().split('T')[0];
        dateInput.setAttribute('max', maxDateStr);

        const parentGroup = dateInput.closest('.form-group');
        if (parentGroup && !parentGroup.querySelector('.date-hint')) {
            const hint = document.createElement('small');
            hint.className = 'date-hint';
            hint.style.color = '#15803D';
            hint.style.fontSize = '11px';
            hint.style.marginTop = '4px';
            hint.innerHTML = '⚡ <em>இன்று முதல் அடுத்த 2-3 நாட்களுக்குள் மட்டுமே டெலிவரி எடுக்க முடியும்.</em>';
            parentGroup.appendChild(hint);
        }
    }

    // 2. STRICT 10-DIGIT MOBILE NUMBER
    const phoneInput = document.querySelector('input[name="phone_number"]');
    if (phoneInput) {
        phoneInput.setAttribute('maxlength', '10');
        phoneInput.addEventListener('input', (e) => {
            let val = e.target.value.replace(/\D/g, '');
            if (val.length > 10) val = val.slice(0, 10);
            e.target.value = val;
        });
    }

    // 3. FILE UPLOAD LIVE PREVIEW
    const fileInput = document.getElementById('file-upload') || document.querySelector('input[name="requirement_file"]');
    const uploadDropzone = document.querySelector('.upload-dropzone');

    if (fileInput && uploadDropzone) {
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            let preview = uploadDropzone.querySelector('.file-preview-name');
            if (!preview) {
                preview = document.createElement('div');
                preview.className = 'file-preview-name';
                uploadDropzone.appendChild(preview);
            }

            if (file) {
                if (file.size > 10 * 1024 * 1024) {
                    alert('கோப்பு அளவு 10MB-க்கு அதிகமாக உள்ளது. 10MB-க்குள் உள்ள கோப்பைத் தேர்ந்தெடுக்கவும்.');
                    fileInput.value = '';
                    preview.innerHTML = '';
                    return;
                }
                preview.innerHTML = `✅ <strong>தேர்ந்தெடுக்கப்பட்டது:</strong> ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
                preview.style.color = '#15803D';
                preview.style.marginTop = '8px';
                preview.style.fontSize = '11px';
            }
        });
    }

    // 4. CLIENT-SIDE SUBMIT CHECK
    const form = document.getElementById('rfq-form') || document.querySelector('form[method="POST"]');
    if (form) {
        form.addEventListener('submit', (e) => {
            const phoneVal = phoneInput ? phoneInput.value.replace(/\D/g, '') : '';
            const bName = form.querySelector('input[name="business_name"]')?.value.trim();
            const cPerson = form.querySelector('input[name="contact_person"]')?.value.trim();
            const dateVal = dateInput ? dateInput.value : '';

            if (!bName || bName.length < 3) {
                e.preventDefault();
                alert('தயவுசெய்து வணிகப் பெயரை சரியாக நிரப்பவும்.');
                form.querySelector('input[name="business_name"]')?.focus();
                return false;
            }

            if (!cPerson || cPerson.length < 2) {
                e.preventDefault();
                alert('தயவுசெய்து உங்கள் பெயரை உள்ளிடவும்.');
                form.querySelector('input[name="contact_person"]')?.focus();
                return false;
            }

            if (phoneVal.length !== 10) {
                e.preventDefault();
                alert('மொபைல் எண் சரியாக 10 இலக்கங்களாக இருக்க வேண்டும்!');
                phoneInput.focus();
                phoneInput.style.borderColor = '#DC2626';
                return false;
            }

            if (dateVal) {
                const selected = new Date(dateVal);
                const today = new Date();
                today.setHours(0, 0, 0, 0);

                const maxAllowed = new Date();
                maxAllowed.setDate(today.getDate() + 2);
                maxAllowed.setHours(23, 59, 59, 999);

                if (selected < today || selected > maxAllowed) {
                    e.preventDefault();
                    alert('டெலிவரி தேதியை இன்றைய தேதியிலிருந்து 2-3 நாட்களுக்குள் மட்டுமே தேர்ந்தெடுக்க முடியும்!');
                    dateInput.focus();
                    dateInput.style.borderColor = '#DC2626';
                    return false;
                }
            }
        });
    }

    // 5. DIRECT WHATSAPP BUTTON (Option 2)
    window.sendViaWhatsAppDirect = function() {
        const business = document.querySelector('input[name="business_name"]')?.value.trim();
        const contact = document.querySelector('input[name="contact_person"]')?.value.trim();
        const phone = document.querySelector('input[name="phone_number"]')?.value.trim();
        const bType = document.querySelector('select[name="business_type"]')?.value || 'B2B';
        const items = document.querySelector('input[name="required_products"]')?.value.trim();
        const qty = document.querySelector('input[name="approx_quantity"]')?.value.trim();
        const loc = document.querySelector('input[name="delivery_location"]')?.value.trim();
        const dateVal = dateInput ? dateInput.value : '';

        if (!business || !contact || !phone) {
            alert('தயவுசெய்து வணிகப் பெயர், உங்கள் பெயர் மற்றும் மொபைல் எண்ணை நிரப்பவும்!');
            document.querySelector('input[name="business_name"]')?.focus();
            return;
        }

        const msg = 
`*வணக்கம் ஊர் உழவன்! புதிய மொத்த விலை விசாரணை:*
-------------------------------------
🏢 *வணிகம்:* ${business}
👤 *தொடர்பு நபர்:* ${contact}
📞 *மொபைல்:* ${phone}
🏷️ *வகை:* ${bType}
📍 *விநியோக இடம்:* ${loc || 'குறிப்பிடப்படவில்லை'}
📅 *தேவைப்படும் தேதி:* ${dateVal || 'அடுத்த 2-3 நாட்களில்'}
📦 *தேவையான பொருட்கள்:* ${items || 'பட்டியல் பார்க்க'}
⚖️ *அளவு/எடை:* ${qty || 'பேச வேண்டும்'}
-------------------------------------
(இணைப்பு / தேவைப் பட்டியல் போட்டோவை இத்துடன் அனுப்புகிறேன்)`;

        openWhatsAppChat('919994021305', msg);
    };

    // 6. CAROUSEL SLIDER FUNCTION
    window.scrollSlider = function(containerId, distance) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.scrollBy({ left: distance, behavior: 'smooth' });
        setTimeout(() => updateDots(containerId), 250);
    };

    function updateDots(containerId) {
        const container = document.getElementById(containerId);
        const dotsContainer = container?.closest('.section')?.querySelector('.carousel-dots');
        if (!container || !dotsContainer) return;

        const dots = dotsContainer.querySelectorAll('.dot');
        const scrollPosition = container.scrollLeft;
        const maxScroll = container.scrollWidth - container.clientWidth;
        
        if (maxScroll <= 0 || dots.length === 0) return;

        const activeIndex = Math.min(
            dots.length - 1, 
            Math.round((scrollPosition / maxScroll) * (dots.length - 1))
        );

        dots.forEach((dot, idx) => {
            if (idx === activeIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }

    ['cat-grid', 'prod-grid'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('scroll', () => updateDots(id));
    });
});