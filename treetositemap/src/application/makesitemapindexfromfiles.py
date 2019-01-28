from .xml.xmlurl import XmlUrl
from .xml.xmlsitemap import XmlSiteMap
from ..domain.resultvalidator import ResultValidator
from ..domain.dateservice import DateService
from ..domain.filefinder import FileFinder
from ..domain.sitemaprepository import SiteMapRepository
from ..domain.sitemapwriter import SiteMapWriter
from ..infrastructure.emptyresult import EmptyResult
from ..lib.helper import *


class MakeSiteMapIndexFromFiles(object):

    def __init__(
            self,
            date_service: DateService,
            sitemap_repository: SiteMapRepository,
            sitemap_file_service: FileFinder,
            book_validator: ResultValidator,
            sitemap_writer: SiteMapWriter,
            sitemaps_folder_name
    ):
        self.__date_service = date_service
        self.__sitemap_writer = sitemap_writer
        self.__sitemaps_folder_name = sitemaps_folder_name
        self.__sitemap_repository = sitemap_repository
        self.__sitemap_file_service = sitemap_file_service
        self.__book_validator = book_validator

    def invoke(
            self,
            files_local_root_directory: str,
            path_pattern: str,
            domain: str,
            destination_path: str,
            max_in_page: int
    ):
        self.__add_urls_to_repository(
            files_local_root_directory,
            path_pattern,
            domain
        )

        if self.__sitemap_repository.is_empty():
            raise EmptyResult("SiteMap repository is empty")

        self.__write_sitemap_files(max_in_page, destination_path, domain)

    def __add_urls_to_repository(
            self,
            files_local_root_directory,
            path_pattern,
            domain
    ):
        file_paths = self.__sitemap_file_service.find_files(
            join_paths(
                files_local_root_directory,
                path_pattern
            ),
            True
        )
        for found_path in file_paths:
            with open(found_path, 'rb') as found_file:
                content = found_file.read()
                if self.__book_validator.is_valid(content):
                    url_loc = replace_root_directory_path(
                        files_local_root_directory,
                        found_path,
                        domain
                    )
                    url = XmlUrl(url_loc)
                    self.__sitemap_repository.add_url(url)

    def __write_sitemap_files(self, max_in_page, local_destination_path, domain):
        urlsets = self.__sitemap_repository.get_urlsets(max_in_page)
        urlset_counter = 0

        for urlset_urls in urlsets:
            urlset_file_path = join_paths(
                local_destination_path,
                self.__sitemaps_folder_name,
                "sitemap-{:06d}.xml".format(urlset_counter)
            )
            self.__sitemap_writer.write_urlset(urlset_file_path, urlset_urls)
            self.__sitemap_repository.add_sitemap(
                XmlSiteMap(
                    replace_root_directory_path(
                        local_destination_path,
                        urlset_file_path,
                        domain
                    ),
                    self.__date_service.now_iso_format()
                )
            )
            urlset_counter += 1

        self.__sitemap_writer.write_sitemapindex(
            join_paths(local_destination_path, "sitemap.xml"),
            self.__sitemap_repository.get_sitemaps()
        )
