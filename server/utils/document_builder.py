
import xlsxwriter
"""
   {
      "id": 165,
      "timestamp": "2024-04-01T16:30:37.575162Z",
      "invested_value": 437223.09,
      "market_value": 442688.93999999994,
      "overall_pl": 5465.8499999999185,
      "change_invested_value": 0.0,
      "change_market_value": 0.0,
      "change_overall_pl": 0.0,
      "percent_change_invested_value": 0.0,
      "percent_change_market_value": 0.0,
      "percent_change_overall_pl": 0.0,
      "created_at": "2024-04-01T16:30:38.211395Z",
      "updated_at": "2024-04-01T16:30:38.211411Z",
      "user": 3
    },
"""

"""
 {
      "id": 1,
      "portfolio_asset": {
        "ticker": "XLP",
        "category": "stocks",
        "name": "XLP",
        "pricing": 76.36,
        "daypl": -0.12999999999999545,
        "daypl_percent": -0.1702462022000988
      },
      "quantity": 1.0,
      "avg_buy_price": 75.43,
      "marketValue": 76.36,
      "profitLoss": 0.9299999999999926,
      "percentPL": 1.232931194484943,
      "daypl": -0.12999999999999545,
      "daypl_percent": -0.17234522073444974
    },
"""

"""
    {
      "id": 33,
      "transaction_asset": {
        "ticker": "X:ETHUSD",
        "category": "crypto",
        "name": "Ethereum"
      },
      "quantity": 5,
      "buy_price": 3561.1,
      "sell_price": null,
      "created_at": "2024-03-30T08:46:07.236565Z",
      "updated_at": "2024-03-30T08:46:07.236595Z",
      "user": 3
    },
"""
def create_xlsx_from_portfolio_details( portfolio_details,userId, stock_holdings,transactions):
    workbook = xlsxwriter.Workbook(f'{userId}_portfolio_details.xlsx')
    worksheet = workbook.add_worksheet("Daily Portfolio")
    worksheet.write('A1', 'Timestamp')
    worksheet.write('B1', 'Invested Value')
    worksheet.write('C1', 'Market Value')
    worksheet.write('D1', 'Overall PL')
    worksheet.write('E1', 'Change Invested Value')
    worksheet.write('F1', 'Change Market Value')
    worksheet.write('G1', 'Change Overall PL')
    worksheet.write('H1', 'Percent Change Invested Value')
    worksheet.write('I1', 'Percent Change Market Value')
    worksheet.write('J1', 'Percent Change Overall PL')
    worksheet.write('K1', 'Created At')
    worksheet.write('L1', 'Updated At')
    worksheet.write('M1', 'User')
    row = 1
    col = 0
    for portfolio in portfolio_details:
        worksheet.write(row, col, portfolio['timestamp'])
        worksheet.write(row, col + 1, portfolio['invested_value'])
        worksheet.write(row, col + 2, portfolio['market_value'])
        worksheet.write(row, col + 3, portfolio['overall_pl'])
        worksheet.write(row, col + 4, portfolio['change_invested_value'])
        worksheet.write(row, col + 5, portfolio['change_market_value'])
        worksheet.write(row, col + 6, portfolio['change_overall_pl'])
        worksheet.write(row, col + 7, portfolio['percent_change_invested_value'])
        worksheet.write(row, col + 8, portfolio['percent_change_market_value'])
        worksheet.write(row, col + 9, portfolio['percent_change_overall_pl'])
        worksheet.write(row, col + 10, portfolio['created_at'])
        worksheet.write(row, col + 11, portfolio['updated_at'])
        worksheet.write(row, col + 12, portfolio['user'])
        row += 1
    worksheet = workbook.add_worksheet("Stock Holdings")
    worksheet.write('A1', 'Ticker')
    worksheet.write('B1', 'Category')
    worksheet.write('C1', 'Name')
    worksheet.write('D1', 'Pricing')
    worksheet.write('E1', 'Day PL')
    worksheet.write('F1', 'Day PL Percent')
    worksheet.write('G1', 'Quantity')
    worksheet.write('H1', 'Avg Buy Price')
    worksheet.write('I1', 'Market Value')
    worksheet.write('J1', 'Profit Loss')
    worksheet.write('K1', 'Percent PL')
    row = 1
    col = 0
    for stock in stock_holdings:
        worksheet.write(row, col, stock['portfolio_asset']['ticker'])
        worksheet.write(row, col + 1, stock['portfolio_asset']['category'])
        worksheet.write(row, col + 2, stock['portfolio_asset']['name'])
        worksheet.write(row, col + 3, stock['portfolio_asset']['pricing'])
        worksheet.write(row, col + 4, stock['portfolio_asset']['daypl'])
        worksheet.write(row, col + 5, stock['portfolio_asset']['daypl_percent'])
        worksheet.write(row, col + 6, stock['quantity'])
        worksheet.write(row, col + 7, stock['avg_buy_price'])
        worksheet.write(row, col + 8, stock['marketValue'])
        worksheet.write(row, col + 9, stock['profitLoss'])
        worksheet.write(row, col + 10, stock['percentPL'])
        row += 1
    worksheet = workbook.add_worksheet("Transactions")
    worksheet.write('A1', 'Transaction Type')
    worksheet.write('B1', 'Ticker')
    worksheet.write('C1', 'Category')
    worksheet.write('D1', 'Name')
    worksheet.write('E1', 'Quantity')
    worksheet.write('F1', 'Price')
    worksheet.write('G1', 'Created At')

    row = 1
    col = 0

    for transaction in transactions:
        worksheet.write(row, col, "Buy" if transaction['sell_price'] is None else "Sell")
        worksheet.write(row, col + 1, transaction['transaction_asset']['ticker'])
        worksheet.write(row, col + 2, transaction['transaction_asset']['category'])
        worksheet.write(row, col + 3, transaction['transaction_asset']['name'])
        worksheet.write(row, col + 4, transaction['quantity'])
        worksheet.write(row, col + 5, transaction['buy_price'] if transaction['sell_price'] is None else transaction['sell_price'])
        worksheet.write(row, col + 6, transaction['created_at'])
        row += 1


    workbook.close()