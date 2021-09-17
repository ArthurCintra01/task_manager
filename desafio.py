import time
import datetime
from sqlalchemy import Column, Integer, ForeignKey,String,Date,delete,update
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import and_
from prettytable import PrettyTable

#iniciando database
eng= create_engine("sqlite:///projetos.db")
Base = declarative_base(bind=eng)
Session = sessionmaker(bind=eng)

#criando table dos projetos na database
class Projeto(Base):
    __tablename__ = 'projeto'
    id = Column(Integer, primary_key=True,autoincrement=True)
    nome = Column(String,nullable=False)
    data_inicio = Column(Date,nullable=False)
    data_fim = Column(Date,nullable=False)
    quantidade_atividades = Column(Integer,default=0)
    atividades_feitas = Column(Integer,default=0)
    atrasado = Column(String,default="Nao")
    atividades = relationship("Atividade",cascade="all,delete",backref='projeto')

#criando table das atividades como 'child' de projetos na database
class Atividade(Base):
    __tablename__ = 'atividade'
    id = Column(Integer,primary_key=True)
    second_id=Column(Integer,default=1)
    id_projeto = Column(Integer, ForeignKey('projeto.id'))
    nome=Column(String,nullable=False)
    data_inicio = Column(Date,nullable=False)
    data_fim = Column(Date,nullable=False)
    finalizada = Column(Boolean,nullable=True)

Base.metadata.create_all()

#criando tabela de projetos
tabela_projetos=PrettyTable()
tabela_projetos.field_names = ["ID Projeto","Nome Projeto","Data Inicio","Data Fim","% Completo","Atrasado"]

#criando tabela de atividades
tabela_atividades=PrettyTable()
tabela_atividades.field_names = ["ID Atividade","ID Projeto","Nome Atividade","Data Inicio","Data Fim","Finalizada?"]

#funcao para preencher a tabela de projetos do prettytable
def preencher_tabela():
    tabela_projetos.clear_rows()
    atrasado=""
    with Session() as s:
        rs=s.query(Projeto).all()
        for projeto in rs:
            #checando se alguma atividade tem data final maior que a do projeto
            rs2=s.query(Atividade).filter(Atividade.id_projeto==projeto.id)
            for atividade in rs2:
                if(atividade.data_fim>projeto.data_fim):
                    projeto.atrasado="Sim"
                else:
                    projeto.atrasado="Nao"
            #checando quantos % do projeto esta completo
            if(projeto.quantidade_atividades==0):
                completo=0
            else:
                completo=int((projeto.atividades_feitas/projeto.quantidade_atividades)*100)  

            #inserindo dados na tabela
            tabela_projetos.add_row([projeto.id,projeto.nome,projeto.data_inicio,projeto.data_fim,(str(completo))+"%",projeto.atrasado])

#funcao para preencher a tabela de atividades com as atividades do projeto escolhido
def preencher_tabela_atividades(i):
    tabela_atividades.clear_rows()
    with Session() as s:
        rs=s.query(Atividade).filter(Atividade.id_projeto==i)
        for ativ in rs:
            #checando se atividade esta realizada
            if(ativ.finalizada==True):
                f="Sim"
            elif(ativ.finalizada==False):
                f="Nao"
            #inserindo dados na tabela
            tabela_atividades.add_row([ativ.second_id,ativ.id_projeto,ativ.nome,ativ.data_inicio,ativ.data_fim,f])

#preenchendo tabela projeto com os dados da database            
preencher_tabela()
#Menu
while True:
    print("\nProjetos disponiveis:\n")
    print(tabela_projetos)
    print('''      Menu
        1 - adicionar projeto
        2 - editar projeto   
        3 - adicionar atividade a um projeto
        4 - ver atividades de um projeto
        5 - editar atividade
        6 - deletar projetos
        7 - sair do programa
    ''')
    #escolher opcao do menu
    x=(int(input("Selecione uma das opcoes: ")))

    #adicionar projeto
    if(x==1):
        #coletando informacoes do projeto
        n=input("nome do projeto: ")
        print("data de inicio: ")
        ano=(int(input("Ano: ")))
        mes=(int(input("Mes: ")))
        dia=(int(input("Dia: ")))
        print("Data Salva")
        print("data de Fim: ")
        ano2=(int(input("Ano: ")))
        mes2=(int(input("Mes: ")))
        dia2=(int(input("Dia: ")))
        datadeinicio=datetime.date(ano,mes,dia)
        datadefim=datetime.date(ano2,mes2,dia2) 
        #checando se a data de fim e maior que a de inicio
        while(datadeinicio>datadefim):
            print("Data de fim deve ser maior que de inicio")
            print("data de inicio: ")
            ano=(int(input("Ano: ")))
            mes=(int(input("Mes: ")))
            dia=(int(input("Dia: ")))
            print("Data Salva")
            print("data de Fim: ")
            ano2=(int(input("Ano: ")))
            mes2=(int(input("Mes: ")))
            dia2=(int(input("Dia: ")))
            datadeinicio=datetime.date(ano,mes,dia)
            datadefim=datetime.date(ano2,mes2,dia2) 

        print("Data Salva")
        #adicionando projeto a database
        with Session() as s:
            s.add_all([ 
            Projeto(nome=n,data_inicio=datadeinicio,data_fim=datadefim),
            ])
            s.commit()
        print("Novo projeto adicionado!")
        #preenchendo a interface tabela
        preencher_tabela() 
        #esperar 1 segundo para voltar a mostrar o menu
        time.sleep(1)

    #editar projeto
    if(x==2):
        i=int(input("Escolha a Id do projeto que deseja editar: "))
        #coletando informacoes do projeto
        n=input("Novo nome do projeto: ")
        print("Nova data de inicio: ")
        ano=(int(input("Ano: ")))
        mes=(int(input("Mes: ")))
        dia=(int(input("Dia: ")))
        print("Data Salva")
        print("Nova data de Fim: ")
        ano2=(int(input("Ano: ")))
        mes2=(int(input("Mes: ")))
        dia2=(int(input("Dia: ")))
        datadeinicio=datetime.date(ano,mes,dia)
        datadefim=datetime.date(ano2,mes2,dia2) 
        #checando se a data de fim e maior que a de inicio
        while(datadeinicio>datadefim):
            print("Data de fim deve ser maior que de inicio")
            print("data de inicio: ")
            ano=(int(input("Ano: ")))
            mes=(int(input("Mes: ")))
            dia=(int(input("Dia: ")))
            print("Data Salva")
            print("data de Fim: ")
            ano2=(int(input("Ano: ")))
            mes2=(int(input("Mes: ")))
            dia2=(int(input("Dia: ")))
            datadeinicio=datetime.date(ano,mes,dia)
            datadefim=datetime.date(ano2,mes2,dia2) 

        print("Data Salva")
        with Session() as s:
            update=s.query(Projeto).filter(Projeto.id==i).update({Projeto.nome:n,Projeto.data_inicio:datadeinicio,Projeto.data_fim:datadefim})
            s.commit()
        print("Projeto editado!")
        #preenchendo a interface tabela
        preencher_tabela()
        #esperar 1 segundo para voltar a mostrar o menu
        time.sleep(1)

    #adicionar atividade a um projeto
    if(x==3):
        #escolhendo o projeto
        i=int(input("Escolha a Id do projeto que deseja criar a atividade: "))
        preencher_tabela_atividades(i)
        print("\nAtividades desse projeto:\n")
        print(tabela_atividades)
        print("Adicionando nova atividade\n")
        #coletando os dados da atividade
        a=input("nome da atividade: ")
        print("data de inicio: ")
        ano=(int(input("Ano: ")))
        mes=(int(input("Mes: ")))
        dia=(int(input("Dia: ")))
        print("Data Salva")
        print("data de Fim: ")
        ano2=(int(input("Ano: ")))
        mes2=(int(input("Mes: ")))
        dia2=(int(input("Dia: ")))    
        datadeinicio=datetime.date(ano,mes,dia)
        datadefim=datetime.date(ano2,mes2,dia2)
        #checando se a data de fim e maior que a de inicio
        while(datadeinicio>datadefim):
            print("Data de fim deve ser maior que de inicio")
            print("data de inicio: ")
            ano=(int(input("Ano: ")))
            mes=(int(input("Mes: ")))
            dia=(int(input("Dia: ")))
            print("Data Salva")
            print("data de Fim: ")
            ano2=(int(input("Ano: ")))
            mes2=(int(input("Mes: ")))
            dia2=(int(input("Dia: ")))
            datadeinicio=datetime.date(ano,mes,dia)
            datadefim=datetime.date(ano2,mes2,dia2) 

        print("Data Salva")
        finalizada=str(input("esta finalizada?(Sim/Nao): "))
        if(finalizada=="Sim"):
            b=True
        elif(finalizada=="Nao"):
            b=False
        #adicionando a atividade no projeto escolhido
        with Session() as s:
            rs = s.query(Projeto).filter(Projeto.id==i)
            if (b==True):
                update1 = s.query(Projeto).filter(Projeto.id==i).update({Projeto.atividades_feitas:Projeto.atividades_feitas+1})
            update=s.query(Projeto).filter(Projeto.id==i).update({Projeto.quantidade_atividades:Projeto.quantidade_atividades + 1})
            for projeto in rs:               
                s.add_all([ 
                Atividade(second_id=projeto.quantidade_atividades,nome=a,id_projeto=projeto.id,data_inicio=datadeinicio,data_fim=datadefim,finalizada=b),
                ])
                s.commit()
                print("atividade adicionada")
        #preenchendo as interfaces tabelas
        preencher_tabela_atividades(i)
        preencher_tabela()
        #esperar 1 segundo para voltar a mostrar o menu
        time.sleep(1)
    #mostrando atividades de um projeto
    if(x==4):
        #escolhendo o projeto que deseja vizualizar
        i=int(input("Escolha a Id do projeto que deseja ver as atividades: "))
        #procurando as atividades certas
        print("\nAtividades do projeto: \n")
        preencher_tabela_atividades(i)
        print(tabela_atividades)
        print("\n")
        #esperar 1 segundo para voltar a mostrar o menu
        time.sleep(1)

    #editar atividade
    if(x==5):
        #escolhendo o projeto
        i=int(input("Escolha a ID do projeto que deseja editar a atividade: "))
        #preenchendo tabela com as atividades do projeto escolhido
        preencher_tabela_atividades(i)
        #mostrando tabela de atividades
        print(tabela_atividades)
        #escolhendo a atividade
        ida=int(input("Escolha o ID da atividade que deseja editar: "))
        #editando atividade escolhida
        n=input("Novo nome da atividade: ")
        print("Nova data de inicio: ")
        ano=(int(input("Ano: ")))
        mes=(int(input("Mes: ")))
        dia=(int(input("Dia: ")))
        print("Data Salva")
        print("Nova data de Fim: ")
        ano2=(int(input("Ano: ")))
        mes2=(int(input("Mes: ")))
        dia2=(int(input("Dia: ")))
        datadeinicio=datetime.date(ano,mes,dia)
        datadefim=datetime.date(ano2,mes2,dia2)
        #checando se a data de fim e maior que a de inicio
        while(datadeinicio>datadefim):
            print("Data de fim deve ser maior que de inicio")
            print("data de inicio: ")
            ano=(int(input("Ano: ")))
            mes=(int(input("Mes: ")))
            dia=(int(input("Dia: ")))
            print("Data Salva")
            print("data de Fim: ")
            ano2=(int(input("Ano: ")))
            mes2=(int(input("Mes: ")))
            dia2=(int(input("Dia: ")))
            datadeinicio=datetime.date(ano,mes,dia)
            datadefim=datetime.date(ano2,mes2,dia2) 

        print("Data Salva")
        finalizada=str(input("esta finalizada?(Sim/Nao): "))
        if(finalizada=="Sim"):
            b=True
        elif(finalizada=="Nao"):
            b=False
        
        with Session() as s:
            if (b==True):
                update1 = s.query(Projeto).filter(Projeto.id==i).update({Projeto.atividades_feitas:Projeto.atividades_feitas+1})
            update=s.query(Atividade).filter(and_(Atividade.id_projeto==i,Atividade.second_id==ida)).update({Atividade.nome:n,Atividade.data_inicio:datadeinicio,Atividade.data_fim:datadefim,Atividade.finalizada:b})
            s.commit()
         
        print("Atividade editada!")
        preencher_tabela_atividades(i)
        #esperar 1 segundo para voltar a mostrar o menu
        time.sleep(1)

    #deletar projetos
    if(x==6):
        #Menu de delete
        print('''
        1 - deletar um projeto 
        2 - deletar todos os projetos e atividades
        3 - cancelar
        ''')
        #input do usuario
        resposta = int(input("Escolha: "))

        if (resposta==3):
            print("Acao cancelada, voltando ao menu...")
            #esperar 1 segundo para voltar a mostrar o menu
            time.sleep(1)

        elif(resposta==2):
            with Session() as s:
                s.query(Projeto).delete()
                s.query(Atividade).delete()
                s.commit()
            print("todos os projetos foram deletados")
            preencher_tabela()
            #esperar 1 segundo para voltar a mostrar o menu
            time.sleep(1)

        elif(resposta==1):
            i=int(input("ID do projeto que deseja deletar: "))
            with Session() as s:
                s.query(Projeto).filter(Projeto.id==i).delete()
                s.query(Atividade).filter(Atividade.id_projeto==i).delete()
                s.commit()
            print("Projeto com id:{} foi deletado".format(i))
            preencher_tabela()
            time.sleep(1)
        else:
            print("Escolha indisponivel, voltando ao menu")
            #esperar 1 segundo para voltar a mostrar o menu
            time.sleep(1)

    #Fechar programa
    if(x==7):
        print("Fechando...")
        exit(0)