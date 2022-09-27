from import_export import resources

from contracts.models import Contract


class ContractResource(resources.ModelResource):

    class Meta:
        model = Contract
        fields = (
            'id', 'contract_date', 'resignation_date', 'contract_city__name', 'employer__name', 'employee__name',
            'type__name', 'paid_period__name', 'position__name', 'city_work__name', 'base_salary',
            'auxiliary_salary_reason', 'auxiliary_salary', 'start_work_date', 'place_work', 'duration'
        )
