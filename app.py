from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import random
import socket
import string

app = Flask(__name__)
app.secret_key = "segredo_impostor"
socketio = SocketIO(app, cors_allowed_origins="*")

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

# ==========================================
# LÓGICA DO MODO SOLO
# ==========================================

def obter_palavra_unica_solo():
    restantes = session.get("palavras_restantes", [])
    if not restantes:
        restantes = session.get("palavras", PALAVRAS_PADRAO).copy()
    palavra = random.choice(restantes)
    restantes.remove(palavra)
    session["palavras_restantes"] = restantes
    return palavra

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/comecar", methods=["POST"])
def comecar():
    jogadores = request.form.getlist("jogadores")
    jogadores = [j.strip() for j in jogadores if j.strip()]
    if len(jogadores) < 3: return redirect("/")
    
    modo = request.form.get("modo")
    qtd_impostores = int(request.form.get("impostores"))
    
    if modo == "personalizado":
        temas = request.form.get("temas", "")
        palavras_base = [t.strip() for t in temas.split(",") if t.strip()]
        if not palavras_base: palavras_base = PALAVRAS_PADRAO.copy()
    else:
        palavras_base = PALAVRAS_PADRAO.copy()

    session["palavras"] = palavras_base
    session["palavras_restantes"] = [] 
    random.shuffle(jogadores)
    session["jogadores"] = jogadores
    session["qtd_impostores"] = qtd_impostores
    session["indice"] = 0
    session["palavra"] = obter_palavra_unica_solo()
    session["impostores"] = random.sample(jogadores, qtd_impostores)
    return redirect("/ver")

@app.route("/ver")
def ver():
    if "jogadores" not in session: return redirect("/")
    i = session["indice"]
    if i >= len(session["jogadores"]): return redirect("/discussao")
    jogador = session["jogadores"][i]
    mensagem = "🕵️ Você é o IMPOSTOR" if jogador in session["impostores"] else f"🎯 Tema: {session['palavra']}"
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
    return render_template("revelar.html", impostores=", ".join(session["impostores"]), palavra=session["palavra"])

@app.route("/recomecar")
def recomecar():
    jogadores = session["jogadores"]
    random.shuffle(jogadores)
    session["jogadores"] = jogadores
    session["indice"] = 0
    session["palavra"] = obter_palavra_unica_solo()
    session["impostores"] = random.sample(jogadores, session["qtd_impostores"])
    return redirect("/ver")

# ==========================================
# LÓGICA DO MODO ONLINE
# ==========================================

salas = {}

def gerar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

@app.route("/online")
def online_page():
    return render_template("online.html")

def atualizar_lista(codigo):
    if codigo in salas:
        jogadores_nomes = list(salas[codigo]['jogadores'].values())
        dono_id = salas[codigo]['dono']
        emit('atualizar_jogadores', {
            'jogadores': jogadores_nomes, 
            'dono_id': dono_id
        }, to=codigo)

@socketio.on('criar_sala')
def on_create(data):
    nome = data['nome'].strip()
    codigo = gerar_codigo()
    salas[codigo] = {
        'jogadores': {request.sid: nome},
        'dono': request.sid,
        'deck_mestre': PALAVRAS_PADRAO.copy(),
        'deck_atual': PALAVRAS_PADRAO.copy(),
        'palavra_atual': '',
        'impostores': []
    }
    join_room(codigo)
    emit('sala_criada', {'codigo': codigo})
    atualizar_lista(codigo)

@socketio.on('entrar_sala')
def on_join(data):
    nome = data['nome'].strip()
    codigo = data['codigo'].upper()
    if codigo not in salas:
        emit('erro', 'SALA NÃO ENCONTRADA!')
        return
    if nome in salas[codigo]['jogadores'].values():
        emit('erro', 'NICK JÁ EM USO!')
        return
    
    salas[codigo]['jogadores'][request.sid] = nome
    join_room(codigo)
    emit('entrou_na_sala', {'codigo': codigo})
    atualizar_lista(codigo)

@socketio.on('iniciar_online')
def iniciar_online(data):
    codigo = data['codigo']
    if codigo not in salas: return
    sala = salas[codigo]
    if request.sid != sala['dono']: return
    
    ids = list(sala['jogadores'].keys())
    if len(ids) < 3:
        emit('erro', 'MÍNIMO 3 JOGADORES!')
        return

    # Lógica de Temas (Clássico vs Personalizado)
    if data.get('modo') == 'personalizado':
        novos_temas = [t.strip() for t in data.get('temas', '').split(',') if t.strip()]
        if novos_temas and sala['deck_mestre'] != novos_temas:
            sala['deck_mestre'] = novos_temas
            sala['deck_atual'] = novos_temas.copy()
    else:
        if sala['deck_mestre'] != PALAVRAS_PADRAO:
            sala['deck_mestre'] = PALAVRAS_PADRAO.copy()
            sala['deck_atual'] = PALAVRAS_PADRAO.copy()

    # Roleta sem repetição
    if not sala['deck_atual']:
        sala['deck_atual'] = sala['deck_mestre'].copy()
    
    palavra = random.choice(sala['deck_atual'])
    sala['deck_atual'].remove(palavra)
    sala['palavra_atual'] = palavra

    qtd = 2 if len(ids) >= 7 else 1
    impostores_ids = random.sample(ids, qtd)
    sala['impostores'] = [sala['jogadores'][i] for i in impostores_ids]
    quem_comeca = random.choice(list(sala['jogadores'].values()))

    for sid in ids:
        msg = "🕵️ VOCÊ É O IMPOSTOR" if sid in impostores_ids else f"🎯 TEMA: {palavra}"
        emit('receber_papel', {'msg': msg, 'quem_comeca': quem_comeca}, to=sid)

@socketio.on('finalizar_partida')
def finalizar(data):
    codigo = data['codigo']
    if codigo in salas and request.sid == salas[codigo]['dono']:
        sala = salas[codigo]
        emit('revelar_online', {'palavra': sala['palavra_atual'], 'impostores': sala['impostores']}, to=codigo)

@socketio.on('remover_jogador')
def remover(data):
    codigo = data['codigo']
    nome_alvo = data['nome_alvo']
    if codigo in salas and request.sid == salas[codigo]['dono']:
        sid_alvo = next((s for s, n in salas[codigo]['jogadores'].items() if n == nome_alvo), None)
        if sid_alvo:
            emit('expulso', to=sid_alvo)
            del salas[codigo]['jogadores'][sid_alvo]
            atualizar_lista(codigo)

@socketio.on('disconnect')
def on_disconnect():
    for codigo in list(salas.keys()):
        if request.sid in salas[codigo]['jogadores']:
            del salas[codigo]['jogadores'][request.sid]
            if not salas[codigo]['jogadores']:
                del salas[codigo]
            else:
                if salas[codigo]['dono'] == request.sid:
                    salas[codigo]['dono'] = list(salas[codigo]['jogadores'].keys())[0]
                atualizar_lista(codigo)
            break

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except: return "127.0.0.1"

if __name__ == "__main__":
    ip = get_ip()
    print(f"Acesse no Celular: http://{ip}:5000")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)