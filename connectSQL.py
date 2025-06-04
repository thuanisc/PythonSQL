# instalar plugin SQL no Python - precisa criar database no MySQL antes:
## pip install sqlalchemy pymysql
## pip install mysql-connector-python

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/PythonSQL")

print("Conexão com o banco de dados criada com sucesso!")

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

#Criando modelos
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios" #nome para a tabela
    id = Column(Integer, primary_key=True) #default: auto_increment - vai criar IDs automaticamente; se False, ID manual
    nome = Column(String(100))
    email = Column(String(100))

    emprestimos = relationship("Emprestimo", back_populates="usuario")


class Livro(Base):
    __tablename__ = 'livros'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200))
    autor = Column(String(100))
    emprestimos = relationship("Emprestimo", back_populates="livro")

class Emprestimo(Base):
    __tablename__ = 'emprestimos'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    livro_id = Column(Integer, ForeignKey('livros.id'))
    data_emprestimo = Column(Date)

    usuario = relationship("Usuario", back_populates="emprestimos")
    livro = relationship("Livro", back_populates="emprestimos")

#Criando tabelas no banco
Base.metadata.create_all(engine)

#Criando sessão
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

#Inserindo dados - demonstração (na prática, usuário add e depois é excluído pelo sistema)
novo_usuario = Usuario(nome="João", email="joao@email.com")
session.add(novo_usuario)  #vai armazenar dentro da sessão
session.commit() #vai enviar o que está armazenado

#Inserindo dados múltiplos
session.add_all([
    Usuario(nome="Thiago", email="thiago@email.com"),
    Usuario(nome="Maria", email="maria@email.com"),
    Usuario(nome="Carlos", email="carlos@email.com")
])
session.commit()

session.add_all([
    Livro(titulo="Python para Iniciantes", autor="Autor A"),
    Livro(titulo="Banco de Dados Avançado", autor="Autor B"),
    Livro(titulo="Aprendendo SQL", autor="Autor C")
])
session.commit()

usuario1 = session.query(Usuario).filter_by(nome="Thiago").first()
usuario2 = session.query(Usuario).filter_by(nome="Maria").first()

livro1 = session.query(Livro).filter_by(titulo="Python para Iniciantes").first()
livro2 = session.query(Livro).filter_by(titulo="Aprendendo SQL").first()

from datetime import date
emprestimo1 = Emprestimo(usuario_id=usuario1.id, livro_id=livro1.id, data_emprestimo=date(2025, 6, 1))
emprestimo2 = Emprestimo(usuario_id=usuario2.id, livro_id=livro2.id, data_emprestimo=date(2025, 6, 2))

session.add_all([emprestimo1, emprestimo2])
session.commit()


#Consultando Dados
usuarios = session.query(Usuario).all()
for u in usuarios:
    print(u.nome, u.email)

#Atualizando Dados
usuario = session.query(Usuario).filter_by(nome="João").first() #first = primeiro registro da lista, mas pode ser outros tipos de busca (ID, etc.) dependendo da amplitude da busca
usuario.email = "novo@email.com" #aloca no sistema
session.commit() #pega no sistema todas as alterações e joga pro banco de dados

#Removendo dados
usuario = session.query(Usuario).filter_by(nome="João").first()
session.delete(usuario)
session.commit()

#Combinar/relacionar tabelas (Join)
resultado = (
    session.query(Usuario.nome, Livro.titulo, Emprestimo.data_emprestimo)
    .join(Emprestimo, Usuario.id == Emprestimo.usuario_id)
    .join(Livro, Livro.id == Emprestimo.livro_id)
    .all()
)

for nome, titulo, data in resultado:
    print(f"{nome} pegou '{titulo}' em {data}")
