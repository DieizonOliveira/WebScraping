Web Scraping para Download e Compactação de Anexos I e II (ANS)
Este repositório contém um script Python que realiza o web scraping no site da Agência Nacional de Saúde Suplementar (ANS) para baixar e compactar os anexos I e II em formato PDF.

Descrição
O script realiza as seguintes etapas:

Acesso ao site: O código acessa a página de atualização do rol de procedimentos da ANS.

Download dos Anexos I e II: Ele localiza e faz o download dos arquivos em formato PDF dos anexos com base no nome do arquivo (Anexo I e Anexo II).

Compactação: Após o download, os arquivos são compactados em um único arquivo ZIP.

Requisitos
Antes de rodar o script, é necessário instalar as dependências. Para isso, você pode usar o requirements.txt.

Dependências
requests: Para realizar as requisições HTTP e baixar os arquivos.

beautifulsoup4: Para analisar o conteúdo HTML e extrair os links dos arquivos.

zipfile: Para compactar os arquivos PDF em um arquivo ZIP.

os: Para manipulação de arquivos e diretórios no sistema operacional.
