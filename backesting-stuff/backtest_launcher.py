from strategy_example import SMACrossoverStrategy, multi_params, single_params, maximize_func, constraint_func
from utils.functions2 import single_backtest_start
from pathlib import Path

strategy = SMACrossoverStrategy

file_path = "historical-data/5min/ARB-USD-5m-2023.csv"
input_directories = ['historical-data/15min', 'historical-data/5min']
start_date = '2022-01-01'
end_date = '2024-10-31'

save_the_plot = True
use_full_data = True
optimize_params = False
bulk_backtest = False

params = {}

if optimize_params:
    params = multi_params
else:
    params = single_params


if not bulk_backtest:
    single_backtest_start(file_path, start_date, end_date, strategy, params, save_the_plot, use_full_data, maximize_func, constraint_func)

if bulk_backtest:
    # # * multi file backtest controls
    for input_directory in input_directories:

        for file_path in Path(input_directory).glob('*.csv'):
            single_backtest_start(file_path, start_date, end_date, strategy, params, save_the_plot, use_full_data, maximize_func, constraint_func)