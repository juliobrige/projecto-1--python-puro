import sys
sys.path.append(r'C:\prog\projecto 1 -python puro')

from datetime import date
from sqlmodel import Session, select
from sqlalchemy import extract  
from models.database import engine
from models.model import Payments, Subscription
from datetime import datetime

class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine

    def create(self, subscription: Subscription):
        with Session(self.engine) as session:
            session.add(subscription)
            session.commit()
            session.refresh(subscription)
        return subscription

    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            result = session.exec(statement).all()
        return result

    def has_payment_this_month(self, subscription_id: int):
        with Session(self.engine) as session:
            statement = select(Payments).where(
                Payments.subscription_id == subscription_id,
                extract('month', Payments.date) == date.today().month,
                extract('year', Payments.date) == date.today().year
            )
            results = session.exec(statement).all()
            return bool(results) 

    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            result = session.exec(statement).one()
            session.delete(result)
            session.commit()

    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            if self.has_payment_this_month(subscription.id):
                question = input("Esta conta já foi paga este mês. Você quer pagar novamente? (S/N): ")
                if question.upper() == "N":
                    return  

            pay = Payments(subscription_id=subscription.id, date=date.today())
            session.add(pay)
            session.commit()
            session.refresh(pay)

    def total_value(self):  
       
        with Session(self.engine) as session:  
            statement = select(Subscription)
            results = session.exec(statement).all()

            total = 0
            for result in results:
                total += result.valor 

            return float(total)  

    def _get_last_12_months_native(self):
        ""
        today = datetime.now()
        year = today.year
        month = today.month
        last_12_months = []
        for i in range(12):
            last_12_months.append((month, year))
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        return last_12_months[::-1]  
    def _get_values_for_months(self, last_12_months):
        with Session(self.engine) as session:
            statement = select(Payments)
            results = session.exec(statement).all()

            values_for_months = []
            for (month, year) in last_12_months:
                total_for_month = sum(
                    payment.valor for payment in results if payment.date.month == month and payment.date.year == year
                )
                values_for_months.append((month, year, total_for_month))

            return values_for_months


ss = SubscriptionService(engine)

new_subscription = Subscription(
    empresa="julio benjamim bernardo",
    site="https://Netflix.com",
    data_assinatura=date.today(),
    valor=120.50,
)

created_subscription = ss.create(new_subscription)
