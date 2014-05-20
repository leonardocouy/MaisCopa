# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import xmltodict
from google.appengine.api import urlfetch
from google.appengine.ext import blobstore


def index(_write_tmpl):
    _write_tmpl('templates/info.html')


def ler_arquivo_dict(fileName):
    blob_key = blobstore.BlobInfo.all().filter('filename = ', fileName).get().key()
    blob_reader = blobstore.BlobReader(blob_key)
    conteudo = blob_reader.read()
    dict = xmltodict.parse(conteudo, process_namespaces=True)
    return dict


def listar_cidades(_json):
    dictCidades = ler_arquivo_dict('cidadesede.xml')
    listaCidades = []  # INICIALIZA A LISTA DE CIDADES.

    for cidade in dictCidades['collection']['http://www.portaltransparencia.gov.br/copa2014:cidadeSede']:  # PROCURE POR CIDADE NO DICTCIDADE
        listaCidades.append(cidade['descricao'])  # ADICIONE NA LISTA O VALOR(NOME DA CIDADE) DA CHAVE "DESCRICAO" DO DICIONARIO CIDADE.


    _json(listaCidades, '')  # Transforme em JSON PROTEGIDO, A LISTA CIDADES.


def listar_temas(_json):
    dictTemas = ler_arquivo_dict('tema.xml')
    listaTemas = []

    for tema in dictTemas['collection']['http://www.portaltransparencia.gov.br/copa2014:tema']:
        listaTemas.append(tema['descricao'])

    _json(listaTemas, '')


def buscar_infos(_json, cidade, tema):

    dictEmp = ler_arquivo_dict('empreendimento.xml')
    lista_infos = []

    for info in dictEmp['collection']['http://www.portaltransparencia.gov.br/copa2014:empreendimento']:
        if (info['cidadeSede']['descricao'].encode('utf-8').find(cidade)) > -1:
            if info['tema']['descricao'].encode('utf-8').find(tema) > -1:
                lista_infos.append(info)

    _json(lista_infos)



def listar_info(_json, cod):
    ns = 'http://www.portaltransparencia.gov.br/copa2014:empreendimento'
    urlfetch.set_default_fetch_deadline(60)
    url = urlfetch.fetch('http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento/%s' % cod)
    dictInfo = (xmltodict.parse(url.content, process_namespaces=True))
    _json(dictInfo[ns])




