from datetime import datetime, timedelta
import csv
import os

class Livro:
    def __init__(self, titulo, autor, ano, copias):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.copias = copias
        self.avaliacoes = []
        self.comentarios = []

    def emprestar(self):
        if self.copias > 0:
            self.copias -= 1
            return True
        return False

    def devolver(self):
        self.copias += 1

    def adicionar_avaliacao(self, nota, comentario=None):
        self.avaliacoes.append(nota)
        if comentario:
            self.comentarios.append(comentario)

    def media_avaliacao(self):
        return sum(self.avaliacoes) / len(self.avaliacoes) if self.avaliacoes else 0

    def estrelas_media(self):
        media = self.media_avaliacao()
        return "★" * int(round(media)) + "☆" * (5 - int(round(media)))

class Usuario:
    def __init__(self, nome, id_usuario, contato):
        self.nome = nome
        self.id_usuario = id_usuario
        self.contato = contato

livros = {}
usuarios = {}
emprestimos = {}

def carregar_livros():
    if not os.path.exists("livros.csv"):
        with open("livros.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["titulo", "autor", "ano", "copias"])
    with open("livros.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            titulo = row["titulo"]
            livros[titulo] = Livro(titulo, row["autor"], int(row["ano"]), int(row["copias"]))
    print(f"{len(livros)} livros carregados.\n")

def salvar_livros(livros_dict, nome_arquivo="livros.csv"):
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["titulo", "autor", "ano", "copias"])
        for livro in livros_dict.values():
            writer.writerow([livro.titulo, livro.autor, livro.ano, livro.copias])

def carregar_usuarios():
    if not os.path.exists("usuarios.csv"):
        with open("usuarios.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id_usuario", "nome", "contato"])
    with open("usuarios.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            id_usuario = row["id_usuario"]
            usuarios[id_usuario] = Usuario(row["nome"], id_usuario, row["contato"])
    print(f"{len(usuarios)} usuários carregados.\n")

def carregar_emprestimos():
    if os.path.exists("emprestimos.csv"):
        with open("emprestimos.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                chave = (row["id_usuario"], row["titulo"])
                emprestimos[chave] = {
                    "data_emprestimo": datetime.strptime(row["data_emprestimo"], "%Y-%m-%d"),
                    "data_prevista": datetime.strptime(row["data_prevista"], "%Y-%m-%d"),
                    "data_devolucao": datetime.strptime(row["data_devolucao"], "%Y-%m-%d") if row["data_devolucao"] else None,
                    "multa": float(row["multa"])
                }
        print(f"{len(emprestimos)} empréstimos carregados.\n")
    else:
        with open("emprestimos.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id_usuario", "titulo", "data_emprestimo", "data_prevista", "data_devolucao", "multa"])
        print("Arquivo de empréstimos criado.\n")

def salvar_emprestimos():
    with open("emprestimos.csv", mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["id_usuario", "titulo", "data_emprestimo", "data_prevista", "data_devolucao", "multa"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for (id_usuario, titulo), dados in emprestimos.items():
            writer.writerow({
                "id_usuario": id_usuario,
                "titulo": titulo,
                "data_emprestimo": dados["data_emprestimo"].strftime("%Y-%m-%d"),
                "data_prevista": dados["data_prevista"].strftime("%Y-%m-%d"),
                "data_devolucao": dados["data_devolucao"].strftime("%Y-%m-%d") if dados["data_devolucao"] else "",
                "multa": dados["multa"]
            })

def emprestar_livro():
    id_usuario = input("ID do usuário: ")
    if id_usuario not in usuarios:
        print("Usuário não encontrado.\n")
        return

    titulo = input("Título do livro: ")
    if titulo not in livros:
        print("Livro não encontrado.\n")
        return

    livro = livros[titulo]
    if livro.copias == 0:
        print("Livro indisponível no momento.\n")
        return

    data_emprestimo = datetime.now()
    data_prevista = data_emprestimo + timedelta(days=7)

    print(f"\nExemplares disponíveis: {livro.copias}")
    print(f"Média das avaliações: {livro.estrelas_media()}")
    print(f"Prazo de devolução: {data_prevista.strftime('%d/%m/%Y')}")
    print("Atenção: a cada dia de atraso, aplica-se uma multa de R$ 2,00.\n")

    confirmar = input("Deseja confirmar o empréstimo? (s/n): ")
    if confirmar.lower() == 's':
        if livro.emprestar():
            chave = (id_usuario, titulo)
            emprestimos[chave] = {
                "data_emprestimo": data_emprestimo,
                "data_prevista": data_prevista,
                "data_devolucao": None,
                "multa": 0.0
            }
            salvar_emprestimos()
            salvar_livros(livros)
            print(f"\nLivro '{titulo}' emprestado com sucesso.")
            print(f"Data para devolução: {data_prevista.strftime('%d/%m/%Y')}\n")
        else:
            print("Não foi possível emprestar o livro.\n")
    else:
        print("Empréstimo cancelado.\n")

def devolver_livro():
    id_usuario = input("ID do usuário: ")
    titulo = input("Título do livro: ")

    chave = (id_usuario, titulo)
    if chave not in emprestimos:
        print("Empréstimo não encontrado.\n")
        return

    emprestimo = emprestimos[chave]
    if emprestimo["data_devolucao"]:
        print("Este livro já foi devolvido.\n")
        return

    data_devolucao = datetime.now()
    atraso = (data_devolucao - emprestimo["data_prevista"]).days
    multa = 0

    if atraso > 0:
        multa = atraso * 2.0
        print(f"Atenção: devolução com {atraso} dia(s) de atraso.")
        print(f"Multa aplicada: R$ {multa:.2f}\n")
    else:
        print("Devolução no prazo. Nenhuma multa aplicada.\n")

    emprestimo["data_devolucao"] = data_devolucao
    emprestimo["multa"] = multa

    if titulo in livros:
        livros[titulo].devolver()
        salvar_livros(livros)
    else:
        print("Aviso: livro não encontrado no sistema, mas empréstimo encerrado.\n")

    salvar_emprestimos()
    print(f"Livro '{titulo}' devolvido com sucesso!\n")

def cadastrar_livro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    ano = int(input("Ano: "))
    copias = int(input("Número de cópias: "))
    livros[titulo] = Livro(titulo, autor, ano, copias)
    salvar_livros(livros)
    print("Livro cadastrado com sucesso!\n")

def cadastrar_usuario():
    id_usuario = input("ID do usuário: ")
    nome = input("Nome: ")
    contato = input("Contato: ")
    usuarios[id_usuario] = Usuario(nome, id_usuario, contato)
    with open("usuarios.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([id_usuario, nome, contato])
    print("Usuário cadastrado com sucesso!\n")

def menu():
    carregar_livros()
    carregar_usuarios()
    carregar_emprestimos()

    while True:
        print("===== SISTEMA DE BIBLIOTECA =====")
        print("1. Cadastrar Livro")
        print("2. Cadastrar Usuário")
        print("3. Emprestar Livro")
        print("4. Devolver Livro")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_livro()
        elif opcao == "2":
            cadastrar_usuario()
        elif opcao == "3":
            emprestar_livro()
        elif opcao == "4":
            devolver_livro()
        elif opcao == "5":
            salvar_emprestimos()
            salvar_livros(livros)
            print("Encerrando sistema. Até logo!")
            break
        else:
            print("Opção inválida.\n")

if __name__ == "__main__":
    menu()
