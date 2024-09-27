import time
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageTk  # Para carregar a imagem PNG como ícone
import subprocess
import sys

# Função para instalar pacotes
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Lista de pacotes necessários
required_packages = ['selenium']

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Instalando o pacote {package}...")
        install(package)

# Variável para controlar a execução do script
executando = False

# Função para iniciar o script em uma nova thread
def iniciar_script_thread():
    threading.Thread(target=iniciar_script).start()

# Função para iniciar o script
def iniciar_script():
    global executando
    executando = True
    
    link = entry_link.get()
    cpf = entry_cpf.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    confirmar_telefone = entry_confirmar_telefone.get()
    tempo = entry_tempo.get()

    if not all([link, cpf, email, telefone, confirmar_telefone, tempo]):
        messagebox.showwarning("Aviso", "Todos os campos precisam ser preenchidos!")
        return

    if telefone != confirmar_telefone:
        messagebox.showerror("Erro", "O telefone e a confirmação não coincidem!")
        return

    try:
        tempo = int(tempo)
    except ValueError:
        messagebox.showerror("Erro", "O campo Tempo deve ser um número válido!")
        return

    log_text.insert(tk.END, "Iniciando o processo...\n")
    log_text.update_idletasks()

    try:
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)  # Timeout de 10 segundos

        first_time = True  # Variável para controlar se é a primeira execução
        click_count = 1  # Inicializa o contador de cliques no botão "+10"

        while executando:
            try:
                # Passo 1: Acessa o link fornecido
                driver.get(link)
                log_text.insert(tk.END, "Acessando o link...\n")
                log_text.update_idletasks()

                # Passo 2: Clica no botão "+10" o número de vezes indicado por `click_count`
                for _ in range(click_count):
                    plus10_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '+ 10')]")))
                    plus10_button.click()
                    time.sleep(1)

                click_count += 1
                log_text.insert(tk.END, f"Clicando no botão '+10' {click_count} vezes...\n")
                log_text.update_idletasks()

                # Passo 3: Clica no botão "Comprar"
                comprar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='ticket-counter-purchase-button']")))
                comprar_button.click()
                log_text.insert(tk.END, "Clicando no botão 'Comprar'...\n")
                log_text.update_idletasks()

                if first_time:
                    # Preenche os inputs apenas na primeira execução
                    cpf_input = wait.until(EC.presence_of_element_located((By.ID, "raffle-checkout-cpf-input")))
                    cpf_input.clear()
                    cpf_input.send_keys(cpf)

                    email_input = wait.until(EC.presence_of_element_located((By.ID, "raffle-checkout-personal-data-social-email")))
                    email_input.clear()
                    email_input.send_keys(email)

                    telefone_input = wait.until(EC.presence_of_element_located((By.ID, "raffle-checkout-personal-data-social-phone")))
                    telefone_input.clear()
                    telefone_input.send_keys(telefone)

                    confirmar_telefone_input = wait.until(EC.presence_of_element_located((By.ID, "raffle-checkout-personal-data-social-confirm-phone")))
                    confirmar_telefone_input.clear()
                    confirmar_telefone_input.send_keys(telefone)

                    prosseguir_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div[1]/div[2]/div[2]/div/button")))
                    prosseguir_button.click()

                    log_text.insert(tk.END, "Preenchendo os dados e clicando em 'Prosseguir'...\n")
                    log_text.update_idletasks()

                    first_time = False

                confirmar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div[1]/div[2]/div/div[3]/div/div/div/div[2]/button/div")))
                confirmar_button.click()

                log_text.insert(tk.END, "Processo concluído com sucesso.\n")
                log_text.update_idletasks()

            except Exception as e:
                log_text.insert(tk.END, f"Ocorreu um erro: {e}\n")
                log_text.update_idletasks()

            # Pausa com base no tempo definido
            log_text.insert(tk.END, f"Aguardando {tempo} segundos para repetir o processo...\n")
            log_text.update_idletasks()
            time.sleep(tempo)

    except Exception as e:
        log_text.insert(tk.END, f"Erro ao iniciar o processo: {e}\n")
        log_text.update_idletasks()

# Função para interromper o script
def interromper_script():
    global executando
    executando = False
    log_text.insert(tk.END, "Processo interrompido pelo usuário.\n")
    log_text.update_idletasks()

# Interface gráfica com tkinter
root = tk.Tk()
root.title("Auto Compra")

# Trocar o ícone da janela com a imagem anexada
# icon_image = Image.open("./robot.png")  # Caminho da imagem enviada
# icon_photo = ImageTk.PhotoImage(icon_image)
# root.iconphoto(False, icon_photo)

# Configuração da interface
root.geometry("750x550")  # Ampliado para permitir mais espaço
root.configure(bg="black")
root.grid_columnconfigure(0, weight=1)

# Título
title_label = tk.Label(root, text="AUTO COMPRA", font=("Helvetica", 16), fg="green", bg="black")
title_label.pack(pady=10)

# Frame para inputs com padding
frame_inputs = tk.Frame(root, bg="black")
frame_inputs.pack(pady=10, padx=24)  # Padding de 24 horizontal

# Link
tk.Label(frame_inputs, text="Link", font=("Helvetica", 12), fg="green", bg="black").grid(row=0, column=0, sticky="e")
entry_link = tk.Entry(frame_inputs, width=40)
entry_link.grid(row=0, column=1, columnspan=3, sticky="ew", padx=24)

# CPF
tk.Label(frame_inputs, text="CPF", font=("Helvetica", 12), fg="green", bg="black").grid(row=1, column=0, sticky="e")
entry_cpf = tk.Entry(frame_inputs)
entry_cpf.grid(row=1, column=1, sticky="ew", padx=24)

# E-mail
tk.Label(frame_inputs, text="E-MAIL", font=("Helvetica", 12), fg="green", bg="black").grid(row=1, column=2, sticky="e")
entry_email = tk.Entry(frame_inputs)
entry_email.grid(row=1, column=3, sticky="ew", padx=24)

# Telefone
tk.Label(frame_inputs, text="Telefone", font=("Helvetica", 12), fg="green", bg="black").grid(row=2, column=0, sticky="e")
entry_telefone = tk.Entry(frame_inputs)
entry_telefone.grid(row=2, column=1, sticky="ew", padx=24)

# Confirmar Telefone
tk.Label(frame_inputs, text="Confirmar Telefone", font=("Helvetica", 12), fg="green", bg="black").grid(row=2, column=2, sticky="e")
entry_confirmar_telefone = tk.Entry(frame_inputs)
entry_confirmar_telefone.grid(row=2, column=3, sticky="ew", padx=24)

# Tempo (em segundos) para o loop
tk.Label(frame_inputs, text="Tempo (segundos)", font=("Helvetica", 12), fg="green", bg="black").grid(row=3, column=0, sticky="e")
entry_tempo = tk.Entry(frame_inputs)
entry_tempo.grid(row=3, column=1, sticky="ew", padx=24)

# Frame para os botões
frame_buttons = tk.Frame(root, bg="black")
frame_buttons.pack(pady=10, anchor='center')

# Botão OK
btn_ok = tk.Button(frame_buttons, text="OK", font=("Helvetica", 14), bg="white", command=iniciar_script_thread)
btn_ok.grid(row=0, column=0, padx=10)

# Botão Interromper
btn_interromper = tk.Button(frame_buttons, text="Interromper", font=("Helvetica", 14), bg="gray", command=interromper_script)
btn_interromper.grid(row=0, column=1, padx=10)

# Área de logs
log_text = scrolledtext.ScrolledText(root, width=60, height=10, bg="black", fg="green", font=("Helvetica", 10))
log_text.pack(pady=10, padx=24, anchor='center')  # Adicionado padding para centralizar adequadamente
log_text.insert(tk.END, "Logs do processo aparecerão aqui...\n")

# Centraliza todos os elementos da janela
for widget in frame_inputs.winfo_children():
    widget.grid_configure(padx=5, pady=5)

# Iniciar a interface gráfica
root.mainloop()
