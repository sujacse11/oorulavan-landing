import urllib.parse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (
    SiteSetting, ProductCategory, TargetAudience, 
    ProcessStep, KeyProduct, WhyChooseUs, WholesaleEnquiry
)
from .forms import WholesaleEnquiryForm

def index(request):
    settings = SiteSetting.objects.first()
    if not settings:
        settings = SiteSetting.objects.create()

    categories = ProductCategory.objects.all()
    audiences = TargetAudience.objects.all()
    steps = ProcessStep.objects.all()
    products = KeyProduct.objects.all()
    why_us = WhyChooseUs.objects.all()

    form = WholesaleEnquiryForm()

    if request.method == 'POST':
        # Handles both text fields (request.POST) and file uploads (request.FILES)
        form = WholesaleEnquiryForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. SAVE ENQUIRY & FILE TO DATABASE (Saved into media/enquiries/)
            enquiry = form.save()

            # 2. FORMAT THE EXACT WHATSAPP MESSAGE
            message_text = f"""வணக்கம் ஊர் உழவன்! புதிய மொத்த விலை விசாரணை:
-------------------------------------
🏢 வணிகம்: {enquiry.business_name}
👤 தொடர்பு நபர்: {enquiry.contact_person}
📞 மொபைல்: {enquiry.phone_number}
🏷️ வகை: {enquiry.business_type}
📍 விநியோக இடம்: {enquiry.delivery_location}
📅 தேவைப்படும் தேதி: {enquiry.delivery_date}
📦 தேவையான பொருட்கள்: {enquiry.required_products}
⚖️ அளவு/எடை: {enquiry.approx_quantity}
-------------------------------------
(இணைப்பு / தேவைப் பட்டியல் போட்டோவை இத்துடன் அனுப்புகிறேன்)"""

            # 3. REDIRECT DIRECTLY TO WHATSAPP CHAT
            encoded_message = urllib.parse.quote(message_text)
            clean_wa_number = settings.whatsapp_number.replace('+', '').replace(' ', '')
            whatsapp_url = f"https://wa.me/{clean_wa_number}?text={encoded_message}"

            return redirect(whatsapp_url)
        else:
            messages.error(request, "படிவத்தில் சில பிழைகள் உள்ளன. சிவப்பு நிற எச்சரிக்கைகளை சரிபார்க்கவும்.")

    context = {
        'settings': settings,
        'categories': categories,
        'audiences': audiences,
        'steps': steps,
        'products': products,
        'why_us': why_us,
        'form': form,
    }
    return render(request, 'landing/index.html', context)