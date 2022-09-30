from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .models import City, Employer, Employee, Position, PaidPeriod, Contract, ContractType, Activity
from .resources import ContractResource


class ActivityInline(admin.TabularInline):
    model = Contract.activities.through
    extra = 0


# @admin.register(Activity)
# class ActivityAdmin(admin.ModelAdmin):
#    list_display = ('id', 'title')
#    search_fields = ('title', 'description')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(ContractType)
class ContractTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(PaidPeriod)
class PaidPeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nit', 'address', 'legal_representative')
    search_fields = ('name', 'nit', 'address', 'legal_representative')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'identification_type', 'identification_number', 'cellphone', 'email', 'nationality')
    search_fields = ('name', 'identification_number', 'cellphone', 'email')


@admin.register(Contract)
class ContractAdmin(ImportExportModelAdmin):
    list_display = (
        'id', 'employer', 'employee', 'type', 'position',
        'confidentiality_signed', 'contract_signed', 'resignation_signed',
        'view_confidentiality_agreement_pdf', 'view_contract_pdf', 'view_resignation_pdf'
    )
    search_fields = (
        'employer__name', 'employee__name', 'contract_date', 'contract_city__name', 'place_work', 'position_description'
    )
    list_filter = ('employer', 'employee', 'type')
    # inlines = (ActivityInline, )
    exclude = ('activities', )
    resource_class = ContractResource

    @admin.display(description='Convenio (en blanco)')
    def view_confidentiality_agreement_pdf(self, obj):
        return format_html(
            f"<a href='{obj.id}/documents/confidentiality/' target='_blank'>Confidencialidad</a>"
        )

    @admin.display(description='Contrato (en blanco)')
    def view_contract_pdf(self, obj):
        return format_html(f"<a href='{obj.id}/documents/contract/' target='_blank'>Contrato</a>")

    @admin.display(description='Resignación (en blanco)')
    def view_resignation_pdf(self, obj):
        return format_html(
            f"<a href='{obj.id}/documents/resignation/' target='_blank'>Resignación</a>"
        )
