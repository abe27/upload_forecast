from django.contrib import admin
from .models import EDIReviseType,RefType,Book,ReviseBook

# Register your models here.
class EDIReviseTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'is_active',
        'created_at',
        'updated_at',
    )
    
    search_fields = (
        'name',
    )
    
    list_filter = ('is_active',)
    sortable_by = ('name',)
    
    # ordering = ("code","name",)
    list_per_page = 25
    
    def created_at(self, obj):
        return obj.created_on.strftime("%d-%m-%Y %H:%M:%S")
    
    def updated_at(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_on.strftime("%d-%m-%Y %H:%M:%S")
    pass

class RefTypeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'description',
        'is_active',
        'created_at',
        'updated_at',
    )
    
    search_fields = (
        'code',
        'name',
    )
    
    list_filter = ('is_active',)
    
    # ordering = ("code","name",)
    list_per_page = 25
    
    def created_at(self, obj):
        return obj.created_on.strftime("%d-%m-%Y %H:%M:%S")
    
    def updated_at(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_on.strftime("%d-%m-%Y %H:%M:%S")
    pass

class BookAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'prefix',
        'description',
        'is_active',
        'created_at',
        'updated_at',
    )
    
    search_fields = (
        'code',
        'name',
    )
    
    list_filter = ('is_active',)
    
    # ordering = ("code","name",)
    list_per_page = 25
    
    def created_at(self, obj):
        return obj.created_on.strftime("%d-%m-%Y %H:%M:%S")
    
    def updated_at(self, obj):
        # return obj.updated_on.strftime("%d %b %Y %H:%M:%S")
        return obj.updated_on.strftime("%d-%m-%Y %H:%M:%S")
    pass

class BookDetailAdmin(admin.ModelAdmin):
    pass

class ReviseBookAdmin(admin.ModelAdmin):
    pass

admin.site.register(EDIReviseType, EDIReviseTypeAdmin,)
admin.site.register(RefType, RefTypeAdmin,)
admin.site.register(Book, BookAdmin,)
# admin.site.register(BookDetail, BookDetailAdmin,)
admin.site.register(ReviseBook, ReviseBookAdmin,)

