from django.contrib import admin 
from aidsbank.models import Manager, Applicant, Centre, AidType, Aid, Asset, Movement, Loan

"""
Manager
"""
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_centres_display',)

admin.site.register(Manager, ManagerAdmin)

"""
Applicant
"""
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Applicant, ApplicantAdmin)

"""
Centre
"""
class CentreAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Centre, CentreAdmin)

"""
AidType
"""
class AidTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(AidType, AidTypeAdmin)

"""
Aid
"""
class AidAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'type', )
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Aid, AidAdmin)

"""
Asset
"""
class AssetAdmin(admin.ModelAdmin):
    list_display = ('code', 'aid', 'centre', 'vendor', 'price',)

admin.site.register(Asset, AssetAdmin)

"""
Loan
"""
class LoanAdmin(admin.ModelAdmin):
    list_display = ('asset', 'applicant', 'place', 'reservation_date', 'loan_date', 'status', )

admin.site.register(Loan, LoanAdmin)

"""
Movement
"""
class MovementAdmin(admin.ModelAdmin):
    list_display = ('asset', 'manager', 'date', 'status', )

admin.site.register(Movement, MovementAdmin)
