from django.core.management.base import BaseCommand
from django.utils import timezone
from base.calendar_service import sync_google_calendar_events


class Command(BaseCommand):
    help = 'Sync events from Google Calendar'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output',
        )

    def handle(self, *args, **options):
        verbose = options.get('verbose', False)
        
        if verbose:
            self.stdout.write('Starting Google Calendar sync...')
        
        try:
            synced_count = sync_google_calendar_events()
            
            if verbose:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully synced {synced_count} events from Google Calendar'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Synced {synced_count} events'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error syncing calendar: {str(e)}'
                )
            )
            
            if verbose:
                import traceback
                self.stdout.write(traceback.format_exc())