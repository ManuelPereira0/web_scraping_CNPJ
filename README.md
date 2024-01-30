# Web Scraping Site de Certificado de Regularidade Cadastral de Entidades

## Programa que verifica se existe certificado de regularidade cadastral de entidades a partir do CNPJ: http://www.cadastrodeentidades.sp.gov.br/(S(qrx4mhzijjtzrt55mpsku445))/CertificadoPublico.aspx

# Passo a passo para utilizar o programa

## Configurar DB
> Atualizar as informações abaixo para o seu DB
```python
host='seu host',
user='seu user',
database='seu database',
password='sua password',
```

### No Linux
Bibliotecas para serem instaladas:
- instalar o pip: sudo apt-get install python3-pip
- pip install selenium 
- pip install pymysql 
- sudo apt update
- sudo apt install firefox 
> Somente se não tiver o FireFox instalado no computador

### No Windows
Para fazer a instalação da versão mais recente do Python no Windows: https://www.python.org/downloads/windows/
- pip install selenium 
- pip install pymysql 

### Para rodar o programa
> No Linux: python3 nome_do_arquivo.py <br>
> No Windows: python nome_do_arquivo.py