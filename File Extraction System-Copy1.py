#!/usr/bin/env python
# coding: utf-8

# In[268]:


import bs4 as bs
import requests 
import pandas as pd
import os
import datetime as dt
import pandas_datareader as web
import pickle


# In[281]:


def load_sp500_tickers():
        link = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        response = requests.get(link)
        soup = bs.BeautifulSoup(response.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers=[]
        for row in table.findAll('tr')[1:]:
          ticker = row.findAll('td')[0].text[:-1]
          tickers.append(ticker) 
        with open("sp500tickers.pickle",'wb') as f:
                pickle.dump(tickers,f)
        return tickers


# In[282]:


def load_prices(reload_tickers=False):
 if reload_tickers:
        tickers = load_sp500_tickers()
 else:
        if os.path.exists('sp500tickers.pickle'):
            with open('sp500tickers.pickle', 'rb') as f:
                tickers = pickle.load(f) 
            if not os.path.exists('companies4'):
                  os.makedirs('companies4')
                  start=dt.datetime(2016,1,1)
                  end=dt.datetime(2019,1,1)
                  for ticker in tickers:
                   if not os.path.exists('companies4/{}.csv'.format(ticker)):
                    print("{} is loading...".format(ticker))
                    df=web.DataReader(ticker,'yahoo', start,end)
                    df.to_csv('companies4/{}.csv'.format(ticker))
                   else:
                    print("{} already downloaded".format(ticker))
         
 return load_prices


# In[283]:


import pandas as pd
import pickle
with open('sp500tickers.pickle','rb') as f:
 tickers = pickle.load(f)
 main_df=pd.DataFrame()
print("Compiling data...")


# In[284]:


main_df.head


# In[287]:


for ticker in tickers:
 df=pd.read_csv('companies4/A.csv'.format(ticker))            
 df.set_index('Date', inplace=True)
 df.rename(columns ={'Adj Close':ticker},inplace=True)
 df.drop(['Open','High','Low','Volume','Close'],1,inplace=True)
 if main_df.empty:
  main_df=main_df
 else:
   main_df=main_df.join(main_df,how='outer')
   main_df.to_csv('sp500A_data.csv')
print('Data Compiled!') 


# In[ ]:


df.tail


# In[290]:


main_df=pd.DataFrame()
#print("Compiling data...")
#main_df.to_csv('sp500_data.csv')
#print("Data compiled!")
#import pandas as pd
sp500=pd.read_csv('sp500_data.csv')


# In[274]:


load_sp500_tickers()


# In[289]:


load_prices


# In[ ]:





# In[ ]:




