from django.contrib import admin
from django import forms
from .models import Guest, Event
from .storage import upload_file_to_contabo_s3

class GuestAdminForm(forms.ModelForm):
    guest_photo = forms.FileField(
        required=False,
        label="Upload Guest Photo"
    )

    class Meta:
        model = Guest
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)

        uploaded_file = self.files.get("guest_photo")
        if uploaded_file:
            try:
                instance.photo_url = upload_file_to_contabo_s3(uploaded_file)
            except Exception as e:
                raise forms.ValidationError(f"Guest photo upload failed: {str(e)}")

        if commit:
            instance.save()
        return instance

class EventAdminForm(forms.ModelForm):
    event_photo = forms.FileField(
        required=False,
        label="Upload Event Photo"
    )

    class Meta:
        model = Event
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)

        uploaded_file = self.files.get("event_photo")
        if uploaded_file:
            try:
                instance.photos = [upload_file_to_contabo_s3(uploaded_file)]
            except Exception as e:
                raise forms.ValidationError(f"Event photo upload failed: {str(e)}")

        if commit:
            instance.save()
            if hasattr(self, 'save_m2m'):
                self.save_m2m()
        return instance

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    form = GuestAdminForm
    list_display = ('full_name', 'position_with_company', 'photo_url')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ('name', 'category', 'event_date', 'status')
    list_filter = ('status', 'category')
    search_fields = ('name', 'description')
    filter_horizontal = ('guests',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description')
        }),
        ('Event Details', {
            'fields': ('event_date', 'register_deadline', 'price', 'slots', 'register_link', 'status')
        }),
        ('Photos', {
            'fields': ('event_photo', 'photos')
        }),
        ('Guests', {
            'fields': ('guests',)
        }),
    )

    readonly_fields = ('photos',)