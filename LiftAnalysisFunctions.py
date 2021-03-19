import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from numpy import log
from statsmodels.tsa.stattools import adfuller
from pmdarima.arima import ADFTest
import pmdarima


def LiftbyVariable(Segments,IndependentVariableName,df,SpendVariable,metrics,trainStartDate,trainEndDate,testStartDate,testEndDate):
    CPLs=[]
    aggregatedTimeSeries=[]
    for v in Segments:
        for m in metrics:
            segmentdf = df.loc[df['Ad Name'] == v]
            print(m+v)
            timeSeries = segmentdf[[IndependentVariableName, m]]
            #Ensures data is stationary
            adfTestSet = timeSeries.loc[f'{trainStartDate}':f'{trainEndDate}']
            adf_test = ADFTest(alpha=.05)
            #Creates test and training sets
            train = timeSeries[m].loc[f'{trainStartDate}':f'{trainEndDate}']
            test = timeSeries[m].loc[f'{testStartDate}':f'{testEndDate}']
            print(test)
            #For smaller training/testing periods - ensures a given segment has data for every day (not necessary for longer windows/analyses with more data)
            if len(timeSeries[m].loc[f'{testStartDate}':f'{testEndDate}'])<22:
                continue
            if len(timeSeries[m].loc[f'{trainStartDate}':f'{trainEndDate}'])<7:
                continue
            #Train the model
            arima_model = pmdarima.auto_arima(train)
            #Make Predictions
            prediction = pd.DataFrame(arima_model.predict(n_periods=len(test.index)), index=test.index)
            prediction.columns = [f'predicted{m}']
            #Merge predictions with actuals to calculage lift,CPL later
            joined = pd.merge(timeSeries, prediction, how='outer', left_index=True, right_index=True)
            Predicted = joined[f'predicted{m}'].mean()
            ObservedPeriod = joined
            ObservedPeriod.index = pd.to_datetime(ObservedPeriod.index)
            ObservedPeriod = ObservedPeriod.loc[f'{testStartDate}':f'{testEndDate}']
            #Calculate avgs for each metric during the observed period CHANGE THIS TO SUM IF YOU ARE NOT USING CALCULATED METRICS
            #For example, CPC should be averages, but conversions should be summed
            Observed = ObservedPeriod[f"{m}"].mean()
            Lift = Observed - Predicted
            Investment = joined[f'{SpendVariable}'].sum()
            CPL=Investment/Lift
            #Create list of Cost per lift by segment and export as csv
            CPLs.append([f'{v}{m}', Investment, Lift, CPL])
            joined.to_csv(f"{IndependentVariableName}by{v}Hrly.csv")
    CPLs = pd.DataFrame(CPLs[0:], index=None, columns=['Metric','Investment','Lift','CPL'])
    CPLs.to_csv("CPLS.csv", index=False)
    return CPLs

