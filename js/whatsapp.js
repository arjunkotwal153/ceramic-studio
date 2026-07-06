const OWNER_WHATSAPP = "919876543210";

document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submitBtn');
    if (!submitBtn) return;

    submitBtn.addEventListener('click', (e) => {
        e.preventDefault();

        // Remove previous validation styling
        document.querySelectorAll('.wa-error-msg').forEach(el => el.remove());
        document.querySelectorAll('.wa-error-border').forEach(el => {
            el.style.borderColor = '';
            el.classList.remove('wa-error-border');
        });

        const fields = [
            { id: 'name', label: 'Name' },
            { id: 'phone', label: 'Phone Number' },
            { id: 'brand', label: 'Car Brand' },
            { id: 'model', label: 'Car Model' },
            { id: 'service', label: 'Selected Service' },
            { id: 'date', label: 'Preferred Date' },
            { id: 'time', label: 'Preferred Time' }
        ];

        let hasError = false;
        const data = {};

        fields.forEach(field => {
            const el = document.getElementById(field.id);
            const val = el ? el.value.trim() : '';
            data[field.id] = val;

            if (!val) {
                hasError = true;
                if (el) {
                    el.classList.add('wa-error-border');
                    el.style.borderColor = '#e8462a';
                    const errorSpan = document.createElement('span');
                    errorSpan.className = 'wa-error-msg';
                    errorSpan.style.color = '#e8462a';
                    errorSpan.style.fontSize = '0.85rem';
                    errorSpan.style.marginTop = '6px';
                    errorSpan.style.display = 'block';
                    errorSpan.textContent = `${field.label} is required.`;

                    // Reset border color when typing
                    el.addEventListener('input', function removeError() {
                        el.style.borderColor = '';
                        el.classList.remove('wa-error-border');
                        if (errorSpan.parentNode) {
                            errorSpan.parentNode.removeChild(errorSpan);
                        }
                        el.removeEventListener('input', removeError);
                    });

                    if (el.parentNode) {
                        el.parentNode.insertBefore(errorSpan, el.nextSibling);
                    }
                }
            }
        });

        const notesEl = document.getElementById('notes');
        const notes = notesEl ? notesEl.value.trim() : '';
        data['notes'] = notes || 'None';

        if (hasError) {
            return;
        }

        const originalContent = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.style.opacity = '0.7';
        submitBtn.style.cursor = 'not-allowed';
        submitBtn.innerHTML = 'Preparing WhatsApp...';

        const msg = `🚗 *NEW BOOKING REQUEST*\n\n👤 Name:\n${data.name}\n\n📞 Phone:\n${data.phone}\n\n🚘 Car Brand:\n${data.brand}\n\n🚙 Model:\n${data.model}\n\n✨ Service:\n${data.service}\n\n📅 Preferred Date:\n${data.date}\n\n🕒 Preferred Time:\n${data.time}\n\n📝 Additional Notes:\n${data.notes}\n\n--------------------------------\n\nBooking submitted from the PRO STUDIO website.`;

        setTimeout(() => {
            const phoneNumber = OWNER_WHATSAPP.replace(/\D/g, ''); // Ensure only digits
            
            // Use the universal WhatsApp API endpoint which avoids the wa.me deeplink 404 bug
            const targetUrl = `https://api.whatsapp.com/send?phone=${phoneNumber}&text=${encodeURIComponent(msg)}`;
                
            window.open(targetUrl, '_blank');
            submitBtn.disabled = false;
            submitBtn.style.opacity = '';
            submitBtn.style.cursor = '';
            submitBtn.innerHTML = originalContent;
        }, 900);
    });
});
