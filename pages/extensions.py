#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page
from pages.base import Base


class ExtensionsHome(Base):

    _page_title = 'Featured Extensions :: Add-ons for Firefox'
    _extensions_locator = (By.CSS_SELECTOR, "div.items div.item")
    _default_selected_tab_locator = (By.CSS_SELECTOR, "#sorter li.selected")

    _sort_by_most_users_locator = (By.CSS_SELECTOR, "div#sorter > ul > li:nth-child(2) > a")

    _updating_locator = (By.CSS_SELECTOR, "div.updating")

    @property
    def extensions(self):
        return [Extension(self.testsetup, element)
                for element in self.selenium.find_elements(*self._extensions_locator)]

    @property
    def default_selected_tab(self):
        return self.selenium.find_element(*self._default_selected_tab_locator).text

    def _wait_for_results_refresh(self):
        WebDriverWait(self.selenium, 10).until(lambda s: not self.is_element_present(*self._updating_locator))

    def sort_by(self, type):
        click_element = self.selenium.find_element(*getattr(self, '_sort_by_%s_locator' % type.replace(' ', '_').lower()))
        footer = self.selenium.find_element(*self._footer_locator)
        ActionChains(self.selenium).\
            move_to_element(footer).\
            move_to_element(click_element).\
            click().perform()
        self._wait_for_results_refresh()


class Extension(Page):
        _name_locator = (By.CSS_SELECTOR, "h3 a")

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def name(self):
            return self._root_element.find_element(*self._name_locator).text

        def click(self):
            self._root_element.find_element(*self._name_locator).click()
            from pages.details import Details
            return Details(self.testsetup)
