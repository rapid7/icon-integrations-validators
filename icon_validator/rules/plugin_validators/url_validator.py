import http.client
import os
import urllib
import urllib.request
from typing import List

from urlextract import URLExtract

from icon_validator.styling import *
from icon_validator.rules.validator import KomandPluginValidator


class URLValidator(KomandPluginValidator):
    """ Search for HTTP(s) links, and testing for invalid ones.  Namely, 400+ HTTP return codes"""
    maximum_timeout = 5

    def __init__(self):
        super().__init__()
        # string to list dictionary
        self._violating_files_to_urls_map = {}
        self._urls_already_tried = []

    def inspect_file_for_urls_and_test_them(self, file_contents: str) -> List[str]:
        """ Find URLs in the file, test for 400 return codes, and return the list of failed urls """
        return_list = []
        if not file_contents or not isinstance(file_contents, str):
            return return_list

        url_extractor = URLExtract()
        urls_from_file = list(set(url_extractor.find_urls(file_contents)))

        for web_address in urls_from_file:
            if web_address.lower() in ["help.md", "license.md", "readme.md"]:
                continue
            if not web_address[0:4] == "http":
                web_address = "http://" + web_address
            address_parts = urllib.parse.urlparse(web_address)
            cleaned_web_address = address_parts.netloc

            path_to_test = r"/"
            if address_parts.path:
                path_to_test = address_parts.path

            url_tested = f"{cleaned_web_address}/{path_to_test}"
            if url_tested in self._urls_already_tried:
                continue

            self._urls_already_tried.append(url_tested)
            try:
                connection = http.client.HTTPConnection(cleaned_web_address, timeout=self.maximum_timeout, port=80)
                connection.request("HEAD", path_to_test)
                response = connection.getresponse()
                code = int(response.status)

                if code >= 400:
                    return_list.append(web_address)
            except Exception as e:
                return_list.append(web_address)
            finally:
                if connection:
                    connection.close()

        return return_list

    def validate(self, spec):
        specfile = spec.directory + "/" + spec.spec_file_name
        if os.path.exists(specfile):
            raw_spec_contents = spec.raw_spec()
            spec_file_bad_urls = self.inspect_file_for_urls_and_test_them(raw_spec_contents)
            if len(spec_file_bad_urls) > 0:
                self._violating_files_to_urls_map[specfile] = spec_file_bad_urls

        helpfile = spec.directory + "/help.md"
        if os.path.exists(helpfile):
            help_file_contents = ""
            with open(helpfile) as h:
                help_file_contents = h.read()
                help_file_bad_urls = self.inspect_file_for_urls_and_test_them(help_file_contents)
                if len(help_file_bad_urls) > 0:
                    self._violating_files_to_urls_map[helpfile] = help_file_bad_urls

        if len(self._violating_files_to_urls_map) > 0:
            header_printed = False

            for violating_file in self._violating_files_to_urls_map:
                with open(violating_file) as f:
                    file_lines = f.read().splitlines()

                violating_urls = self._violating_files_to_urls_map[violating_file]
                for url in violating_urls:
                    lines_with_url = list(filter(lambda i: url in file_lines[i], range(1, len(file_lines))))

                    for line in lines_with_url:
                        actual_line_number_in_file = str(int(line) + 1)
                        if not header_printed:
                            header = " ".join((f"{YELLOW}WARNING: URLs found that return a 4xx code.",
                                               "Verify they are publicly accessible and if not, update with a working URL."))
                            print(header)
                            header_printed = True
                        file_name = os.path.basename(violating_file)
                        print(f"{YELLOW}violation: {file_name}[{actual_line_number_in_file}]: {str(url)}")
