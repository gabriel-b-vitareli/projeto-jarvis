# PROJETO JARVIS

## Feito com Python e Ollama e compatível com Windows, Linux e MacOS

## Sobre o Projeto:

JARVIS é uma IA hospeadada localmente no seu computador a partir do Ollama, que deve estar baixado no computador e precisa estar rodando para que o JARVIS funcione. Você pode baixar o Ollama por [aqui](https://ollama.com/download).

Ele é capaz de realizar diversas tarefas, entre elas:

- Pensar e responder as mensagens enviadas pelo usuário;
- Realizar cálculos médios e avançados (a precisão ainda não é perfeita);
- Criar e gerenciar diretórios e seus conteúdos (organizando-os, deletando arquivos e pastas desnecessários ou qualquer outro comando que o usuário dê);
- Abrir programas e páginas web pelo navegador (ele pode falhar ao tentar abrir programas, mas o acesso a páginas web está quase perfeito);
- Funciona offline (algumas funções podem não funcionar, mas o raciocínio básico é operacional mesmo sem acesso á internet);
- Funciona sem limites de tokens;
- Tem memória dinâmica (costuma falhar), ou seja, é capaz de pensar sozinho se vale a pena ou não salvar algo na memória dele, assim fazendo-o ou não (pode salvar de forma forçada caso o usuário mande ele fazer isso);


Futuramente, ele deve receber as seguintes funcionalidades:

- Voz offline TTS (Text-To-Speech);
- Avanços e melhorias nos seus sistemas já existentes;
- Capacidade de reconhecer fala e câmera;
- Memória avançada, para impedir que ele esqueça de coisas importantes com o tempo;
- Velocidade maior de resposta;
- Entre outras;

Você pode iniciar o JARVIS ao abrir um terminal na pasta onbde todos seus arquivos e subpastas estão localizados e então digitar:

python jarvis.py

Digite "sair" (sem aspas) para fechar o JARVIS.
Cuidado para:
- Não fornecer informações pessoais de mais;
- Não passar comandos para ele realizar que não sejam seguros (por exemplo, deletar a pasta system32), já que ele o realizará sem questionar;
- Evite perguntas existenciais ou solicitar que ele se desligue (por experiência própria);
