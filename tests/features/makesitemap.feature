Feature: Tests for making the gutenberg sitemaps use case

  Scenario: Properly make the index and sitemaps
    Given A sitemap repository
    And A file finder service
    And A content regex result validator with pattern expression as "(?s)\A(?!.*?(?<!\w)(I do not want this file)(?!\w)).*"
    And A date service with forced date as "2019-01-25T08:06:35Z"
    And A sitemap file writer configured with attributes xmlns as "http://www.sitemaps.org/schemas/sitemap/0.9" and xmlns:mobile as "http://www.google.com/schemas/sitemap-mobile/1.0"
    And A making sitemap index from files use case with url sets folder name as "sitemaps"
    When I invoke this use case for the given absolute path to local root directory as "tests/sample/gutenberg", file search pattern as "./**/*.htm*", destination pointing to as "https://www.westial.dot/", a temporary destination path with prefix as "/tmp/treetositemap" and value "4" as for maximum number of urls for url set
    Then Sitemap repository has "6" urls
    And Sitemap repository has "2" sitemaps
    And Created file as "sitemaps/sitemap-000000.xml" is equal than sample file as "tests/sample/sitemaps/sitemap-000000.xml"
    And Created file as "sitemaps/sitemap-000001.xml" is equal than sample file as "tests/sample/sitemaps/sitemap-000001.xml"
    And Created file as "sitemap.xml" is equal than sample file as "tests/sample/sitemap.xml"