🎭 Jogo do Impostor
O Jogo do Impostor é uma aplicação web interativa desenvolvida para transformar qualquer reunião de amigos em um desafio de dedução social. Inspirado em mecânicas de jogos clássicos, o app utiliza tecnologia web moderna para oferecer uma experiência fluida diretamente no navegador do celular.

🚀 Funcionalidades Principais
Gerenciamento Dinâmico de Jogadores: Adicione ou remova participantes de forma simples através da interface.

Inteligência de Temas: Algoritmo de sorteio que impede a repetição de palavras antes que todo o baralho seja utilizado.

Modo Personalizado: Liberdade para os jogadores inserirem seus próprios temas e palavras via interface.

Suporte Multi-Impostor: Configuração ajustável para partidas com 1 ou 2 impostores (mínimo de 7 jogadores para 2 impostores).

Persistência de Dados (localStorage): Nomes e configurações permanecem salvos mesmo se a página for atualizada, facilitando o início de novas rodadas.

Design Responsivo: Interface otimizada para dispositivos móveis com efeitos de Glassmorphism e transições suaves.

🛠️ Tecnologias Utilizadas
Backend: Flask (Python) para gerenciamento de rotas e lógica de jogo.

Frontend: HTML5 semântico e CSS3 com variáveis modernas para estilização.

Lógica de Cliente: JavaScript Vanilla para manipulação do DOM e persistência local.

⚙️ Como Executar o Projeto
Clone este repositório:

Bash

git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
cd NOME_DO_REPOSITORIO
Instale as dependências necessárias:

Bash

pip install flask
Inicie o servidor local:

Bash

python app.py
Acesse o jogo:

No computador: http://127.0.0.1:5000

No celular (Rede Local): O endereço IP específico para acesso via Wi-Fi será exibido no seu terminal ao iniciar o servidor.

📝 Regras do Jogo
O Segredo: Cada jogador deve clicar em seu nome para revelar seu papel em segredo e passar o celular adiante.

O Impostor: Enquanto a maioria recebe um Tema, o(s) impostor(es) recebem apenas a mensagem de que são os infiltrados.

A Discussão: O grupo debate para identificar contradições. O objetivo do grupo é encontrar o impostor; o do impostor é descobrir o tema ou sobreviver à votação.

A Revelação: Após a votação, a tela de revelação mostra o tema real e quem eram os impostores da rodada.

Desenvolvido para proporcionar diversão e integração entre amigos.
