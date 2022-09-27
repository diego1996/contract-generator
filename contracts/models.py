from django.db import models
from djmoney.models.fields import MoneyField


# Create your models here.

class City(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=300)

    class Meta:
        verbose_name = 'Ciudad/Municipio'
        verbose_name_plural = 'Ciudades/Municipios'

    def __str__(self):
        return self.name


def get_employer_upload_path(instance, filename):
    return f'employer/{instance.pk}/images/{filename}'


def get_employee_upload_path(instance, filename):
    return f'employee/{instance.employee.pk}/files/{filename}'


class Employer(models.Model):
    name = models.CharField(verbose_name='Nombre del empleador', max_length=200)
    nit = models.CharField(verbose_name='NIT No.', max_length=15)
    address = models.CharField(verbose_name='Dirección del empleador', max_length=200)
    city = models.ForeignKey(City, verbose_name='Ciudad de domicilio', on_delete=models.CASCADE)
    legal_representative = models.CharField(verbose_name='Representante legal', max_length=800)
    consecutive_prefix = models.CharField(verbose_name='Prefijo del consecutivo', max_length=10, default='-')
    logo = models.ImageField(verbose_name='Logo', upload_to=get_employer_upload_path, null=True, blank=True)
    footer = models.ImageField(verbose_name='Pie de página', upload_to=get_employer_upload_path, null=True, blank=True)

    class Meta:
        verbose_name = 'Empleador'
        verbose_name_plural = 'Empleadores'

    def __str__(self):
        return self.name


class Employee(models.Model):
    TYPE_IDS = (
        ('CC', 'Cédula de ciudadanía'),
        ('CE', 'Cédula de extranjería'),
    )
    name = models.CharField(verbose_name='Nombre del trabajador', max_length=300)
    identification_type = models.CharField(
        verbose_name='Tipo de documento', choices=TYPE_IDS, default='CC', max_length=3
    )
    identification_number = models.CharField(verbose_name='Documento de identidad', max_length=15)
    identification_expedition_place = models.CharField(verbose_name='Lugar de expedición', max_length=100)
    address = models.CharField(verbose_name='Dirección del trabajador', max_length=200)
    cellphone = models.CharField(verbose_name='Teléfono/Celular', max_length=15)
    email = models.CharField(verbose_name='Correo electrónico', max_length=100)
    place_birth = models.CharField(verbose_name='Lugar de nacimiento', max_length=100)
    date_birth = models.DateField(verbose_name='Fecha de nacimiento')
    nationality = models.CharField(verbose_name='Nacionalidad', max_length=100)  # normalizar

    class Meta:
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajadores'

    def __str__(self):
        return self.name


class ContractType(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=300)

    class Meta:
        verbose_name = 'Tipo de contrato'
        verbose_name_plural = 'Tipos de contratos'

    def __str__(self):
        return self.name


class PaidPeriod(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=300)

    class Meta:
        verbose_name = 'Periodo de pago'
        verbose_name_plural = 'Periodos de pago'

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=300)

    class Meta:
        verbose_name = 'Cargo u oficio'
        verbose_name_plural = 'Cargos u oficios'

    def __str__(self):
        return self.name


class Activity(models.Model):
    title = models.CharField(verbose_name='Título', max_length=300)
    description = models.TextField(verbose_name='Descripción de la actividad', max_length=100000, default='')

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return self.title


class Contract(models.Model):
    consecutive = models.CharField(verbose_name='Consecutivo del contrato', unique=True, max_length=10, default='')
    contract_date = models.DateField(verbose_name='Fecha del contrato', null=True, blank=True)
    contract_city = models.ForeignKey(
        City, verbose_name='Ciudad', related_name='contract_city', on_delete=models.CASCADE
    )
    employer = models.ForeignKey(Employer, verbose_name='Empleador', on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, verbose_name='Trabajador', on_delete=models.CASCADE)
    type = models.ForeignKey(ContractType, verbose_name='Clase de contrato', on_delete=models.CASCADE)
    paid_period = models.ForeignKey(PaidPeriod, verbose_name='Periodo de pago', on_delete=models.CASCADE)
    position = models.ForeignKey(Position, verbose_name='Cargo u oficio', on_delete=models.CASCADE)
    city_work = models.ForeignKey(
        City, verbose_name='Ciudad de trabajo', related_name='city_work', on_delete=models.CASCADE
    )
    base_salary = MoneyField(
        verbose_name='Salario básico',
        decimal_places=0,
        default=0,
        default_currency='COP',
        max_digits=50,
    )
    auxiliary_salary_reason = models.CharField(verbose_name='Motivo del salario auxiliar', default='', max_length=500)
    auxiliary_salary = MoneyField(
        verbose_name='Salario auxiliar',
        decimal_places=0,
        default=0,
        default_currency='COP',
        max_digits=50,
    )
    auxiliary_salary_text = models.CharField(verbose_name='Salario auxiliar (en texto)', default='', max_length=900)
    start_work_date = models.DateField(verbose_name='Fecha de iniciación de labores', null=True, blank=True)
    place_work = models.CharField(verbose_name='Lugar de donde desempeñará labores', max_length=200)
    position_description = models.TextField(verbose_name='Trabajo o labor contratada', max_length=900)
    partner = models.CharField(verbose_name='Cliente principal', max_length=600)
    duration = models.CharField(verbose_name='Duración del contrato', max_length=100, default='tres (03) meses')
    test_period_duration = models.CharField(
        verbose_name='Duración del periodo de prueba', max_length=100, default='dieciocho (18) días'
    )
    special_activities = models.TextField(verbose_name='Actividades especiales del contrato', max_length=100000, default='')
    activities = models.ManyToManyField(Activity, verbose_name='Actividades especiales del contrato')
    confidentiality_signed = models.FileField(
        verbose_name='Modelo de confidencialidad firmado', blank=True, null=True, upload_to=get_employee_upload_path
    )
    contract_signed = models.FileField(
        verbose_name='Contrato firmado', blank=True, null=True, upload_to=get_employee_upload_path
    )

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

    def __str__(self):
        return f'{self.contract_date} - {self.employer} - {self.employee}'
