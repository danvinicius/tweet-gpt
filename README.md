# tweet-gpt
Chatbot integrado com o ChatGPT para comentar tweets dado um assunto ou tag específica do Twitter. O projeto faz parte do trabalho final da disciplina Sistemas Web 3.

## Como rodar

1. Abra o terminal e clone o projeto
```bash
git clone https://github.com/danvinicius/tweet-gpt.git
```
##
2. Instale as dependências da API
```bash
pip install flask
pip install flask_script==2.0.5
pip install flask_cors
```
##
3. Crie o arquivo .env na raiz da API para adicionar as variáveis de ambiente
```bash .env
# autenticação do ChatGPT
GPT_TOKEN=<seu token>

# autenticação do twitter
consumer_key=<sua chave>
consumer_secret=<seu consumer secret>
access_token=<seu token>
access_token_secret=<seu token secret>

# jwt e banco
JWT_SECRET=<seu jwt secret>
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=123456
DB_NAME=tweet_gpt
```
##
4. Rode a API
```bash
py run.py runserver
```
##
5. Na pasta cliente, instale as dependências com o NPM ou YARN
```bash
npm install
# ou
yarn install
```
##
6. Faça o build do Typescript
```bash
npm run build
# ou
yarn build
```
##
7. Rode o cliente com o **Live Server** ou acessando a página **login.html**
##
#### Feito por [Daniel Vinicius](https://github.com/danvinicius) e [Cássia Mariane](https://github.com/cassiamariane)


