import __init__
from views.view import SubscriptionService
from models.database import engine
from models.model import Subscription
from datetime import datetime
from decimal import Decimal


class UI:
    def __init__(self):
        self.subscription_service = SubscriptionService(engine)

    def start(self):
        while True:
            print('''
            [1] -> Adicionar assinatura
            [2] -> Remover assinatura
            [3] -> Valor total
            [4] -> Gastos últimos 12 meses
            [5] -> Sair
            ''')

            try:
                choice = int(input('Escolha uma opção: '))
                if choice == 1:
                    self.add_subscription()
                elif choice == 2:
                    self.delete_subscription()
                elif choice == 3:
                    self.total_value()
                elif choice == 4:
                    self.subscription_service.gen_chart()
                elif choice == 5:
                    break
                else:
                    print("Opção inválida! Tente novamente.")
            except ValueError:
                print("Por favor, insira um número válido.")

    def add_subscription(self):
        try:
            empresa = input('Empresa: ')
            site = input('Site: ')
            data_assinatura = datetime.strptime(input('Data da assinatura (dd/mm/aaaa): '), '%d/%m/%Y')
            valor = Decimal(input('Valor: '))
            subscription = Subscription(empresa=empresa, site=site, data_assinatura=data_assinatura, valor=valor)
            self.subscription_service.create(subscription)
            print("Assinatura adicionada com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar assinatura: {e}")

    def delete_subscription(self):
        try:
            subscriptions = self.subscription_service.list_all()
            if not subscriptions:
                print("Nenhuma assinatura disponível para exclusão.")
                return

            print("Assinaturas disponíveis:")
            for index, subscription in enumerate(subscriptions, start=1):
                print(f"[{index}] {subscription.empresa} - {subscription.site}")

            choice = int(input("Escolha o número da assinatura que deseja excluir: "))
            if 1 <= choice <= len(subscriptions):
                self.subscription_service.delete(subscriptions[choice - 1].id)
                print("Assinatura removida com sucesso!")
            else:
                print("Escolha inválida!")
        except Exception as e:
            print(f"Erro ao excluir assinatura: {e}")

    def total_value(self):
        try:
            total = self.subscription_service.total_value()
            print(f"Valor total das assinaturas: {total:.2f}")
        except Exception as e:
            print(f"Erro ao calcular valor total: {e}")



if __name__ == "__main__":
    ui = UI()
    ui.start()
