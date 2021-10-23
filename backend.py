import csv
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

votes = dict()  

def create_dict_of_votes(file: str) -> dict:
    """
    Creates a dictionary from the given csv file of votes.
    """
    with open(file) as csvfile:
        entries = csv.reader(csvfile)
        header = next(entries)
        # add valid entries to the dictionary
        for entry in entries:
            # create full name of voter
            name = " ".join(entry[0:2])
            # get the party the person voted for
            party = entry[2]
            # add vote to dictionary if the vote is valid
            auth_vote(name, party, votes)
            
        return votes


def auth_vote(name: str, party: str, votes: dict) -> bool:
    """
    Adds the vote to the given dictionary if the vote is valid. A vote is valid if:
        (1) the person has not already voted; and
        (2) they have voted for 1 valid party
    """
    return not (name in votes) and (party in {'Pineapple Pizza Party', 'Pronounced Jiff Union', 'Socks and Crocs Reform League'})


def count_party_votes(votes: dict) -> dict:
    """
    Returns dictionary matching party to their number of votes.
    """
    vote_count = {'Pineapple Pizza Party': 0, 'Pronounced Jiff Union': 0, 'Socks and Crocs Reform League': 0}
    for person in votes:
        vote_count[votes[person]] += 1
    return vote_count


def update_vote(name: str, party: str, votes: dict, vote_count: dict) -> bool:
    """
    Adds a voter's vote to the total (assuming their id is correct).
    """
    if auth_vote(name, party, votes):
        vote_count[party] += 1
        return True
    return False


def image_to_text(img_path: str) -> str:
    """
    Takes an image and returns the text inside the image.
    """
    img = cv2.imread(img_path)
    return pytesseract.image_to_string(img)


def verify_image_id(name: str, img_text: str) -> bool:
    """
    Verifies if the voter's first and last name are present in the image.
    """
    fst, snd = name.lower().split()
    text = img_text.lower()
    return fst in text and snd in text


def save_csv_file(votes: dict) -> None:
    """
    Saves the csv file containing all the votes
    """
    with open("votingList.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["First Name", "Last Name", "Vote"])
        for vote in votes.keys():
            entry = votes[vote]
            fst, snd = vote.split()
            writer.writerow([fst, snd, entry])

def run_Program(sourcePath):
    votes = create_dict_of_votes(sourcePath)
    vote_counts = count_party_votes(votes)
    # print(votes)
    save_csv_file(votes)
    return vote_counts
