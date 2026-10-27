import base64
import io
import re

from PIL import Image

from odoo import models

from ..models.ideaa_matrix import CONDITION_SELECTION, SIGNIFICANCE_THRESHOLD

import logging

_logger = logging.getLogger(__name__)

TITLE = 'MATRIZ IDENTIFICACIÓN DE ASPECTOS, EVALUACIÓN DE IMPACTOS AMBIENTALES'
HEADERS = [
    'Nº',
    'ETAPA DEL CICLO DE VIDA',
    'PROCESO',
    'ACTIVIDAD',
    'ASPECTO AMBIENTAL',
    'IMPACTO AMBIENTAL',
    'CONDICIÓN',
    'CONTROLES',
    'FRECUENCIA',
    'SEVERIDAD',
    'ALCANCE',
    'NIVEL DE IMPACTO',
    'SIGNIFICANCIA',
    'CONTROL A IMPLEMENTAR',
    'RESPONSABLE',
]
# Ancho de las columnas A:O (en caracteres), igual que la plantilla
COLUMN_WIDTHS = [6.7, 22.3, 29.4, 32.9, 27.7, 24.6, 18, 32.1, 7.1, 7.1, 7.1, 16.3, 23.9, 43.9, 31.3]
FIRST_ROW = 6   # fila (base 0) de los encabezados
LOGO_COLUMNS = (0, 1, 2)
LOGO_ROWS_HEIGHT = (26.25, 21.75, 21.75)    # alto en puntos de las filas 1 a 3
SIGNIFICANT_TEXT = 'Significativo (S)'
NOT_SIGNIFICANT_TEXT = 'No Significativo (NS)'


def _col_pixels(width):
    return int(width * 7 + 5) if width >= 1 else int(width * 12 + 0.5)


class IDEAAMatrixXLSXReport(models.AbstractModel):
    _name = 'report.sga_ideaa_matrix_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Reporte XLSX de la matriz de identificación de aspectos ambientales'

    @staticmethod
    def _sheet_name(matrix, used):
        base = re.sub(r'[\[\]:*?/\\]', ' ', matrix.code or matrix.name or 'MATRIZ').strip()[:28] or 'MATRIZ'
        name, i = base, 1
        while name.lower() in used:
            i += 1
            name = '%s (%d)' % (base[:28 - len(str(i))], i)
        used.add(name.lower())
        return name

    def _insert_logo(self, sheet):
        """Inserta el logo de la compañía centrado en el rango combinado A1:C3."""
        logo = self.env.company.logo
        if not logo:
            return
        data = base64.b64decode(logo)
        image = Image.open(io.BytesIO(data))
        width, height = image.size
        box_w = sum(_col_pixels(COLUMN_WIDTHS[c]) for c in LOGO_COLUMNS)
        box_h = sum(round(h * 4 / 3) for h in LOGO_ROWS_HEIGHT)
        margin = 4
        scale = min((box_w - 2 * margin) / width, (box_h - 2 * margin) / height)
        sheet.insert_image('A1', 'logo.png', {
            'image_data': io.BytesIO(data),
            'x_scale': scale,
            'y_scale': scale,
            'x_offset': max(int((box_w - width * scale) / 2), 0),
            'y_offset': max(int((box_h - height * scale) / 2), 0),
            'object_position': 1,
        })

    @staticmethod
    def _responsibles(action):
        employees = action.exec_hr_resp_ids or action.exec_hr_resp
        if employees:
            return ', '.join(employees.mapped('name'))
        return ''

    def generate_xlsx_report(self, workbook, data, matrixes):
        def fmt(**kwargs):
            base = {'font_name': 'Calibri', 'font_size': 10, 'align': 'center', 'valign': 'vcenter',
                    'text_wrap': True, 'border': 1}
            base.update(kwargs)
            return workbook.add_format(base)

        format_title = fmt(font_name='Arial', font_size=14, bold=True, bg_color='#D9D9D9')
        format_info = fmt(font_name='Arial', font_size=11, bold=True, bg_color='#D9D9D9')
        format_logo = fmt()
        format_header = fmt(font_size=14, bold=True, bg_color='#E7E6E6')
        format_header_rot = fmt(font_size=12, bold=True, bg_color='#E7E6E6', rotation=90)
        format_number = fmt(font_name='Arial', font_size=8.5)
        format_text = fmt(font_name='Arial', font_size=8.5)
        format_center = fmt()
        format_left = fmt(align='left')
        format_level = fmt(font_size=11)
        format_significant = workbook.add_format({'bg_color': '#FF0000'})
        format_not_significant = workbook.add_format({'bg_color': '#00B050'})

        used_names = set()
        for matrix in matrixes:
            sheet = workbook.add_worksheet(self._sheet_name(matrix, used_names))
            sheet.hide_gridlines(2)
            sheet.set_landscape()
            sheet.set_paper(9)
            sheet.fit_to_pages(1, 0)
            for col, width in enumerate(COLUMN_WIDTHS):
                sheet.set_column(col, col, width)
            for row, height in enumerate(LOGO_ROWS_HEIGHT):
                sheet.set_row(row, height)
            sheet.set_row(3, 11.4)
            sheet.set_row(4, 9.6)
            sheet.set_row(FIRST_ROW - 1, 130.2)

            # Cabecera: logo, título y datos del documento
            sheet.merge_range('A1:C3', '', format_logo)
            self._insert_logo(sheet)
            sheet.merge_range('D1:M3', TITLE, format_title)
            sheet.merge_range('N1:O1', 'Código: %s' % (matrix.code or ''), format_info)
            sheet.merge_range('N2:O2', 'Versión: %02d' % (matrix.version or 0), format_info)
            validation_date = matrix.date_validate.strftime('%d/%m/%Y') if matrix.date_validate else 'Sin definir'
            sheet.merge_range('N3:O3', 'Fecha de validación: %s' % validation_date, format_info)

            for col, header in enumerate(HEADERS):
                rotated = 8 <= col <= 10
                sheet.write(FIRST_ROW - 1, col, header, format_header_rot if rotated else format_header)

            conditions = dict(CONDITION_SELECTION)
            row = FIRST_ROW
            for number, line in enumerate(matrix.line_ids, start=1):
                excel_row = row + 1
                sheet.write_number(row, 0, number, format_number)
                sheet.write(row, 1, line.stage or '', format_text)
                sheet.write(row, 2, line.process or '', format_center)
                sheet.write(row, 3, line.activity or '', format_center)
                sheet.write(row, 4, line.aspect or '', format_center)
                sheet.write(row, 5, line.impact or '', format_center)
                sheet.write(row, 6, conditions.get(line.condition, ''), format_center)
                sheet.write(row, 7, line.controls or '', format_left)
                for col, value in ((8, line.frequency), (9, line.severity), (10, line.scope)):
                    if value:
                        sheet.write_number(row, col, int(value), format_level)
                    else:
                        sheet.write_blank(row, col, None, format_level)
                sheet.write_formula(
                    row, 11,
                    '=IF(OR(I{r}="", J{r}="", K{r}=""), "", I{r}*J{r}*K{r})'.format(r=excel_row),
                    format_level, line.impact_level or '')
                sheet.write_formula(
                    row, 12,
                    '=IF(L{r}="", "", IF(L{r}>={t}, "{s}", "{ns}"))'.format(
                        r=excel_row, t=SIGNIFICANCE_THRESHOLD, s=SIGNIFICANT_TEXT, ns=NOT_SIGNIFICANT_TEXT),
                    format_center,
                    {'significant': SIGNIFICANT_TEXT, 'not_significant': NOT_SIGNIFICANT_TEXT}.get(line.significance, ''))
                sheet.write(row, 13, '\n'.join('- ' + a.name for a in line.action_ids), format_left)
                sheet.write(row, 14, '\n'.join(self._responsibles(a) for a in line.action_ids), format_center)
                row += 1

            last_row = max(row, FIRST_ROW + 1)
            sheet.autofilter(FIRST_ROW - 1, 2, last_row - 1, 14)
            if matrix.line_ids:
                sheet.data_validation(FIRST_ROW, 8, last_row - 1, 10, {
                    'validate': 'list', 'source': ['1', '3', '5']})
                sheet.data_validation(FIRST_ROW, 6, last_row - 1, 6, {
                    'validate': 'list', 'source': list(conditions.values())})
                sheet.conditional_format(FIRST_ROW, 12, last_row - 1, 12, {
                    'type': 'cell', 'criteria': '==', 'value': '"%s"' % SIGNIFICANT_TEXT,
                    'format': format_significant})
                sheet.conditional_format(FIRST_ROW, 12, last_row - 1, 12, {
                    'type': 'cell', 'criteria': '==', 'value': '"%s"' % NOT_SIGNIFICANT_TEXT,
                    'format': format_not_significant})
