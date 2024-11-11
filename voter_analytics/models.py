from django.db import models
from django.utils.dateparse import parse_date
import csv

# Create your models here.
class Voter(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.precinct_number})"

# Define valid party affiliations for validation
VALID_PARTY_AFFILIATIONS = {'D', 'R', 'CC', 'L', 'T', 'O', 'G', 'J', 'Q', 'FF'}

def load_data():
    '''Load the data records from a CSV file and create Django model instances'''

    # Delete all existing voter records to start fresh
    Voter.objects.all().delete()

    # Define the path to your CSV file
    filename = r"C:\Users\nickj\Documents\Work\CS412\newton_voters.csv"
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        headers = f.readline().strip()  # Discard the header line

        # Loop through each line in the file
        for line in f:
            line = line.strip()
            fields = line.split(',')

            try:
                # Parse date fields
                date_of_birth = parse_date(fields[7])
                date_of_registration = parse_date(fields[8])

                # Strip whitespace from party affiliation and validate
                party_affiliation = fields[9].strip()
                if party_affiliation not in VALID_PARTY_AFFILIATIONS:
                    party_affiliation = 'O'  # Default to 'Other' if value is unrecognized

                # Convert boolean fields
                v20state = fields[11].strip().upper() == 'TRUE'
                v21town = fields[12].strip().upper() == 'TRUE'
                v21primary = fields[13].strip().upper() == 'TRUE'
                v22general = fields[14].strip().upper() == 'TRUE'
                v23town = fields[15].strip().upper() == 'TRUE'

                # Handle voter_score, converting non-numeric values to 0
                try:
                    voter_score = int(fields[16])
                except ValueError:
                    voter_score = 0

                # Correct index for precinct_number if necessary
                precinct_number = fields[9] 

                # Create a new instance of Voter using fields from CSV
                voter = Voter(
                    last_name=fields[1],
                    first_name=fields[2],
                    street_number=fields[3],
                    street_name=fields[4],
                    apartment_number=fields[5] if fields[5] else None,
                    zip_code=fields[6],
                    date_of_birth=date_of_birth,
                    date_of_registration=date_of_registration,
                    party_affiliation=party_affiliation,
                    precinct_number=precinct_number,
                    v20state=v20state,
                    v21town=v21town,
                    v21primary=v21primary,
                    v22general=v22general,
                    v23town=v23town,
                    voter_score=voter_score
                )
                
                print(f'Created voter: {voter}')
                voter.save()  # Save to the database
            
            except Exception as e:
                print(f"Exception occurred: {fields}. Error: {e}")

    print("Done.")
