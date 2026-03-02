import base64
import io

from odoo import fields, models
from PIL import Image
from datetime import datetime
import logging 


_logger = logging.getLogger(__name__)


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
        format26_c_bold = workbook.add_format(
                {'font_size': 26,   'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format21_c_bold = workbook.add_format(
                {'font_size': 10,   'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        company = self.env.company
        for matrix in matrixes.sudo():
            sheet = workbook.add_worksheet('Matriz de identificación de aspectos ambientales')
            #header 
            
            current_row = 0
            sheet.merge_range('A1:C3', '', )
            if hasattr(matrix, 'company_id') and matrix.company_id:
                company = matrix.company_id

            buf_image = io.BytesIO(base64.b64decode(company.logo))
            im = Image.open(buf_image)
            width, height = im.size
            image_width = width
            image_height = height
            cell_width = 48.0
            cell_height = 48.0

            x_scale = cell_width/image_width
            y_scale = cell_height/image_height
            sheet.insert_image('A1', "logo.png", {
                'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
            
            sheet.merge_range(current_row, 3, current_row +2, 16, 'Matriz IDEAA', format26_c_bold)
            sheet.merge_range(current_row, 17, current_row,21, 'Código: '+str(matrix.code or ''), format21_c_bold)
            sheet.merge_range(current_row+1, 17, current_row+1,21,
                                'Edición: '+str(matrix.version), format21_c_bold)
            sheet.merge_range(current_row+2, 17, current_row+2,21, 'Fecha de aprobación: '+str(
                matrix.date_validate or "Sin definir"), format21_c_bold)
            
            
            current_row += 4
            
            sheet.merge_range(current_row, 0, current_row, 6, 'Identificación de Aspectos, Impactos y Riesgos Ambientales', format_header_group1)
            sheet.merge_range(current_row, 7, current_row, 16, 'Evaluación de Significancia de Aspectos Ambientales', format_header_group2)
            sheet.merge_range(current_row, 17, current_row, 21, 'Evaluación del Riesgo Residual / Oportunidad Implementada', format_header_group3)

            current_row += 1
            sheet.merge_range(current_row, 0, current_row +1, 0, 'NOMBRE', format_header_group1)
            sheet.merge_range(current_row, 1, current_row+1, 1, 'ETAPA', format_header_group1)
            sheet.merge_range(current_row, 2, current_row+1, 2, 'ACTIVIDAD', format_header_group1)
            sheet.merge_range(current_row, 3, current_row+1, 3, 'TAREA', format_header_group1)
            sheet.merge_range(current_row, 4, current_row+1, 4, 'PUESTOS DE TRABAJO', format_header_group1)
            sheet.merge_range(current_row, 5, current_row+1, 5, 'ASPECTO', format_header_group1)
            sheet.merge_range(current_row, 6, current_row+1, 6, 'IMPACTO', format_header_group1)

            sheet.merge_range(current_row, 7, current_row+1, 7, 'PROBABILIDAD', format_header_group2)
            sheet.merge_range(current_row, 8, current_row, 12, 'Criterios para valorar las consecuencias', format_header2_group2)
            sheet.write(current_row+1, 8, 'Legal/Cumplimiento', format_header_group2_rotation)
            sheet.write(current_row+1, 9, 'Medio Ambiente', format_header_group2_rotation)
            sheet.write(current_row+1, 10, 'Partes interesadas (Regional, Nacional, Internacional)', format_header_group2_rotation)
            sheet.write(current_row+1, 11, 'Capacidad de Producción', format_header_group2_rotation)
            sheet.write(current_row+1, 12, 'Financiera', format_header_group2_rotation)
            sheet.merge_range(current_row, 13, current_row+1, 13, 'CONSECUENCIA', format_header_group2)
            sheet.merge_range(current_row, 14, current_row+1, 14, 'CALIFICACICÓN', format_header_group2)
            sheet.merge_range(current_row, 15, current_row+1, 15, 'G=P*C', format_header_group2)
            sheet.merge_range(current_row, 16, current_row+1, 16, 'REQUISITOS LEGALES', format_header_group2)

            sheet.merge_range(current_row, 17, current_row+1, 17, 'CONTROL', format_header_group3)
            sheet.merge_range(current_row, 18, current_row+1, 18, 'Frecuencia / Probabilidad', format_header_group3_rotation)
            sheet.merge_range(current_row, 19, current_row+1, 19, 'Consecuencia ', format_header_group3_rotation)
            sheet.merge_range(current_row, 20, current_row, 21, 'Riesgo Residual / Oportunidad Implementada ', format_header2_group3)
            sheet.write(current_row+1, 20, 'PxC', format_header_group3_rotation)
            sheet.write(current_row+1, 21, 'Calificación', format_header2_group3)

            sheet.set_column('A:G', 20)
            sheet.set_column('E:E', 25)
            sheet.set_column('H:P', 10)
            sheet.set_column('Q:Q', 15)
            sheet.set_column('R:V', 10)
            sheet.set_row(5, 50)
            sheet.set_row(6, 100)

            row = current_row +2
            process_count = len(matrix.process_evaluation_ids)
            control_count = len(matrix.process_control_ids)
            max_records = max(process_count, control_count)
            processes = matrix.process_evaluation_ids
            controls = matrix.process_control_ids

            if max_records > 1:
                sheet.merge_range(row, 0, row + max_records - 1, 0, matrix.name or '', format_cell_left)
            if max_records == 1:
                sheet.write(row, 0, matrix.name or '', format_cell_left)

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
                
