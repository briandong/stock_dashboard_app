import streamlit as st
import pandas as pd
import akshare as ak

# 股票
# 实时行情数据-新浪
stock_df = ak.stock_zh_a_spot()
print(stock_df.tail())
print(stock_df.loc[stock_df.代码=='sh600036', ['名称', '最新价', '涨跌幅', '涨跌额']])
print(stock_df.loc[stock_df.代码=='sz000333', ['名称', '最新价', '涨跌幅', '涨跌额']])

# 基金
# ETF基金实时行情-东财
# etf_list = ak.fund_etf_spot_em()
# print(etf_list.tail())
#
# print(etf_list.loc[etf_list.代码=='510880', ['最新价', '涨跌额']])
# print(etf_list.loc[etf_list.代码=='515180', ['最新价', '涨跌额']])
# print(etf_list.loc[etf_list.代码=='sh501009'], ['最新价', '涨跌额'])

# 基金实时行情-新浪
etf_df = ak.fund_etf_category_sina(symbol="ETF基金")
print(etf_df.tail())
print(etf_df.loc[etf_df.代码=='sh510880', ['名称', '最新价', '涨跌幅', '涨跌额']])
print(etf_df.loc[etf_df.代码=='sh515180', ['名称', '最新价', '涨跌幅', '涨跌额']])

