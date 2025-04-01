import os #Módulo que permite interagir com o sistema operacional.
import requests #Faz as requisições HTTP para o servidor (site ANS).
import zipfile  #ZIP, usado para compactar os arquivos.
from bs4 import BeautifulSoup #Import do BeautifulSoup para analisar o documento HTML.
from urllib.parse import urljoin #Garante o acesso ao arquivo pois fornece URL absoluta, desde o caminho inicial de acesso a página até o local do arquivo.

# URL inicial da página da ANS.
URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Definição da pasta para salvar os arquivos baixados e nome do arquivo compactado.
DOWNLOAD_FOLDER = "downloads"
ZIP_FILENAME = "arquivos_comprimidos.zip"

# Criação da pasta de download se não existir, usando o módulo os.
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Função para baixar arquivos.
def download_file(url, folder): #definicao da funcao url e folder são os parâmetros fornecidos quando a função é chamada.
    # A linha `local_filename = os.path.join(folder, url.split("/")[-1])` cria o caminho completo do arquivo a ser salvo.
    # `url.split("/")` divide a URL em partes usando "/" como delimitador e `[-1]` pega o último item da lista, que é o nome do arquivo.
    # `os.path.join(folder, ...)` junta o nome do arquivo com o diretório fornecido, formando o caminho completo para salvar o arquivo.
    local_filename = os.path.join(folder, url.split("/")[-1]) 
    #faz uma requisição HTTP GET para a URL fornecida e, ao passar stream=True, indica que o conteúdo da resposta deve ser tratado de forma stream
    #(fluxo contínuo de dados).
    response = requests.get(url, stream=True)
    #Verifica se a resposta de status HTTP é 200
    if response.status_code == 200:
        with open(local_filename, "wb") as file: #Com a função open do Python abre um arquivo no modo de escrita binário
            for block in response.iter_content(1024): #Define que cada bloco será de 1024.
                file.write(block) #Escreve cada bloco por vez enquanto o proximo é baixado.
        print(f"Arquivo baixado: {local_filename}") #Print no terminal de que o arquivo foi baixado.
    return local_filename #Retorna o caminho completo até o arquivo pasta+nome_arquivo(usado na lista baixados-linha 54).

# Acesso a página e encontrar links de anexos.
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Busca por links <a>, que tenham conteúdo no href.
links = soup.find_all("a", href=True)

# Verificação dos links encontrados.
download_links = [] #Inicia uma lista vazia que irá armazenar os links que sigam os criterios definidos.
for link in links: #Percorre cada link na lista encontrada.
    href = link["href"] #Extrai o atributo href(url do link)
    # Verifica se o link termina com .pdf e se o texto do link contém as palavras chaves  "Anexo I" ou "Anexo II".
    if href.endswith((".pdf")) and any(keyword in link.get_text() for keyword in ["Anexo I", "Anexo II"]):
        full_url = urljoin(URL, href) #Une a URL inicial da pagina ao link relativo transformando em um link absoluto.
        download_links.append(full_url) #Adicionao link absoluto na lista download_links.
        if len(download_links) == 2:  # Verifica se já tem dois arquivos que cumpram os critérios acima e para de rodar o loop.
            break

#(List comprehension)iteração sobre cada link em 'download_links', chama a função 'download_file' passando o link e a pasta de destino, 
# e armazena o caminho dos arquivos baixados na lista 'baixados'(o return da funcao que traz esse dado.)
baixados = [download_file(link, DOWNLOAD_FOLDER) for link in download_links]

# Compactar os arquivos baixados em um .zip
zip_path = os.path.join(DOWNLOAD_FOLDER, ZIP_FILENAME) #Variavel que contém o caminho completo do arquivo, juntando o nome com a pasta de destino.
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf: #Cria um arquivo zipe no modo de escrita.
    for file in baixados: #Itera sobre cada arquivo na lista baixados.
        zipf.write(file, os.path.basename(file))  # Adiciona o arquivo ao ZIP aberto anteriormente

print(f"Arquivos comprimidos em {zip_path}")
