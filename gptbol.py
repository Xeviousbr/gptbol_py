# Compatível com Gptbol 1.8

import re
import os

log_messages = []
ocorreu_erro = False
log_file_path = os.path.join(os.getcwd(), "log.txt")

def log(mensagem):
    global ocorreu_erro
    log_messages.append(mensagem)
    print(mensagem)  

    with open(log_file_path, "a") as log_file:
        log_file.write(mensagem + "\n")
    if "Erro" in mensagem:
        ocorreu_erro = True

def remover_cdata(conteudo):
    if "<![CDATA[" in conteudo:
        return conteudo.replace("<![CDATA[", "").replace("]]>", "")
    return conteudo

def aplicar_alteracoes_gptbol(conteudo_gptbol):
    global ocorreu_erro
    arquivo = None
    linhas = None
    cursor_linha = 0

    regex_tag = re.compile(r'<(\w+)(.*?)>')
    
    for match in regex_tag.finditer(conteudo_gptbol):
        tag = match.group(1).lower()
        atributos = dict(re.findall(r'(\w+)=[\'"](.*?)[\'"]', match.group(2)))

        if tag == 'abr':
            arquivo = atributos.get('cam')
            if arquivo:
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        linhas = f.readlines()
                    cursor_linha = 0
                    log(f"Abrindo arquivo: {arquivo}")
                except FileNotFoundError:
                    log(f"Erro: Arquivo não encontrado - {arquivo}")
                    return
            else:
                log("Erro: Caminho do arquivo não especificado na tag <abr>")
                return

        elif tag == 'nav':
            if linhas is None:
                log("Erro: Nenhum arquivo foi aberto para navegação.")
                ocorreu_erro = True
                return
            
            tipo = atributos.get('tp')
            texto = atributos.get('texto')
            quantidade = int(atributos.get('qt', 1))
            if tipo == 'bus' and texto:
                encontrado = False
                texto_pattern = re.compile(re.escape(texto).replace(r"\ ", r"\s*"), re.IGNORECASE)
                for i in range(cursor_linha, len(linhas)):
                    if texto_pattern.search(linhas[i]):
                        cursor_linha = i
                        encontrado = True
                        log(f"Texto '{texto}' encontrado na linha {cursor_linha + 1}")
                        break
                if not encontrado:
                    log(f"Erro: Texto '{texto}' não encontrado.")
                    ocorreu_erro = True
            elif tipo == 'lin':
                direcao = atributos.get('dir', 'down').lower()
                if direcao == 'down':
                    cursor_linha = min(cursor_linha + quantidade, len(linhas) - 1)
                elif direcao == 'up':
                    cursor_linha = max(cursor_linha - quantidade, 0)
                log(f"Navegando {quantidade} linhas para {direcao}, linha atual: {cursor_linha}")

        elif tag == 'sub':
            if linhas is not None and 0 <= cursor_linha < len(linhas):
                antigo = atributos.get('old')
                novo = atributos.get('new')
                linha_alvo = cursor_linha

                pattern = re.compile(re.escape(antigo).replace(r"\ ", r"\s*"), re.IGNORECASE)
                linhas[linha_alvo], num_subs = pattern.subn(novo, linhas[linha_alvo])
                if num_subs > 0:
                    log(f"Substituído '{antigo}' por '{novo}' na linha {linha_alvo + 1}, {num_subs} ocorrências")
                else:
                    log(f"A expressão '{antigo}' não foi encontrada na linha {linha_alvo + 1}")

        elif tag == 'ins':
            conteudo_interno = remover_cdata(match.group(2))
            if conteudo_interno:
                linhas.insert(cursor_linha + 1, conteudo_interno + "\n")
                log(f"Conteúdo inserido após a linha {cursor_linha + 1}")
            else:
                log("Erro: Nenhum conteúdo fornecido para inserção.")
        
        elif tag == 'sav':
            if not ocorreu_erro and arquivo and linhas:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.writelines(linhas)
                log(f"Arquivo {arquivo} salvo com sucesso.")
            else:
                log(f"Erro ao salvar o arquivo {arquivo}")

def obter_gptbol_usuario():
    print("Digite o conteúdo gptbol abaixo. Pressione Enter duas vezes para finalizar:")
    conteudo_gptbol = []
    while True:
        linha = input()
        if linha == "":
            break
        conteudo_gptbol.append(linha)
    return "\n".join(conteudo_gptbol)

conteudo_gptbol_usuario = obter_gptbol_usuario()

aplicar_alteracoes_gptbol(conteudo_gptbol_usuario)
