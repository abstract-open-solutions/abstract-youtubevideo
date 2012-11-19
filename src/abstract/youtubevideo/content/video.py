# -*- coding: utf-8 -*-
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import link
from abstract.youtubevideo import youtubevideoMessageFactory as _
from abstract.youtubevideo.interfaces import IVideo
from abstract.youtubevideo.config import PROJECTNAME


schema = atapi.Schema(())

videoSchema = getattr(link.ATLink, 'schema',
                                    atapi.Schema(())).copy() + schema.copy()

videoSchema['description'].widget.description = _(
    u"Usato nell'elenco degli elementi e nei risultati delle ricerche.<br/>"
    u"Accessibilita': descrizione alternativa del contenuto.")
videoSchema['description'].widget.i18n_domain = 'abstract.youtubevideo'


class Video(link.ATLink):
    """File System Image"""
    implements(IVideo)

    portal_type = "Video"
    schema = videoSchema

atapi.registerType(Video, PROJECTNAME)
