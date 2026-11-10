from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    SiteSetting, ProductCategory, TargetAudience, 
    ProcessStep, KeyProduct, WhyChooseUs, WholesaleEnquiry
)

admin.site.site_header = "ஊர் உழவன் — நிர்வாகக் கட்டுப்பாடு"
admin.site.site_title = "ஊர் உழவன் Admin"
admin.site.index_title = "தள மேலாண்மை (Landing Page Management)"

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'phone', 'whatsapp_number', 'email', 'edit_action')

    @admin.display(description="மாற்றுக (Change)")
    def edit_action(self, obj):
        url = reverse('admin:landing_sitesetting_change', args=[obj.pk])
        return format_html('<a class="changelink" href="{}">Change</a>', url)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'order', 'edit_action')
    list_display_links = ('title', 'tag')
    list_editable = ('order',)
    search_fields = ('title', 'tag', 'description')

    @admin.display(description="மாற்றுக (Change)")
    def edit_action(self, obj):
        url = reverse('admin:landing_productcategory_change', args=[obj.pk])
        return format_html('<a class="changelink" href="{}">Change</a>', url)


@admin.register(TargetAudience)
class TargetAudienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'badge_left', 'badge_right', 'order', 'edit_action')
    list_display_links = ('title', 'subtitle')
    list_editable = ('order',)

    @admin.display(description="மாற்றுக (Change)")
    def edit_action(self, obj):
        url = reverse('admin:landing_targetaudience_change', args=[obj.pk])
        return format_html('<a class="changelink" href="{}">Change</a>', url)


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag_badge', 'step_number', 'edit_action')
    list_display_links = ('title',)
    list_editable = ('step_number',)

    @admin.display(description="மாற்றுக (Change)")
    def edit_action(self, obj):
        url = reverse('admin:landing_processstep_change', args=[obj.pk])
        return format_html('<a class="changelink" href="{}">Change</a>', url)


@admin.register(KeyProduct)
class KeyProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_tag', 'description', 'order', 'edit_action')
    list_display_links = ('name',)
    list_editable = ('order', 'category_tag')
    search_fields = ('name', 'description')

    @admin.display(description="மாற்றுக (Change)")
    def edit_action(self, obj):
        url = reverse('admin:landing_keyproduct_change', args=[obj.pk])
        return format_html('<a class="changelink" href="{}">Change</a>', url)


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_type', 'order', 'edit_action')
    list_display_links = ('title',)
    list_editable = ('order',)

    @admin.display(description="மாற்றுக (Change)")
    def edit_action(self, obj):
        url = reverse('admin:landing_whychooseus_change', args=[obj.pk])
        return format_html('<a class="changelink" href="{}">Change</a>', url)


@admin.register(WholesaleEnquiry)
class WholesaleEnquiryAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'contact_person', 'phone_number', 'business_type', 'delivery_date', 'status', 'created_at', 'edit_action')
    list_display_links = ('business_name',)
    list_filter = ('status', 'business_type', 'created_at')
    search_fields = ('business_name', 'contact_person', 'phone_number', 'delivery_location')
    list_editable = ('status',)
    readonly_fields = ('created_at',)

    @admin.display(description="மாற்றுக (Change)")
    def edit_action(self, obj):
        url = reverse('admin:landing_wholesaleenquiry_change', args=[obj.pk])
        return format_html('<a class="changelink" href="{}">Change</a>', url)
