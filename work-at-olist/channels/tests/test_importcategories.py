"""ImportCategories command's test cases."""

import os
import csv
import tempfile
from django.test import TestCase
from django.core.management import call_command, CommandError
from channels.models import Channel


def create_tempcsv(content):
    """Creates a temporary csv file and fill with 'content'. Returns its
    'filename'.
    """
    csvfile = tempfile.NamedTemporaryFile(mode='w', delete=False)

    fieldnames = ['Category']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in content:
        writer.writerow({'Category': item})

    filename = csvfile.name
    csvfile.close()

    return filename


class ImportCategoriesTest(TestCase):
    """ImportCategories Command's Test Cases."""

    def test_empty(self):
        """Tests importcategories command against a empty file."""
        csvfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        filename = csvfile.name
        csvfile.close()

        args = ['empty', filename]
        opts = {}
        try:
            call_command('importcategories', *args, **opts)
        finally:
            os.unlink(filename)

        channel = Channel.objects.get(reference='empty')
        self.assertIsNotNone(channel)

        self.assertEqual(channel.categories.count(), 0)

    def test_one_category(self):
        """Tests importcategories command against a file with only one
        category.
        """
        content = ['Books']
        filename = create_tempcsv(content)

        args = ['onecategory', filename]
        opts = {}
        try:
            call_command('importcategories', *args, **opts)
        finally:
            os.unlink(filename)

        channel = Channel.objects.get(reference='onecategory')
        self.assertIsNotNone(channel)

        categories = channel.categories.all()
        self.assertEqual(categories.count(), 1)
        self.assertEqual(categories.first().name, content[0])

    def test_full_tree(self):
        """Tests importcategories command against a file with a complete
        category tree.
        """
        content = [
            'Books', 'Books / National Literature',
            'Books / National Literature / Science Fiction',
            'Books / National Literature / Fiction Fantastic',
            'Books / Foreign Literature', 'Books / Computers',
            'Books / Computers / Applications', 'Books / Computers / Database',
            'Books / Computers / Programming', 'Games', 'Games / XBOX 360',
            'Games / XBOX 360 / Console', 'Games / XBOX 360 / Games',
            'Games / XBOX 360 / Accessories', 'Games / XBOX One',
            'Games / XBOX One / Console', 'Games / XBOX One / Games',
            'Games / XBOX One / Accessories', 'Games / Playstation 4',
            'Computers', 'Computers / Notebooks', 'Computers / Tablets',
            'Computers / Desktop'
        ]
        filename = create_tempcsv(content)

        args = ['onecategory', filename]
        opts = {}
        try:
            call_command('importcategories', *args, **opts)
        finally:
            os.unlink(filename)

        channel = Channel.objects.get(reference='onecategory')
        self.assertIsNotNone(channel)

        categories = channel.categories.all()
        self.assertEqual(categories.count(), len(content))

    def test_missing_parent(self):
        """Tests importcategories command against a file with a missing parent
        category.
        """
        content = [
            'Games',
            'Games / XBOX 360 / Console',
        ]
        filename = create_tempcsv(content)

        args = ['onecategory', filename]
        opts = {}
        try:
            call_command('importcategories', *args, **opts)
        except CommandError as err:
            error = err.__str__()
        finally:
            os.unlink(filename)

        if not error:
            self.fail('No exception was triggered.')

    def test_reimport(self):
        """Tests importcategories command against reimportation.
        """
        content = [
            'Books', 'Books / National Literature',
            'Books / National Literature / Science Fiction',
            'Books / National Literature / Fiction Fantastic',
            'Books / Foreign Literature', 'Books / Computers',
            'Books / Computers / Applications', 'Books / Computers / Database',
            'Books / Computers / Programming', 'Games', 'Games / XBOX 360',
            'Games / XBOX 360 / Console', 'Games / XBOX 360 / Games',
            'Games / XBOX 360 / Accessories', 'Games / XBOX One',
            'Games / XBOX One / Console', 'Games / XBOX One / Games',
            'Games / XBOX One / Accessories', 'Games / Playstation 4',
            'Computers', 'Computers / Notebooks', 'Computers / Tablets',
            'Computers / Desktop'
        ]
        filename = create_tempcsv(content)

        args = ['reimport', filename]
        opts = {}
        try:
            call_command('importcategories', *args, **opts)
            call_command('importcategories', *args, **opts)
        finally:
            os.unlink(filename)

        channel = Channel.objects.get(reference='reimport')
        self.assertIsNotNone(channel)

        categories = channel.categories.all()
        self.assertEqual(categories.count(), len(content))
