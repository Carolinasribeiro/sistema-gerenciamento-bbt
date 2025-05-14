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
                data = datetime.strptime(row["data_devolucao"], "%Y-%m-%d")
                emprestimos[chave] = data
        print(f"{len(emprestimos)} empréstimos carregados.\n")
    else:
        print("Arquivo de empréstimos não encontrado. Criando novo.")

def salvar_emprestimos():
    with open("emprestimos.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id_usuario", "titulo", "data_devolucao"])
        for (id_usuario, titulo), data in emprestimos.items():
            writer.writerow([id_usuario, titulo, data.strftime("%Y-%m-%d")])

def cadastrar_livro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    ano = int(input("Ano: "))
    copias = int(input("Número de cópias: "))
    livros[titulo] = Livro(titulo, autor, ano, copias)
    with open("livros.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([titulo, autor, ano, copias])
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

def emprestar_livro():
    id_usuario = input("ID do usuário: ")
    if id_usuario not in usuarios:
        print("Usuário não encontrado.")
        return
    id
    titulo = input("Título do livro: ")
    if titulo not in livros:
        print("Livro não encontrado.\n")
        return
    livro = livros[titulo]
    if livro.copias == 0:
        print("Livro indisponível no momento.\n")
        return

    devolucao = datetime.now() + timedelta(days=7)
    print(f"\nExemplares disponíveis: {livro.copias}")
    print(f"Média das avaliações: {livro.estrelas_media()}")
    print(f"Prazo de devolução: {devolucao.strftime('%d/%m/%Y')}")
    print("Atenção: a cada dia de atraso, aplica-se uma multa de R$ 2,00.\n")
    confirmar = input("Deseja confirmar o empréstimo? (s/n): ")
    if confirmar.lower() == 's':
        if livro.emprestar():
            emprestimos[(id_usuario, titulo)] = devolucao
            print(f"\nLivro '{titulo}' emprestado com sucesso.")
            print(f"Data para devolução: {devolucao.strftime('%d/%m/%Y')}\n")
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
    devolucao_esperada = emprestimos.pop(chave)
    livro = livros[titulo]
    livro.devolver()
    atraso = (datetime.now() - devolucao_esperada).days
    if atraso > 0:
        multa = atraso * 2
        print(f"Livro devolvido com {atraso} dia(s) de atraso. Multa: R$ {multa:.2f}")
    else:
        print("Livro devolvido no prazo.")

    while True:
        try:
            nota = int(input("Avalie o livro de 1 a 5: "))
            if 1 <= nota <= 5:
                break
            else:
                print("Nota inválida. Digite entre 1 e 5.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro entre 1 e 5.")

    comentario = input("Deseja deixar um comentário? (Enter para pular): ")
    livro.adicionar_avaliacao(nota, comentario if comentario.strip() else None)
    print("Avaliação registrada.\n")

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
            print("Encerrando sistema. Até logo!")
            break
        else:
            print("Opção inválida.\n")

if __name__ == "__main__":
    menu()
