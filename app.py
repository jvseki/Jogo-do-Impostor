from flask import Flask, render_template, request, redirect, session
import random
import socket

app = Flask(__name__)
app.secret_key = "segredo_impostor"

PALAVRAS_PADRAO = [
    "Praia", "Escola", "Hospital", "Cinema", "Restaurante",
    "Aeroporto", "Shopping", "Estádio", "Parque", "Academia",
    "Hotel", "Ônibus", "Metrô", "Navio", "Ilha",
    "Floresta", "Deserto", "Montanha", "Cachoeira", "Caverna",
    "Fazenda", "Zoológico", "Museu", "Biblioteca", "Castelo",
    "Circo", "Teatro", "Delegacia", "Laboratório", "Universidade",
    "Navio Pirata", "Nave Espacial", "Cassino", "Submarino",
    "Ilha Deserta", "Base Militar", "Fábrica", "Usina",
    "Posto de Gasolina", "Padaria", "Mercado",
    "Quadra", "Piscina", "Parquinho",
    "Cemitério", "Praça", "Bunker"
]

def obter_palavra_unica():
    """
    Função auxiliar para pegar uma palavra sem repetir até acabar o estoque.
    """
    restantes = session.get("palavras_restantes", [])
    
    # Se não houver mais palavras ou se a lista não existir, recarrega tudo
    if not restantes:
        restantes = session["palavras"].copy()
    
    # Escolhe uma palavra aleatória das restantes
    palavra = random.choice(restantes)
    
    # Remove a palavra escolhida para não repetir na próxima
    restantes.remove(palavra)
    
    # Atualiza a sessão
    session["palavras_restantes"] = restantes
    
    return palavra

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/comecar", methods=["POST"])
def comecar():
    jogadores = request.form.getlist("jogadores")
    jogadores = [j.strip() for j in jogadores if j.strip()]

    if len(jogadores) < 3:
        return redirect("/")

    modo = request.form.get("modo")
    qtd_impostores = int(request.form.get("impostores"))

    if qtd_impostores == 2 and len(jogadores) < 7:
        return redirect("/")

    # Definição das palavras base
    if modo == "personalizado":
        temas = request.form.get("temas", "")
        palavras_base = [t.strip() for t in temas.split(",") if t.strip()]
        if not palavras_base:
            palavras_base = PALAVRAS_PADRAO.copy()
    else:
        palavras_base = PALAVRAS_PADRAO.copy()

    # Salva a lista MESTRE de palavras na sessão
    session["palavras"] = palavras_base
    # Limpa as restantes para forçar um recarregamento na função auxiliar
    session["palavras_restantes"] = [] 

    random.shuffle(jogadores)

    session["jogadores"] = jogadores
    session["modo"] = modo
    session["qtd_impostores"] = qtd_impostores
    session["indice"] = 0
    
    # Usa a função inteligente para pegar a palavra
    session["palavra"] = obter_palavra_unica()
    session["impostores"] = random.sample(jogadores, qtd_impostores)

    return redirect("/ver")

@app.route("/ver")
def ver():
    if "jogadores" not in session:
        return redirect("/")

    i = session["indice"]
    # Proteção caso o índice estoure (reload indevido)
    if i >= len(session["jogadores"]):
        return redirect("/discussao")

    jogador = session["jogadores"][i]

    if jogador in session["impostores"]:
        mensagem = "🕵️ Você é o IMPOSTOR"
    else:
        mensagem = f"🎯 Tema: {session['palavra']}"

    ultimo = i == len(session["jogadores"]) - 1

    return render_template("ver.html", jogador=jogador, mensagem=mensagem, ultimo=ultimo)

@app.route("/proximo")
def proximo():
    session["indice"] += 1
    return redirect("/ver")

@app.route("/discussao")
def discussao():
    return render_template("discussao.html")

@app.route("/revelar")
def revelar():
    return render_template(
        "revelar.html",
        impostores=", ".join(session["impostores"]),
        palavra=session["palavra"]
    )

@app.route("/recomecar")
def recomecar():
    jogadores = session["jogadores"]
    qtd = session["qtd_impostores"]

    # 1. EMBARALHAR A ORDEM DOS JOGADORES NOVAMENTE
    random.shuffle(jogadores)
    session["jogadores"] = jogadores

    session["indice"] = 0
    
    # 2. PEGAR PALAVRA NOVA SEM REPETIR (lógica do baralho)
    session["palavra"] = obter_palavra_unica()
    
    session["impostores"] = random.sample(jogadores, qtd)

    return redirect("/ver")

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    ip = get_ip()
    print(f"Acesse no celular: http://{ip}:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)