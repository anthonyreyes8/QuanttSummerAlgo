import mlfinlab as ml
import numpy as np

class team2(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2020, 6, 26)  # Set Start Date
        self.SetCash(100000000)  # Set Strategy Cash
        
        #set universe
        self.HRL = self.AddEquity("HRL", Resolution.Daily).Symbol
        self.AAL = self.AddEquity("AAL", Resolution.Daily).Symbol
        self.DAL = self.AddEquity("DAL", Resolution.Daily).Symbol
        
        #setting indicators
        #simple moving average
        self.AAL_sma = self.SMA("AAL", 60, Resolution.Daily)
        self.DAL_sma = self.SMA("DAL", 60, Resolution.Daily)
       
        #indicator warm up period
        self.SetWarmUp(timedelta(days = 60))
        
        #place trade for HRL 120 min after market opens
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen('HRL', 120), self.daily_check)

    def daily_check(self):
        #if indicator isnt ready exit strategy
        if self.IsWarmingUp:
            return
        
        #not sure if this WORKS WILL UPDATE
        aalClose = self.AAL.close
        dalClose = self.DAL.close
    
        #training the ornstainUhlenbeck method
        data_train = np.array([aalClose], [dalClose])
        data_oos = np.array([aalClose], [dalClose])
        
        example = ml.OrnsteinUhlenbeck()
        example.fit(data_train, data_frequency="D", discount_rate=0.5, transaction_cost=0, stop_loss=0.5)
        
        example.description()
        
        #entry criteria 
        #currPrice less than optimal entry and sma trending upwards
        if  self.AAL.Price < example.optimal_entry_level() and self.AAL_sma.Current.Value < self.AAL.Price:
            self.SetHoldings("AAL", 0.5)
            self.SetHoldings("DAL", -0.5)
            self.Log('AAL %' + str(round((self.Securities["AAL"].Price * self.Portfolio['AAL'].Quantity)/self.Portfolio.TotalPortfolioValue,4)))
            self.Log('DAL %' + str(round((self.Securities["DAL"].Price * self.Portfolio['DAL'].Quantity)/self.Portfolio.TotalPortfolioValue,4)))

"""
        #currPrice less than optimal entry and sma trending downwards
        elif AAL.Price < example.optimal_entry_level() and self.smaAAL > self.Securities["AAL"].Price :
            self.SetHoldings("AAL", -aal_wt)
            self.SetHoldings("DAL", dal_wt)

        #currPrice greater than optimal entry and sma trending upwards 
        elif AAL.Price > example.optimal_entry_level() and self.smaAAL < self.Securities["AAL"].Price :
            self.SetHoldings("HRL", 0.1)

        #currPrice greater than optimal entry and sma trending downwards 
        elif AAL.Price > example.optimal_entry_level() and self.smaAAL > self.Securities["AAL"].Price :
            self.SetHoldings("HRL", 0.1)   

        #exit criteria
        #currPrice less than optimal exit and sma trending upwards
        elif  AAL.Price < example.optimal_liquidation_level() and self.smaAAL < self.Securities["AAL"].Price :
            self.SetHoldings("HRL", 0.1)  

        #currPrice less than optimal exit and sma trending downwards
        elif AAL.Price < example.optimal_liquidation_level() and self.smaAAL > self.Securities["AAL"].Price :
            self.SetHoldings("AAL", -aal_wt)
            self.SetHoldings("DAL", dal_wt)

        #currPrice greater than optimal exit and sma trending upwards 
        elif AAL.Price > example.optimal_liquidation_level() and self.smaAAL < self.Securities["AAL"].Price :
            self.SetHoldings("HRL", 0.1)

        #currPrice greater than optimal exit and sma trending downwards 
        elif AAL.Price > example.optimal_liquidation_level() and self.smaAAL > self.Securities["AAL"].Price :
            self.SetHoldings("HRL", 0.1) 
        else:
            self.SetHoldings("HRL", 0.1)
        
        #retrain model
        example.fit_to_assets(data_oos)
    """
