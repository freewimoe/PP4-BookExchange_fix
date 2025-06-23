import csv
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from books.models import SchoolBook

class Command(BaseCommand):
    help = 'Import books from the official school booklist CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing school books before import',
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        clear_existing = options['clear']

        if clear_existing:
            self.stdout.write('Clearing existing school books...')
            SchoolBook.objects.all().delete()

        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                created_count = 0
                updated_count = 0
                skipped_count = 0
                
                with transaction.atomic():
                    for row_num, row in enumerate(reader, 1):
                        try:
                            # Data cleaning and validation
                            title = self.clean_text(row.get('title', '').strip())
                            isbn = self.clean_isbn(row.get('isbn', '').strip())
                            
                            if not title or not isbn:
                                self.stdout.write(
                                    self.style.WARNING(f'Row {row_num}: Skipping - missing title or ISBN')
                                )
                                skipped_count += 1
                                continue
                            
                            # Clean and validate other fields
                            author = self.clean_text(row.get('author', '').strip())
                            edition = self.clean_text(str(row.get('edition', '')).strip())
                            publisher = self.clean_text(row.get('publisher', '').strip())
                            school_class = self.clean_school_class(row.get('school_class', '').strip())
                            subject = self.clean_text(row.get('subject', '').strip())
                            section = self.clean_section(row.get('section', '').strip())
                            notes = self.clean_text(row.get('notes', '').strip())
                            
                            # Skip invalid school classes
                            if not self.is_valid_school_class(school_class):
                                self.stdout.write(
                                    self.style.WARNING(f'Row {row_num}: Invalid school class: {school_class}')
                                )
                                skipped_count += 1
                                continue
                            
                            # Create or update book
                            book, created = SchoolBook.objects.update_or_create(
                                isbn=isbn,
                                defaults={
                                    'title': title,
                                    'author': author,
                                    'edition': edition,
                                    'publisher': publisher,
                                    'school_class': school_class,
                                    'subject': subject,
                                    'section': section,
                                    'notes': notes,
                                    'academic_year': '2023-2024',
                                    'is_active': True,
                                }
                            )
                            
                            if created:
                                created_count += 1
                            else:
                                updated_count += 1
                                
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(f'Row {row_num}: Error processing - {str(e)}')
                            )
                            skipped_count += 1
                            continue

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Import completed!\n'
                        f'Created: {created_count}\n'
                        f'Updated: {updated_count}\n'
                        f'Skipped: {skipped_count}\n'
                        f'Total processed: {created_count + updated_count + skipped_count}'
                    )
                )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {csv_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reading file: {str(e)}')
            )

    def clean_text(self, text):
        """Clean text fields"""
        if not text or text.lower() in ['null', 'none', '']:
            return ''
        
        # Fix encoding issues
        text = text.replace('Ã¶', 'ö').replace('Ã¼', 'ü').replace('Ã¤', 'ä')
        text = text.replace('Ã–', 'Ö').replace('Ãœ', 'Ü').replace('Ã„', 'Ä')
        text = text.replace('ÃŸ', 'ß').replace('Ã©', 'é').replace('Ã±', 'ñ')
        text = text.replace('â€"', '–').replace('â€™', "'")
        
        return text.strip()

    def clean_isbn(self, isbn):
        """Clean and validate ISBN"""
        if not isbn:
            return ''
        
        # Remove non-digit characters except hyphens
        isbn = re.sub(r'[^\d\-]', '', isbn)
        
        # Remove extra spaces and special characters
        isbn = isbn.strip()
        
        return isbn if len(isbn) >= 10 else ''

    def clean_school_class(self, school_class):
        """Clean school class field"""
        if not school_class:
            return ''
        
        school_class = str(school_class).strip().upper()
        
        # Handle common issues in the data
        if school_class.isdigit():  # Sometimes edition year appears here
            return ''
        
        return school_class

    def clean_section(self, section):
        """Clean section field"""
        if not section:
            return ''
        
        section = section.strip().upper()
        
        # Map common variations
        section_map = {
            'DEUTSCH': 'DE',
            'GERMAN': 'DE', 
            'ENGLISH': 'EN',
            'FRANÇAIS': 'FR',
            'FRENCH': 'FR',
            'FRANCAIS': 'FR',
        }
        
        return section_map.get(section, section)

    def is_valid_school_class(self, school_class):
        """Validate school class format"""
        if not school_class:
            return False
        
        # Valid patterns: S1DE, S2EN, S3FR, etc.
        pattern = r'^S[1-7](DE|EN|FR)$'
        return bool(re.match(pattern, school_class))