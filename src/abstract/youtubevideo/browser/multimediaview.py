from Products.Five import BrowserView
from Products.CMFPlone.utils import getToolByName
from Products.ATContentTypes.interface.folder import IATFolder
from Products.ATContentTypes.interface.topic import IATTopic


class MultimediaView(BrowserView):
    """ """

    def getLinks(self):
        """docstring for getLinks"""
        catalog = getToolByName(self.context, 'portal_catalog')

        query = {}

        if IATFolder.providedBy(self.context):

            query['portal_type'] = 'Video'
            query['path'] = {'query': '/'.join(self.context.getPhysicalPath()),
                                                                'depth': 100}
            query['sort_on'] = 'getObjPositionInParent'

            items = catalog(**query)

            return items

        if IATTopic.providedBy(self.context):
            return self.context.queryCatalog(batch=True)

        return []
