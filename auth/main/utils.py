import io

import xlsxwriter

from django.http import HttpResponse


def group_contacts(queryset):
    all_contacts = []
    contact = []
    for i in queryset:
        for v in i.values():
            if type(v) == dict:
                for v2 in v.values():
                    all_contacts.append(v2)
            else:
                all_contacts.append(v)
        contact.append(all_contacts)
        all_contacts = []
    return contact


def perform_excel(queryset, columns, filename):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('data')
    bold = workbook.add_format({'bold': True})

    row = 1

    for linea in queryset:
        for i in range(len(columns)):
            linea = list(linea)
            worksheet.write(row, i, linea[i])
        row += 1

    for i in range(len(columns)):
        x = 'A'
        val = chr(ord(x) + i)
        worksheet.write(val + '1', columns[i], bold)

    workbook.close()

    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename) + '.xlsx'

    return response