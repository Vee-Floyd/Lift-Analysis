import pandas as pd
import numpy as np
from LiftAnalysisFunctions import LiftbyVariable

#Read in CSV and set index to date
df=pd.read_csv('[PATH_TO_RAW_DATA_CSV]')
df=df.set_index(df['Date'])
df=df.index=pd.to_datetime(df.index)
#Replace NaNs (if needed)
df=df.replace([np.inf, -np.inf], np.nan).dropna(subset=['CPA','ROAS','AOV','Conversions'], how="all")
df=df.dropna()

#Define metrics we can to calculate lift for
metrics=['CPA','ROAS','AOV','Conversions']
#Define segments (ad name or source/medium etc)
Segments=[LIST_OF_SEGMENT_NAMES]


#Run csv through Lift by variable funciton
LiftbyVariable(Segments=Segments,IndependentVariableName='TVSpend',df=df,SpendVariable='TVSpend',metrics=metrics,trainStartDate='2020-12-14',trainEndDate='2020-12-20',testStartDate='2020-12-21',testEndDate='2021-01-11')


