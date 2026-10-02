from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "mural-achados-perdidos-secret"
BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "achados_perdidos.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL CHECK(tipo IN ('Perdido', 'Encontrado')),
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            local TEXT NOT NULL,
            contato TEXT NOT NULL,
            resolvido INTEGER NOT NULL DEFAULT 0,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    filtro = request.args.get("filtro", "Todos")
    conn = get_db()

    if filtro in ("Perdidos", "Encontrados"):
        tipo = "Perdido" if filtro == "Perdidos" else "Encontrado"
        itens = conn.execute(
            "SELECT * FROM itens WHERE tipo = ? ORDER BY resolvido ASC, criado_em DESC",
            (tipo,)
        ).fetchall()
    else:
        filtro = "Todos"
        itens = conn.execute(
            "SELECT * FROM itens ORDER BY resolvido ASC, criado_em DESC"
        ).fetchall()

    conn.close()
    return render_template("index.html", itens=itens, filtro=filtro)


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        tipo = request.form.get("tipo", "").strip()
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()
        local = request.form.get("local", "").strip()
        contato = request.form.get("contato", "").strip()

        if tipo not in ("Perdido", "Encontrado"):
            flash("Selecione se o item foi perdido ou encontrado.", "erro")
            return render_template("cadastrar.html")

        if not all([nome, descricao, local, contato]):
            flash("Preencha todos os campos.", "erro")
            return render_template("cadastrar.html")

        conn = get_db()
        conn.execute(
            """
            INSERT INTO itens (tipo, nome, descricao, local, contato)
            VALUES (?, ?, ?, ?, ?)
            """,
            (tipo, nome, descricao, local, contato)
        )
        conn.commit()
        conn.close()

        flash("Item cadastrado com sucesso!", "sucesso")
        return redirect(url_for("index"))

    return render_template("cadastrar.html")


@app.post("/resolver/<int:item_id>")
def resolver(item_id):
    conn = get_db()
    conn.execute("UPDATE itens SET resolvido = 1 WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    flash("Item marcado como Devolvido/Resolvido.", "sucesso")
    return redirect(request.referrer or url_for("index"))


@app.post("/reabrir/<int:item_id>")
def reabrir(item_id):
    conn = get_db()
    conn.execute("UPDATE itens SET resolvido = 0 WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    flash("Item voltou para os itens ativos.", "sucesso")
    return redirect(request.referrer or url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
