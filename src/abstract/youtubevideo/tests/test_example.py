import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from abstract.youtubevideo.testing import\
    ABSTRACT_YOUTUBEVIDEO_INTEGRATION


class TestExample(unittest.TestCase):

    layer = ABSTRACT_YOUTUBEVIDEO_INTEGRATION
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
    
    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product 
            installed
        """
        pid = 'abstract.youtubevideo'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')
