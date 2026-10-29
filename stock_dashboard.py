import streamlit as st
import pandas as pd
import akshare as ak

def markdown_info():
    guide = '''
## User Guide

### Cheatsheet

| Key | Function |
| -- | -- |
|  | **File Browser** |
| `F3` | open browser |
| `,t` | open the location of current file |
|  | **Tab** |
| `tt` | open new tab |
| `<Alt>-left/right` | navigate tabs |
| `-` | choose window |
|  | **Clipboard** |
| `<Ctrl>-p/n` | cycle through clipboard (yank) history |
|  | **Find** |
| `,e` | find file recursively. `<Ctrl>-t` to open the file in new tab |
| `,f` | find any text in current file |
| `,F` | find any text in all opened files |
| `,wf` | find current text under the cursor in current file |
| `,wF` | find current text under the cursor in all opened files |
| `,g` | find symbol (class/method/variable/...) in current file |
| `,G` | find symbol (class/method/variable/...) in all opened files |
| `,wg` | find current symbol under the cursor in current file |
| `,wG` | find current symbol under the cursor in all opened files |
| `,c` | find commands (internal vim commands, or custom commands)|
| `,r` | grep code recursively using Ack! |
| `,wr` | grep current word under the cursor recursively using Ack! |
|  | **Coding** |
| `,d` | go to definition of the thing under the cursor |
| `,o` | find occurrences of the thing under the cursor |
| `<Shift>-k` | show docstring of the thing under the cursor |
| `\\ci` | comment/uncomment code |
| `F2` | open pending tasks list (comments in the current file starting with "TODO", "FIXME", etc) |
| `F4` | open the item list of current file |
|  | **Git** |
| `:Git <CMD>` |  such as `:Git status`, `:Git blame`, `:Git log`, `:Git commit`, etc |


'''
    st.markdown(guide)


# st.set_page_config(layout="wide") #display app in wide mode

# sidebar
st.sidebar.subheader('Input CSV')
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.subheader('DataFrame')
    st.sidebar.write(df)
else:
    st.sidebar.info('Upload a CSV file')

# main page
st.title('Dashboard')

markdown_info()

if uploaded_file:
    symbols = df.symbol
    shares = df.shares
    bonus = df.bonus
    data_load_state = st.text('Loading data...')
    stock_df = ak.stock_zh_a_spot()
    fund_etf_df = ak.fund_etf_category_sina(symbol="ETF基金")
    data_load_state.text("Loading done!")
    names, prices, change_rates, change_values = [], [], [], []
    for symbol in symbols:
        if symbol.startswith('sz1') or symbol.startswith('sh5'): # ETF
            name = fund_etf_df.loc[fund_etf_df.代码 == symbol, '名称'].values[0]
            price = float(fund_etf_df.loc[fund_etf_df.代码 == symbol, '最新价'].values[0])
            change_rate = fund_etf_df.loc[fund_etf_df.代码 == symbol, '涨跌幅'].values[0]/100
            change_value = fund_etf_df.loc[fund_etf_df.代码 == symbol, '涨跌额'].values[0]
        else: # stock
            name = stock_df.loc[stock_df.代码==symbol, '名称'].values[0]
            price = float(stock_df.loc[stock_df.代码==symbol, '最新价'].values[0])
            change_rate = stock_df.loc[stock_df.代码==symbol, '涨跌幅'].values[0]/100
            change_value = stock_df.loc[stock_df.代码 == symbol, '涨跌额'].values[0]
        names.append(name)
        prices.append(price)
        change_rates.append(change_rate)
        change_values.append(change_value)

    my_stock_df = pd.DataFrame({
        '名称': names,
        '份额': shares,
        '价格': prices,
        '涨跌幅': change_rates,
        '涨跌额': change_values
    })

    my_stock_df['涨跌'] = my_stock_df['涨跌额'] * my_stock_df['份额']
    my_stock_df['市值'] = my_stock_df['价格'] * my_stock_df['份额']
    my_stock_df['每股分红'] = bonus
    my_stock_df['分红'] = my_stock_df['每股分红'] * my_stock_df['份额']
    my_stock_df['股息率'] = my_stock_df['每股分红'] / my_stock_df['价格']

    # formatting
    my_stock_df['涨跌幅'] = my_stock_df['涨跌幅'].map(lambda x: format(x, '.2%'))
    # my_stock_df['份额'] = my_stock_df['份额'].map(lambda x: format(x, ','))
    # my_stock_df['市值'] = my_stock_df['市值'].map(lambda x: format(x, ','))
    # my_stock_df['分红'] = my_stock_df['分红'].map(lambda x: format(x, ','))
    my_stock_df['股息率'] = my_stock_df['股息率'].map(lambda x: format(x, '.2%'))

    # summing
    my_stock_df.loc[len(my_stock_df)] = my_stock_df.loc[:, ['涨跌', '市值', '分红']].sum()

    st.write(my_stock_df)
