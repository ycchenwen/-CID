# name列添加其计数列count
import pandas as pd
def countc(s,ls):
	return ls.count(s)
df['count']=df['name'].apply(countc,args=(list(pd.Series(df['name'])),))
