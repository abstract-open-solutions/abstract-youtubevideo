from random import sample
from zope import schema
from zope.component import getUtility, getMultiAdapter
from zope.interface import implements
from zope.formlib import form
from Products.ATContentTypes.interface.folder import IATFolder
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.portlets.portlets import base
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize import ram
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from abstract.youtubevideo import youtubevideoMessageFactory as _


def ytp_key(method, self, folder_path):
    return (self, folder_path)


class IYouTubePortlet(IPortletDataProvider):
    """"""
    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        required=True
    )
    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=3)
    target = schema.Choice(
            title=_(u"Nome della sorgente"),
            description=_(
                    u"Ricerca della sorgente dati (cartella o collezione)"),
            required=True,
            source=SearchableTextSourceBinder(
                {'portal_type': ('Folder', 'Topic', 'Collection')},
            default_query='path:'))
    showVideo = schema.Bool(
            title=_(u'Mostra il Player'),
            description=_(u'Se attivo visualizza il player'),
            required=False,
            default=True,
    )
    randomOrder = schema.Bool(
            title=_(u'Ordinamento Casuale'),
            description=_(u''),
            required=False,
            default=False,
    )
    footer = schema.TextLine(
        title=_(u"Portlet footer"),
        description=_(u"Footer of the rendered portlet"),
        default=u"Galleria filmati YouTube",
        required=True
    )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IYouTubePortlet)

    count = 5
    target = None
    header = ""
    footer = u"Galleria filmati YouTube"
    showVideo = True
    randomOrder = False

    def __init__(self, count=5, target=None, header="",
                                showVideo=True, randomOrder=False, footer=""):
        self.count = count
        self.target = target
        self.header = header
        self.showVideo = showVideo
        self.randomOrder = randomOrder
        self.footer = footer

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "YouTube Playlist Portlet - %s" % (self.header)


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('youtubeplaylist_portlet.pt')

    @memoize
    def getTarget(self):
        target_path = self.data.target
        if not target_path:
            return None

        if target_path.startswith('/'):
            target_path = target_path[1:]

        if not target_path:
            return None

        portal = self.portal_state.portal()
        if isinstance(target_path, unicode):
            #restrictedTraverse accept only strings
            target_path = str(target_path)

        return portal.restrictedTraverse(target_path, default=None)

    @ram.cache(ytp_key)
    def getLinkFolder(self, folder_path='/'):

        if folder_path:
            pc = getToolByName(self.context, 'portal_catalog')

            links = pc.searchResults(path={'query': folder_path, 'depth': 100},
                                      portal_type=['Video'],
                                      exclude_from_nav=False,
                                      sort_on='getObjPositionInParent')
            return links

        return []

    @property
    def portal_state(self):
        return getMultiAdapter((self.context, self.request),
                                name=u'plone_portal_state')

    def getLinks(self):
        """ """
        target = self.getTarget()
        randomOrder = self.data.randomOrder
        count = self.data.count

        if target:
            if IATFolder.providedBy(target):
                path = '/'.join(target.getPhysicalPath())
                links = self.getLinkFolder(folder_path=path)
            else:
                links = target.queryCatalog()

            if not randomOrder:
                return links[:count]

            links_len = len(links)

            if count > links_len:
                return sample(links, links_len)
            else:
                return sample(links, count)

        return []

    def css_id(self):
        """Generate a CSS class from the portlet header
        """
        target = self.getTarget()
        normalizer = getUtility(IIDNormalizer)
        text = normalizer.normalize(self.data.header)

        if target:
            text = target.UID()

        return "ytvideo-%s" % text

    def showVideo(self):
        return self.data.showVideo

    def showPlayer(self):
        return self.data.showVideo and 'true' or 'false'

    def attributeVideoURL(self):
        return self.data.showVideo and 'href' or 'rel'


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IYouTubePortlet)
    form_fields['target'].custom_widget = UberSelectionWidget

    label = _(u"Add YouTube Playlist Portlet")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IYouTubePortlet)
    form_fields['target'].custom_widget = UberSelectionWidget
    label = _(u"Edit YouTube Playlist Portlet")
