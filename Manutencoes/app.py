from flask import Flask, request, render_template
# import no conector do banco de dados
import mysql.connector

app = Flask(__name__)

# ---------------------------------------------------------
# CONFIGURAÇÃO DO BANCO
# Substitua os valores abaixo pelos dados de conexão do banco.
# ---------------------------------------------------------
db_config = {
    "host": "",
    "port": 3306,
    "database": "u970229402_aulaweb",
    "user": "u970229402_alunosweb",
    "password": "Web$$2026"
}


# ---------------------------------------------------------
# ROTA INICIAL
# ---------------------------------------------------------
@app.route("/")
def home():
    return render_template("agenda.html")

# ---------------------------------------------------------
# CADASTRO
# Recebe os dados do formulário e grava no MySQL.
# ---------------------------------------------------------
@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    # 1. Recebe os dados enviados pelo formulário
    nome = request.form["nome"]
    apelido = request.form["apelido"]
    telefone = request.form["telefone"]

    # 2. Abre a conexão com o banco
    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()

    # 3. Prepara o INSERT
    sql = "INSERT INTO contato1 (nome, apelido, telefone) VALUES (%s, %s, %s)"

    valores = (nome, apelido, telefone)

    # 4. Executa o INSERT
    cursor.execute(sql, valores)

    # 5. Confirma a inclusão no banco
    conexao.commit()

    # 6. Fecha cursor e conexão
    cursor.close()
    conexao.close()

    # Resposta simples para o navegador
    return f"<h1>Contato cadastrado com sucesso!</h1><p>Nome: {nome}</p><p>Apelido: {apelido}</p><p>Telefone: {telefone}</p><p><a href='/'>Cadastrar outro contato</a></p><p><a href='/consultar'>Consultar contatos</a></p>"
 
# ---------------------------------------------------------
# CONSULTA
# Busca os contatos no MySQL e monta o HTML no próprio Python.
# ---------------------------------------------------------
@app.route("/consultar")
def consultar():

    # 1. Abre a conexão com o banco
    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()

    # 2. Executa o SELECT
    cursor.execute(
        "SELECT id, nome, apelido, telefone FROM contato1 ORDER BY id"
    )

    # 3. Recupera todas as linhas
    contatos = cursor.fetchall()

    # 4. Fecha cursor e conexão
    cursor.close()
    conexao.close()

    # 5. Monta uma resposta HTML 
    html = "<h1>Contatos cadastrados</h1>"

    if len(contatos) == 0:
        html += "<p>Nenhum contato cadastrado.</p>"
    else:
        for contato in contatos:
            html += f"""
                <p>
                    <strong>ID:</strong> {contato[0]}<br>
                    <strong>Nome:</strong> {contato[1]}<br>
                    <strong>Apelido:</strong> {contato[2]}<br>
                    <strong>Telefone:</strong> {contato[3]}
                </p>
                <hr>
            """

    html += '<p><a href="/">Voltar ao cadastro</a></p>'

    return html


# ---------------------------------------------------------
# EXECUÇÃO DA APLICAÇÃO
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
