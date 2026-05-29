
class DynamicPricingEngine:
    ELASTICITY = {'Home Decor':1.8,'Gifts':2.1,'Kitchen':1.5,
                   'Seasonal':2.5,'Stationery':1.2}

    def __init__(self, category='Home Decor'):
        self.e = self.ELASTICITY.get(category, 1.8)

    def recommend(self, price, stock, days, rate):
        surplus  = max(0, (stock - rate*days) / stock)
        urgency  = min(0.5, surplus*0.6 + (0.1 if days<14 else 0))
        opt_p    = round(price*(1-urgency), 2)
        new_rate = rate*(1-self.e*((opt_p-price)/price))
        rev_now  = min(stock,rate*days) * price
        rev_new  = min(stock,new_rate*days) * opt_p
        return {'optimal_price':opt_p,
                'discount_pct':round((1-opt_p/price)*100,1),
                'revenue_gain':round(rev_new-rev_now,2)}