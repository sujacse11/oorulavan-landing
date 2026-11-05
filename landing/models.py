from django.db import models

class SiteSetting(models.Model):
    site_name = models.CharField("தள பெயர்", max_length=100, default="ஊர் உழவன்")
    tagline = models.CharField("துணை வாசகம்", max_length=100, default="மொத்த விற்பனை")
    phone = models.CharField("தொலைபேசி எண்", max_length=50, default="+91 99940 21305")
    whatsapp_number = models.CharField("WhatsApp எண்", max_length=20, default="919994021305")
    email = models.EmailField("மின்னஞ்சல்", default="orders@oorulavan.com")
    location = models.CharField("முகவரி", max_length=200, default="மொத்த வியாபார வளாகம், தமிழ்நாடு - 641001")
    service_hours = models.CharField("சேவை நேரம்", max_length=100, default="24/7 திருமண ஆர்டர் சேவை")
    hero_title = models.CharField(
        "Hero முதன்மை தலைப்பு",
        max_length=255, 
        default="“உங்கள் வணிகத்திற்குத் தேவையான புதிய காய்கறிகள் மற்றும் பழங்கள் — நம்பிக்கையுடன் நேரடியாக விநியோகம்.”"
    )
    hero_description = models.TextField(
        "Hero விவர உரை",
        default="திருமண நிகழ்ச்சி, ஹோட்டல்கள், கேட்டரிங், காய்கறி மற்றும் பழக்கடைகளுக்கான தேவையான மொத்த காய்கறிகள், பழங்கள், அரிசி, மளிகைப் பொருட்கள் மற்றும் பிற அத்தியாவசியப் பொருட்கள் — அனைத்தும் நேரடியாக உங்கள் இடத்திற்கு."
    )

    class Meta:
        verbose_name = "தள அமைப்பு (Site Settings)"
        verbose_name_plural = "தள அமைப்பு (Site Settings)"

    def __str__(self):
        return self.site_name


class ProductCategory(models.Model):
    title = models.CharField("பிரிவு பெயர் (Tamil)", max_length=150)
    tag = models.CharField("Tag (e.g. Fresh Vegetables)", max_length=100)
    description = models.TextField("விவரம் (Description)")
    image_url = models.CharField("படம் URL (Image Link)", max_length=500, blank=True)
    order = models.PositiveIntegerField("வரிசை எண்", default=1)

    class Meta:
        verbose_name = "பொருட்களின் வகை (Category)"
        verbose_name_plural = "பொருட்களின் வகைகள் (Categories)"
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.tag})"


class TargetAudience(models.Model):
    title = models.CharField("தலைப்பு (e.g. ஹோட்டல்கள் (Hotels))", max_length=150)
    subtitle = models.CharField("துணைத் தலைப்பு", max_length=200)
    description = models.TextField("விவரம்")
    badge_left = models.CharField("இடது பேட்ஜ்", max_length=100)
    badge_right = models.CharField("வலது பேட்ஜ்", max_length=100)
    icon_type = models.CharField("ஐகான் வகை (hotel/food/catering/wedding/shop/office)", max_length=50, default="hotel")
    order = models.PositiveIntegerField("வரிசை எண்", default=1)

    class Meta:
        verbose_name = "யாருக்கு விநியோகம் (Target Audience)"
        verbose_name_plural = "யாருக்கு விநியோகம் (Target Audience)"
        ordering = ['order']

    def __str__(self):
        return self.title


class ProcessStep(models.Model):
    step_number = models.PositiveIntegerField("படி எண் (1 to 4)", default=1)
    title = models.CharField("தலைப்பு", max_length=150)
    description = models.TextField("விவரம்")
    tag_badge = models.CharField("பேட்ஜ் குறிப்பு", max_length=100)

    class Meta:
        verbose_name = "செயல்முறை படி (Process Step)"
        verbose_name_plural = "செயல்முறை படிகள் (How It Works)"
        ordering = ['step_number']

    def __str__(self):
        return f"படி {self.step_number}: {self.title}"


class KeyProduct(models.Model):
    name = models.CharField("பொருள் பெயர்", max_length=150)
    category_tag = models.CharField("பிரிவு குறிப்பு", max_length=100, default="காய்கறிகள்")
    description = models.CharField("விவரம்", max_length=255)
    image_url = models.CharField("படம் URL", max_length=500, blank=True)
    order = models.PositiveIntegerField("வரிசை எண்", default=1)

    class Meta:
        verbose_name = "முக்கிய பொருள் (Key Product)"
        verbose_name_plural = "முக்கிய பொருட்கள் (Featured Products)"
        ordering = ['order']

    def __str__(self):
        return self.name


class WhyChooseUs(models.Model):
    title = models.CharField("தலைப்பு", max_length=150)
    description = models.TextField("விவரம்")
    icon_type = models.CharField("ஐகான் வகை", max_length=50, default="basket")
    order = models.PositiveIntegerField("வரிசை எண்", default=1)

    class Meta:
        verbose_name = "ஏன் ஊர் உழவன் (Why Choose Us)"
        verbose_name_plural = "ஏன் ஊர் உழவன் அம்சங்கள் (Why Choose Us)"
        ordering = ['order']

    def __str__(self):
        return self.title


class WholesaleEnquiry(models.Model):
    BUSINESS_TYPES = [
        ('ஹோட்டல் & ரெஸ்டாரன்ட்', 'ஹோட்டல் & ரெஸ்டாரன்ட் (Hotels & Restaurants)'),
        ('கேட்டரிங் சர்வீஸ்', 'கேட்டரிங் சர்வீஸ் (Catering Services)'),
        ('திருமண நிகழ்ச்சி & விழாக்கள்', 'திருமண நிகழ்ச்சி & விழாக்கள் (Wedding & Events)'),
        ('காய்கறி & பழக்கடை', 'காய்கறி & பழக்கடை (Retail Vegetable / Fruit Shop)'),
        ('ஹாஸ்டல் & கேன்டீன்', 'ஹாஸ்டல் & கேன்டீன் (Hostels & Canteens)'),
        ('பிற B2B வணிகம்', 'பிற B2B வணிகம் (Other Business)'),
    ]

    STATUS_CHOICES = [
        ('NEW', 'புதிய கோரிக்கை (New)'),
        ('CONTACTED', 'தொடர்பு கொள்ளப்பட்டது (Contacted)'),
        ('QUOTED', 'விலைப்பட்டியல் அனுப்பப்பட்டது (Quoted)'),
        ('COMPLETED', 'நிறைவுற்றது (Completed)'),
        ('CANCELLED', 'ரத்து செய்யப்பட்டது (Cancelled)'),
    ]

    business_name = models.CharField("வணிகம் / வாடிக்கையாளர் பெயர்", max_length=200)
    contact_person = models.CharField("தொடர்பு கொள்ள வேண்டிய நபர்", max_length=150)
    phone_number = models.CharField("கைபேசி எண் / WhatsApp", max_length=15)
    business_type = models.CharField("வணிக வகை", max_length=100, choices=BUSINESS_TYPES)
    delivery_location = models.CharField("விநியோக இடம் / முகவரி", max_length=255)
    delivery_date = models.DateField("தேவையான விநியோக தேதி")
    required_products = models.CharField("தேவையான பொருட்கள்", max_length=255)
    approx_quantity = models.CharField("தோராயமான அளவு / எடையளவு", max_length=150)
    additional_notes = models.TextField("கூடுதல் தகவல் / குறிப்புகள்", blank=True, null=True)
    requirement_file = models.FileField("தேவைப் பட்டியல் கோப்பு", upload_to='enquiries/', blank=True, null=True)
    status = models.CharField("நிலை (Status)", max_length=20, choices=STATUS_CHOICES, default='NEW')
    created_at = models.DateTimeField("பதிவு செய்யப்பட்ட நேரம்", auto_now_add=True)

    class Meta:
        verbose_name = "மொத்த விலை விசாரணை (Wholesale Enquiry)"
        verbose_name_plural = "மொத்த விலை விசாரணைகள் (Wholesale Enquiries)"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.business_name} - {self.phone_number} ({self.created_at.strftime('%d-%m-%Y')})"