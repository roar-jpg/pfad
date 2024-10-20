import streamlit as st
import random

# Function to check if the input is a valid integer between low bound and high bound
def is_valid_guess(guess, low, high):
    try:
        guess = int(guess)
        if low <= guess <= high:
            return guess
        else:
            st.error(f"Please input a number between {low} and {high}.")
    except ValueError:
        st.error("Invalid input. Please input an integer.")
    return None

# Main function for the game
def guessing_game():
    # Initialize or retrieve variables; default to set guess number bound between 1 and 100. 4 round of guesses.
    if "ans" not in st.session_state:
        st.session_state.ans = random.randint(1, 100)
        st.session_state.low = 1
        st.session_state.high = 100
        st.session_state.guesses = []
        st.session_state.round = 1  # Start from 1
        st.session_state.game_over = False

    # Game title and game rule
    st.title("Number Guessing Game")
    st.write("Make a guess between 1 and 100!")
    # print(st.session_state.ans) # checking purpose only

    # User input for guess
    user_guess = st.text_input("Enter your guess:", key="input_guess")

    # Run game logic only if user provides input and game is not over
    if user_guess and not st.session_state.game_over:
        valid_guess = is_valid_guess(user_guess, st.session_state.low, st.session_state.high)

        # Check if the guess is valid
        if valid_guess is not None:
            # Check if the guess has already been made
            if valid_guess in [int(g.split("'")[1]) for g in st.session_state.guesses if "'" in g]:
                st.warning("You've already guessed that number! Please try a different one.")
            else:
                # Store the guess in the history
                st.session_state.guesses.append(f"You have guessed '{valid_guess}'.")

                # Check if the guess is correct
                if valid_guess == st.session_state.ans:
                    st.session_state.guesses.append("Congratulations! You made it!")  # Store correct guess message
                    st.session_state.game_over = True
                else:
                    st.session_state.guesses.append("Your guess is wrong!")  # Store wrong guess message

                    # Update low bound or high bound to narrow the guess range
                    if st.session_state.low <= st.session_state.ans < valid_guess:
                        st.session_state.high = valid_guess  # Update 'high' if 'ans' is between low bound and the guess
                    elif valid_guess < st.session_state.ans <= st.session_state.high:
                        st.session_state.low = valid_guess  # Update 'low' if 'ans' is between the guess and high bound

                # Increment round after processing a valid guess
                st.session_state.round += 1

                # Check if the game is over due to the number of rounds
                if st.session_state.round > 4:
                    st.session_state.guesses.append(f"Game over! The correct answer was {st.session_state.ans}.")
                    st.session_state.game_over = True
                
                # Display the current bounds and remaining guesses
                if not st.session_state.game_over:
                    guesses_left = 4 - st.session_state.round + 1  # 4 rounds total
                    bounds_message = f"Current bounds: {st.session_state.low} to {st.session_state.high}. You have {guesses_left} guesses left."
                    st.session_state.guesses.append(bounds_message)  # Store bounds message in history

    # Display the history of guesses and responses
    if st.session_state.guesses:
        st.write("Response History:")
        for idx, response in enumerate(st.session_state.guesses, 1):
            st.write(f"{idx}. {response}")

# Start the game
if __name__ == "__main__":
    guessing_game()