import re
from datetime import date, timedelta
from django import forms
from .models import WholesaleEnquiry

class WholesaleEnquiryForm(forms.ModelForm):
    class Meta:
        model = WholesaleEnquiry
        fields = [
            'business_name', 'contact_person', 'phone_number', 
            'business_type', 'delivery_location', 'delivery_date', 
            'required_products', 'approx_quantity', 'additional_notes', 
            'requirement_file'
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={
                'placeholder': 'எ.கா. அன்னபூர்ணா கேட்டரிங் / ஹோட்டல்', 
                'class': 'form-input', 
                'required': True
            }),
            'contact_person': forms.TextInput(attrs={
                'placeholder': 'உங்கள் பெயர்', 
                'class': 'form-input', 
                'required': True
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '10 இலக்க மொபைல் எண் (எ.கா. 9876543210)', 
                'class': 'form-input', 
                'required': True, 
                'maxlength': '10'
            }),
            'business_type': forms.Select(attrs={
                'class': 'form-select', 
                'required': True
            }),
            'delivery_location': forms.TextInput(attrs={
                'placeholder': 'மண்டபம்/கடை/ஹோட்டல் முகவரி மற்றும் ஊர்', 
                'class': 'form-input', 
                'required': True
            }),
            'delivery_date': forms.DateInput(attrs={
                'class': 'form-input', 
                'type': 'date', 
                'required': True
            }),
            'required_products': forms.TextInput(attrs={
                'placeholder': 'எ.கா. தக்காளி, வெங்காயம், உருளை, அரிசி...', 
                'class': 'form-input', 
                'required': True
            }),
            'approx_quantity': forms.TextInput(attrs={
                'placeholder': 'எ.கா. 50 kg, 200 kg, 10 மூட்டை', 
                'class': 'form-input', 
                'required': True
            }),
            'additional_notes': forms.Textarea(attrs={
                'placeholder': 'குறிப்பிட்ட தரம், கட் காய்கறி தேவை அல்லது சிறப்பு விவரங்களை இங்கே குறிப்பிடவும்..', 
                'class': 'form-textarea', 
                'rows': 3
            }),
            'requirement_file': forms.FileInput(attrs={
                'class': 'file-input', 
                'id': 'file-upload', 
                'accept': '.pdf,.xlsx,.xls,.png,.jpg,.jpeg'
            }),
        }

    # 1. STRICT 10-DIGIT MOBILE NUMBER
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        digits = re.sub(r'\D', '', phone)
        if len(digits) < 10:
            raise forms.ValidationError("மொபைல் எண் 10 இலக்கங்களுக்கு குறைவாக இருக்கக்கூடாது.")
        if len(digits) > 10:
            raise forms.ValidationError("மொபைல் எண் 10 இலக்கங்களுக்கு அதிகமாக இருக்கக்கூடாது.")
        if not digits[0] in '6789':
            raise forms.ValidationError("சரியான மொபைல் எண்ணை உள்ளிடவும் (6, 7, 8 அல்லது 9 இல் தொடங்க வேண்டும்).")
        return digits

    # 2. DELIVERY DATE: STRICTLY TODAY TILL NEXT 2 DAYS (e.g. 5th till 7th)
    def clean_delivery_date(self):
        deliv_date = self.cleaned_data.get('delivery_date')
        if not deliv_date:
            raise forms.ValidationError("விநியோக தேதியை தேர்ந்தெடுக்கவும்.")

        today = date.today()
        max_booking_date = today + timedelta(days=2)

        if deliv_date < today:
            raise forms.ValidationError("கடந்த தேதிகளை முன்பதிவு செய்ய முடியாது.")
        if deliv_date > max_booking_date:
            raise forms.ValidationError(
                f"டெலிவரி தேதியை இன்றைய தேதியிலிருந்து 2-3 நாட்களுக்குள் மட்டுமே முன்பதிவு செய்ய முடியும் ({today.strftime('%d/%m/%Y')} முதல் {max_booking_date.strftime('%d/%m/%Y')} வரை)."
            )
        return deliv_date

    # 3. BUSINESS NAME
    def clean_business_name(self):
        name = self.cleaned_data.get('business_name', '').strip()
        if len(name) < 3:
            raise forms.ValidationError("வணிகப் பெயர் குறைந்தது 3 எழுத்துக்களாக இருக்க வேண்டும்.")
        return name

    # 4. CONTACT PERSON
    def clean_contact_person(self):
        person = self.cleaned_data.get('contact_person', '').strip()
        if len(person) < 2:
            raise forms.ValidationError("தொடர்பு நபர் பெயர் சரியானதாக இருக்க வேண்டும்.")
        return person

    # 5. LOCATION
    def clean_delivery_location(self):
        loc = self.cleaned_data.get('delivery_location', '').strip()
        if len(loc) < 4:
            raise forms.ValidationError("முழுமையான விநியோக முகவரியை உள்ளிடவும்.")
        return loc

    # 6. FILE VALIDATION (Max 10MB)
    def clean_requirement_file(self):
        file = self.cleaned_data.get('requirement_file')
        if file:
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("கோப்பின் அளவு 10MB-க்குள் இருக்க வேண்டும்.")
            allowed_extensions = ('.pdf', '.xlsx', '.xls', '.jpg', '.jpeg', '.png')
            if not file.name.lower().endswith(allowed_extensions):
                raise forms.ValidationError("PDF, Excel (.xlsx, .xls) அல்லது படங்கள் (.jpg, .png) மட்டுமே அனுமதிக்கப்படுகின்றன.")
        return file