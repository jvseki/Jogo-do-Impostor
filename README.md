# 🎭 Jogo do Impostor
O Jogo do Impostor é uma aplicação web interativa desenvolvida para transformar qualquer reunião de amigos em um desafio de dedução social. Inspirado em mecânicas de jogos clássicos, o app utiliza tecnologia web moderna para oferecer uma experiência fluida diretamente no navegador do celular.

# 🚀 Funcionalidades Principais
Gerenciamento Dinâmico de Jogadores: Adicione ou remova participantes de forma simples através da interface.

Inteligência de Temas: Algoritmo de sorteio que impede a repetição de palavras antes que todo o baralho seja utilizado.

Modo Personalizado: Liberdade para os jogadores inserirem seus próprios temas e palavras via interface.

Suporte Multi-Impostor: Configuração ajustável para partidas com 1 ou 2 impostores (mínimo de 7 jogadores para 2 impostores).

Persistência de Dados (localStorage): Nomes e configurações permanecem salvos mesmo se a página for atualizada, facilitando o início de novas rodadas.

Design Responsivo: Interface otimizada para dispositivos móveis com efeitos de Glassmorphism.

# 🛠️ Tecnologias Utilizadas
Backend: Flask (Python) para gerenciamento de rotas e lógica de jogo.

Frontend: HTML5 semântico e CSS3 com variáveis modernas.

Lógica de Cliente: JavaScript Vanilla para manipulação do DOM e persistência local via localStorage.

# ⚙️ Instalação e Execução Local
Clone este repositório:

Bash

git clone https://github.com/jvseki/Jogo-do-impostor.git
cd Jogo-do-impostor
Instale o Flask:

Bash

pip install flask
Inicie o servidor:

Bash

python app.py
# 🌐 Como Jogar com Amigos (Acesso Externo)
Para disponibilizar o jogo para pessoas fora da sua rede Wi-Fi, este projeto foi testado com duas abordagens:

# ⚡ Teste Rápido (ngrok)
Ideal para partidas imediatas onde o servidor roda do seu computador:

Com o Flask ativo, execute: ngrok http 5000.

O ngrok criará um túnel seguro fornecendo uma URL temporária https.

Compartilhe o link gerado para que seus amigos acessem pelo 4G/5G.

# ☁️ Hospedagem Permanente (PythonAnywhere)
Para manter o jogo online 24h sem depender do seu computador ligado:

O projeto é totalmente compatível com o PythonAnywhere.

Basta realizar o upload dos arquivos, configurar o ambiente virtual Flask e recarregar o Web App para ter seu próprio domínio jvseki.pythonanywhere.com.

# 📝 Regras do Jogo
Distribuição: Cada jogador deve clicar em seu nome para revelar seu papel em segredo e passar o celular adiante.

O Impostor: Enquanto a maioria recebe um Tema, o(s) impostor(es) recebem apenas a mensagem de que são os infiltrados.

Discussão: O grupo debate para identificar contradições. O objetivo do grupo é encontrar o impostor; o do impostor é descobrir o tema ou sobreviver à votação.

Revelação: Após a votação, a tela de revelação mostra o tema real e quem eram os impostores da rodada.

Desenvolvido por jvseki para proporcionar diversão e integração entre amigos.
