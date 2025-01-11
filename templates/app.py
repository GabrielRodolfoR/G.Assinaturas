import __init__
from models.database import engine
from models.model import Subscription, Payments
from views.view import SubscriptionService
from datetime import date, datetime
from decimal import Decimal

class UI:
    def __init__(self):
        self.subscription_service = SubscriptionService(engine)
        
    def start(self):
        while True:
            print('''
                  [1] Adicionar assinatura
                  [2] Pagar assinatura
                  [3] Remover assinatura
                  [4] Valor total
                  [5] Gastos últimos 12 meses
                  [6] Sair
                  ''')
            
            choice = int(input("Comando: "))
            
            if choice == 1:
                self.add_subscription()
            
            elif choice == 2:
                self.pay_subscription()
                
            elif choice == 3:
                self.delete_subscription()
            
            elif choice == 4:
                self.total_value()
            
            elif choice == 5:
                self.subscription_service.gen_charts()
                        
            else:
                break
            
    def add_subscription(self):
        empresa = input("Empresa: ")
        site = input("Site: ")
        data_assinatura = datetime.strptime(input("Data de assinatura: "), "%d/%m/%Y")
        valor = Decimal(input("Valor: "))
        subscription = Subscription(empresa=empresa, site=site, data_assinatura=data_assinatura, valor=valor)
        self.subscription_service.create(subscription)
        
    def delete_subscription(self):
        subscriptions = self.subscription_service.list_all()
        
        if not subscriptions:
            print("Nenhuma assinatura disponível para excluir.")
            return
        
        print("Escolha a assinatura para excluir")
        
        for subscription in subscriptions:
            print(f"[{subscription.id}] -> {subscription.empresa}")
                        
        delete = int(input("Escolha qual assinatura deseja excluir: "))
        self.subscription_service.delete(delete)
        print(f"Assinatura do(a) {subscription.empresa} excluida com sucesso!")
        
    def total_value(self):
        print(f"O valor total da assinatura é: {self.subscription_service.total_value()}")

        
UI().start()