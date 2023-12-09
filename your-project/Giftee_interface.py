
import streamlit as st
import pandas as pd


# Load the giftee database outside of the main function
giftee = pd.read_csv("giftee_database.csv")

# Global variables to store state
receiver = None
kid_age = None
adult_hobbies = None
kid_hobbies = None
adult_book_genre = None
kid_book_genre = None
adult_game_type = None
kid_game_type = None
adult_sport_type = None
kid_sport_type = None
kid_budget = None
adult_budget = None


def main():
    global receiver, kid_age, adult_hobbies, kid_hobbies, adult_book_genre, kid_book_genre, adult_game_type, \
        kid_game_type, adult_sport_type, kid_sport_type, kid_budget, adult_budget

    st.title("Giftee")
    # Questionnaire Section

    with st.sidebar:
        st.header("Let's have a talk")
        receiver = st.selectbox("For whom are you looking for a gift?", ["", "A Man", "A Woman", "A Kid"])

        if receiver:
            if receiver == "A Kid":
                kid_age = st.selectbox("How old are they?", ["", "Below 6 years old", "Above 6 years old"])

                if kid_age:
                    kid_hobbies = st.selectbox("What are their hobbies?", ["", "Books", "Games", "Sports"])

                    if kid_hobbies:
                        show_kid_hobbies_sub_question(kid_hobbies)
                        show_kid_budget_followup()

            else:
                adult_hobbies = st.selectbox("What are their hobbies?", ["", "Books", "Games", "Sports"])

                if adult_hobbies:
                    show_adult_hobbies_sub_question(adult_hobbies)
                    show_adult_budget_followup()


    # Display the result
    st.write("We are ready for you! Please press Let's Go to start the search")


    # Create two columns for the "Clear" and "Let's Go" buttons
    col_restart, col_go = st.columns(2)

    # "Clear" button
    if col_restart.button("Restart"):
        st.rerun()

    # "Let's Go" button
    if col_go.button("Let's Go"):
        perform_search()


def show_adult_hobbies_sub_question(adult_hobbies_value):
    global adult_book_genre, adult_game_type, adult_sport_type
    if adult_hobbies_value == "Books":
        adult_book_genre = st.selectbox("What kind of book do they read?",
                                        ["", "art and design", "food and drink",
                                         "fiction", "crime", "education", "languages",
                                         "literature", "biography", "history", "business, economics and law",
                                         "music", "travel"])

    elif adult_hobbies_value == "Games":
        adult_game_type = st.selectbox("What kind of games do they play?",
                                       ["", "nintendo", "lego", "ps4"])

    elif adult_hobbies_value == "Sports":
        adult_sport_type = st.selectbox("What kind of sport do they play?",
                                        ["", "cycling", "running", "trekking",
                                         "swimming", "training", "football",
                                         "basketball", "padel", "tennis", "surfing"])


def show_kid_hobbies_sub_question(kid_hobbies_value):
    global kid_book_genre, kid_game_type, kid_sport_type
    if kid_hobbies_value == "Books":
        kid_book_genre = st.selectbox("What kind of book do they read?",
                                      ["", "fiction", "education", "languages", "literature", "music", "children's"])

    elif kid_hobbies_value == "Games":
        kid_game_type = st.selectbox("What kind of games do they play?",
                                     ["", "nintendo", "lego", "ps4"])

    elif kid_hobbies_value == "Sports":
        kid_sport_type = st.selectbox("What kind of sport do they play?",
                                      ["", "cycling", "running", "trekking", "swimming",
                                       "training", "football", "basketball", "padel", "tennis", "surfing"])


def show_adult_budget_followup():
    global adult_budget
    adult_budget = st.selectbox("What is your budget range for adults?",
                                ["", "<20 euros", "20-50 euros", ">50 euros"])


def show_kid_budget_followup():
    global kid_budget
    kid_budget = st.selectbox("What is your budget range for kids?",
                              ["", "<20 euros", "20-50 euros", ">50 euros"])


def perform_search():
    # search logic
    st.write("Certainly! Here are some suggestions for what you are looking for")

    # Get selected values
    gender = receiver
    age = kid_age
    hobbies = adult_hobbies if gender != "A Kid" else kid_hobbies
    book_genre = adult_book_genre if gender != "A Kid" else kid_book_genre
    game_type = adult_game_type if gender != "A Kid" else kid_game_type
    sport_type = adult_sport_type if gender != "A Kid" else kid_sport_type
    budget_range = declare_budget_range(kid_budget if gender == "A Kid" else adult_budget)

    st.write(f"Selected values - Gender: {gender}, Age: {age}, Hobbies: {hobbies}, "
             f"Book Genre: {book_genre}, Game Type: {game_type}, Sport Type: {sport_type}, Budget Range: {budget_range}")

    if hobbies == "Books":
        search_book(book_genre, budget_range)

    elif hobbies == "Games":
        search_game(game_type, age, budget_range)

    elif hobbies == "Sports":
        search_sport(sport_type, gender, budget_range)


def declare_budget_range(budget):
    if budget == "<20 euros":
        return 0, 20
    elif budget == "20-50 euros":
        return 20, 50
    elif budget == ">50 euros":
        return 50, 10000
    else:
        return 0
def display_images_in_table(df):
    st.markdown("<h2>Search Results:</h2>", unsafe_allow_html=True)
    html = "<div style='display: flex; flex-wrap: wrap;'>"

    for i, row in df.iterrows():
        html += f"<div style='margin: 10px;'><h3>Item {i + 1}</h3>"
        for col, value in row.items():
            if col == 'image':
                # Embed image using the image URL
                html += f"<img src='{value}' style='max-width:200px; max-height:200px; margin-bottom: 10px;'/>"
            else:
                html += f"<p><strong>{col}:</strong> {value}</p>"

        html += "</div>"

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)



def search_book(book_genre, budget_range):
    st.write(f"Searching for : {book_genre}, budget: {budget_range}")
    excluded_columns = ['collection', 'section', 'age_group']

    filtered_books = giftee[(giftee['group'] == 'books') &
                            (giftee['category'] == book_genre) &
                            (giftee['suggested_price(€)'].between(budget_range[0], budget_range[1]))]

    # Drop the excluded columns from the DataFrame
    filtered_books = filtered_books.drop(columns=excluded_columns, errors='ignore')

    # Check if there are enough items in the filtered DataFrame
    if len(filtered_books) < 1:
        st.write("We are sorry there is not enough options found. Would you mind adjusting your search criteria.")
    else:
        # Select a random sample of 10 books from the filtered DataFrame
        random_books = filtered_books.sample(n=min(10, len(filtered_books)), replace=False, random_state=42)

        st.write("Here are some suggestions:")
        display_images_in_table(random_books)


def search_game(game_type, age, budget_range):
    st.write(f"Searching {game_type} for : {age}, budget: {budget_range}")
    excluded_columns = ['author', 'collection', 'section',"category"]
    filtered_game = giftee[
        (giftee['group'] == 'games') &
        (giftee['category'] == game_type) &
        (
                (giftee['age_group'].isin(['1.5-3 year old', '4-5 year old','under 6 year old']) & (age == 'Below 6 years old')) |
                (~giftee['age_group'].isin(['1.5-3 year old', '4-5 year old','under 6 year old']) & (age == 'Above 6 years old'))
        ) &
        (giftee['suggested_price(€)'].between(budget_range[0], budget_range[1]))
        ]

    # Drop the excluded columns from the DataFrame
    filtered_game = filtered_game.drop(columns=excluded_columns, errors='ignore')
    # Select a random sample of 10 books from the filtered DataFrame
    random_game = filtered_game.sample(n=min(10, len(filtered_game)), random_state=42)

    st.write("Here are some suggestions:")
    display_images_in_table(random_game)


def search_sport(sport_type, gender, budget_range):
    st.write(f"Searching {sport_type} for : {gender}, budget: {budget_range}")

    excluded_columns = ['author','collection','age_group']

    filtered_sport = giftee[
        (giftee['group'] == 'sport') &
        (giftee['section'] == sport_type) &
        (
                (giftee['collection'].isin(['woman', 'adult',""]) & (gender == 'A Woman')) |
                (giftee['collection'].isin(['man', 'adult',""]) & (gender == 'A Man')) |
                (giftee['collection'].isin(['kid']) & (gender == 'A Kid'))
        ) &

        # (giftee['collection'] == collection_value) &
        (giftee['suggested_price(€)'].between(budget_range[0], budget_range[1]))]

    # Drop the excluded columns from the DataFrame
    filtered_sport= filtered_sport.drop(columns=excluded_columns, errors='ignore')
    # Select a random sample of 10 books from the filtered DataFrame
    random_sport = filtered_sport.sample(n=min(10, len(filtered_sport)), replace=False, random_state=42)

    st.write("Here are some suggestions:")
    display_images_in_table(random_sport)


# styling section
import base64

local_audio_path = "joyful-jingle-173919.mp3"

# Read the audio file
try:
    audio_data = open(local_audio_path, "rb").read()

    # Encode the audio file to base64
    audio_base64 = base64.b64encode(audio_data).decode("utf-8")

    # Display the audio
    st.audio(audio_data, format="audio/mp3")
except FileNotFoundError:
    st.error(f"File not found at: {local_audio_path}")

additional_css = """

h1 {
    margin-top: 1vh;
    font-size: 4.5em;
    color: rgb(219, 119, 52);
}

h2 {
    margin-top: 5vh; /* Adjusted value */
    text-align: center;
    font-size: 2em;
    color: #dbb134;
}

p {
    font-size: 2em;
    color: #dbb134;
}

.bouncing-image {
    position: fixed;
    bottom: 400px;
    left: 340px;
    animation: bounce 2s infinite;
    z-index: 2; /* Set a higher z-index for the bouncing image to make it appear in front */
  }

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-30px);
    }
    60% {
        transform: translateY(-15px);
    }
}
.bouncing-image img {
    width: 100px; 
    height: auto;
}

.bounce {
    position: fixed;
    bottom: 400px;
    right: 300px;
    animation: bounce 2s infinite;
    z-index: 2; /* Set a higher z-index for the bouncing image to make it appear in front */
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-30px);
    }
    60% {
        transform: translateY(-15px);
    }
}


.bounce img {
    width: 100px; 
    height: auto; 
}


.main{
    background: url("https://mcdn.wallpapersafari.com/medium/15/54/EFQ0dl.jpg") no-repeat center center fixed;
    background-size: cover;
    margin: 0;
    padding: 0;
    height: 100vh;
}

.st-emotion-cache-6qob1r {
    background: url("https://mcdn.wallpapersafari.com/medium/15/54/EFQ0dl.jpg") no-repeat center center fixed;
    background-size: cover;
    margin: 0;
    padding: 0;
    height: 100vh;
}


.walker {
    position: fixed;
    bottom: 0;
    left: -100px;
    width: 350px; 
    height: 250px;
    background: url('https://www.misskatecuttables.com/uploads/shopping_cart/10443/large_cute-flying-reindeer-pull-santa.png') no-repeat center center; /* Placeholder image for the figure */
    background-size: contain;
    animation: walk 10s linear infinite; 
    z-index: 1;
}

@keyframes walk {
    to {
        left: 100%; /* Move the figure to the right edge of the viewport */
    }
}

"""

additional_html = """
<style>
    {additional_css}
</style>

<div class="bouncing-image">
    <img src="https://www.pathstoliteracy.org/wp-content/uploads/2022/10/Gingerbreadman.png" alt="Bouncing Image">
</div>

<div class="bounce">
    <img src="https://annettescakesupplies.com/wp-content/uploads/2023/01/gingerbread-girl.png" alt="Bouncing Image">
</div>


<div class="walker"></div>

"""
# Display the HTML and CSS content in the Streamlit app using st.markdown
st.markdown(additional_html, unsafe_allow_html=True)
st.markdown(f'<style>{additional_css}</style>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()