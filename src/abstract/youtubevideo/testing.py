from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import abstract.youtubevideo


ABSTRACT_YOUTUBEVIDEO = PloneWithPackageLayer(
    zcml_package=abstract.youtubevideo,
    zcml_filename='testing.zcml',
    gs_profile_id='abstract.youtubevideo:testing',
    name="ABSTRACT_YOUTUBEVIDEO")

ABSTRACT_YOUTUBEVIDEO_INTEGRATION = IntegrationTesting(
    bases=(ABSTRACT_YOUTUBEVIDEO, ),
    name="ABSTRACT_YOUTUBEVIDEO_INTEGRATION")

ABSTRACT_YOUTUBEVIDEO_FUNCTIONAL = FunctionalTesting(
    bases=(ABSTRACT_YOUTUBEVIDEO, ),
    name="ABSTRACT_YOUTUBEVIDEO_FUNCTIONAL")
