import psutil
import time
from plyer import notification
import platform
import subprocess
from datetime import datetime

def obter_processador():
    if platform.system() == "Windows":
        try:
            processador = subprocess.check_output("wmic cpu get caption", shell=True).decode().split("\n")[1].strip()
            return processador
        except Exception as e:
            return f"Erro ao obter processador: {str(e)}"
    elif platform.system() == "Linux":                                                                                                                                                  
        try:
            processador = subprocess.check_output("lscpu | grep 'Model name'", shell=True).decode().split(":")[1].strip()
            return processador
        except Exception as e:
            return f"Erro ao obter processador: {str(e)}"
    elif platform.system() == "Darwin":  # macOS
        try:
            processador = subprocess.check_output("sysctl -n machdep.cpu.brand_string", shell=True).decode().strip()
            return processador
        except Exception as e:
            return f"Erro ao obter processador: {str(e)}"
    else:
        return "Desconhecido"

def obter_uso_cpu():
    return psutil.cpu_percent(interval=1)

def obter_uso_memoria():
    memoria = psutil.virtual_memory()
    return memoria.percent

def obter_uso_disco():
    discos = psutil.disk_partitions()
    for disco in discos:
        if disco.device.lower().startswith("c:"):
            uso_disco = psutil.disk_usage(disco.mountpoint)
            return uso_disco.percent
    return None

def obter_uso_rede():
    redes = psutil.net_if_addrs()
    for interface, endereco in redes.items():
        if interface.lower().startswith("eth") or interface.lower().startswith("en"):
            estatisticas = psutil.net_if_stats().get(interface)
            if estatisticas and estatisticas.isup:
                return "Ativa"
            else:
                return "Desconectada"
    return "Sem Ethernet"

def exibir_notificacao_windows(uso_cpu, uso_memoria, uso_disco, uso_rede):
    mensagem = (
        f"Memória RAM: {uso_memoria}%\n"
        f"HD/SSD: {uso_disco}%\n"
        f"Rede: {uso_rede}\n"
        f"Uso da CPU: {uso_cpu}%"
    )
    print(f"Enviando notificação com os dados: {mensagem}")
    notification.notify(
        title="Desempenho do Sistema",
        message=mensagem,
        timeout=10 
    )


def registrar_em_arquivo(uso_cpu, uso_memoria, uso_disco, uso_rede):
   
    data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    mensagem_arquivo = (
        f"{data_hora_atual}\n| "
        f"Memoria RAM: {uso_memoria}%\n| "
        f"HD/SSD: {uso_disco}%\n| "
        f"Rede: {uso_rede}\n| "
        f"Uso da CPU: {uso_cpu}%\n "
        + "-"*40 + "\n"
    )
    
    with open("monitoramento_desempenho.txt", "a") as f:
        f.write(mensagem_arquivo)

def monitorar():
    iteracao = 0  
    while True:
        iteracao += 1
        print(f"Iniciando a iteração {iteracao}...") 

        start_time = time.time() 
        
        uso_cpu = obter_uso_cpu()
        uso_memoria = obter_uso_memoria()
        uso_disco = obter_uso_disco()
        uso_rede = obter_uso_rede()

        uso_disco = uso_disco if uso_disco else "Desconhecido"

        exibir_notificacao_windows(uso_cpu, uso_memoria, uso_disco, uso_rede)
        
        registrar_em_arquivo(uso_cpu, uso_memoria, uso_disco, uso_rede)
        
        end_time = time.time()
        iteration_duration = end_time - start_time
        print(f"Tempo de execução da iteração: {iteration_duration:.2f} segundos")
        
        print(f"Aguardando próximo monitoramento (1 hora)...")
        time.sleep(3600) 

if __name__ == "__main__":
    monitorar()
