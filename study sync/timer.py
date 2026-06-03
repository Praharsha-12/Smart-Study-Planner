import time
import os

def start_pomodoro(minutes=25):
    """Counts down from a specified number of minutes."""
    seconds = minutes * 60
    while seconds > 0:
        # Calculate minutes and seconds left
        mins, secs = divmod(seconds, 60)
        # Format the timer display as MM:SS
        timer_display = f"{mins:02d}:{secs:02d}"
        
        # Print timer over the same line in terminal
        print(f"Focus Time Remaining: {timer_display}", end="\r")
        
        time.sleep(1)
        seconds -= 1
    
    print("\n🔔 Time's up! Take a short break.")
