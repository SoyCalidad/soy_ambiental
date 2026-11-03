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


# Hoja informativa "CRITERIOS" (copiada de la plantilla): tablas de criterios de valoración
CRITERIA_SHEET_NAME = 'CRITERIOS'
CRITERIA_TITLE = 'TABLAS DE CRITERIOS PARA VALORACIÓN DE ASPECTOS E IMPACTOS AMBIENTALES'
CRITERIA_CONDITIONS_TITLE = '1. Tabla de Criterios de Evaluación por Condiciones'
CRITERIA_CONDITIONS_HEADERS = [
    'Puntuación',
    'F - Frecuencia en Condición Normal (N) o Anormal (A)',
    'F - Frecuencia en Condición de Emergencia (E)',
    'S - Severidad Intensidad del Impacto)',
    'A - Alcance / Extensión',
]
CRITERIA_CONDITIONS_ROWS = [
    ['Baja (1)',
     'Raramente: La actividad o situación ocurre una o dos veces al año, o con menor frecuencia.',
     'Improbable: No existen antecedentes conocidos de que haya ocurrido y se cuenta con medidas adecuadas para '
     'evitarla. No se observan señales de que pueda suceder.',
     'Leve: No genera un daño importante al ambiente y sus efectos desaparecen rápidamente.',
     'Puntual: El impacto ambiental se limita a un espacio pequeño y específico donde se realiza la actividad, '
     'sin extenderse a otras áreas.'],
    ['Media (3)',
     'Ocasional: La actividad o situación ocurre desde una vez al mes hasta una vez por semana.',
     'Posible: Ha ocurrido alguna vez o existen condiciones que podrían ocasionarla, aunque se cuenta con '
     'algunas medidas para prevenirla.',
     'Moderado: Genera un daño al ambiente que puede mantenerse por un tiempo y necesita acciones para '
     'corregirse.',
     'Local: El impacto ambiental se extiende a otras áreas cercanas al lugar donde se origina, pero permanece '
     'dentro de las instalaciones o zona de trabajo.'],
    ['Alta (5)',
     'Constante: La actividad o situación ocurre varias veces por semana, diariamente o de forma continua.',
     'Muy probable: Ha ocurrido varias veces o existen fallas, daños o condiciones peligrosas que hacen '
     'probable que suceda nuevamente.',
     'Grave: Genera un daño importante al ambiente que puede durar mucho tiempo o ser difícil de corregir.',
     'Externo: El impacto ambiental llega más allá de las instalaciones o zona donde se realiza la actividad y '
     'puede afectar otros lugares.'],
]
CRITERIA_IMPACT_TITLE = '2. Tabla de Criterios de Valoración de Impactos'
# Texto con formato mixto: la parte intermedia va en negrita
CRITERIA_IMPACT_TEXT = ('Para calcular el ', 'Nivel de Impacto (NI)',
                        ', aplicas la fórmula matemática polinomial basada en tu procedimiento:')
CRITERIA_IMPACT_FORMULA = 'NI = F * S * A'
CRITERIA_IMPACT_HEADERS = ['Puntuación', 'Significancia', 'Medida de Control Operacional Obligatoria']
CRITERIA_IMPACT_NOT_SIGNIFICANT = [
    'Bajo / Medio', ('De ', '1 a 25'), NOT_SIGNIFICANT_TEXT,
    'No requiere control adicional. Es opcional aplicar buenas prácticas ambientales para prevenir, reducir o '
    'controlar el impacto ambiental adverso.']
CRITERIA_IMPACT_SIGNIFICANT = [
    'Alto', ('Igual o superior a ', '27'), SIGNIFICANT_TEXT,
    ('Acciones de prioridad primaria obligatorias',
     ' para la prevención, control y/o reducción de los impactos. '
     'Estos aspectos serán elementos de entrada para establecer los objetivos y metas ambientales del SIG y serán '
     'motivo de monitoreo o verificación periódica.')]
# Ancho de las columnas A:F y alto (en puntos) de las filas 1 a 19, igual que la plantilla
CRITERIA_COLUMN_WIDTHS = [2.55, 14.55, 36.11, 36.11, 40.44, 33.66]
CRITERIA_ROW_HEIGHTS = [10.35, 27, 10.35, 13.35, 13.35, 28.95, 59.4, 59.4, 59.4, 10.35, 13.35, 10.35, 13.8, 14.4,
                        29.4, 14.4, 14.4, 69.6, 69.6]


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

    @staticmethod
    def _write_criteria_sheet(workbook):
        """Agrega la hoja informativa CRITERIOS con las tablas de criterios de valoración."""
        def fmt(**kwargs):
            base = {'font_name': 'Calibri', 'font_size': 9, 'align': 'center', 'valign': 'vcenter',
                    'text_wrap': True, 'border': 1}
            base.update(kwargs)
            return workbook.add_format(base)

        def run(**kwargs):
            # Formato de un tramo de texto dentro de una celda (solo propiedades de fuente)
            base = {'font_name': 'Calibri', 'font_size': 9}
            base.update(kwargs)
            return workbook.add_format(base)

        format_title = fmt(font_size=14, bold=True, bg_color='#E7E6E6')
        format_section = fmt(bold=True, align='left', border=0, bg_color='#E2EFDA')
        format_header = fmt(bold=True, font_color='#000000', bg_color='#DFDFDF')
        format_score = fmt()
        format_criteria = fmt(bold=True, align='left', font_color='#1F1F1F')
        format_text = fmt(align='left', font_color='#1F1F1F')
        format_text_bold = fmt(bold=True, align='left', font_color='#1F1F1F')
        format_text_arial = fmt(font_name='Arial', font_size=11, align='left', border=0, text_wrap=False)
        format_formula = fmt(font_name='Arial', font_size=11, bg_color='#E7E6E6')
        format_ns = fmt(bold=True, font_color='#FFFFFF', bg_color='#00AF50')
        format_s = fmt(bold=True, font_color='#FFFFFF', bg_color='#FF0000')
        format_score_rich = fmt()
        run_header_letter = run(bold=True, font_color='#C00000')
        run_header_text = run(bold=True, font_color='#000000')
        run_normal = run(font_color='#1F1F1F')
        run_bold = run(bold=True, font_color='#1F1F1F')
        run_arial = run(font_name='Arial', font_size=11)
        run_arial_bold = run(font_name='Arial', font_size=11, bold=True)

        sheet = workbook.add_worksheet(CRITERIA_SHEET_NAME)
        sheet.hide_gridlines(2)
        sheet.set_zoom(115)
        sheet.set_landscape()
        sheet.set_paper(9)
        sheet.fit_to_pages(1, 0)
        for col, width in enumerate(CRITERIA_COLUMN_WIDTHS):
            sheet.set_column(col, col, width)
        for row, height in enumerate(CRITERIA_ROW_HEIGHTS):
            sheet.set_row(row, height)

        sheet.merge_range('A2:F2', CRITERIA_TITLE, format_title)

        # 1. Criterios de evaluación por condiciones
        for col in (0, 4, 5):
            sheet.write_blank(3, col, None, format_section)
        sheet.merge_range('B4:D4', CRITERIA_CONDITIONS_TITLE, format_section)
        sheet.write(5, 1, CRITERIA_CONDITIONS_HEADERS[0], format_header)
        for col, header in enumerate(CRITERIA_CONDITIONS_HEADERS[1:], start=2):
            # "F - " (letra del criterio) en rojo y el resto en negro
            letter, text = header.split(' - ', 1)
            sheet.write_rich_string(5, col, run_header_letter, letter + ' - ', run_header_text, text, format_header)
        for row, values in enumerate(CRITERIA_CONDITIONS_ROWS, start=6):
            sheet.write(row, 1, values[0], format_score)
            for col, value in enumerate(values[1:], start=2):
                # "Raramente:" en negrita y la descripción en texto normal
                label, text = value.split(':', 1)
                sheet.write_rich_string(row, col, run_bold, label + ':', run_normal, text, format_criteria)

        # 2. Criterios de valoración de impactos
        for col in (0, 4, 5):
            sheet.write_blank(10, col, None, format_section)
        sheet.merge_range('B11:D11', CRITERIA_IMPACT_TITLE, format_section)
        before, bold, after = CRITERIA_IMPACT_TEXT
        sheet.write_rich_string(12, 1, run_arial, before, run_arial_bold, bold, run_arial, after, format_text_arial)
        sheet.merge_range('B15:F15', CRITERIA_IMPACT_FORMULA, format_formula)
        for col, header in enumerate(CRITERIA_IMPACT_HEADERS, start=2):
            sheet.write(16, col, header, format_header)
        for row, values, format_significance, format_measure, run_measure in (
                (17, CRITERIA_IMPACT_NOT_SIGNIFICANT, format_ns, format_text, None),
                (18, CRITERIA_IMPACT_SIGNIFICANT, format_s, format_text_bold, run_normal)):
            sheet.write(row, 1, values[0], format_score)
            before, bold = values[1]
            sheet.write_rich_string(row, 2, before, run_bold, bold, run_normal, ' ', format_score_rich)
            sheet.write(row, 3, values[2], format_significance)
            if run_measure:
                bold, text = values[3]
                sheet.write_rich_string(row, 4, bold, run_measure, text, format_measure)
            else:
                sheet.write(row, 4, values[3], format_measure)

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

        # Se reserva el nombre de la hoja informativa para que ninguna matriz lo use
        used_names = {CRITERIA_SHEET_NAME.lower()}
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

        self._write_criteria_sheet(workbook)
