import sqlite3
import datetime
import tkinter as tk

window = tk.Tk() # Create the main window
window.title("Custom Window") # Set the title of the window
window.geometry("400x300") # Set the window size (width x height)

label = tk.Label(window, text="Welcome to Bench Bloopers") # Add a label widget to window
label.pack(pady=20) # Add padding around label

button = tk.Button(window, text="Click Me", command=lambda: print("Button clicked!")) # Add a button to the window
button.pack(pady=10)

window.mainloop() # Run the Tkinter event loop to display window

# Set up the database
def create_db():
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS health_goals (
            id INTEGER PRIMARY KEY,
            water_goal INTEGER,
            exercise_goal INTEGER,
            sleep_goal INTEGER,
            streak INTEGER,
            last_logged_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Add a new user
def add_user(water_goal, exercise_goal, sleep_goal):
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO health_goals (water_goal, exercise_goal, sleep_goal, streak, last_logged_date)
        VALUES (?, ?, ?, 0, ?)
    ''', (water_goal, exercise_goal, sleep_goal, str(datetime.date.today())))
    conn.commit()
    conn.close()

# Log progress
def log_progress(water_intake, exercise_time, sleep_hours):
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()

    # Fetch the user's last logged data
    c.execute('SELECT * FROM health_goals ORDER BY id DESC LIMIT 1')
    user_data = c.fetchone()

    if user_data:
        # Check if we are still in the streak
        last_logged_date = user_data[5]
        today = str(datetime.date.today())

        # If we logged yesterday's data, increase streak
        if last_logged_date == str(datetime.date.today() - datetime.timedelta(days=1)):
            streak = user_data[4] + 1
        else:
            streak = 1  # Reset streak if we missed a day

        # Update the record
        c.execute('''
            UPDATE health_goals
            SET water_goal = ?,
                exercise_goal = ?,
                sleep_goal = ?,
                streak = ?,
                last_logged_date = ?
            WHERE id = ?
        ''', (water_intake, exercise_time, sleep_hours, streak, today, user_data[0]))
        conn.commit()

        print(f"Streak: {streak} days")
        if streak >= 7:
            print("🎉 Congrats! You hit a 7-day streak! You've earned a bonus!")

    else:
        print("User not found.")
    
    conn.close()

# View today's progress
def view_progress():
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()
    c.execute('SELECT * FROM health_goals ORDER BY id DESC LIMIT 1')
    user_data = c.fetchone()

    if user_data:
        print(f"Today's Progress:")
        print(f"Water Goal: {user_data[1]} oz")
        print(f"Exercise Goal: {user_data[2]} minutes")
        print(f"Sleep Goal: {user_data[3]} hours")
        print(f"Streak: {user_data[4]} days")
    else:
        print("No user data found.")

    conn.close()

# Main function for the health tracker
def main():
    create_db()

    # Uncomment below to add a new user (run once to initialize)
    # add_user(64, 30, 8)  # Example: 64 oz of water, 30 min exercise, 8 hours sleep

    while True:
        print("\nHealth Habit Fitness Tracker")
        print("1. Log Progress")
        print("2. View Today's Progress")
        print("3. Exit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            water = int(input("Enter water intake in oz: "))
            exercise = int(input("Enter exercise time in minutes: "))
            sleep = int(input("Enter sleep time in hours: "))
            log_progress(water, exercise, sleep)
        elif choice == "2":
            view_progress()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
