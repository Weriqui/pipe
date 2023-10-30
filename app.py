from flask import Flask, request, jsonify
import datetime
import pytz
import json
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

produto = {19:"TAX SN",
    27:"Redução Parcelamentos",
    52:"Transação PF",
    20:"Transação Individual",
    21:"COP",
    22:"PSF",
    23:"SCORE",
    24:"HOLDING",
    63:"TAX parcelamentos",
    25:"LAUDO",
    26:"RB",
    44:"MS",
    45:"AUDITORIA",
    49:"TAX - LP",
    50:"TAX - LR",
    66:"SN Dívida Ativa",
    67:"PRF (Débitos ajuizados PJ)",
    69:"ALIQUOTA ZERO",
    70:"PERSE HT",
    71:"MS SN",
    72:"Redução PERT PJ",
    73:"Redução PERT PF",
    74:"Termo exclusão PERT",
    75:"Redução PERT (Clientes VBB)",
    77:"PNV (Venda de franquia)",
    79:"Redução de parcelamento (clientes VBB)",
    80:"PRF PF (CDAS Recentes)",
    81:"TAX LR DIVIDA (supermercado)",
    82:"TAX LR DIVIDA (construtora)",
    83:"TAX LR DIVIDA (transportadora)",
    90:"PS CORP"
}

def notas(mensagem, idleed, org_id, idpessoa):
    token = "fb1912394dd41792e43c0b2d71a40d4e9dccf6ac"
    url = f"https://api.pipedrive.com/v1/notes?api_token={token}"
    # Obtém a data e hora atual no fuso horário UTC
    data_hora_atual = datetime.datetime.utcnow()

    # Converte para o fuso horário de Brasília
    fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')
    data_hora_brasilia = data_hora_atual.astimezone(fuso_horario_brasilia)

    # Formata a data e hora no formato desejado
    ano = data_hora_brasilia.year
    mes = f'{data_hora_brasilia.month:02}'
    dia = f'{data_hora_brasilia.day:02}'
    hora = f'{data_hora_brasilia.hour:02}'
    minuto = f'{data_hora_brasilia.minute:02}'
    segundo = f'{data_hora_brasilia.second:02}'

    time = f'{ano}-{mes}-{dia} {hora}:{minuto}:{segundo}'

    payload = json.dumps({
      "content": mensagem,
      "lead_id": idleed,
      "deal_id": None,
      "person_id": idpessoa,
      "org_id": org_id,
      "user_id": 14172500,
      "add_time": time,
      "pinned_to_lead_flag": False,
      "pinned_to_deal_flag": False,
      "pinned_to_organization_flag": False,
      "pinned_to_person_flag": False
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Cookie': '__cf_bm=CAiYJCxsk1AokQ7mboRh2nItjrbctRPLu.86OF1yzbo-1691006853-0-AYTlsOZQdgqHzYgQjvm1UfMhltGX5VHAF3cNfOjanC9jLn178YZNp1C1Ho1UkggDrAsxzCgpw5plOCXSJH+YeYQ='
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code

def etiquetaPessoa(idpessoa, responsavel, marcacao=None):
    token = "fb1912394dd41792e43c0b2d71a40d4e9dccf6ac"
    url = f"https://api.pipedrive.com/v1/persons/{idpessoa}?api_token={token}"

    if marcacao == None:
        payload = json.dumps({
        "2f006f9e3261b17e2026b52e0e67db917ff748f0":responsavel
        })
    
    else:
        payload = json.dumps({
        "cb6c573810116f88e186b47c471deee0d35c943d": marcacao,
        "2f006f9e3261b17e2026b52e0e67db917ff748f0":responsavel
        })
        
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Cookie': '__cf_bm=mwaEfBL5dCRFDH_Va5F.g5HnBgcxfnXBs8W0uMbDZfA-1692302746-0-AQqPMtPgjnzg69VR5jkBdls2FLLU2CdS7ljogouSyBFmxEqoCcd54t8Jz//69tVGrQB9GbIG0iRReozw31ePtDU='
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    
    return response.status_code

def pesquisa(numero):
    token = token = "fb1912394dd41792e43c0b2d71a40d4e9dccf6ac"
    url = f"https://api.pipedrive.com/v1/persons/search?term={numero}&start=0&api_token={token}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'Cookie': '__cf_bm=7cyLDhVPC4pJqVp0V1cvJDU4n4lk2sAAzD7Ro.I8IW4-1697220861-0-AU0FSheWG7gjnOPcuudNkxQr2tNhxACLASFsWV1byPiZGGZrltezMyGJ3g4UUM+cqvKSB2tcD16Pgbn+fx+oLx8='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    pessoa = dict(response.json())
    if len(pessoa['data']['items']) == 1:
        individuo = pessoa['data']['items'][0]['item']
        individuo = {'id':individuo['id'],
                    'nome':individuo['name'],
                    'telefone':individuo['phones'][0],
                    'organizacao':individuo['organization']['name'],
                    'endereco':individuo['organization']['address'],
                    'id_empresa':individuo['organization']['id']}

        url = f"https://api.pipedrive.com/v1/organizations/{individuo['id_empresa']}?api_token={token}"

        payload = {}
        headers = {
        'Accept': 'application/json',
        'Cookie': '__cf_bm=PmfPrtl8xejVtaER3jbS8TCHTSrmHGPZ_ynM81ZgUQg-1697465664-0-AVvtK3GOWRk3qhyh6WiDc2P7VqJavqwk8inofCtWi/nwQT/z80eX4bsJSxbASVsttwYOrUkbZoNveSKSljcM2bo='
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        cnpj = {'cnpj':response.json()['data']["c1dffa1d3f6d26c2472b9d6b075032089b3b0805"]}

        titulo = individuo['organizacao']
        idpessoa = individuo['id']
        url = f"https://api.pipedrive.com/v1/leads/search?term={titulo}&person_id={idpessoa}&api_token={token}"

        payload = {}
        headers = {
        'Accept': 'application/json',
        'Cookie': '__cf_bm=.AgbIrUtSlchrpHOILp0Op5MGTvuhikoj_nAKhHwtlE-1690918724-0-AaHrU1qeXEyxII/EY6AR+tenwEcLbIkBI6RfpFMRPBz7PGrLUrgHsqZzyIjgsnPc4YqeeDqHOzx54dFKaDVoAmU='
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        idleed = response.json()['data']['items'][0]['item']['id']

        url = f"https://api.pipedrive.com/v1/leads/{idleed}?api_token={token}"

        payload = {}
        headers = {
        'Accept': 'application/json',
        'Cookie': '__cf_bm=FS_X2E03_FRS_ql23cFstNVOofVeJpTbpio7I_G5MB8-1690919637-0-AX0+l9jLFOb6zVxLB4t2ELbA8ZojlpaCK2iUkVgedQyui69EM+H8FxwzExsXBayhGcyrIWoIAYKyO6A/EBZIueQ='
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        lead = dict(response.json())
        lead = {'titulo-lead':lead['data']['title'], 'produto':produto[int(lead['data']['5fca6336de210f847b78ce5fd7de950530e26e94'])]}

        url = f"https://api.pipedrive.com/v1/persons/{idpessoa}?api_token=fb1912394dd41792e43c0b2d71a40d4e9dccf6ac"

        payload = {}
        headers = {
        'Accept': 'application/json',
        'Cookie': '__cf_bm=ZGT4Uo6DRvnIXkY4kuiBTz6O11CZY42KIrsz1xfmmWc-1697222543-0-AXKnpEEKpL3drX3iLmaK/2ZZ+d03HCAKmdSn2lpc2aM55dsHsQcbTFdK43ajcU6TQPDXSedbE3QHGzCNyQCTQzI='
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        contato ={'tipo-contato':response.json()['data']['cb6c573810116f88e186b47c471deee0d35c943d'] if response.json()['data']['cb6c573810116f88e186b47c471deee0d35c943d'] in ["30","29","28","31"] else "00"} 
        lead.update(individuo)
        lead.update(contato)
        lead.update(cnpj)
        lead.update({'id_lead':idleed})
        return lead
    
    elif len(pessoa['data']['items']) > 1:
      for i in range(len(pessoa['data']['items'])):
        individuo = pessoa['data']['items'][i]['item']
        individuo = {
            'id':individuo['id'],
            'nome':individuo['name'],
            'telefone':individuo['phones'][0],
            'organizacao':individuo['organization']['name'],
            'endereco':individuo['organization']['address'],
            'id_empresa':individuo['organization']['id']
        }
        url = f"https://api.pipedrive.com/v1/organizations/{individuo['id_empresa']}?api_token={token}"

        payload = {}
        headers = {
        'Accept': 'application/json',
        'Cookie': '__cf_bm=PmfPrtl8xejVtaER3jbS8TCHTSrmHGPZ_ynM81ZgUQg-1697465664-0-AVvtK3GOWRk3qhyh6WiDc2P7VqJavqwk8inofCtWi/nwQT/z80eX4bsJSxbASVsttwYOrUkbZoNveSKSljcM2bo='
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        cnpj = {'cnpj':response.json()['data']["c1dffa1d3f6d26c2472b9d6b075032089b3b0805"]}

        titulo = individuo['organizacao']
        idpessoa = individuo['id']
        url = f"https://api.pipedrive.com/v1/leads/search?term={titulo}&person_id={idpessoa}&api_token={token}"

        payload = {}
        headers = {
        'Accept': 'application/json',
        'Cookie': '__cf_bm=.AgbIrUtSlchrpHOILp0Op5MGTvuhikoj_nAKhHwtlE-1690918724-0-AaHrU1qeXEyxII/EY6AR+tenwEcLbIkBI6RfpFMRPBz7PGrLUrgHsqZzyIjgsnPc4YqeeDqHOzx54dFKaDVoAmU='
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if len(response.json()['data']['items']) > 0:
          idleed = response.json()['data']['items'][0]['item']['id']

          url = f"https://api.pipedrive.com/v1/leads/{idleed}?api_token={token}"

          payload = {}
          headers = {
          'Accept': 'application/json',
          'Cookie': '__cf_bm=FS_X2E03_FRS_ql23cFstNVOofVeJpTbpio7I_G5MB8-1690919637-0-AX0+l9jLFOb6zVxLB4t2ELbA8ZojlpaCK2iUkVgedQyui69EM+H8FxwzExsXBayhGcyrIWoIAYKyO6A/EBZIueQ='
          }

          response = requests.request("GET", url, headers=headers, data=payload)
          lead = dict(response.json())
          lead = {'titulo-lead':lead['data']['title'], 'produto':produto[int(lead['data']['5fca6336de210f847b78ce5fd7de950530e26e94'])]}

          url = f"https://api.pipedrive.com/v1/persons/{idpessoa}?api_token=fb1912394dd41792e43c0b2d71a40d4e9dccf6ac"

          payload = {}
          headers = {
          'Accept': 'application/json',
          'Cookie': '__cf_bm=ZGT4Uo6DRvnIXkY4kuiBTz6O11CZY42KIrsz1xfmmWc-1697222543-0-AXKnpEEKpL3drX3iLmaK/2ZZ+d03HCAKmdSn2lpc2aM55dsHsQcbTFdK43ajcU6TQPDXSedbE3QHGzCNyQCTQzI='
          }

          response = requests.request("GET", url, headers=headers, data=payload)

          contato ={'tipo-contato':response.json()['data']['cb6c573810116f88e186b47c471deee0d35c943d'] if response.json()['data']['cb6c573810116f88e186b47c471deee0d35c943d'] in ["30","29","28","31"] else "31"} 
          lead.update(individuo)
          lead.update(contato)
          lead.update(cnpj)
          lead.update({'id_lead':idleed})
          return lead
          break

        else:
          continue

        

    else:
        return {'resposta':'Lead não encontrado'}

@app.route('/pesquisa', methods=['POST'])
def process_request():
    data = request.get_json()
    numero = data['q']
    dados = pesquisa(numero)

    return jsonify(dados)

@app.route('/altera', methods=['POST'])
def process_request_alter():
    data = request.get_json()
    idleed = data['idleed']
    org_id = data['org_id']
    idpessoa = data['idpessoa']
    mensagem = data['mensagem']
    marcacao = data['marcacao']
    responsavel = data['assessor'] 
    if mensagem != '':
        nota = notas(mensagem, idleed, org_id, idpessoa)
    else:
        nota = 200
        
    if marcacao!="00":
        etiqueta = etiquetaPessoa(idpessoa, responsavel, marcacao)
    else:
        etiqueta = etiquetaPessoa(idpessoa, responsavel)
    

    return jsonify({'nota':nota, 'etiqueta':etiqueta})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


