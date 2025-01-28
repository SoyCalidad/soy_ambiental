import base64
import io

from odoo import fields, models
from PIL import Image
from datetime import datetime


class IDEAAMatrixXLSXReport(models.AbstractModel):
    _name = 'report.sga_ideaa_matrix_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, matrixes):
        format_title = workbook.add_format(
            {'font_size': 18, 'font_name': 'Calibri', 'color': '#FFFFFF', 'bg_color': '#4F81BD',
             'valign': 'vcenter', 'align': 'center', 'bold': True, 'text_wrap': True, 'border': 1})
        format_header = workbook.add_format(
            {'font_size': 12, 'font_name': 'Calibri', 'color': '#FFFFFF', 'bg_color': '#4F81BD',
             'valign': 'vcenter', 'align': 'left', 'bold': True, 'text_wrap': True, 'border': 1})

        format_cell_left = workbook.add_format(
            {'font_size': 11, 'font_name': 'Calibri', 'align': 'left', 'valign': 'vcenter',
             'bold': False, 'text_wrap': True, 'border': 1})

        format_cell_right = workbook.add_format(
            {'font_size': 11, 'font_name': 'Calibri', 'align': 'right', 'valign': 'vcenter',
             'bold': False, 'text_wrap': True, 'border': 1})
        format_cell_center = workbook.add_format(
            {'font_size': 11, 'font_name': 'Calibri', 'align': 'center', 'valign': 'vcenter',
             'bold': False, 'text_wrap': True, 'border': 1})
        format_monetary = workbook.add_format(
            {'num_format': '#,##0.00', 'font_size': 11, 'font_name': 'Arial Narrow', 'align': 'right',
             'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': 1})
        format_percent = workbook.add_format(
            {'num_format': '0.00"%"', 'font_size': 11, 'font_name': 'Arial Narrow', 'align': 'right',
             'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': 1})


        format_header_group1 = workbook.add_format(
            {'font_size': 10, 'bg_color': '#C4D79B', 'valign': 'vcenter', 'align': 'center', 'bold': True,
             'text_wrap': True, 'border': 1})

        format_header_group2 = workbook.add_format(
            {'font_size': 10, 'bg_color': '#76933C', 'valign': 'vcenter', 'align': 'center', 'bold': True,
             'text_wrap': True, 'border': 1})

        format_header2_group2 = workbook.add_format(
            {'font_size': 10, 'bg_color': '#76933C', 'valign': 'vcenter', 'align': 'center', 'bold': False,
             'text_wrap': True, 'border': 1})

        format_header_group3 = workbook.add_format(
            {'font_size': 10, 'bg_color': '#00B050', 'valign': 'vcenter', 'align': 'center', 'bold': True,
             'text_wrap': True, 'border': 1})

        format_header2_group3 = workbook.add_format(
            {'font_size': 10, 'bg_color': '#00B050', 'valign': 'vcenter', 'align': 'center', 'bold': False,
             'text_wrap': True, 'border': 1})

        format_header_group2_rotation = workbook.add_format(
            {'font_size': 10, 'bg_color': '#76933C', 'valign': 'vcenter', 'align': 'center', 'bold': False,
             'text_wrap': True, 'border': 1})
        format_header_group2_rotation.set_rotation(90)

        format_header_group3_rotation = workbook.add_format(
            {'font_size': 10, 'bg_color': '#00B050', 'valign': 'vcenter', 'align': 'center', 'bold': False,
             'text_wrap': True, 'border': 1})
        format_header_group3_rotation.set_rotation(90)

        sheet = workbook.add_worksheet('Matriz de identificación de aspectos ambientales')
        sheet.merge_range(0, 0, 0, 6, 'Identificación de Aspectos, Impactos y Riesgos Ambientales', format_header_group1)
        sheet.merge_range(0, 7, 0, 16, 'Evaluación de Significancia de Aspectos Ambientales', format_header_group2)
        sheet.merge_range(0, 17, 0, 21, 'Evaluación del Riesgo Residual / Oportunidad Implementada', format_header_group3)

        sheet.merge_range(1, 0, 2, 0, 'NOMBRE', format_header_group1)
        sheet.merge_range(1, 1, 2, 1, 'ETAPA', format_header_group1)
        sheet.merge_range(1, 2, 2, 2, 'ACTIVIDAD', format_header_group1)
        sheet.merge_range(1, 3, 2, 3, 'TAREA', format_header_group1)
        sheet.merge_range(1, 4, 2, 4, 'PUESTOS DE TRABAJO', format_header_group1)
        sheet.merge_range(1, 5, 2, 5, 'ASPECTO', format_header_group1)
        sheet.merge_range(1, 6, 2, 6, 'IMPACTO', format_header_group1)

        sheet.merge_range(1, 7, 2, 7, 'PROBABILIDAD', format_header_group2)
        sheet.merge_range(1, 8, 1, 12, 'Criterios para valorar las consecuencias', format_header2_group2)
        sheet.write(2, 8, 'Legal/Cumplimiento', format_header_group2_rotation)
        sheet.write(2, 9, 'Medio Ambiente', format_header_group2_rotation)
        sheet.write(2, 10, 'Partes interesadas (Regional, Nacional, Internacional)', format_header_group2_rotation)
        sheet.write(2, 11, 'Capacidad de Producción', format_header_group2_rotation)
        sheet.write(2, 12, 'Financiera', format_header_group2_rotation)
        sheet.merge_range(1, 13, 2, 13, 'CONSECUENCIA', format_header_group2)
        sheet.merge_range(1, 14, 2, 14, 'CALIFICACICÓN', format_header_group2)
        sheet.merge_range(1, 15, 2, 15, 'G=P*C', format_header_group2)
        sheet.merge_range(1, 16, 2, 16, 'REQUISITOS LEGALES', format_header_group2)

        sheet.merge_range(1, 17, 2, 17, 'CONTROL', format_header_group3)
        sheet.merge_range(1, 18, 2, 18, 'Frecuencia / Probabilidad', format_header_group3_rotation)
        sheet.merge_range(1, 19, 2, 19, 'Consecuencia ', format_header_group3_rotation)
        sheet.merge_range(1, 20, 1, 21, 'Riesgo Residual / Oportunidad Implementada ', format_header2_group3)
        sheet.write(2, 20, 'PxC', format_header_group3_rotation)
        sheet.write(2, 21, 'Calificación', format_header2_group3)

        sheet.set_column('A:G', 20)
        sheet.set_column('E:E', 25)
        sheet.set_column('H:P', 10)
        sheet.set_column('Q:Q', 15)
        sheet.set_column('R:V', 10)
        sheet.set_row(1, 50)
        sheet.set_row(2, 100)

        row = 3
        for matrix in matrixes:
            process_count = len(matrix.process_evaluation_ids)
            control_count = len(matrix.process_control_ids)
            max_records = max(process_count, control_count)
            processes = matrix.process_evaluation_ids
            controls = matrix.process_control_ids

            if max_records > 0:
                sheet.merge_range(row, 0, row + max_records - 1, 0, matrix.name or '', format_cell_left)

            for i in range(max_records):
                if i < process_count:
                    process = processes[i]
                    sheet.write(row, 1, process.stage_id.name or '', format_cell_left)
                    sheet.write(row, 2, process.activity_id.name or '', format_cell_left)
                    sheet.write(row, 3, process.task_id.name or '', format_cell_left)
                    sheet.write(row, 4, '\n'.join(['- ' + x.name for x in process.job_ids]), format_cell_left)
                    sheet.write(row, 5, '\n'.join(['- ' + x.name for x in process.aspect_ids]), format_cell_left)
                    sheet.write(row, 6, '\n'.join(['- ' + x.name for x in process.impact_ids]), format_cell_left)

                    probabilidad = next(
                        (
                            x.evaluation_value_id.name
                            for x in process.evaluation_ids
                            if x.evaluation_item_id.name == 'Probabilidad de ocurrencia' and x.evaluation_value_id
                        ),
                        ''
                    )
                    sheet.write(row, 7, probabilidad, format_cell_left)
                    criterio_columns = {
                        "Legal/Cumplimiento": 8,
                        "Medio ambiente": 9,
                        "Partes interesadas": 10,
                        "Capacidad de producción": 11,
                        "Financiera": 12
                    }

                    for x in process.evaluation_ids:
                        if x.evaluation_item_id.name == 'Consecuencia':
                            for criterio in x.evaluation_item_id.criterio_ids:
                                col_index = criterio_columns.get(criterio.name)
                                if col_index:
                                    value = criterio.item_value_id.name if criterio.item_value_id else ''
                                    sheet.write(row, col_index, value, format_cell_left)

                    consecuencia = next(
                        (
                            x.evaluation_value_id.name
                            for x in process.evaluation_ids
                            if x.evaluation_item_id.name == 'Consecuencia' and x.evaluation_value_id
                        ),
                        ''
                    )
                    sheet.write(row, 13, consecuencia, format_cell_left)
                    sheet.write(row, 14, process.level, format_cell_left)
                    sheet.write(row, 15, process.evaluation_pxc, format_cell_left)
                    sheet.write(row, 16, '\n'.join(['- ' + x.name for x in process.legal_ids]), format_cell_left)

                if i < control_count:
                    control = controls[i]
                    sheet.write(row, 17, '\n'.join(['- ' + x.name for x in control.action_ids]), format_cell_left)

                    probabilidad = next(
                        (
                            x.evaluation_value_id.name
                            for x in control.reevaluation_ids
                            if x.evaluation_item_id.name == 'Probabilidad de ocurrencia' and x.evaluation_value_id
                        ),
                        ''
                    )
                    sheet.write(row, 18, probabilidad, format_cell_left)

                    consecuencia = next(
                        (
                            x.evaluation_value_id.name
                            for x in control.reevaluation_ids
                            if x.evaluation_item_id.name == 'Consecuencia' and x.evaluation_value_id
                        ),
                        ''
                    )
                    sheet.write(row, 19, consecuencia, format_cell_left)
                    sheet.write(row, 20, control.control_pxc, format_cell_left)
                    sheet.write(row, 21, control.control_level, format_cell_left)

                row += 1
