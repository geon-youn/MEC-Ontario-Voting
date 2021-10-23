import csv
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'


votes = dict()  
vote_count = {'Pineapple Pizza Party': 0, 'Pronounced Jiff Union': 0, 'Socks and Crocs Reform League': 0}
parties_set = {
    'Pineapple Pizza Party', 'Pronounced Jiff Union', 'Socks and Crocs Reform League'
}


def create_dict_of_votes(file: str):
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
            if auth_vote(name, party, votes):
                votes[name] = party


def count_party_votes(votes: dict):
    """
    Returns dictionary matching party to their number of votes.
    """
    for person in votes:
        vote_count[votes[person]] += 1


def auth_vote(name: str, party: str, votes: dict) -> bool:
    """
    Returns if a vote is valid. A vote is valid if:
        (1) the person has not already voted; and
        (2) they have voted for ONE valid party
    """
    return not name in votes and party in parties_set


def update_vote(name: str, img_path: str, votes: dict, vote_count: dict) -> bool:
    """
    Adds a voter's vote.
    """
    # Authenticate voter's identity
    while not verify_image_id(name, image_to_text(img_path)):
        print("ERROR > could not detect your name in the given ID.\nPlease take a better photo or use a different ID.")
        img_path = input("Enter a new pathfile or exit by typing \"exit\": ")
        if img_path == "exit":
            return False
    
    # Have voter select a party
    print("Authenticated. Please vote for a party: (1) Pineapple Pizza Party, (2) Pronounced Jiff Union, (3) Socks and Crocs Reform League.")
    vote = 0
    while vote < 1 or vote > 3:
        try:
            vote = int(input("Enter a valid number (1, 2, or 3): "))
            if vote == 1 or vote == 2 or vote == 3:
                break
        except:
            continue
    if vote == 1:
        party = "Pineapple Pizza Party"
    elif vote == 2:
        party = "Pronounced Jiff Union"
    else:
        party = "Socks and Crocs Reform League"

    # Add voter's vote if they haven't already voted
    if auth_vote(name, party, votes):
        vote_count[party] += 1
        votes[name] = party
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


def save_votes_as_csv(filename: str, votes: dict) -> None:
    """
    Saves a dictionary as a csv file.
    """
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["First Name", "Last Name", "Vote"])
        for vote in votes.keys():
            entry = votes[vote]
            fst, snd = vote.split()
            writer.writerow([fst, snd, entry])


def update() -> None:
    """
    Updates the votes with new votes and removes invalid votes.
    """
    name = input("Full name: ")
    img_path = input("ID path file: ")
    if not update_vote(name, img_path, votes, vote_count):
        print(f"{name} has already voted.")
        return
    save_votes_as_csv("votingList.csv", votes)


def print_current_votes() -> None:
    """
    Prints the current votes for each party and the current winning parties.
    """
    m = 0
    for i in vote_count.keys():
        c = vote_count[i]
        if c > m:
            m = c
        print(f"{i}: {vote_count[i]} votes.")
    print("In the lead: ", end="")
    for i in vote_count.keys():
        if vote_count[i] == m:
            print(i, end=" ")
    print()


if __name__ == "__main__":
    create_dict_of_votes("votingList.csv")
    count_party_votes(votes)
    print_current_votes()
    while True:
        print()
        update()
        print()
        continue_question = input("Is there more (Y/n)? ")
        if continue_question == "n":
            break
    print()
    print_current_votes()