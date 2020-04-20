from django.test import TestCase

from helpers.custom_paginator import AppPaginator


class AppPaginatorTest(TestCase):

    def test_pagination(self):

        value = [1, 2, 3, 4, 5]
        data, num_data = AppPaginator(value, page_size=2, page_number=1).paginate_objects()
        self.assertEqual(data, [1, 2])
        self.assertEqual(num_data, 5)

    def test_pagination_without_page_size(self):

        value = [1, 2, 3, 4, 5]
        data, num_data = AppPaginator(value, page_number=1).paginate_objects()
        self.assertEqual(data, [1, 2, 3, 4, 5])
        self.assertEqual(num_data, 5)

    def test_pagination_without_page_number(self):

        value = [1, 2, 3, 4, 5]
        data, num_data = AppPaginator(value, page_size=3).paginate_objects()
        self.assertEqual(data, [1, 2, 3])
        self.assertEqual(num_data, 5)

    def test_pagination_empty_values(self):

        value = []
        data, num_data = AppPaginator(value, page_size=1, page_number=1).paginate_objects()
        self.assertEqual(data, [])
        self.assertEqual(num_data, 0)