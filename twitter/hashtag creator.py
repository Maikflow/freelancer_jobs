__author__ = 'maikflow'
import xlrd
import tagcloud

some_list = []
workbook = xlrd.open_workbook('hashtags.xls')
worksheets = workbook.sheet_names()
for worksheet_name in worksheets:
    worksheet = workbook.sheet_by_name(worksheet_name)
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    curr_row = -2
    while curr_row < num_rows:
        row = worksheet.row(curr_row)
        # print 'Row:', curr_row
        curr_row += 3
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
            # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
            # cell_type = worksheet.cell_type(curr_row, curr_cell)
            try:
                cell_value = worksheet.cell_value(curr_row, curr_cell)
                print cell_value.encode('utf8')
                some_list.append(cell_value.encode('utf8'))
            except IndexError:
                pass
# print type(some_list[0].encode('utf8'))
tagcloud.make_cloud(''.join(some_list),'#epp2014')