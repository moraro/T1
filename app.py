from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

usuarios = [
    {"id": 1, "nome": "Usuário 1", "email": "user1@example.com", "celular": "1234567890",
     "data_nascimento": "1990-01-01", "cpf": "111.111.111-11", "nivel": "Usuário"},
    {"id": 2, "nome": "Usuário 2", "email": "user2@example.com", "celular": "9876543210",
     "data_nascimento": "1985-05-10", "cpf": "222.222.222-22", "nivel": "Administrador"},
]

filmes = [
    {"id": 1, "titulo": "Nebulosa Escarlate", "genero": "Ficção Científica", "ano": 2023, "duracao": 128},
    {"id": 2, "titulo": "Réquiem de Verão", "genero": "Drama", "ano": 2021, "duracao": 104},
]

categorias = [
    {"id": 1, "nome": "Ficção Científica", "descricao": "Histórias envolvendo tecnologia e futuro."},
    {"id": 2, "nome": "Drama", "descricao": "Narrativas centradas em conflitos humanos."},
]


def proximo_id_usuario():
    if len(usuarios) == 0:
        return 1
    maior_id = usuarios[0]["id"]
    for usuario in usuarios:
        if usuario["id"] > maior_id:
            maior_id = usuario["id"]
    return maior_id + 1


def proximo_id_filme():
    if len(filmes) == 0:
        return 1
    maior_id = filmes[0]["id"]
    for filme in filmes:
        if filme["id"] > maior_id:
            maior_id = filme["id"]
    return maior_id + 1


def proximo_id_categoria():
    if len(categorias) == 0:
        return 1
    maior_id = categorias[0]["id"]
    for categoria in categorias:
        if categoria["id"] > maior_id:
            maior_id = categoria["id"]
    return maior_id + 1


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Aqui entraria a validação real de e-mail/senha.
        return redirect(url_for("listar_usuarios"))
    return render_template("login.html")

@app.route("/usuarios")
def listar_usuarios():
    return render_template("usuarios_listar.html", usuarios=usuarios)


@app.route("/usuarios/cadastrar", methods=["GET", "POST"])
def cadastrar_usuario():
    erros = []
    sucesso = False

    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        celular = request.form["celular"].strip()
        data_nascimento = request.form["data_nascimento"].strip()
        cpf = request.form["cpf"].strip()
        nivel = request.form["nivel"].strip()

        if nome == "":
            erros.append("O campo Nome é obrigatório.")
        elif len(nome) < 3:
            erros.append("O Nome deve ter pelo menos 3 letras.")

        if email == "" or "@" not in email:
            erros.append("Informe um e-mail válido.")

        if cpf == "":
            erros.append("O campo CPF é obrigatório.")

        if nivel == "":
            erros.append("Escolha o Nível de Acesso.")

        if len(erros) == 0:
            novo_usuario = {
                "id": proximo_id_usuario(),
                "nome": nome,
                "email": email,
                "celular": celular,
                "data_nascimento": data_nascimento,
                "cpf": cpf,
                "nivel": nivel,
            }
            usuarios.append(novo_usuario)
            sucesso = True

    return render_template("usuarios_cadastro.html", erros=erros, sucesso=sucesso)


@app.route("/usuarios/excluir/<int:usuario_id>")
def excluir_usuario(usuario_id):
    global usuarios
    usuarios = [u for u in usuarios if u["id"] != usuario_id]
    return redirect(url_for("listar_usuarios"))



@app.route("/filmes")
def listar_filmes():
    return render_template("filmes_listar.html", filmes=filmes)


@app.route("/filmes/cadastrar", methods=["GET", "POST"])
def cadastrar_filme():
    erros = []
    sucesso = False

    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        genero = request.form["genero"].strip()
        ano_texto = request.form["ano"].strip()
        duracao_texto = request.form["duracao"].strip()

        if titulo == "":
            erros.append("O campo Título é obrigatório.")

        if genero == "":
            erros.append("Escolha um Gênero.")
        ano = 0
        if ano_texto == "":
            erros.append("O campo Ano de Lançamento é obrigatório.")
        elif not ano_texto.isdigit():
            erros.append("O Ano de Lançamento deve ser um número.")
        else:
            ano = int(ano_texto)
            if ano < 1900 or ano > 2100:
                erros.append("O Ano de Lançamento deve estar entre 1900 e 2100.")

        duracao = 0
        if duracao_texto == "":
            erros.append("O campo Duração é obrigatório.")
        elif not duracao_texto.isdigit():
            erros.append("A Duração deve ser um número.")
        else:
            duracao = int(duracao_texto)
            if duracao <= 0:
                erros.append("A Duração deve ser maior que 0.")

        if len(erros) == 0:
            novo_filme = {
                "id": proximo_id_filme(),
                "titulo": titulo,
                "genero": genero,
                "ano": ano,
                "duracao": duracao,
            }
            filmes.append(novo_filme)
            sucesso = True

    return render_template("filmes_cadastro.html", erros=erros, sucesso=sucesso, categorias=categorias)


@app.route("/filmes/excluir/<int:filme_id>")
def excluir_filme(filme_id):
    global filmes
    filmes = [f for f in filmes if f["id"] != filme_id]
    return redirect(url_for("listar_filmes"))




@app.route("/categorias")
def listar_categorias():
    return render_template("categorias_listar.html", categorias=categorias)


@app.route("/categorias/cadastrar", methods=["GET", "POST"])
def cadastrar_categoria():
    erros = []
    sucesso = False

    if request.method == "POST":
        nome = request.form["nome"].strip()
        descricao = request.form["descricao"].strip()

        if nome == "":
            erros.append("O campo Nome é obrigatório.")

        if descricao == "":
            erros.append("O campo Descrição é obrigatório.")

        if len(erros) == 0:
            nova_categoria = {
                "id": proximo_id_categoria(),
                "nome": nome,
                "descricao": descricao,
            }
            categorias.append(nova_categoria)
            sucesso = True

    return render_template("categorias_cadastro.html", erros=erros, sucesso=sucesso)


@app.route("/categorias/excluir/<int:categoria_id>")
def excluir_categoria(categoria_id):
    global categorias
    categorias = [c for c in categorias if c["id"] != categoria_id]
    return redirect(url_for("listar_categorias"))


if __name__ == "__main__":
    app.run(debug=True)
