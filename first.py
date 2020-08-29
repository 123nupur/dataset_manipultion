# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.



df1 = pd.read_csv("../input/hotel-booking-demand/hotel_bookings.csv")
df2 = pd.read_csv("../input/hotel-booking-demand/hotel_bookings.csv")
df1.head()
# for renaming some of the columns in df2 
df2= df2.rename(columns={'arrival_date_week_number':'arrival_date_week','arrival_date_day_of_month':'arrival_date_day_of_mon','days_in_waiting_list':'days_in_waiting_li'})
df2.head()
#changing the data-type of some of the columns
df2=df2.astype({'is_canceled':float,'stays_in_week_nights':float,'booking_changes':float,'total_of_special_requests':float})
display(df2)

#Function for calculating Perfect match 
def getMatchScore(s1, s2):                                
  rows = len(s1)+1
  cols = len(s2)+1
  distance = np.zeros((rows,cols),dtype = int)
  for i in range(1, rows):
    for k in range(1,cols):
      distance[0][k] = k
    distance[i][0] = i

  for col in range(1, cols):
    for row in range(1, rows):
      if s1[row-1] == s2[col-1]:
        cost = 0
      else:
        cost = 2
      distance[row][col] = min( (distance[row-1][col] + 1), (distance[row][col-1] + 1),(distance[row-1][col-1] + cost) )
  Score = ((rows+cols-2) - (distance[row][col])) / (rows+cols-2)
  return Score*100                                            

def getPerfectMatch(s,s_list):                               
    scores = max(list(map(lambda s1:(getMatchScore(s,s1),s1),s_list)))
    return scores                                                

#Function for column_Rename.
def ColumnRename(dfnew,dfold):
    columns1 = dfnew.columns
    columns2=dfold.columns
    for i in columns2:
        if i not in columns1:
            replace=getPerfectMatch(i,columns1)
            dfold= dfold.rename(columns={i:replace[1]})  
    return dfnew,dfold
    

#Function for comparing datatype
def datatype(df):
    (df_new,df_old) = df
    df_newtypes = df_new.dtypes
    df_newtypes.to_dict()
    df_oldtypes = df_old.dtypes
    df_oldtypes.to_dict() 
    dicts={}

    for i in df_newtypes.keys():
        lists=[]
        if i in (df_oldtypes.keys()):
            if(df_newtypes[i]!=df_oldtypes[i]):
                dicts.update( {i : df_newtypes[i]} )
  
    df_old = df_old.astype(dicts)
    return df_new,df_old


df_2,df_1=datatype(ColumnRename(df2,df1))
df_1.head()

import matplotlib.pyplot as plt
df_2.plot(kind='scatter',x='arrival_date_day_of_mon',y='stays_in_weekend_nights', color='red')
df_2.plot(kind='bar',x='stays_in_weekend_nights',y='stays_in_week_nights')
plt.show()
