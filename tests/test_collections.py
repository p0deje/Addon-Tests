#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import random

from unittestzero import Assert
from pages.home import Home

nondestructive = pytest.mark.nondestructive
destructive = pytest.mark.destructive


class TestCollections:

    @destructive
    def test_create_collection(self, mozwebqa):

        home_page = Home(mozwebqa)
        collections_page = home_page.header.site_navigation_menu('Collections').click()
        create_collection_page = collections_page.click_create_collection_button()
        home_page.login('browserID')

        random_name = 'random number following%s' % random.randrange(1, 100)

        create_collection_page.type_name(random_name)
        create_collection_page.type_description(random_name)
        collection = create_collection_page.click_create_collection()

        Assert.equal(collection.notification, 'Collection created!')
        Assert.equal(collection.collection_name, random_name)
        collection.delete()
        user_collections = collection.delete_confirmation()
        if len(user_collections.collections) > 0:
            for collection_element in range(len(user_collections.collections)):  # If the condition is satisfied, iterate through the collections items on the page
                Assert.true(random_name not in user_collections.collections[collection_element].text)  # Check for each collection that the name is not the same as the deleted collections name
        else:
            Assert.equal(user_collections.collection_text, 'No collections found.')  # It means the collection has been deleted and we test for that
