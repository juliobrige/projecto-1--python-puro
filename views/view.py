import __init__
from models.database import engine
from models.model import Subscription
from sqlmodel import Session, select
from datetime import date

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



ss = SubscriptionService(engine)

new_subscription = Subscription(
    empresa="julio benjamim bernardo",
    site="https://Netflix.com",
    data_assinatura=date.today(),
    valor=120.50
)

created_subscription = ss.create(new_subscription)
print(f"Assinatura criada: {created_subscription}")


all_subscriptions = ss.list_all()
print("Lista de assinaturas:")
for subscription in all_subscriptions:
    print(subscription)
