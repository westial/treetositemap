import time

from behave import *

from treetositemap.src.application.makesitemapindexfromfiles import MakeSiteMapIndexFromFiles
from treetositemap.src.infrastructure.fakeresultvalidator import FakeResultValidator
from treetositemap.src.infrastructure.inmemorysitemaprepository import \
    InMemorySiteMapRepository
from treetositemap.src.infrastructure.localfilefinder import LocalFileFinder
from treetositemap.src.infrastructure.xmlsitemapwriter import XmlSiteMapWriter

import xml.etree.ElementTree as ET

from tests.mock.mockdateservice import MockDateService

use_step_matcher("re")


@given("A sitemap repository")
def step_impl(context):
    context.sitemap_repository = InMemorySiteMapRepository()


@step("A file finder service")
def step_impl(context):
    context.sitemap_file_service = LocalFileFinder()


@step("A result validator")
def step_impl(context):
    context.validator = FakeResultValidator()


@step(
    'A making sitemap index from files use case with url sets folder name as "([^\"]+)"')
def step_impl(context, sitemaps_folder_name):
    context.sitemaps_folder_name = sitemaps_folder_name
    context.use_case = MakeSiteMapIndexFromFiles(
        context.date_service,
        context.sitemap_repository,
        context.sitemap_file_service,
        context.validator,
        context.sitemap_writer,
        context.sitemaps_folder_name
    )


@when('I invoke this use case for the given absolute path to local root directory as "([^\"]+)", file search pattern as "([^\"]+)", destination pointing to as "([^\"]+)", a temporary destination path with prefix as "([^\"]+)" and value "([^\"]+)" as for maximum number of urls for url set')
def step_impl(
        context,
        files_local_root_directory,
        path_pattern,
        domain,
        tmp_destination_root_path,
        raw_max_in_page
):
    max_in_page = int(raw_max_in_page)
    context.current_test_destination = "{0}/{1}".format(
        tmp_destination_root_path,
        int(time.time())
    )
    print("DEBUG: temporary destination path is " + context.current_test_destination)
    context.use_case.invoke(
        files_local_root_directory,
        path_pattern,
        domain,
        context.current_test_destination,
        max_in_page
    )


@then('Sitemap repository has "([^\"]+)" sitemaps')
def step_impl(context, raw_expected_sitemaps):
    assert int(raw_expected_sitemaps) == \
           context.sitemap_repository.count_sitemaps(), \
        "int(raw_expected_sitemaps({0})) == " \
        "context.sitemap_repository.count_sitemaps()({1})".format(
            raw_expected_sitemaps,
            context.sitemap_repository.count_sitemaps()
        )


@then('Sitemap repository has "([^\"]+)" urls')
def step_impl(context, raw_expected_urls):
    assert int(raw_expected_urls) == \
           context.sitemap_repository.count_urls(), \
        "int(raw_expected_urls({0})) == " \
        "context.sitemap_repository.count_urls()({1})".format(
            raw_expected_urls,
            context.sitemap_repository.count_urls()
        )

@given('A sitemap file writer configured with attributes xmlns as "([^\"]+)" and xmlns:mobile as "([^\"]+)"')
def step_impl(context, xmlns, xmlns_mobile):
    context.schema_prefix = "{" + xmlns + "}"
    context.sitemap_writer = XmlSiteMapWriter(xmlns, xmlns_mobile)


@then(
    'Created file as "([^\"]+)" is equal than sample file as "([^\"]+)"')
def step_impl(context, created_file_name, sample_file_path):
    created_file_path = "{0}/{1}".format(
        context.current_test_destination,
        created_file_name
    )
    with open(created_file_path) as created_file:
        created_file_content = created_file.read()

    with open(sample_file_path) as sample_file:
        sample_file_content = sample_file.read()

    assert sample_file_content == created_file_content, "sample == created"


def check_node_name(context, xml_tag: ET.Element, expected_name):
    return xml_tag.tag == "{0}{1}".format(context.schema_prefix, expected_name)


@given('A date service with forced date as "([^\"]+)"')
def step_impl(context, forced):
    context.date_service = MockDateService(forced)
