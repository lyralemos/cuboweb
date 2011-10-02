import warnings

warnings.simplefilter('ignore', RuntimeWarning)

from compress.filter_base import FilterBase
from cuboweb.apps.cms.filters.cssmin.cssmin import minimalize 

class CssMinFilter(FilterBase):
    def filter_css(self,css):
        return minimalize(css)