import __init__
from models.database import engine
from models.model import Subscription, Payments
from sqlmodel import Session, select
from datetime import date, datetime

class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine
    
    def create(self, payments: Payments):
        with Session(self.engine) as session:
            session.add(payments)
            session.commit()
            return payments
    
    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
            return results
        
    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            results = session.exec(statement).one()
            session.delete(results)
            session.commit()
    
    def _has_pay(self, results):
        for result in results:
            if result.date.month == date.today().month:
                return True

        return False           
    
    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription).where(Subscription.empresa == subscription.empresa)
            results = session.exec(statement).all()
                    
            if self._has_pay(results):
                confirmation = input("A conta já foi paga esse mês. Desenja pagar novamente? (Y/n): ")
                
                if not confirmation.upper() == "Y":
                    return 
                
            pay = Payments(subscription_id = subscription.id, date=date.today())
            session.add(pay)
            session.commit()
            
    def total_value(self):
        with Session (self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
            
        total = 0
        for result in results:
            total += result.valor
        return float(total)
    
    def _get_last_12_months(self):
        today = datetime.now()
        year = today.year
        month = today.month
        last_12_months = []
        
        for i in range(12):
            last_12_months.append((month, year))
            month -= 1
            if month <= 0:
                month = 12
                year -= 1
            
        return last_12_months[::-1]
    
    def _get_value_for_month(self, last_12_months):
        with Session (self.engine) as session:
            statement = select(Payments)
            results = session.exec(statement).all()
            
            value_for_months = []
            for i in last_12_months:
                value = 0                
                for result in results:
                    if result.date.month == i[0] and result.date.year == i[1]:
                        value += float(result.subscription.valor)
                value_for_months.append(value)
            return value_for_months
    
    def gen_charts(self):
        last_12_months = self._get_last_12_months()
        values_for_month = self._get_value_for_month(last_12_months)
        last_12_months = list(map(lambda x: x[0], self._get_last_12_months()))
        
        import matplotlib.pyplot as plt
        
        plt.plot(last_12_months, values_for_month)
        plt.show()
        
                    
ss = SubscriptionService(engine)

"""
assinaturas = ss.list_all()

for i, s in enumerate(assinaturas):
    print(f"[{i}] -> {s.empresa}")
    
x = int(input())   
subscription = assinaturas[x]
"""