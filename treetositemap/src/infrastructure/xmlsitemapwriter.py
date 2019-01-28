import errno
import os
from typing import List
import xml.etree.ElementTree as ET
from xml.dom import minidom

from ..application.xml.constant import *
from ..domain.dto.sitemap import SiteMap
from ..domain.dto.url import Url
from ..domain.sitemapwriter import SiteMapWriter


class XmlSiteMapWriter(SiteMapWriter):

    def __init__(self, xmlns, xmlns_mobile):
        self.__xmlns = xmlns
        self.__xmlns_mobile = xmlns_mobile

    @classmethod
    def __write_xml(cls, file_path: str, root_tag: ET.Element):
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise exc
        with open(file_path, 'w+') as xml_file:
            xml_file.write(
                cls.__prettify(
                    ET.tostring(root_tag, 'utf-8')
                )
            )

    @classmethod
    def __prettify(self, xml_content):
        prettifier = minidom.parseString(xml_content)
        return prettifier.toprettyxml(indent="\t")

    def write_urlset(self, file_path: str, urls: List[Url]):
        urlset_tag = ET.Element(URLSET)
        urlset_tag.set(XMLNS, self.__xmlns)
        urlset_tag.set(XMLNS_MOBILE, self.__xmlns_mobile)
        while urls:
            url: Url = urls.pop(0)
            url_tag = ET.SubElement(urlset_tag, URL)
            loc_tag = ET.SubElement(url_tag, LOC)
            loc_tag.text = url.loc
        self.__write_xml(file_path, urlset_tag)

    def write_sitemapindex(self, file_path: str, sitemaps: List[SiteMap]):
        sitemapindex_tag = ET.Element(SITEMAPINDEX)
        sitemapindex_tag.set(XMLNS, self.__xmlns)
        for sitemap in sitemaps:
            sitemap_tag = ET.SubElement(sitemapindex_tag, SITEMAP)
            loc_tag = ET.SubElement(sitemap_tag, LOC)
            loc_tag.text = sitemap.loc
            lastmod_tag = ET.SubElement(sitemap_tag, LASTMOD)
            lastmod_tag.text = sitemap.lastmod
        self.__write_xml(file_path, sitemapindex_tag)

