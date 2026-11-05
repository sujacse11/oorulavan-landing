from django.contrib import admin
from .models import (
    SiteSetting, ProductCategory, TargetAudience, 
    ProcessStep, KeyProduct, WhyChooseUs, WholesaleEnquiry
)

admin.site.site_header = "ஊர் உழவன் — நிர்வாகக் கட்டுப்பாடு"
admin.site.site_title = "ஊர் உழவன் Admin"
admin.site.index_title = "தள மேலாண்மை (Landing Page Management)"

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'phone', 'whatsapp_number', 'email')

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'order')
    list_display_links = ('title',)
    list_editable = ('order',)

@admin.register(TargetAudience)
class TargetAudienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'badge_left', 'badge_right', 'order')
    list_display_links = ('title',)
    list_editable = ('order',)

@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag_badge', 'step_number')
    list_display_links = ('title',)
    list_editable = ('step_number',)

@admin.register(KeyProduct)
class KeyProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_tag', 'description', 'order')
    list_display_links = ('name',)
    list_editable = ('order', 'category_tag')
    search_fields = ('name', 'description')

@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_type', 'order')
    list_display_links = ('title',)
    list_editable = ('order',)

@admin.register(WholesaleEnquiry)
class WholesaleEnquiryAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'contact_person', 'phone_number', 'business_type', 'delivery_date', 'status', 'created_at')
    list_display_links = ('business_name',)
    list_filter = ('status', 'business_type', 'created_at')
    search_fields = ('business_name', 'contact_person', 'phone_number', 'delivery_location')
    list_editable = ('status',)
    readonly_fields = ('created_at',)