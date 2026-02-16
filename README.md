




## Fazer o build do conteiner da ingestão de dados 


Certifique que o pc que vc fez o download do codigo tenha o docker instalado. 

Faz o build para que a imagem seja gerado no seu pc. Ou, utiliza a imagem disponivel no docker hub ()

```bash 
docker build -t api-datathon:v1.0.0 .
````

Para executar a run da imagem, executa o seguinte comando: 

```bash 
docker run -p 8008:8000 -d api-datathon:v1.0.0
```

Para verificar se o container subiu com sucesso, execute esse seguintes comandos:
```bash
docker ps | grep -i api-datathon
```
ou 
```web
http://localhost:8008/health
```


# Fazer manualmente a ingestão dos dados pela api:


### RAW
curl --location --request POST 'http://127.0.0.1:8008/ingestao/raw' --data ''

### TRUSTED
curl --location --request POST 'http://127.0.0.1:8008/ingestao/trusted' --data ''

### REFINED
curl --location --request POST 'http://127.0.0.1:8008/ingestao/refined' --data ''



