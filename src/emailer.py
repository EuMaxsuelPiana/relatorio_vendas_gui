# -*- coding: utf-8 -*-
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def enviar_email_com_anexo(smtp_server, smtp_port, remetente_email, remetente_senha, destinatario_email, assunto, corpo, arquivo_anexo):
    """Envia um e-mail com anexo usando SMTP."""
    
    mensagem = MIMEMultipart()
    mensagem["From"] = remetente_email# -*- coding: utf-8 -*-
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def enviar_email_com_anexo(smtp_server, smtp_port, remetente_email, remetente_senha, destinatario_email, assunto, corpo, arquivo_anexo):
    """Envia um e-mail com anexo usando SMTP."""
    
    mensagem = MIMEMultipart()
    mensagem["From"] = remetente_email
    mensagem["To"] = destinatario_email
    mensagem["Subject"] = assunto

    # Adicionar corpo do e-mail
    mensagem.attach(MIMEText(corpo, "plain"))

    # Adicionar anexo
    if arquivo_anexo and os.path.exists(arquivo_anexo):
        nome_arquivo = os.path.basename(arquivo_anexo)
        try:
            with open(arquivo_anexo, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {nome_arquivo}",
            )
            mensagem.attach(part)
        except Exception as e:
            raise Exception(f"Erro ao anexar o arquivo {nome_arquivo}: {e}")
    elif arquivo_anexo:
        raise FileNotFoundError(f"Arquivo de anexo não encontrado: {arquivo_anexo}")

    # Enviar o e-mail
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo() # Can be omitted
            server.starttls(context=context)
            server.ehlo() # Can be omitted
            server.login(remetente_email, remetente_senha)
            server.sendmail(remetente_email, destinatario_email, mensagem.as_string())
            print("E-mail enviado com sucesso!") # Log interno
    except smtplib.SMTPAuthenticationError:
        raise ConnectionRefusedError("Falha na autenticação SMTP. Verifique seu e-mail e senha.")
    except smtplib.SMTPConnectError:
        raise ConnectionRefusedError(f"Não foi possível conectar ao servidor SMTP {smtp_server}:{smtp_port}. Verifique o endereço e a porta.")
    except smtplib.SMTPServerDisconnected:
         raise ConnectionAbortedError("O servidor SMTP desconectou inesperadamente.")
    except socket.gaierror:
         raise ConnectionRefusedError(f"Não foi possível resolver o nome do servidor SMTP: {smtp_server}. Verifique o endereço.")
    except Exception as e:
        raise Exception(f"Ocorreu um erro ao enviar o e-mail: {e}")

# Exemplo de uso (para teste, se necessário)
if __name__ == "__main__":
    # Substitua com dados reais para teste
    # CUIDADO: Não comite senhas no código!
    smtp_server_teste = "smtp.gmail.com" # Ex: smtp.gmail.com ou smtp.office365.com
    smtp_port_teste = 587
    remetente_teste = "seu_email@gmail.com"
    senha_teste = "sua_senha_de_app" # Use senha de aplicativo se tiver 2FA
    destinatario_teste = "email_destino@exemplo.com"
    assunto_teste = "Teste de Envio de Relatório"
    corpo_teste = "Segue em anexo o relatório de vendas gerado pelo aplicativo."
    # Crie um arquivo dummy para teste
    arquivo_teste = "/home/ubuntu/relatorio_vendas_gui/output/teste.txt"
    with open(arquivo_teste, "w") as f:
        f.write("Este é um arquivo de teste.")
    
    try:
        print(f"Tentando enviar e-mail de {remetente_teste} para {destinatario_teste} via {smtp_server_teste}")
        enviar_email_com_anexo(
            smtp_server_teste,
            smtp_port_teste,
            remetente_teste,
            senha_teste,
            destinatario_teste,
            assunto_teste,
            corpo_teste,
            arquivo_teste
        )
        print("Teste de envio concluído (verifique a caixa de entrada e spam).")
    except Exception as e:
        print(f"Erro no teste de envio: {e}")
    finally:
        if os.path.exists(arquivo_teste):
            os.remove(arquivo_teste)

    mensagem["To"] = destinatario_email
    mensagem["Subject"] = assunto

    # Adicionar corpo do e-mail
    mensagem.attach(MIMEText(corpo, "plain"))

    # Adicionar anexo
    if arquivo_anexo and os.path.exists(arquivo_anexo):
        nome_arquivo = os.path.basename(arquivo_anexo)
        try:
            with open(arquivo_anexo, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {nome_arquivo}",
            )
            mensagem.attach(part)
        except Exception as e:
            raise Exception(f"Erro ao anexar o arquivo {nome_arquivo}: {e}")
    elif arquivo_anexo:
        raise FileNotFoundError(f"Arquivo de anexo não encontrado: {arquivo_anexo}")

    # Enviar o e-mail
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo() # Can be omitted
            server.starttls(context=context)
            server.ehlo() # Can be omitted
            server.login(remetente_email, remetente_senha)
            server.sendmail(remetente_email, destinatario_email, mensagem.as_string())
            print("E-mail enviado com sucesso!") # Log interno
    except smtplib.SMTPAuthenticationError:
        raise ConnectionRefusedError("Falha na autenticação SMTP. Verifique seu e-mail e senha.")
    except smtplib.SMTPConnectError:
        raise ConnectionRefusedError(f"Não foi possível conectar ao servidor SMTP {smtp_server}:{smtp_port}. Verifique o endereço e a porta.")
    except smtplib.SMTPServerDisconnected:
         raise ConnectionAbortedError("O servidor SMTP desconectou inesperadamente.")
    except socket.gaierror:
         raise ConnectionRefusedError(f"Não foi possível resolver o nome do servidor SMTP: {smtp_server}. Verifique o endereço.")
    except Exception as e:
        raise Exception(f"Ocorreu um erro ao enviar o e-mail: {e}")

# Exemplo de uso (para teste, se necessário)
if __name__ == "__main__":
    # Substitua com dados reais para teste
    # CUIDADO: Não comite senhas no código!
    smtp_server_teste = "smtp.gmail.com" # Ex: smtp.gmail.com ou smtp.office365.com
    smtp_port_teste = 587
    remetente_teste = "seu_email@gmail.com"
    senha_teste = "sua_senha_de_app" # Use senha de aplicativo se tiver 2FA
    destinatario_teste = "email_destino@exemplo.com"
    assunto_teste = "Teste de Envio de Relatório"
    corpo_teste = "Segue em anexo o relatório de vendas gerado pelo aplicativo."
    # Crie um arquivo dummy para teste
    arquivo_teste = "/home/ubuntu/relatorio_vendas_gui/output/teste.txt"
    with open(arquivo_teste, "w") as f:
        f.write("Este é um arquivo de teste.")
    
    try:
        print(f"Tentando enviar e-mail de {remetente_teste} para {destinatario_teste} via {smtp_server_teste}")
        enviar_email_com_anexo(
            smtp_server_teste,
            smtp_port_teste,
            remetente_teste,
            senha_teste,
            destinatario_teste,
            assunto_teste,
            corpo_teste,
            arquivo_teste
        )
        print("Teste de envio concluído (verifique a caixa de entrada e spam).")
    except Exception as e:
        print(f"Erro no teste de envio: {e}")
    finally:
        if os.path.exists(arquivo_teste):
            os.remove(arquivo_teste)
