import os
import tempfile
from os.path import splitext, basename

import pdfkit
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from sys import platform
from django.shortcuts import render

# Create your views here.
from django.template import loader, Template, Context
from django.test import override_settings
from django.views.generic import TemplateView

from contracts.models import Contract


class PDFView(LoginRequiredMixin, TemplateView):
    filename = None
    inline = False
    pdfkit_options = None

    def get_context_data(self, **kwargs):
        context = super(PDFView, self).get_context_data(**kwargs)
        try:
            pk = self.kwargs.get('pk')
            contract = Contract.objects.get(pk=pk)
            context['contract_date'] = contract.contract_date
            context['contract_type'] = contract.type.name.upper()
            context['contract_city'] = contract.contract_city.name.upper()
            context['contract_place_work'] = contract.place_work.upper()
            context['contract_position'] = contract.position.name.upper()
            context['contract_position_description'] = contract.position_description.upper()
            context['contract_base_salary'] = contract.base_salary
            context['contract_auxiliary_salary'] = contract.auxiliary_salary
            context['contract_auxiliary_salary_text'] = contract.auxiliary_salary_text.upper()
            context['contract_partner'] = contract.partner
            context['contract_duration'] = contract.duration
            context['contract_start_work_date'] = contract.start_work_date
            context['contract_paid_period'] = contract.paid_period.name.upper()
            context['contract_test_period_duration'] = contract.test_period_duration
            context['contract_activities'] = contract.activities.all()
            context['employer_logo'] = contract.employer.logo.url if contract.employer.logo else None
            context['employer_footer'] = contract.employer.footer.url if contract.employer.footer else None
            context['employer_name'] = contract.employer.name.upper()
            context['employer_nit'] = contract.employer.nit.upper()
            context['employer_address'] = contract.employer.address.upper()
            context['employer_city'] = contract.employer.city.name.upper()
            context['employer_legal_representative'] = contract.employer.legal_representative.upper()
            context['employee_name'] = contract.employee.name.upper()
            context['employee_identification_type'] = contract.employee.identification_type.upper()
            context['employee_identification_number'] = contract.employee.identification_number.upper()
            context[
                'employee_identification_expedition_place'] = contract.employee.identification_expedition_place.upper()
            context['employee_address'] = contract.employee.address.upper()
            context['employee_cellphone'] = contract.employee.cellphone.upper()
            context['employee_email'] = contract.employee.email
            context['employee_place_birth'] = contract.employee.place_birth.upper()
            context['employee_date_birth'] = contract.employee.date_birth
            context['employee_nationality'] = contract.employee.nationality.upper()
            context[
                'employee_identification_expedition_place'
            ] = contract.employee.identification_expedition_place.upper()

            context['contract_special_activities'] = contract.special_activities
            return context
        except Exception as e:
            print(e)
            return context

    def get(self, request, *args, **kwargs):
        if 'html' in request.GET:
            content = self.render_html(*args, **kwargs)
            return HttpResponse(content)
        else:
            content = self.render_pdf(*args, **kwargs)
            response = HttpResponse(content, content_type='application/pdf')
            if (not self.inline or 'download' in request.GET) and 'inline' not in request.GET:
                response['Content-Disposition'] = 'inline; filename=%s' % self.get_filename()
            response['Content-Length'] = len(content)
            return response

    def render_pdf(self, *args, **kwargs):
        html = self.render_html(*args, **kwargs)
        options = self.get_pdfkit_options()
        options['footer-font-size'] = '9'
        # options['footer-left'] = "1252-F-GDE-36-V1"
        # options['footer-center'] = "Página [page] de [topage]"
        # options['footer-right'] = ""
        # options['header-font-size'] = '9'

        if 'debug' in self.request.GET and settings.DEBUG:
            options['debug-javascript'] = '1'

        kwargs = {}
        wkhtmltopdf_bin = os.environ.get('WKHTMLTOPDF_BIN')
        if wkhtmltopdf_bin:
            kwargs['configuration'] = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_bin)

        platforms = ["win32", "linux", "linux2"]
        if platform in platforms:
            self.render_temp_html('contracts/temp/header.html', 'header-html', options, **kwargs)
            self.render_temp_html('contracts/temp/footer.html', 'footer-html', options, **kwargs)
        else:
            options['header-html'] = 'templates/contracts/header.html'
            options['footer-html'] = 'templates/contracts/footer.html'

        try:
            pdf = pdfkit.from_string(html, False, options, **kwargs)
        finally:
            pass
            # os.remove(options['header-html'])
        return pdf

    def get_pdfkit_options(self):
        if self.pdfkit_options is not None:
            return self.pdfkit_options
        return {
            'dpi': '300',
            'page-size': 'Letter',
            'encoding': 'UTF-8',
            'header-spacing': '20',
            'footer-spacing': '1',
            'margin-top': '1.0in',
            'margin-bottom': '1.0in',
            'margin-right': '0in',
            'margin-left': '0in',
            'load-error-handling': 'skip'
        }

    def get_filename(self):
        if self.filename is None:
            name = splitext(basename(self.template_name))[0]
            return '{}.pdf'.format(name)

        return self.filename

    def render_html(self, *args, **kwargs):
        static_url = '%s://%s%s' % (self.request.scheme, self.request.get_host(), settings.STATIC_URL)
        media_url = '%s://%s%s' % (self.request.scheme, self.request.get_host(), settings.MEDIA_URL)

        with override_settings(STATIC_URL=static_url, MEDIA_URL=media_url):
            template = loader.get_template(self.template_name)
            context = self.get_context_data(**kwargs)
            html = template.render(context)
            return html

    def render_temp_html(self, template_path, option_name, options, **kwargs):
        static_url = settings.MINIO_STORAGE_STATIC_URL or '%s://%s%s' % (
            self.request.scheme, self.request.get_host(), settings.MEDIA_URL
        )
        media_url = settings.MINIO_STORAGE_MEDIA_URL or '%s://%s%s' % (
            self.request.scheme, self.request.get_host(), settings.MEDIA_URL
        )
        with override_settings(STATIC_URL=static_url, MEDIA_URL=media_url):
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as header:
                options[option_name] = header.name
                context = self.get_context_data(**kwargs)
                header.write(loader.render_to_string(template_path, context).encode('utf-8'))
                header.flush()

    def with_config(self, method):
        static_url = settings.MINIO_STORAGE_STATIC_URL or '%s://%s%s' % (
            self.request.scheme, self.request.get_host(), settings.MEDIA_URL
        )
        media_url = settings.MINIO_STORAGE_MEDIA_URL or '%s://%s%s' % (
            self.request.scheme, self.request.get_host(), settings.MEDIA_URL
        )
        with override_settings(STATIC_URL=static_url, MEDIA_URL=media_url):
            method()
