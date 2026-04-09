############################################################################################################################################################################################
#    
#   O programa a seguir é destinado a auxiliar na compreensão do PROCESSO DE ANALISE DE DADOS e o uso de Python e suas bibliotecas: Pandas, Matplotlib e NumPy.
#     Tais bibliotecas não veem intaladas no python por padrão, tendo que realizarmos a instalação na nossa maquina, é so seguir o passo a passo abaixo.
#
##############################################################################################################################################################################

############################################################  COMO INSTALAR AS BIBLIOTECAS NECESSÁRIAS   ##########################################################################
#
# 1º. Abra o Terminal do seu computador:
#
#    -Pressione a tecla Windows, digite "cmd" e abra o "Prompt de Comando".
#    -Ou pesquise por "Terminal" ou "PowerShell" e abra o aplicativo correspondente.
#
# 2º. Copie o comando abaixo, cole no terminal e aperte ENTER:
#
#    pip install pandas matplotlib numpy scipy
#
# 3º. O terminal fará o download da internet. Irá aparecer algumas linhas indicando o progresso, caso tenha dado certo, a ultima linha começarar com "Successfully installed...".
#    
#   !!!!Caso não duncionar com 'pip' no Windows, tente usar: python -m pip install pandas matplotlib numpy scipy)!!!!
# 
##############################################################################################################################################################################

########################################################################### FINALIDADE DO PROGRAMA ##########################################################################################
#O PROGAMA A SEGUIR É UM EXEMPLO DE ANÁLISE DE DADOS TOPOGRÁFICOS PARA PROJETO DE ESTRADAS.
# 
#  ELE UTILIZA DADOS SIMULADOS DE UMA NUVEM DE PONTOS (CSV), UM PERFIL LONGITUDINAL (CSV) E UM ARQUIVO DE CONFIGURAÇÕES (TXT) PARA:
# 
# - CALCULAR A DIFERENÇA ENTRE O TERRENO EXISTENTE E O PROJETO
# - CALCULAR O VOLUME DE CORTE E ATERRO NECESSÁRIO PARA A EXECUÇÃO DO PROJETO
# - ANALISAR AS DECLIVIDADES DO TERRENO EXISTENTE
# - DETECTAR TRECHOS CRÍTICOS COM BASE EM UM LIMITE DE DECLIVIDADE (FORNECIDO POR UM ARQUIVO DE CONFIGURAÇÃO)
# - FORNECER VISUALIZAÇÕES GRÁFICAS DO PERFIL LONGITUDINAL E DO MAPA DE RELEVO
# - GERAR UM DATASET FINAL COM TODAS AS INFORMAÇÕES CALCULADAS PARA ANÁLISE E CONSULTA FUTURA
# - CLASSIFICAR O TIPO DE TERRENO (PLANO, ONDULADO, MONTANHOSO)
#
# Obs.: Este código é um exemplo didático e pode haver simplificações em relação a um projeto real de engenharia.
#####################################################################################################################################################################################

#################################################################   FLUXO DO FUNCIONAMENTO      ##############################################################################################################################
#  
#  Para melhor compreensão do código, segue abaixo o processo de funcionamento do programa, dividido em etapas:
#   
#  1 -Ao executar o programa ele ira entrar no processo de inicialização, onde irá carregar os dados dos arquivos CSV e TXT, e preparar o ambiente para análise.
#     Tal fucnionalidade é realizada pela função >>>>iniciar_sistema()<<<<<<<, nela é realizado:
#       
#        > a leitura de parametros através da função ler_parametros();
#        > a leitura da nuvem de pontos através da função ler_nuvem_pontos(); 
#        > a análise do perfil longitudinal através da função analisar_perfil();
#        > o cálculo das declividades através da função calcular_declividades();
#        > a definição do limite de declividade crítica a partir dos parametros lidos.
#     Ao final da função >>>>>inicia_sistema()<<<<<<<, o sistema estará pronto para as análises, e o menu de opções será exibido.
#
#  2 - O programa então exibirá um menu de opções para o usuário, onde ele poderá interagir e escolher as análises que deseja realizar.
#      A exibição do menu é realizada pela função >>>>mostrar_menu()<<<<<, ela apresenta as opções disponíveis:
#         
#        >mostrar o perfil da estrada através da função exibir_perfil_analisado();
#        >mostrar as declividades através da função mostrar_declividades();
#        >detectar trechos críticos através da função detectar_trechos_criticos();
#        >calcular corte e aterro através da função calcular_corte_aterro();
#        >exibir o gráfico do perfil através da função grafico_perfil();
#        >exibir o mapa de relevo através da função mapa_relevo();
#        >gerar o dataset final de análise através da função gerar_dataset_final();
#        > e por fim, a opção de sair do programa.
#
#     Durante a interação com o menu é  utilizada a função mostrar_texto(), responsavel por exibir os resultados através de uma janela  grafica.
#     E nas opções do menu onde é deduzida/gerada uma nova tabela de dados, através da manipulação das arquivos de dados iniciais, é perguntado
#     ao usuario se ele deseja salvar a tabela exibida, a função perguntar_salvar() é a responsavel por isso. 
##################################################################################################################################################################################################################

##################################################!!!!!!!!!!!!!! AVISO !!!!!!!!!!!!!!!!!!!!!!!!!######################################################################################################
#  
#   Para a execução feito é nescessario que na mesma pasta que ele (mesmo diretório) tenha os seguintes arquivos:
#        >>>> "nuvem_pontos.csv", "perfil_longitudinal.csv" e "parametros.txt".
#        
#   No decorrer do programa outros arquivos csv serão gerados no mesmo diretorio.
#   Caso algum desses arquivos esteja faltando, o programa irá apresentar um erro de leitura, e não conseguirá ser executado.
# 
#   O conteúdo desses arquivos é simulado, e pode ser editado para testar o programa e sua compreensão, mas eles precisam estar presentes para o programa funcionar.
#   Então sugiro fazer uma cópia desses arquivos, e editá-los para testar o programa, mas mantendo os originais para garantir a execução do código. 
#
##################################################################################################################################################################################################################


######################## CONCEITO FUNDAMENTAL: O DATAFRAME (BIBLIOTECA PANDAS) #####################################################################################################
# 
#   No processamento de dados, lidamos com grandes conjuntos de dados (ex: nuvens de pontos topográficos com dezenas de milhares de coordenadas). 
#   O DataFrame é a estrutura de dados otimizada para armazenar e processar essas informações.
#
# ------------------------------ A ESTRUTURA DO DATAFRAME----------------------------------------------------------------------------------------------------------------
# 
#   O DataFrame foi projetado como uma matriz bidimensional estruturada. Exemplo:
#
#             cota_terreno  cota_projeto   <-- Series
#        0    100.00        101.50    |
#        1    101.20        101.70    |-- Values 
#        2    102.50        101.90    |
#        ^
#     Index 
#
#   - Series (colunas): Vetores onde cada coluna armazena obrigatoriamente UM UNICO TIPO DE DADO numérico ou textual, oque permite operações algébricas estritas.
#   
#   - Index (índice): O sistema de coordenadas das linhas, que mantém a ordem dos dados.
#   
#   - Values (valores): Os dados subjacentes, que podem ser acessados com a devida combinação de índiex e series.
#
# ----------------------- O MOTIVO DA UTILIZAÇÃO -------------------------------------------------------------------------------------------------------------------------
#   
#   Imagine que temos 100.000 pontos de um perfil longitudinal, e queremos calcular a diferença entre a cota do terreno e a cota do projeto para cada ponto.
#   Se utilizássemos estruturas nativas, como Listas, para subtrair a cota do terreno da cota do projeto em 100.000 pontos, precisaríamos de um loop iterativo:
#
#     diferencas = []
#     for i in range(len(cota_projeto)):
#         calculo = cota_projeto[i] - cota_terreno[i]
#         diferencas.append(calculo)
#
#   O computador é forçado a ler e calcular uma linha de cada vez. Ja o DataFrame resolve esse gargalo através da "Vetorização". 
#
#   Em vez de iterar linha por linha, o Pandas envia a instrução para o processador calcular os vetores inteiros de uma única vez.
#   O mesmo cálculo feito acima é resolvido com uma única expressão algébrica:
#
#     df['diferenca'] = df['cota_projeto'] - df['cota_terreno']
#
#   Oque torna o código mais limpo, fácil de entender e mais leve computacionalmente, processando os dados de forma quase instantânea.
#
# ##################################################################################################################################################################################################################

################################################# OS DATASETS (CONJUNTOS DE DADOS) UTILIZADOS  ####################################################################################################
# 
# A arquitetura dos arquivos utilizados neste projeto segue os seguintes formatos:
#
# ----NUVEM DE PONTOS (nuvem_pontos.csv)----
#
#   Simula um levantamento topografico, onde cada linha representa um ponto  medido em campo.
#   Formato: Matriz espacial em CSV. 
#   
#   As colunas são:
#   - id: Identificador numérico do ponto.
#   - x, y: São as coordenadas do terreno.
#   - z: A altitude do terreno.
#
# ----PERFIL LONGITUDINAL (perfil_longitudinal.csv)----
#
#   Contem informações que visam simular o traçado que alinha o chão natural à uma proposta de estrada.
#   Formato: Matriz bidimensional em csv.
#
#      As colunas são:
#       - estaca: Unidade de marcação padrão de estradas (geralmente a cada 20 metros).
#       - distancia: Distância acumulada em metros (a partir do marco zero).
#       - cota_terreno: A real altitude medida no chão natural.
#       - cota_projeto: Altitude idealizada para a pista.
#
# --- ARQUIVO DE CONFIGURAÇÃO (parametros.txt)-----------
#   
#   Contem parâmetros de controle para a análise, dados pre-definidos que serão "regras/leis" a serem usadas durante todo o código.
#
#   Formato: Arquivo de texto simples utilizando a sintaxe 'chave=valor'.
#       - Exemplo: declividade_maxima=0.08  - A declividade máxima tolerada para o projeto.
#
#############################################################################################################################################################################################################################


############################## IMPORTAR BIBLIOTECAS #################################################################################################################################################
#
#   Aqui o python busca as bibliotecas nos arquivos do computador e as carrega na memoria, tornando-as disponíveis para uso no código.
#   Atribuimos uma variavel a cada biblioteca para facilitar o uso delas ao longo do código.
#   Ao inves de digitar matplotlib.pyplot.plot(), usamos plt.plot(). Mais rapido e simples.
#
#   Utilizaremos pandas (pd) para operações matemáticas e manipulação de arrays.
#   Utilizaremos matplotlib (plt) para criar gráficos e visualizar dados.
#   Utilizaremos numpy (np) para operações numéricas.
#   Utilizaremos scipy.interpolate.griddata para interpolar os dados de uma grade.
#
#############################################################################################################################################################################################


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata


###################################################### MOSTRAR TEXTO ########################################################################################################################################
# 
#   Utilizada para exibir as informações/resultados em uma janela gráfica, através da biblioteca Matplotlib.
#   Ela recebe uma string formatada e a renderiza em um layout visualmente organizado, com título e formatação de texto personalizada.
#  
#
#def mostrar_texto(titulo, texto): - Os parametros nescessarios são: o título da janela e o texto que será exibido.
#   plt.figure(figsize=(10, 6)) - Aqui instancia um novo quadro, definindo o tamanho da janela (10x6).
#   plt.axis("off") - Desativa a renderização das réguas dos eixos X e Y, se tivesse ligado teriamos linhas no fundo, uma grade.
#   plt.title(titulo, fontweight='bold') - Insere o título rebedio na parte superior da janela, fontweight='bold' o coloca em negrito.
#   plt.text( - Inicia o comando de plotagem das informações no quadro.
#       0.30, 0.95, texto, - Define a posição (x, y) de onde o texto começará a ser exibido e passa a variável do texto. 
#       O valor 0.30 significa que o texto começará a 30% da largura da janela, e 0.95 significa que começará a 95% da altura da janela (quase no topo).
#       fontsize=11, family="monospace", - Ajusta o tamanho da fonte e define a família tipográfica. 
#       A "monospace" garante que todas as letras ocupem a mesma largura, melhorando o alinhamento.
#       verticalalignment="top", horizontalalignment="left" - Alinha o texto horizontalmente à esquerda e verticalmente ao topo.
#   ) - Fecha a configuração do comando de texto.
#   
#   plt.show() - Exibe a janela/interface gráfica contendo o texto,
#  
#   IMPORTANTE: O terminal ficará "congelado" enquanto a janela estiver aberta, como forma de ter certeza de que o usuário visualizou todos os resultados.
#
######################################################################################################################################################################################################################################################

def mostrar_texto(titulo, texto):
    plt.figure(figsize=(10, 6))
    plt.axis("off")
    plt.title(titulo, fontweight='bold')
    plt.text(
        0.30, 0.95, texto,
        fontsize=11, family="monospace",
        verticalalignment="top", horizontalalignment="left"
    )
    plt.show()

###################################################### PERGUNTAR SIM NÃO ########################################################################################################################################
#
#   Durante o programa, será necessário perguntar ao usuário se ele deseja salvar os resultados de uma análise específica.
#   Essa função é a responsável por isso. Ela cria um sistema de interação com o usuário que é à prova de erros, garantindo que o programa só avance com respostas válidas.  
#
#
#def perguntar_sim_nao(mensagem): - Tem como parametro de entrada a string da pergunta que será impressa na tela.
#   
#   while True: - Inicia um loop infinito intencional. O programa ficará preso aqui até que o usuário faça a coisa certa.
#       resposta = input(mensagem).strip().lower() - Exibe a pergunta e aguarda a digitação. .strip() é para remover espaços acidentais o .lower() força tudo para letras minúsculas.
#       Isso garante que se o usuário digitar "S ", "s " ou "S", o programa entenda da mesma forma.
#       if resposta == 's': -             Verifica se a resposta limpa é o caractere 's'.
#           return True -                     Se sim, quebra o loop e encerra a função devolvolvendo a flag Booleana True.
#       elif resposta == 'n': -           Na exclusão do 's', verifica se o usuário digitou 'n'.
#           return False -                    Se sim, quebra o loop e encerra a função devolvolvendo a flag Booleana False.
#       else: -                           Rota de contingência: Acionada caso o usuário digite números, letras aleatórias ou deixe em branco.
#           print("Entrada inválida...") -    Informa que a entrada(Input) é invalida. E o 'while True' puxa o fluxo de volta para o início, perguntando de novo.
#
##############################################################################################################################################################################################


def perguntar_sim_nao(mensagem):

    while True:
        resposta = input(mensagem).strip().lower()
        if resposta == 's':
            return True
        elif resposta == 'n':
            return False
        else:
            print("Entrada inválida. Por favor, digite apenas 's' para Sim ou 'n' para Não.")

############################################### FORMATAR PERFIL ##############################################################################################################################################################################################
#   
#   Recebe o dataframe com os dados do perfil longitudinal e o pacote de estatísticas calculadas, e retorna uma string formatada pronta para exibição.
#   Essa string formatada é uma especie de relatório textual que apresenta as estatísticas do terreno e uma tabela comparativa entre o terreno e o projeto.
#
#def formatar_perfil(df, stats): - Como parametro de entrada ela precisa de: o dataframe de traçado e o pacote de estatísticas (que serão calculadas por outra função).
#   texto = "ESTATÍSTICAS DO TERRENO\n" - Começa a criação do 'texto' pondo o titulo e duas quebras de linha ('\n').
#   texto += f"{'Altitude média: '} {stats['media']:.2f} m\n" -    Concatena a string "Altitude média:" + a média + "m\n" junto a string que ta sendo criada.
#   O parametro :.2f é uma formatação para exibir so as primeiras 2 casas decimais após o ponto float, nessecaria fazer para controlar a exibição de dados floats.
#   texto += f"{'Altitude máxima:'} {stats['maxima']:.2f} m\n" -   Continua a concatenação da string com o valor de altitude máxima.
#   texto += f"{'Altitude mínima:'} {stats['minima']:.2f} m\n" -   Finaliza o bloco de estatísticas com a altitude mínima.
#   texto += "\n" + "="*50 + "\n\n" - Cria uma linha divisória estética exibindo o caractere '=' cinquenta vezes seguidas "="*50.
#   texto += f"{'ESTACA':12} | {'TERRENO (m)':12} | {'PROJETO (m)':12} \n" - Cria o cabeçalho descritivo da tabela, separando visualmente as colunas com '|'.
#   O :12 após cada campo/coluna é para a tornar a formatação de largura fixa (12 caracteres).
#   texto += "-" * 50 + "\n" - Insere outra linha divisória para separar o cabeçalho dos dados, usando o caractere '-' dessa vez.
#   for i in range(len(df)): - Inicia o loop para processar as linhas do dataframe de i = 0 até o valor do comprimento do dataframe.
#       estaca_label = f"Estaca {df['estaca'][i]}" -      A string estaca_label recebe 'Estaca ' + o valor da estaca (ex: 'Estaca 0').
#       cota_t = f"{df['cota_terreno'][i]:.2f}" -         Pega a cota flutuante, com 2 casas decimais após o ponto, e o converte em texto.
#       cota_p = f"{df['cota_projeto'][i]:.2f}" -         Faz o mesmo com a cota de projeto.
#       texto += f"{estaca_label:12} | {cota_t:12} | {cota_p:12} \n" - Funde as variáveis numéricas convertidas em uma linha da tabela e anexa ao blocão de texto.               
#       O :12 é para manter a formatação de largura fixa, garantindo que os dados exibidos fiquem alinhados mesmo que tenham quantidades diferentes de dígitos.
#   
#   return texto - Devolve string formatada.
#
##############################################################################################################################################################################

def formatar_perfil(df, stats):
    texto = "ESTATÍSTICAS DO TERRENO\n\n"
    texto += f"{'Altitude média: '} {stats['media']:.2f} m\n"
    texto += f"{'Altitude máxima:'} {stats['maxima']:.2f} m\n"
    texto += f"{'Altitude mínima:'} {stats['minima']:.2f} m\n"

    texto += "\n" + "="*50 + "\n\n"
    texto += f"{'ESTACA':12} | {'TERRENO (m)':12} | {'PROJETO (m)':12} \n"
    texto += "-" * 50 + "\n"
    
    for i in range(len(df)):
        estaca_label = f"Estaca {df['estaca'][i]}"
        cota_t = f"{df['cota_terreno'][i]:.2f}"
        cota_p = f"{df['cota_projeto'][i]:.2f}"
        texto += f"{estaca_label:12} | {cota_t:12} | {cota_p:12} \n"

    return texto

############################################### FORMATAR DECLIVIDADES ########################################################################
#  
#   Utilizada para converter a matriz altimétrica em um relatório legível focando exclusivamente nos percentuais de rampa e inclinação.
#   Lembrando que o calculo de declividades será em outra função, essa é apenas para formatar o resultado em uma string organizada para exibição.
#
#def formatar_declividades(df): - Solicita como parametro de entrada um dataframe de dados (que terá uma series de declividades).
#   
#   texto = "Declividades\n\n" -  Inicia a string com o título Declividades e quebras de linha.
#   for i in range(len(df)): -    Inicia o laço de repetição que varrerá todas as linhas do dataframe, de i=0 até o valor do comprimento do dataframe.
#       estaca_texto = f"Estaca {df['estaca'][i]}" -     Cria a string de identificação da estaca (ex. Estaca 1).
#       valor_texto = f"{round(df['declividade'][i]*100, 2)} %" - Pega o valor decimal da declividade,
#       multiplica por 100 para converter em percentual, arredonda para 2 casas decimais e adiciona o símbolo de porcentagem.
#       texto += f"{estaca_texto:12} - {valor_texto}\n" - Concatena a linha construída na string base. 
#       :12 para a largarua da coluna e o caracter '-' para separar visualmente a estaca do valor.
#   
#   return texto - Devolve a string com o relatório das declividades em percentual.
#
##############################################################################################################################################

def formatar_declividades(df):

    texto = "Declividades\n\n"
    for i in range(len(df)):
        estaca_texto = f"Estaca {df['estaca'][i]}"
        valor_texto = f"{round(df['declividade'][i]*100, 2)} %"
        texto += f"{estaca_texto:12} - {valor_texto}\n"
    
    return texto

############################################### FORMATAR TRECHOS CRÍTICOS ######################################################################################################
#
#   Utilizada para gerar o relatório informando o pontos de trechos críticos. Possui tratamento condicional de layout não tenha trechos críticos.
#   Essas declividades críticas são calculadas em outra função e são definidas por um limite máximo de tolerância, que é fornecido pelo arquivo de configuração.
#
#def formatar_trechos_criticos(criticos): - Solicita como parametro de entrada de um sub-DataFrame (que será resultado de um filtro de limites críticos na outra função).
#   texto = "Trechos críticos\n\n" - Inicializa o cabeçalho com o titulo.
#   if len(criticos) == 0: - Utiliza um teste logico como para verificar se o pacote de dados filtrado chegou vazio (nenhum trecho critico encontrado).
#       texto += "Nenhum trecho crítico..." - Caso esteja vazio, concatena ao texto que a o caminho não possui tais trechos, passou na tolerância.
#   else: - Caso a matriz possua dados, existem trechos fora da tolerância.
#       for i in range(len(criticos)): - Inicia o laço de repetição que vai de i = 0 até o comprimento do DataFrame (Que contém apenas os trechos críticos).
#           texto += ( - Abre concatenação estruturada.
#               f"Estaca {criticos.iloc[i]['estaca']} - " - Utiliza a função .iloc[] do Pandas (Localizador por Índice de Linha) para fatiar o dado mesmo com o índice desordenado.
#               f"{round(criticos.iloc[i]['declividade']*100,2)} %\n" - Extrai o valor da declividade da estaca, formata o percentual e pula linha.
#           ) - Encerra a concatenação da linha na string base.
#
#   return texto - Envia a string com o relatório dos trechos críticos.
#
################################################################################################################################################################################


def formatar_trechos_criticos(criticos):
    texto = "Trechos críticos\n\n"
    if len(criticos) == 0:
        texto += "Nenhum trecho crítico encontrado"
    else:
        for i in range(len(criticos)):
            texto += (
                f"Estaca {criticos.iloc[i]['estaca']} → "
                f"{round(criticos.iloc[i]['declividade']*100,2)} %\n"
            )

    return texto

############################################### GRÁFICO PERFIL ###############################################################################
#
#   Utilizada para gerar a representação visual (plotagem 2D) do perfil longitudinal da rodovia. 
#   Utiliza a biblioteca Matplotlib para desenhar as linhas e "pintar" as zonas críticas de terraplanagem que demandam atenção. 
#   Como as zonas criticas são as zonas que exigem corte ou aterro, a função utiliza a diferença entre o terreno e o projeto para identificar onde estão essas zonas, 
#   e as de corte de vermelho e as de aterro de azul.
#
#def grafico_perfil(df): - Define a função de plotagem gráfica, exigindo a matriz de dados.
#   plt.figure(figsize=(12, 5)) - Instancia um novo quadro na janela, definindo as proporções (12x5 polegadas).
#   plt.plot(..., 'g-', label="Terreno") -  Plota o vetor de distâncias (X) e cotas (Y) do terreno real. E atribui um rótulo de "Terreno" para usar na legenda.
#   'g-' formata como uma linha verde contínua, onde o "g" é a cor verde (green) e "-" é o estilo de linha, uma linha contínua.
#   Você pode alterar para outras cores e estilos, como 'b--' para azul tracejado ou 'y:' para amarelo pontilhado.
#   plt.plot(..., 'r--', label="Projeto") - Sobrepõe a linha ideal de projeto. 'r--' formata linha vermelha tracejada. E o rótulo é "Projeto".
#   plt.fill_between(...) - Chama a ferramenta que realiza a "coloração" nas aréas onde o terreno natural está abaixo do projeto, indicando a necessidade de aterro.
#               where=(df["dif"] > 0.03), - Aqui está a condição: Pintar apenas a área onde a diferença exceder a tolerância de 0.03m.
#               color='blue', alpha=0.3, label="Aterro") - Aqui colocamos a estetica: Cor = azul, opacidade = 0.3 = 30% (translúcido) e o rotulo = Aterro.
#   plt.fill_between(...) - Invoca novamente, so que agora para indicar visualmente as áreas onde o terreno natural está acima do projeto, indicando a necessidade de corte.
#               where=(df["dif"] < -0.03), - A condição: pinta os trechos onde a diferença exige corte de terra.
#               color='red', alpha=0.3, label="Corte") - A estetica: a cor vermelha, opacidade = 0.3 = 30% (translúcido) e o rotulo associada a ela = Corte.
#   plt.title(...) -   Coloca no topo superior do quadro o título que descreve o gráfico.
#   plt.legend() -     Organiza os rótulos (labels) declarados em uma caixa de legenda.
#   plt.show() -       Compila a imagem e exibe numa janela.
#   
#   Obs.: Para salvar a imagem/grafico tem uma opção na janela formada, um icone de disquete, basta clicar e escolher o local para salvar
#
##############################################################################################################################################

def grafico_perfil(df):
    plt.figure(figsize=(12, 5))
    plt.plot(df["distancia"], df["cota_terreno"], 'g-', label="Terreno")
    plt.plot(df["distancia"], df["cota_projeto"], 'r--', label="Projeto")
    plt.fill_between(df["distancia"], df["cota_terreno"], df["cota_projeto"], 
                     where=(df["dif"] > 0.03), 
                     color='blue', alpha=0.3, label="Aterro Crítico")
    plt.fill_between(df["distancia"], df["cota_terreno"], df["cota_projeto"], 
                     where=(df["dif"] < -0.03), 
                     color='red', alpha=0.3, label="Corte Crítico")
    plt.title("Zonas de Intervenção Crítica (> 3%)")
    plt.legend()
    plt.show()


############################################### MAPA DE RELEVO #########################################################################################################
# 
#   Utilizada para gerar um mapa de revelo bidimensional. 
#   Ela recebe a nuvem de pontos e interpola algoritmicamente entre os pontos, projetando uma superfície digital contínua de terreno.
#
#def mapa_relevo(df): - Solicita como parâmetro a matriz contendo a nuvem de pontos de campo.
#   
#   x, y, z = df["x"], df["y"], df["z"] -  Separa as componentes espaciais da matriz e as guarda em variáveis independentes.
#   xi = np.linspace(min(x), max(x), 30) - Cria uma trena virtual (NumPy) com 30 marcadores equidistantes no eixo X.
#   yi = np.linspace(min(y), max(y), 30) - Executa o mesmo procedimento para o eixo Y.
#   xi, yi = np.meshgrid(xi, yi) -         Reconfigura as duas trenas, cruzando-as, para formar uma grade (30x30).
#   zi = griddata(...) - Atribui uma altitude aos nós da grade baseando-se no metodo de valor mais próximo (method="nearest").
#   !!!! A função griddata do SciPy pega os pontos que você conhece e preenche as altitudes dos espaços vazios no meio deles, através do método de interpolação.
#
#   plt.figure() - Libera segmento de memória parar gerar a tela.
#   plt.pcolormesh(xi, yi, zi, cmap="terrain", shading='auto') - Reveste a grade com gradiente. A paleta 'terrain' do matplotlib pinta cotas como mapas topográficos.
#   plt.colorbar(label="Altitude") -    Posiciona a escala de cores (legenda) informando a relação entre cores e valores numéricos.
#   plt.xlabel("X") e plt.ylabel("Y") - Estabelecem legendas horizontais e verticais dos eixos.
#   plt.title("Mapa de Relevo (Grade)") - Insere título da janela no topo.
#   plt.show() - Exibe a janela na tela.
#   
#   Recomendo que salvem esse arquivo como está e depois brinque com os parâmetros, como numeros de grade e método de interpolação, para entender melhor o processo.
##########################################################################################################################################################################

def mapa_relevo(df):

    x, y, z = df["x"], df["y"], df["z"]
    xi = np.linspace(min(x), max(x), 30)
    yi = np.linspace(min(y), max(y), 30)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata((x, y), z, (xi, yi), method="nearest")

    plt.figure()
    plt.pcolormesh(xi, yi, zi, cmap="terrain", shading='auto')
    plt.colorbar(label="Altitude")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Mapa de Relevo (Grade)")
    plt.show()

############################ MOSTRAR O MENU #########################################################################################################################################   
#   
#   Utilizada para exibir no terminal o menu de opções operacionais disponiveis. 
#   Atua como um painel de controle textual, orientando/informando o processo de navegação pelas funcionalidades do programa.
# 
# def mostrar_menu(): - Encapsula a exibição do menu sem exigir nenhum dado externo para funcionamento.
#
#############################################################################################################################################################################################

def mostrar_menu():
    print("\n======================================")
    print("          MENU DE ANÁLISE")
    print("======================================")
    print("1 - Mostrar perfil da estrada")
    print("2 - Mostrar declividades")
    print("3 - Detectar trechos críticos")
    print("4 - Calcular corte e aterro")
    print("5 - Gráfico do perfil")
    print("6 - Mapa de relevo")
    print("7 - Gerar dataset final de análise")
    print("0 - Sair")

############################################### FUNÇOES DE PROCESSAMENTO DE DADOS ############################################################################################################################################################################################

############################################### LER PARÂMETROS ###################################################################################################################
#
#   Utilizada para ler as configurações pre-definidas do projeto. A função recebe o arquivo de texto e decodifica para um dicionário.
#
#def ler_parametros(parametros_txt): - Exige o objeto do arquivo de texto já previamente aberto.
#   
#   parametros = {} - Cria um dicionário vazio, que irá atuar como uma tabela das variáveis de projeto.
#   for linha in parametros_txt: - Inicia a iteração que ler linha por linha do arquivo.
#       linha = linha.strip() -  Remove quebras de linha invisíveis e espaços que sobraram.
#       if linha == "": -        Verifica se a linha lida está vazia.
#           continue -               Ignora o espaço em branco e pula para a próxima iteração do loop.
#       chave, valor = linha.split("=")  - Quando não é vazio, ele divide o texto da linha no marcador '='. Oque ta do lado esquerdo vira a chave, oque tiver do lado direito o valor.
#              Seguindo o padrão de configuração 'chave=valor' do dicionario.  
#        parametros[chave] = float(valor) - Converte o texto da direita para decimal (float) e armazena no dicionário.
#   
#   return parametros - Devolve um dicionário com os parâmetros lidos.
#
#################################################################################################################################################################################

def ler_parametros(parametros_txt):
 
    parametros = {}
    for linha in parametros_txt:
        linha = linha.strip()
        if linha == "":
            continue
        chave, valor = linha.split("=")
        parametros[chave] = float(valor)

    return parametros

############################################### LER NUVEM DE PONTOS ##############################################################################################################
#
#   Utilizada para transformar as um arquivo CSV, contendo as coordenadas topográficas, em uma lista estruturada de dicionários.
#
#def ler_nuvem_pontos(nuvem_csv): - Define a função exigindo o ponteiro do arquivo CSV.
#   
#   linhas = nuvem_csv.readlines() -   .readlines() irá pegar, linha por linha, o conteudo do arquivo inteiro, e irá armazenar cada linha como um item de uma lista.
#   
#   pontos = [] - Instancia uma lista nativa vazia que servirá "recipiente".
#   
#   for linha in linhas[1:]: -       Detalhe: Inicia a iteração no índice [1] para contornar e ignorar o cabeçalho do arquivo CSV, que iriam conter os nomes das colunas.
#   partes = linha.strip().split(",") - Limpa espaços residuais e fatia a linha nas vírgulas, isolando os números.
#   ponto = { ... } -                 Abre um dicionário LOCAL para organizar o registro atual, simulando um plano cartesiano.
#   !!!!Como esse arquivo csv foi aberto em forma de leitura, os dados são lidos como texto (string).!!!!
#   !!!!!! Para realizar cálculos ou análises numéricas, é necessário converter esses textos em números.!!!!!
#       "id": int(partes[0]), -     Pega o primeiro valor da linha e converte para número inteiro. O identificador do ponto.
#       "x": float(partes[1]), -    O segundo valor é convertido para decimal, representando a coordenada X do ponto.
#       "y": float(partes[2]), -    O terceiro valor é convertido para decimal, representando a coordenada Y do ponto.
#       "z": float(partes[3]) -     O quarto valor é convertido para decimal, representando a altitude (Z) do ponto.
#       pontos.append(ponto) -   Empacota o dicionário recem gerado da lista principal.
#   
#   return pontos - Devolve a matriz de pontos formatada.
#
###############################################################################################################################################################################3

def ler_nuvem_pontos(nuvem_csv):

    linhas = nuvem_csv.readlines()
    pontos = []
    for linha in linhas[1:]:
        partes = linha.strip().split(",")
        ponto = {
            "id": int(partes[0]),
            "x": float(partes[1]),
            "y": float(partes[2]),
            "z": float(partes[3])
        }
        pontos.append(ponto)

    return pontos

############################################### ANALISAR PERFIL #############################################################################################################
#
#   Utilizada para calcular vetorialmente as variações verticais do projeto. 
#   Aqui realizamos via pandas, para exemplificar a facilidade de uso em grandes conjuntos de dados. 
#
# def analisar_perfil(df): - Define a função requisitando como parametro de entrada a estrutura DataFrame.
#   
#   df['dif'] = df['cota_projeto'] - df['cota_terreno'] - Subtrai o vetor do terreno do vetor do projeto de uma só vez, criando a variável 'dif'.  
#   Aqui foi criada uma nova coluna no DataFrame, onde cada linha é a diferença entre a cota do projeto e a cota do terreno para aquela estaca específica.
#   É bastante pratico criar colunas novas em um DataFrame, pois ele é uma estrutura de dados muito flexível e projetada visando a manipulação de tabelas.
#   
#   infos = { ... } - Instancia um dicionário {} para agrupar os dados estatísticos das informações contidas no dataframe.
#       'media': df['cota_terreno'].mean(), - .mean() ira fornecer a cota média da coluna 'cota_terreno' do datframe.
#       'maxima': df['cota_terreno'].max(), - .max() irá fornecer a cota máxima da coluna 'cota_terreno' do datframe, ou seja, o ponto mais alto do terreno natural.
#       'minima': df['cota_terreno'].min() -  .min() irá fornecer a cota mínima da coluna 'cota_terreno' do datframe, ou seja, o ponto mais baixo do terreno natural.
#   return df, infos - Devolve o DataFrame atualizado e o pacote estatístico.
#
#############################################################################################################################################################################

def analisar_perfil(df):

    df['dif'] = df['cota_projeto'] - df['cota_terreno']
    infos = {
        'media': df['cota_terreno'].mean(),
        'maxima': df['cota_terreno'].max(),
        'minima': df['cota_terreno'].min()
    }

    return df, infos

############################################### CALCULAR DECLIVIDADES ########################################################################
#
#   Utilizada para calcular a inclinação (declividade) trecho a trecho, aplicando: delta de altura / delta de distância.
#
# def calcular_declividades(df): - Define a função que precisa como parametro de entrada uma matriz (DataFrame) de dados.
#   df["declividade"] = ( ... ) - Cria a nova coluna no DataFrame que armazenará o resultado das inclinações.
#   df["cota_terreno"].diff() - Com o pandas, é possivel calcular instantaneamente a diferença de altura entre a estaca atual e a anterior.
#   / df["distancia"].diff() - Calcula delta de altura / delta de distância, para obter a inclinação percentual.
#   .fillna(0) - Como a estaca inicial (linha 0) não possui uma estaca anterior, o .diff() gera um valor vazio (NaN). 
#   O fillna() varre a coluna e substitui esse vazio por 0.
#   return df - Devolve a matriz atualizada e calculada em alta performance computacional.
#
##############################################################################################################################################

def calcular_declividades(df):
    df["declividade"] = (df["cota_terreno"].diff() / df["distancia"].diff()).fillna(0)
    return df

############################################### FILTRAR TRECHOS CRÍTICOS #####################################################################
#
#   Utilizada para identificar quais trechos são críticos, que são os trechos cujas inclinações ultrapassam o limite técnico.
#   Que, conforme o arquivo de configuração, é de 8% (0.08 em decimal).
#
#def filtrar_trechos_criticos(df, limite): -         Exige o DataFrame e o valor numérico de limite predefinido. (no caso, 0.08 para 8%).
#   criticos = df[abs(df["declividade"]) > limite] - Cria um sub-df com os trechos críticos, que são os trechos da coluna delividade com valor absoluto maior que o limite.
#   abs() avalia o valor absoluto (ignorando se é subida ou descida), se o valor for -0.09 ou 0.09, ambos serão considerados críticos, pois ultrapassam o limite de 0.08.
#   return criticos - Devolve o sub-DataFrame apenas com os trechos críticos.
#
##############################################################################################################################################

def filtrar_trechos_criticos(df, limite):
    criticos = df[abs(df["declividade"]) > limite]
    return criticos

############################################### CALCULAR CORTE E ATERRO ######################################################################
#
#   Utilizada para comparar o traçado natural com o ideal, calculando se é nescessario remover terra (corte) ou acrescentar (aterro).
#   De forma que a cota do terreno seja igual a cota do projeto, ou seja, o valor da diferença entre eles aproximadamente 0.
#
#def calcular_corte_aterro(df): - Define a função para processar os volumes da matriz.
#   diferenca = df["cota_terreno"] - df["cota_projeto"] - Calcula vetorialmente a diferença algébrica entre o chão natural e a pista para TODAS as estacas de uma vez.
#   df["corte"] = np.where(diferenca > 0, diferenca, 0) - Usando o Numpy, ele encontra onde a diferença for maior que 0 (excesso), anote a diferença. 
#   Caso contrário, anote 0". Tudo sem usar 'if'.
#   df["aterro"] = np.where(diferenca < 0, abs(diferenca), 0) - O mesmo se aplica ao aterro onde a diferença for menor que 0 (falta), converte para positivo com abs() e anota.
#   Caso contrário, anote 0.
#   A função np.where() é uma maneira eficiente de aplicar condições em arrays, evitando a necessidade de loops explícitos e otimizando o desempenho.
#
#   return df, df["corte"].sum(), df["aterro"].sum() - Retorna a matriz atualizada e usa o motor do Pandas (.sum) para entregar os totais calculados instantaneamente.
#   .sum() irá somar todos os valores da coluna 'corte' para fornecer o volume total de corte necessário, e o mesmo para a coluna 'aterro'.
#
##############################################################################################################################################

def calcular_corte_aterro(df):
   
    diferenca = df["cota_terreno"] - df["cota_projeto"]
    df["corte"] = np.where(diferenca > 0, diferenca, 0)
    df["aterro"] = np.where(diferenca < 0, abs(diferenca), 0)

    return df, df["corte"].sum(), df["aterro"].sum()

########################################### CLASSIFICAR TERRENO ###################################################################################################################################################   
#   Utilizada para atribuir uma qualificação descritiva (Plano, Ondulado, Montanhoso) para cada coordenada, com base sua inclinação percentual.
#
#def classificar_terreno(df): - Recebe um dataframe como parametro.
#   tipos = [] - Inicializa a lista que guardará as classificações.
#   for i in range(len(df)): - Inicia o loop para processamento linha a linha de i = 0 até o comprimento do dataframe.
#       declive = abs(df["declividade"][i]) - Extrai o valor absoluto da declividade local da estaca.
#       if declive < 0.03:  -  Avalia se a inclinação é inferior a 3%.
#           tipos.append("Plano") - Se verdadeiro, insere o texto "Plano" na lista.
#       elif declive < 0.08:  -  Avalia se a inclinação está compreendida entre 3% e o limite de 8%.
#           tipos.append("Ondulado") - Se verdadeiro, insere o texto "Ondulado".
#       else: - Se a inclinação superar todas as regras acima.
#           tipos.append("Montanhoso") - Insere o texto "Montanhoso".
#   df["tipo_terreno"] = tipos - Transforma a lista de textos criada em uma nova coluna no dataframe.
#   
#   return df - Retorna o DataFrame com a nova coluna contendo a classificação .
#
#############################################################################################################################################################################################

def classificar_terreno(df):
    tipos = []
    for i in range(len(df)):
        declive = abs(df["declividade"][i])
        if declive < 0.03:
            tipos.append("Plano")
        elif declive < 0.08:
            tipos.append("Ondulado")
        else:
            tipos.append("Montanhoso")
    df["tipo_terreno"] = tipos
    return df


############################################### COMPILAR DATASET FINAL #######################################################################
#
#   Utilizada para reorganizar o dataframe para salva-lo, descartando as colunas temporárias de cálculo que não são necessárias.
#
#def compilar_dataset_final(df): - Exige o DataFrame em seu estado de processamento atual.
#   
#   dataset_final = df[[ - Inicializa a criação de um sub-DataFrame usando indexação dupla de chaves no Pandas, note o "[[" "]]"".
#
#       "estaca", "distancia", "cota_terreno", "cota_projeto", "declividade", "tipo_terreno", "corte", "aterro" 
#   ]] - Encerramos a indexação, o que não estiver listado aqui (ex: coluna 'dif') não estará no dataframe retornado.
#   
#   return dataset_final - Devolve a matriz contendo somente as informações listadas.
#
##############################################################################################################################################

def compilar_dataset_final(df):
    
    dataset_final = df[[
        "estaca", "distancia", "cota_terreno", "cota_projeto",
        "declividade", "tipo_terreno", "corte", "aterro"
    ]]
    return dataset_final

############################################### SALVAR DATASET ###############################################################################
#
#   Utilizada para salvar o dataframe no disco rígido (formato CSV).
#   Aqui também é abordado superficialmente o tratamento de erros, para evitar que o programa quebre caso o usuário tente salvar o arquivo 
#   enquanto ele ainda está aberto em outro programa, como Excel.
#
#def salvar_dataset(df, nome_arquivo): - Recebe a matriz (df) e o nome final do arquivo desejado.
#   
#   try: -  Abre o bloco de tentativa de salvamento seguro.
#       df.to_csv(nome_arquivo, index=False) - Tenta a gravação em disco. index=False impede de salvar o contador natural de linhas. A coluna Index/Indice.
#       return True, f" Sucesso..." - Devolve o status positivo e uma string de confirmação.
#   except PermissionError: - Intercepta erro de permissão, o python não pode acessar o arquivo devido a outro porgamar estar com ele aberto.
#       return False, f" Erro de Permissão..." - Devolve aviso específico orientando o usuário a fechar programas que estão com permissão de alteração do arquivo.
#   except Exception as e: Aqui é quando é outro erro que pode influencias (disco cheio, caminho bloqueado).
#       return False, f" Erro inesperado..." - Informa falha geral e concatena o código do erro do sistema 'e'.
#
##############################################################################################################################################

# #################### DATASET FINAL (dataset_final_analise.csv) ####################################################################################################
# 
#   Uma matriz que possui diversas informações do projeto, tanto as que tinham sido fornecidas inicialmente, quanto as que foram calculadas ao longo do processo.
#   
#   Como:
#       - declividade: Inclinação calculada entre as estacas adjacentes.
#       - tipo_terreno: Classificação do tipo do terreno (Plano, Ondulado ou Montanhoso).
#       - corte:  Diferença onde o terreno natural supera o projeto.
#       - aterro: Diferença onde o terreno natural está abaixo do projeto.
#   
#   Formato: Arquivo CSV gerado pelo Pandas.
# 
#####################################################################################################################################################################

def salvar_dataset(df, nome_arquivo):

    try:
        df.to_csv(nome_arquivo, index=False)
        return True, f" Sucesso: Arquivo '{nome_arquivo}' salvo corretamente."
    except PermissionError:
        return False, f" Erro de Permissão: O arquivo '{nome_arquivo}' não pôde ser salvo. \n Verifique se ele está aberto em outro programa e feche-o antes de tentar novamente."
    except Exception as e:
        return False, f" Erro inesperado ao salvar '{nome_arquivo}': {e}"

############################################### INICIAR SISTEMA ##############################################################################
#
#   Aqui está o ponto de entrada do sistema. Ele Recebe os arquivos base, repassa para as funções de cálculo e retorna os dados processados, para uso no programa principal.
#
#def iniciar_sistema(df_perfil, txt_parametros, txt_nuvem): - Exige o DataFrame e os dois arquivos de texto abertos.
#   
#   parametros = ler_parametros(txt_parametros) - Chama a conversão do texto TXT para dicionário lógico e o salva na variável 'parametros'.
#   pontos = ler_nuvem_pontos(txt_nuvem) - Roda a estruturação do CSV em matriz 3D e a armazena na variável 'pontos'.
#   df, infos_perfil = analisar_perfil(df_perfil) - Captura a base modificada e as estatísticas de variação e as armazena em 'df' e 'infos_perfil', respectivamente.
#   df = calcular_declividades(df) - Passa o dataframe, pós processamento em analisar_perfil(), parar a função de calcular declividades, atualizando o df com coluna de "declividade".
#   limite = parametros["declividade_maxima"] - Extrai a variável de tolerância extraída do dicionário.
#   return parametros, pontos, df, infos_perfil, limite - Envia tudo que foi processado de volta ao programa principal do sistema.
#
##############################################################################################################################################

def iniciar_sistema(df_perfil, txt_parametros, txt_nuvem):
    
    
    parametros = ler_parametros(txt_parametros)
    pontos = ler_nuvem_pontos(txt_nuvem)
    df, infos_perfil = analisar_perfil(df_perfil)
    df = calcular_declividades(df)
    limite = parametros["declividade_maxima"]
    return parametros, pontos, df, infos_perfil, limite



############################################### PROGRAMA PRINCIPAL ###########################################################################
#
#   É o ponto de partida, onde a execução real começa. Aqui onde definimos o fluxo de dados, utilizamos as funções criadas anteriormente e realizamos a interação com o usuário.
#
#   print(...) - Exibe o cabeçalho de boas-vindas do sistema no terminal.
#   df_perfil = pd.read_csv("perfil_longitudinal.csv") - Utiliza o Pandas para ler a matriz CSV NA PASTA do projeto e carregá-la na memória RAM de uma vez só.
#   txt_parametros = open("parametros.txt", "r") -  Abre o arquivo de texto em modo de leitura pura ('r' de read).
#   txt_nuvem = open("nuvem_pontos.csv", "r") -     Abre o arquivo CSV da nuvem de pontos como fluxo de texto puro ('r' de read).
#   parametros, pontos, df, ... = iniciar_sistema(...) - Chama a função iniciar_sistema que: processa os arquivos, aciona os cálculos essenciais pro programa.
#   txt_nuvem.close() / txt_parametros.close() - Fecha os ponteiros dos arquivos abertos para liberar espaço em memória do PC, uma boa prática de programação.
#   print(f"-> {len(pontos)}...") - Usa f-string para exibir dinamicamente o total de pontos processados medindo o tamanho da lista com len().
#   print(f"-> Parâmetros lidos: {parametros}") - Exibe o dicionário de parâmetros.
#   e, por fim, o print("Sistema pronto.\n") - Indica que o sistema está operacional e pronto para receber comandos do usuário.
#
##############################################################################################################################################

print("\n======================================")
print("  ANÁLISE DE DADOS TOPOGRÁFICOS")
print("  PARA PROJETO DE ESTRADAS")
print("======================================\n")



print("Inicializando o sistema e carregando dados...")

df_perfil = pd.read_csv("perfil_longitudinal.csv")
txt_parametros = open("parametros.txt", "r")
txt_nuvem = open("nuvem_pontos.csv", "r")

parametros, pontos, df, infos_perfil, limite = iniciar_sistema(df_perfil, txt_parametros, txt_nuvem)

print("Dados carregados com sucesso!")

txt_nuvem.close()
txt_parametros.close()

print("Arquivos de dados fechados.")

df_pontos = pd.DataFrame(pontos)

print(f"-> {len(pontos)} pontos topográficos carregados.")
print(f"-> Parâmetros lidos: {parametros}")
print("Sistema pronto.\n")



while True:
    mostrar_menu()
    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        texto_formatado = formatar_perfil(df, infos_perfil)
        mostrar_texto("Perfil Longitudinal Detalhado", texto_formatado)

    elif opcao == "2":
        texto_formatado = formatar_declividades(df)
        mostrar_texto("Declividades", texto_formatado)
        
        if perguntar_sim_nao("Deseja salvar a tabela de declividades? (s/n): "):
            tabela_salvar = df[["estaca", "declividade"]]
            sucesso, mensagem = salvar_dataset(tabela_salvar, "declividades.csv")
            print(mensagem)

    elif opcao == "3":
        df_criticos = filtrar_trechos_criticos(df, limite)
        texto_formatado = formatar_trechos_criticos(df_criticos)
        mostrar_texto("Trechos Críticos", texto_formatado)
        
        if perguntar_sim_nao("Deseja salvar os trechos críticos? (s/n): "):
            sucesso, mensagem = salvar_dataset(df_criticos, "trechos_criticos.csv")
            print(mensagem)

    elif opcao == "4":
        df, volume_corte, volume_aterro = calcular_corte_aterro(df)
        texto_volumes = (
            f"Volume de corte aproximado: {round(volume_corte, 2)}\n"
            f"Volume de aterro aproximado: {round(volume_aterro, 2)}"
        )
        mostrar_texto("Volumes de Corte e Aterro (m³)", texto_volumes)

    elif opcao == "5":
        grafico_perfil(df)

    elif opcao == "6":
        mapa_relevo(df_pontos)

    elif opcao == "7":
        df = classificar_terreno(df)
        if "corte" not in df.columns:
            df, _, _ = calcular_corte_aterro(df)
            
        dataset_final = compilar_dataset_final(df)
        mostrar_texto("Dataset Final Gerado", dataset_final.to_string())        
        
        if perguntar_sim_nao("Deseja exportar o dataset final para CSV? (s/n): "):
            sucesso, mensagem = salvar_dataset(dataset_final, "dataset_final_analise.csv")
            print(mensagem)
    
    elif opcao == "0":
        print("Encerrando programa. Até a próxima!")
        break
    else:
        print("Opção inválida. Escolha um número do menu.")