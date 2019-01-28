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
            content_validator: ResultValidator,
            sitemap_writer: SiteMapWriter,
            sitemaps_folder_name
    ):
        self.__date_service = date_service
        self.__sitemap_writer = sitemap_writer
        self.__sitemaps_folder_name = sitemaps_folder_name
        self.__sitemap_repository = sitemap_repository
        self.__sitemap_file_service = sitemap_file_service
        self.__content_validator = content_validator

    def invoke(
            self,
            files_local_root_directory: str,
            path_pattern: str,
            domain: str,
            destination_path: str,
            max_in_page: int
    ):
        print(
            "DEBUG: Indexing local directory {0} "
            "looking for items under pattern as {1}"
            "to create a sitemap for {2} domain destination.".format(
                files_local_root_directory,
                path_pattern,
                domain
            )
        )

        self.__add_urls_to_repository(
            files_local_root_directory,
            path_pattern,
            domain
        )

        if self.__sitemap_repository.is_empty():
            raise EmptyResult("SiteMap repository is empty")

        print("DEBUG: All items indexed")

        print("DEBUG: Writing sitemap resource files")

        self.__write_sitemap_files(max_in_page, destination_path, domain)

        print(
            "DEBUG: Successfully done. See results in {0}".format(
                destination_path
            )
        )

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
            if self.__content_validator \
                    and not self.__content_validator.is_valid(found_path):
                continue
            url_loc = replace_root_directory_path(
                files_local_root_directory,
                found_path,
                domain
            )
            url = XmlUrl(url_loc)
            print("DEBUG: Added item url as {0}".format(url_loc))
            self.__sitemap_repository.add_url(url)

    def __write_sitemap_files(self, max_in_page, local_destination_path,
                              domain):
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
            print("DEBUG: File {0} written".format(urlset_file_path))
            urlset_counter += 1

        print("DEBUG: Writing sitemap index file")

        self.__sitemap_writer.write_sitemapindex(
            join_paths(local_destination_path, "sitemap.xml"),
            self.__sitemap_repository.get_sitemaps()
        )
