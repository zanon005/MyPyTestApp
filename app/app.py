###########################################################################################
#   1. [Configurar custo por KM] Permitir que o usuário informe o custo por km rodado (em 
#  R$). O programa deverá consistir que o valor é positivo e lembrar o valor digitado 
#  pelo usuário para as demais opções;
#   2. [Consultar trecho] Permitir que o usuário digite o nome de duas cidades: o programa 
#  deverá mostrar a distância rodoviária entre elas e o custo total calculado; se um 
#  nome de cidade não existir, informar ao usuário;
#   3. [Consultar rota] Permitir que o usuário digite o nome de duas ou mais cidades
#  (separadas por vírgulas, ex. “porto alegre, florianopolis, curitiba”): o programa 
#  deverá considerar uma rota que passa, em ordem, pelas cidades informadas. O 
#  programa deverá exibir:
#       a. Para cada trecho: os nomes das cidades e a distância entre elas;
#       b. A distância total percorrida;
#       c. O custo da viagem, considerando o custo por KM informado no item 1;
#       d. O total de litros de gasolina consumidos ao final da viagem (supondo que o 
#      veículo consome 2,57 litros a cada km);
#       e. O número de dias para finalizar a viagem (supondo que por dia são 
#     percorridos, em média, 283 km);
#   4. [Terminar o programa] Permitir que o usuário saia do programa.
###########################################################################################
# MATHEUS ZANON NUNES
# "Linkedin: https://www.linkedin.com/in/matheus-zanon-nunes/"

import sys
import pandas as pd

class App:
    def __init__(self, mapa_distancias, avg_gas_consuption = 2.57, avg_km_perday = 283, cost_per_km = None):
        self.avg_gas_consuption = avg_gas_consuption # Quando de gasolina eh consumido, em media, a cada KM 
        self.avg_km_perday =  avg_km_perday # Quantos KM sao percorridos, em media, por dia
        self.mapa_distancias =mapa_distancias # Valor default, definido na inicializacao!
        self.cost_per_km = cost_per_km # Valor default, usuario deve definir!

    # Funcao para configurar a variavel de controle que define o custo a cada KM
    def config_cost_km(self):
        try: 
            user_resp = float(input("Informe o custo por KM: "))
            if(user_resp >= 0):
                self.cost_per_km = user_resp
            else: raise ValueError
        except ValueError:
            print(" !!ATENCAO!! -> Valor digitado invalido, digite um numero real maior que zero, use ponto como separador decimal, tente novamente.")

    # Funcao para consultar a distancia entre duas cidades
    def consult_segment(self):
        if(self.cost_per_km is not None):
            origin_city = input("Digite o nome cidade de origem: ").upper()
            if(origin_city in self.mapa_distancias):
                destination_city = input("Digite o nome cidade de destino: ").upper()
                if(destination_city in self.mapa_distancias):
                    distancia = float(self.mapa_distancias[origin_city][destination_city])
                    custo = float(distancia * self.cost_per_km)
                    print(f"A distancia entre '{origin_city}' e '{destination_city}' eh de {distancia:.2f} km")
                    print(f"Custo de R$ {custo:.2f}")
                else:
                    print(f" !!ATENCAO!! -> A cidade digitada '{destination_city}' nao eh uma cidade valida!, tente novamente.")
            else:
                print(f" !!ATENCAO!! -> A cidade digitada '{origin_city}' nao eh uma cidade valida!, tente novamente.")
        else:
            print(" !!ATENCAO!! -> O custo por KM ainda nao foi definido, impossivel calcular...")

    # Funcao auxiliar que retorna a distancia entre duas cidades
    def dist_CityA_CityB(self, city_a, city_b):
        return float( self.mapa_distancias[city_a][city_b] )

    # Funcao para consultar a distancia, consumo e tempo em dias para uma rota entre varias cidades
    def consult_route(self):
        if(self.cost_per_km is not None):
            cities = input("Digite o nome de duas ou mais cidades separadas por virgula: ").upper().split(",")
            #convertendo todas cidades para maiusculo e removendo espacos extras
            cities[:] = [city.upper().strip() for city in cities]

            #Verficando se todas cidades digitadas existem no mapeamento
            if( not all(city in self.mapa_distancias for city in cities) ):
                print(" !!ATENCAO!! -> Pelo menos uma das cidades digitadas nao eh uma cidade valida!, tente novamente")
                return

            total_km = 0.0
            for i in range(len(cities)-1): #Percorrendo a lista de cidades e calculando sempre a atual com a proxima
                city = cities[i].strip()
                next_city = cities[i+1].strip()
                distancia = self.dist_CityA_CityB(city, next_city)
                total_km += distancia
                print(f"{city} -> {next_city} ({distancia:.2f} km)")
            litros_totais = float(total_km/self.avg_gas_consuption)
            dias_totais = float(total_km/self.avg_km_perday)
            print(f"Distancia total: {total_km:.2f} km")
            print(f"O total de litros gastos foi de: {litros_totais:.2f} litros")
            print(f"A viagem durou {dias_totais:.2f} dias")
        else:
            print(" !!ATENCAO!! -> O custo por KM ainda nao foi definido, impossivel calcular...")

    def end_prog(self):
        sys.exit()

def main():
    print("Programa feito por: Matheus Zanon Nunes")
    print("!!Obs!! Arquivo que mapeia as distancias de cidades sendo usado eh o 'DNIT-Distancias.csv'")

    #Carregando o csv de distancias para o programa...
    try:
        mapa_distancias = pd.read_csv("DNIT-Distancias.csv", delimiter= ";") #Le o '.csv' usando ';' como separador de tokens
    except FileNotFoundError:
        print(" !!ATENCAO!! -> arquivo 'DNIT-Distancias.csv' nao encontrado no diretorio do programa!!")
    #   A primeira linha do csv contem o nome das colunas, das cidades, para saber a distancia entre a cidade X e Y posso usar
    #estas "colunas" como indice das linhas da tabela, desta forma a 'coluna 0' tera o indice '0', a 'coluna 1' tera o 'indice 1'...
    #ou seja, a primeira coluna "ARACAJU" tera como indice "ARACAJU"e isto retornara distancia 0, mas se consultarmos o seguinte:
    # dataframe["ARACAJU"]["CURITIBA"] estamos acessando -> dataframe[linha que contem indice "ARACAJU"][coluna de nome "CURITIBA"]
    #e este comando vai retornar o custo para ir de "ARACAJU" ate "CURITIBA".
    mapa_distancias.set_index(mapa_distancias.columns,inplace= True)

    # Criando e inicializando a instancia da aplicacao
    app = App(avg_gas_consuption=2.57, avg_km_perday=283, mapa_distancias=mapa_distancias)

    actions = { # dicionario com todas as opcoes do menu do programa e suas funcoes
        "1": app.config_cost_km,
        "2": app.consult_segment,
        "3": app.consult_route,
        "4": app.end_prog
    }
    #Loop do programa!
    while True:
        print(f"""\n\n==== MENU ====
        1. Configurar custo por KM (Valor atual = {(app.cost_per_km if app.cost_per_km is not None else "Nao definido")})
        2. Consultar trecho
        3. Consultar rota
        4. Terminar o programa"""
        )

        user_resp = input("Escolha uma das opcoes: ")

        #Se a resposta do usuario for uma acao valida
        if(user_resp in actions):
            actions[user_resp]() # entao chamamos a funcao correspondente a opcao escolhida
        else:
            print(f" !!ATENCAO!! -> A opcao digitada '{user_resp}' nao eh uma opcao valida!!")

if __name__ == "__main__":
    main()