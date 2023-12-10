import logging
import typing

import gspread_asyncio
from gspread_asyncio import AsyncioGspreadClient


async def create_spreadsheet(client: AsyncioGspreadClient, spreadsheet_name: str):
    spreadsheet = await client.create(spreadsheet_name)
    spreadsheet = await client.open_by_key(spreadsheet.id)
    return spreadsheet

async def add_worksheet(async_spreadsheet: gspread_asyncio.AsyncioGspreadSpreadsheet,
                        worksheet_name: str):
    worksheet = await async_spreadsheet.add_worksheet(worksheet_name, rows=1000, cols=50)
    worksheet = await async_spreadsheet.worksheet(worksheet_name)
    return worksheet

async def share_spreadsheet(async_spreadsheet: AsyncioGspreadClient,
                            file_id: str,value:str, role: str = 'writer'):
    await async_spreadsheet.insert_permission(file_id=file_id, value=value, perm_type ='anyone', role=role)

async def fill_in_data(worksheet: gspread_asyncio.AsyncioGspreadWorksheet, data: typing.Tuple[typing.Tuple]):
    await worksheet.append_row(data)

async def refactor_in_data(worksheet: gspread_asyncio.AsyncioGspreadWorksheet, data: typing.Tuple[typing.Tuple]):
    row = await worksheet.find(data[0])
    s_row = str(row)
    await worksheet.update_cell(row=int(s_row[7]), col=6, value=data[-1])

async def refactor2_in_data(worksheet: gspread_asyncio.AsyncioGspreadWorksheet, data: typing.Tuple[typing.Tuple]):
    row = await worksheet.find(data[0])
    s_row = str(row)
    await worksheet.update_cell(row=int(s_row[7]), col=7, value=data[-1])