from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from urllib3.exceptions import MaxRetryError, NewConnectionError
import pymysql.cursors
import datetime

def criar_conexao():
    return pymysql.connect(
        host='seu host',
        user='seu user',
        database='seu database',
        password='sua password',
        cursorclass=pymysql.cursors.DictCursor
    )

def iniciar_driver():
    driver = webdriver.Firefox()
    driver.get("http://www.cadastrodeentidades.sp.gov.br/(S(qrx4mhzijjtzrt55mpsku445))/CertificadoPublico.aspx")
    return driver

conexao = criar_conexao()

c = 1
registro = 1
contador_cnpj = 0

driver = iniciar_driver()

while True:
    cursor = conexao.cursor()
    try:
        comando =("SELECT (sua coluna) FROM (seu DB) WHERE status is null LIMIT 1000")
        cursor.execute(comando)

        CNPJ = cursor.fetchone()
        if CNPJ is None:
            break

        while CNPJ:
            cnpj = CNPJ['cnpj']

            data_hora_atual = datetime.datetime.now()
            data_hora_formada = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')
            print(f'{cnpj} , {data_hora_formada} , Registro Nº{registro}, Nº{c}')

            try:
                input_cnpj = driver.find_element(By.ID, 'txtLogin_txtCNPJ')
                input_cnpj.send_keys(cnpj)
            except NoSuchElementException:
                driver.quit()
                driver = iniciar_driver()

            sleep(0.2)

            try:    
                botao = driver.find_element(By.ID, 'btnAcessar')
                sleep(0.2)
                botao.click()
            except:
                driver.quit()
                driver = iniciar_driver()
            c += 1

            sleep(0.7)
            window_handles = driver.window_handles

            if len(window_handles) > 1:
                driver.switch_to.window(window_handles[1])
                sleep(1)

                # Obter a URL da nova aba
                nova_janela_url = driver.current_url
                atualizar = f'UPDATE (seu DB) SET status = "{nova_janela_url}" WHERE cnpj = "{cnpj}"'
                cursor.execute(atualizar)
                conexao.commit() 
                
                # Fechar a nova aba
                driver.close()

                # Alternar de volta para a aba original
                driver.switch_to.window(window_handles[0])
                # Encerre o driver após concluir
            else:
                msg = driver.find_element(By.ID, "lblErro")
                atualizar = f'UPDATE (seu DB)J SET status = "{msg.text}" WHERE cnpj = "{cnpj}"'
                cursor.execute(atualizar)
                conexao.commit() 
            
            contador_cnpj += 1  # Incrementa o contador de CEPs processados

            if contador_cnpj == 100:
                # Fechar todas as abas sobresalentes
                for handle in driver.window_handles[1:]:
                    driver.switch_to.window(handle)
                    driver.close()
                driver.switch_to.window(driver.window_handles[0])
                
                driver.quit()
                contador_cnpj = 0
                driver = iniciar_driver()

            CNPJ = cursor.fetchone()

    except pymysql.err.OperationalError as e:

        if e.args[0] == 2013:
            print("Conexão perdida. Reconectando.")
            conexao = criar_conexao()
            cursor = conexao.cursor()
        else:
            raise

    except MaxRetryError as e:
        print(f"Erro MaxRetryError: {e}")
        driver.quit()
        sleep(3)
        driver = iniciar_driver()
    
    except NewConnectionError as e:
        print(f"Erro NewConnectionError: {e}")
        driver.quit()
        sleep(3)
        driver = iniciar_driver()
        
    except NoSuchElementException:
        driver.quit()
        driver = iniciar_driver()

    finally:
        registro += 1 

driver.quit()

