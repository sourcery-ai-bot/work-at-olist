"""A custom 'manage.py' command that imports categories from a CSV file."""

import csv
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from channels.models import Channel, Category


class Command(BaseCommand):
    """Command that imports categories from a CSV file.

    The 'importcategories' command creates a Channel if the provided name don't
    exists. And then, it creates all the imported categories. If
    """

    help = 'Imports categories from a CSV file'

    def add_arguments(self, parser):
        """Adds 'channel' and 'csv' args to the command."""
        parser.add_argument('channel', type=str)
        parser.add_argument('csv', type=open)

    def validate_ancestors(self, channel_ref, categories):
        """Checks if all category ancestors are already registered and returns
        the last one, the parent. Because of the reference format, checking
        only the parent will validate every ancestor.
        """
        if not len(categories):
            return None, None

        parent_ref = Category.generate_reference(
            categories[-1], [channel_ref] + categories[0:-1])
        try:
            parent = Category.objects.get(reference=parent_ref)
        except Category.DoesNotExist:
            return None, 'Parent does not exist'

        return parent, None

    @transaction.atomic
    def handle(self, *args, **options):
        """Perform the operations of importcategories command."""
        channel_ref = Channel.generate_reference(options['channel'])
        channel, created = Channel.objects.get_or_create(
            reference=channel_ref, defaults={'name': options['channel']})

        if not created:
            Category.objects.filter(channel=channel).delete()

        reader = csv.DictReader(options['csv'])
        for row in reader:
            full_path = [x.strip() for x in row['Category'].split('/')]
            ancestors = full_path[0:-1]
            current = full_path[-1]

            parent, error = self.validate_ancestors(channel_ref, ancestors)
            if error:
                raise CommandError('Unable to process "{:s}": {:s}'.format(row[
                    'Category'], error))

            category_ref = Category.generate_reference(
                current, [channel_ref] + ancestors)
            Category.objects.create(
                reference=category_ref,
                name=current,
                channel=channel,
                parent=parent)
