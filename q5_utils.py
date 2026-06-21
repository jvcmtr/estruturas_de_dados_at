from q5_data import *
from math import inf

PESO_ESPERA = 1
PESO_URGENCIA = 1
PESO_PRIORIDADE = 1
FATOR_PRIORIDADE_FINAL = 1

HUBS = [x[0] for x in NODES if x[1]==True]
DELIVERY_TARGETS = [x[0] for x in DELIVERIES]

def get_priority(delivery, t=0):
    # Ao subtrairmos a janela de inicio do tempo atual (t), desestimulamos
    # o algorítimo à escolher entregas nas quais devemos ficar esperando. 
    # Limitamos este valor numeros negativos para que, uma vez que a janela 
    # esteja aberta, ela não influencie na **urgencia**
    #
    # Ao subtrairmos o tempo t do fim da janela de entrega, obtemos uma valor
    # que é proporcional a urgencia da entrega, isto é, conforme o tempo t
    # se aproxima do tempo limite, o valor cresce, estimulando o algorítimo
    # a realizar logo esta entrega antes que atrase. Limitamos este valor a
    # numeros positivos assumindo que, uma vez que a entrega já esteja 
    # atrasada, não faz mais sentido se preocupar com o atraso. 
    #
    # Existe na estrutura de deliveries uma propriedade chamada prioridade. 
    # Contudo, quando é definido o que o sistema deve otimizar, esta propriedade
    # não é citada. Sendo assi, podemos considera-la ser uma forma de ajuste por
    # entrega do algoritimo.
    #
    # Para ajuste fino do quanto cada parâmetro influencia na prioridade final de
    # uma entrega, adotou-se uma abordagem de pesos, onde cada outro parâmetro 
    # possui um peso associado que o multiplica.  
    
    return (
          (min((t+1)/ (delivery[1]+1), 1) *PESO_ESPERA) 
        + (max((t+1)/ (delivery[2]+1) , 1 ) *PESO_URGENCIA) 
        + (delivery[3] *PESO_PRIORIDADE)
    ) * FATOR_PRIORIDADE_FINAL 



if __name__ == "__main__":
    print("Prioridade das entregas:")
    for e in DELIVERIES:
        print(e, "  \t  \t", f"{get_priority(e):.2f}")

