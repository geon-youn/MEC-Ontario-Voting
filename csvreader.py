import csv
from dataclasses import dataclass

@dataclass
class Party:
    party_name: str
    leader: str
    bio: str


    def get_party_bio():
        return {Party('Pineapple Pizza Party', 'John Doe', 'This is a bio.'),
                Party('Pronounced Jiff Union', 'Steve Joe', 'This is a bio.'),
                Party('Socks and Crocs Reform League', 'Lohn Loe', 'This is a bio.')
                }


def create_dict_of_votes(file):
    """
    Creates a dictionary from the given csv file of votes.
    ------------------------------------------------------
    Inputs:
        file -> str
    Outputs:
        dict
    """
    with open(file) as csvfile:
        entries = csv.reader(csvfile)
        header = next(entries)
        votes = dict()

        # add valid entries to the dictionary
        for entry in entries:
            # create full name of voter
            name = " ".join(entry[0:2])
            # get the party the person voted for
            party = entry[2]
            # add vote to dictionary if the vote is valid
            auth_vote(name, party, votes)
            
        return votes


def auth_vote(name, party, votes):
    """
    Adds the vote to the given dictionary if the vote is valid. A vote is valid if:
        (1) the person has not already voted; and
        (2) they have voted for 1 valid party
    -------------------------------------------------------------------------------
    Inputs:
        name -> str
        party -> str
        votes -> dict
    Outputs:
        None
    """
    if name not in votes and party in {'Pineapple Pizza Party', 'Pronounced Jiff Union', 'Socks and Crocs Reform League'}:
        votes[name] = party


def count_party_votes(votes):
    """
    Returns dictionary matching party to their number of votes.
    -------------------------------------------------------------------------------
    Inputs:
        votes: dict
    Outputs:
        vote_count: dict
    """
    vote_count = {'Pineapple Pizza Party': 0, 'Pronounced Jiff Union': 0, 'Socks and Crocs Reform League': 0}
    for person in votes:
        vote_count[votes[person]] += 1
    return vote_count


def run_Program(sourcePath):
    votes = create_dict_of_votes(sourcePath)
    vote_counts = count_party_votes(votes)
    # print(votes)
    return vote_counts