# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Damian Schwyrz

from urllib.parse import urlparse
from inc.Headers import *
from inc.Payload import *
from random import shuffle


class PrepareAttackRequest:

    def __init__(self, config, host_params):
        self.config = config
        self.host_params = host_params
        self.tests = []

        self.__create_request_data()

    def __create_request_data(self):

        for attacked_site in self.config.urls:
            url = self.__make_url(attacked_site)
            path = self.__get_path(url)
            hostname = self.__get_host(url)
            port = self.__get_port(url)

            self.custom_params = []

            if hostname in self.host_params:
                self.custom_params = self.host_params[hostname]

            self.__create_tests(hostname, path, port, url)

        self.__shuffle_tests_if_allowed()

    def __shuffle_tests_if_allowed(self):
        if self.config.shuffle_tests:
            shuffle(self.tests)

    def __create_tests(self, hostname, path, port, url):
        if self.config.type_get:
            self.custom_params_base_get = list(self.__chunks(self.custom_params, self.config.chunk_size_get))

            for inner_list in self.custom_params_base_get:
                self.__put_get_attack_to_tests("GET", url, hostname, port, path, '', inner_list)

        if self.config.type_post:
            self.custom_params_base_post = list(self.__chunks(self.custom_params, self.config.chunk_size_post))

            for inner_list in self.custom_params_base_post:
                self.__put_post_attack_to_tests("POST", url, hostname, port, path, '', inner_list)

    def __put_post_attack_to_tests(self, method, url, hostname, port, path, test_char, parameters):

        headers = Headers(self.config)
        headers.set("Host", hostname)
        headers.add_user_defined_headers()

        if self.config.cookies != "":
            headers.set("Cookie", self.config.cookies)

        headers.set("Referer", "{}".format(url))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "application/x-www-form-urlencoded")

        payload = Payload()
        payload.generate_get_string(parameters, test_char)

        self.tests.append({
            'url': url,
            'port': port,
            'method': method,
            'host': hostname,
            'path': "{}".format(path),
            'base_path': "{}?".format(path),
            'headers': headers.make(),
            'body': payload.string,
            'test_char': test_char,
            'payload_information': payload.payload_information
        })

    def __put_get_attack_to_tests(self, method, url, hostname, port, path, test_char, parameters):

        headers = Headers(self.config)
        headers.set("Host", hostname)
        headers.add_user_defined_headers()

        if self.config.cookies != "":
            headers.set("Cookie", self.config.cookies)

        headers.set("Referer", "{}".format(url))
        headers.set("User-Agent", headers.get_random_user_agent())
        headers.set("Content-Type", "text/html")

        payload = Payload()
        payload.generate_get_string(parameters, test_char)

        self.tests.append({
            'url': url,
            'port': port,
            'method': method,
            'host': hostname,
            'path': "{}?{}".format(path, payload.string),
            'base_path': "{}?".format(path),
            'headers': headers.make(),
            'body': '',
            'test_char': test_char,
            'payload_information': payload.payload_information
        })


    @staticmethod
    def __make_url(attacked_site):

        url = attacked_site

        if not attacked_site.startswith("http"):
            url = "http://{}/".format(attacked_site)

        return url

    @staticmethod
    def __get_path(url):

        parser = urlparse(url)

        return parser.path

    @staticmethod
    def __get_host(url):

        parser = urlparse(url)

        return parser.hostname

    @staticmethod
    def __get_port(url):

        parser = urlparse(url)

        return parser.port

    @staticmethod
    def __chunks(params, size):

        for i in range(0, len(params), size):
            yield params[i:i + size]
