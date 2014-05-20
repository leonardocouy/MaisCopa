# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import files
from google.appengine.api import urlfetch
from google.appengine.ext import blobstore

# FUNÇÃO PARA BAIXAR O XML NO SITE, PEGAR O SEU CONTEUDO E SALVAR NO BLOB DO SERVIDOR.


def salvar_blob(linkxml, filename):
    blobstore.delete(blobstore.BlobInfo.all().filter('filename = ', filename+'.xml').get().key())
    urlfetch.set_default_fetch_deadline(60)  # DEFININDO A DEADLINE PARA 60 SEGUNDOS
    arquivoXML = urlfetch.fetch(linkxml)  # BAIXANDO O CONTEUDO DO XML
    nome_arquivo = files.blobstore.create(mime_type='text/xml',_blobinfo_uploaded_filename=filename+'.xml')  # CRIANDO O ARQUIVO XML

    with files.open(nome_arquivo,   'a') as linha:  # NAVEGANDO LINHA POR LINHA DO ARQUIVO
        linha.write(arquivoXML.content)  # ADICIONANDO CADA LINHA DO XML AO ARQUIVO CRIADO NO SERVIDOR

    files.finalize(nome_arquivo)  # FINALIZANDO O ARQUIVO.


def baixar_xml():
    salvar_blob('http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento', 'empreendimento')
    salvar_blob('http://www.portaltransparencia.gov.br/copa2014/api/rest/cidadesede', 'cidadesede')
    salvar_blob('http://www.portaltransparencia.gov.br/copa2014/api/rest/tema', 'tema')
