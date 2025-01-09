import sys
sys.path.append(r'C:\prog\projecto 1 -python puro')

from datetime import date, datetime
from sqlmodel import Session, select
from sqlalchemy import extract
from models.database import engine
from models.model import Payments, Subscription


class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine

    def create(self, subscription: Subscription):
        try:
            with Session(self.engine) as session:
                session.add(subscription)
                session.commit()
                session.refresh(subscription)  # Carrega o objeto novamente
            return subscription
        except Exception as e:
            print(f"Erro ao criar assinatura: {e}")
            raise

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

    def delete(self, id: int):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            result = session.exec(statement).one_or_none()
            if result:
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
            total = session.exec(select(Subscription.valor)).all()
            return sum(total)

    def _get_last_12_months_native(self):
        today = datetime.now()
        year = today.year
        month = today.month
        last_12_months = []
        for _ in range(12):
            last_12_months.append((month, year))
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        return last_12_months[::-1]

    def _get_values_for_months(self, last_12_months):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription)
            results = session.exec(statement).all()

            values_for_months = []
            for (month, year) in last_12_months:
                value = 0
                for result in results:
                    # Valida mês e ano
                    if result.date.month == month and result.date.year == year:
                        if result.subscription:  # Confirma a relação
                            value += float(result.subscription.valor)
                values_for_months.append(value)

        return values_for_months

    def gen_chart(self):
        last_12_months = self._get_last_12_months_native()
        values_for_months = self._get_values_for_months(last_12_months)

        # Gera um gráfico usando matplotlib
        import matplotlib.pyplot as plt
        months = [f"{month}/{year}" for month, year in last_12_months]
        plt.bar(months, values_for_months)
        plt.xlabel("Últimos 12 meses")
        plt.ylabel("Valores (R$)")
        plt.title("Assinaturas - Valores dos últimos 12 meses")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


# Testando a funcionalidade
if __name__ == "__main__":
    ss = SubscriptionService(engine)

    # Criando nova assinatura
    new_subscription = Subscription(
        empresa="Julio Benjamim Bernardo",
        site="https://Netflix.com",
        data_assinatura=date.today(),
        valor=120.50,
    )

    created_subscription = ss.create(new_subscription)
    print("Assinatura criada com sucesso:", created_subscription)

   
    ss.gen_chart()
