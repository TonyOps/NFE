import requests
import jwt

CNPJ = 'seu_cnpj'
CERTIFICATE = 'caminho_para_certificado.pfx'
PASSWORD = 'senha_do_certificado'
PRIVATE_KEY = 'caminho_para_chave_privada.key'
TOKEN_URL = 'https://api-erp-hom.fazenda.rj.gov.br/api/v1/autenticacao/oauth2/token'
API_URL = 'https://api-erp-hom.fazenda.rj.gov.br/api/v1/nfe'

def recuperar_nfe(chave_acesso):
    with open(PRIVATE_KEY, 'r') as key_file:
        private_key = key_file.read()
        token = jwt.encode(
            {'iss': CNPJ},
            private_key,
            algorithm='RS256'
        ).decode()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    payload = {
        'chaveAcesso': chave_acesso
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        cert=CERTIFICATE,
        password=PASSWORD
    )

    if response.status_code == 200:
        nfe = response.json()

        print(f'Chave de acesso: {nfe["chaveAcesso"]}')
        print(f'Número: {nfe["numero"]}')
        print(f'Data de emissão: {nfe["dataEmissao"]}')
        print(f'Valor total: R$ {nfe["valorTotal"]:.2f}')

        for produto in nfe['produtos']:
            print(f'Produto: {produto["descricao"]}')
            print(f'Quantidade: {produto["quantidade"]}')
            print(f'Valor unitário: R$ {produto["valorUnitario"]:.2f}')
            print(f'Valor total: R$ {produto["valorTotal"]:.2f}')
            print(f'Código do produto: {produto["codigo"]}')

    else:
        print(f'Erro ao recuperar NFe: {response.status_code} - {response.text}')