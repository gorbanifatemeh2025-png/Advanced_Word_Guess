"""
🎮 Word Guess Game - نسخه نهایی با API واقعی
"""

import random
import json
import csv
import os
import requests
from datetime import datetime

# ============================================
# لیست کلمات داخلی (فقط برای مواقعی که API کار نکنه)
# ============================================

WORD_LIST = [
    ("carpet", "object"), ("shirt", "object"), ("book", "object"),
    ("clock", "object"), ("table", "object"), ("chair", "object"),
    ("window", "object"), ("bottle", "object"), ("pencil", "object"),
    ("computer", "object"), ("keyboard", "object"), ("glasses", "object"),
    ("orange", "fruit"), ("apple", "fruit"), ("banana", "fruit"),
    ("grape", "fruit"), ("strawberry", "fruit"), ("melon", "fruit"),
    ("peach", "fruit"), ("pear", "fruit"),
    ("john", "boy_name"), ("peter", "boy_name"), ("ali", "boy_name"),
    ("reza", "boy_name"), ("mohammad", "boy_name"), ("hossein", "boy_name"),
    ("sarah", "girl_name"), ("maryam", "girl_name"), ("fatemeh", "girl_name"),
    ("zahra", "girl_name"), ("leila", "girl_name"), ("sara", "girl_name"),
    ("tiger", "animal"), ("lion", "animal"), ("elephant", "animal"),
    ("mouse", "animal"), ("rabbit", "animal"), ("giraffe", "animal"),
    ("red", "color"), ("blue", "color"), ("green", "color"),
    ("yellow", "color"), ("black", "color"), ("white", "color"),
]

# ============================================
# کلاس SettingsManager (JSON)
# ============================================

class SettingsManager:
    def __init__(self, filename="game_settings.json"):
        self.filename = filename
        self.settings = {"difficulty": "normal", "max_tries": 10}
        self.load()
        self.save()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.settings = json.load(f)
            except:
                self.settings = {"difficulty": "normal", "max_tries": 10}

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.settings, f, indent=2)

    def set_difficulty(self, level):
        levels = {"easy": 15, "normal": 10, "hard": 6, "impossible": 4}
        if level in levels:
            self.settings["difficulty"] = level
            self.settings["max_tries"] = levels[level]
            self.save()
            return True
        return False

    def get_max_tries(self):
        return self.settings.get("max_tries", 10)

    def get_difficulty_name(self):
        return self.settings.get("difficulty", "normal").capitalize()


# ============================================
# کلاس ScoreManager (CSV)
# ============================================

class ScoreManager:
    def __init__(self, filename="scores.csv"):
        self.filename = filename
        self.scores = []
        self.load()

    def load(self):
        self.scores = []
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["player", "word", "chances_used", "group_mode", "date"])
            return

        with open(self.filename, "r") as f:
            reader = csv.reader(f)
            try:
                next(reader)
            except StopIteration:
                return
            for row in reader:
                if row and len(row) >= 5:
                    try:
                        self.scores.append({
                            "player": row[0],
                            "word": row[1],
                            "chances_used": int(row[2]),
                            "group_mode": row[3] == "True",
                            "date": row[4]
                        })
                    except:
                        continue

    def save(self):
        with open(self.filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["player", "word", "chances_used", "group_mode", "date"])
            for score in self.scores:
                writer.writerow([
                    score["player"],
                    score["word"],
                    score["chances_used"],
                    score["group_mode"],
                    score["date"]
                ])

    def add_score(self, player, word, chances_used, group_mode):
        score = {
            "player": player,
            "word": word,
            "chances_used": chances_used,
            "group_mode": group_mode,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.scores.append(score)
        self.scores.sort(key=lambda x: x["chances_used"])
        self.save()


# ============================================
# کلاس Word (با API واقعی)
# ============================================

class Word:
    def __init__(self):
        self.word = ""
        self.word_group = ""
        self.letters = []
        self.display_word = []
        self.chances = 10
        self.original_chances = 10
        self.group_mode = False

    def get_word_from_api(self):
        """دریافت یک کلمه تصادفی از API"""
        try:
            response = requests.get("https://random-word-api.herokuapp.com/word", timeout=3)
            if response.status_code == 200:
                return response.json()[0].lower()
        except:
            pass
        return None

    def find_group_for_word(self, word):
        """پیدا کردن گروه یک کلمه از لیست داخلی"""
        for w, g in WORD_LIST:
            if w == word:
                return g
        return "unknown"

    def choose_word(self, group_mode=False, max_tries=10):
        """انتخاب کلمه با توجه به حالت"""
        self.group_mode = group_mode
        
        base_chances = max_tries
        self.chances = base_chances - (3 if group_mode else 0)
        if self.chances < 1:
            self.chances = 1
        self.original_chances = self.chances
        
        # 🔥 دریافت کلمه از API
        word = self.get_word_from_api()
        
        if word:
            # ✅ کلمه از API اومده
            self.word = word
            if group_mode:
                self.word_group = self.find_group_for_word(word)
            else:
                self.word_group = ""
        else:
            # ❌ API کار نکرد، از لیست داخلی استفاده کن
            word, group = random.choice(WORD_LIST)
            self.word = word
            self.word_group = group if group_mode else ""
        
        self.letters = list(self.word)
        self.display_word = ["_"] * len(self.word)

    def show_group(self):
        if self.group_mode and self.word_group:
            return f"📁 Category: {self.word_group}"
        return ""

    def get_chances(self):
        return self.chances

    def decrease_chance(self):
        self.chances -= 1
        return self.chances

    def game_lose(self):
        if self.chances <= 0:
            print(f"\n😢 Game Over! The word was: {self.word}")
            if self.group_mode:
                print(f"📁 Category: {self.word_group}")
            return True
        return False

    def game_win(self):
        if self.display_word == list(self.word):
            print(f"\n🎉 Congratulations! You guessed '{self.word}'!")
            if self.group_mode:
                print(f"📁 Category: {self.word_group}")
            return True
        return False


# ============================================
# کلاس Choose (بازی اصلی)
# ============================================

class Choose:
    def __init__(self):
        self.word = Word()
        self.settings = SettingsManager()
        self.scores = ScoreManager()

    def guess(self):
        max_tries = self.settings.get_max_tries()
        difficulty_name = self.settings.get_difficulty_name()

        print("\n" + "=" * 50)
        print("🎮 WORD GUESS GAME - SETUP")
        print("=" * 50)
        print(f"📊 Current Difficulty: {difficulty_name} ({max_tries} chances)")
        print("-" * 50)
        print("1. With category (easier, -3 chances)")
        print("2. Without category (harder, normal chances)")

        mode = input("\nChoose your mode (1-2): ").strip()

        group_mode = False
        if mode == "1":
            group_mode = True
        elif mode == "2":
            group_mode = False
        else:
            print("❌ Invalid! Using default mode (no category).")
            group_mode = False

        final_chances = max_tries - (3 if group_mode else 0)
        if final_chances < 1:
            final_chances = 1

        print(f"\n📊 Difficulty: {difficulty_name}")
        print(f"📊 Base chances: {max_tries}")
        print(f"📊 Final chances: {final_chances} ({'-3' if group_mode else '0'} for category)")

        # انتخاب کلمه
        self.word.choose_word(group_mode=group_mode, max_tries=max_tries)

        print("\n" + "=" * 50)
        print("🎮 WORD GUESS GAME")
        print("=" * 50)

        if group_mode:
            print("📁 Category mode: Category is shown to help you!")
            print(self.word.show_group())
        else:
            print("📁 Simple mode: No category, just guess the word")

        print(f"📝 Word: {' '.join(self.word.display_word)}")
        print(f"📏 Word has {len(self.word.letters)} letters")
        print(f"❤️ Chances: {self.word.get_chances()}")
        print("-" * 30)

        while True:
            guess = input("\n🔤 Guess a letter: ").lower()

            if not guess.isalpha() or len(guess) != 1:
                print("❌ Please enter a single letter!")
                continue

            if guess in self.word.letters:
                print("✅ Correct letter!")
                for i, letter in enumerate(self.word.letters):
                    if letter == guess:
                        self.word.display_word[i] = guess
                print(f"📝 Word: {' '.join(self.word.display_word)}")
                
                if self.word.game_win():
                    chances_used = self.word.original_chances - self.word.chances
                    name = input("Enter your name: ").strip() or "Anonymous"
                    self.scores.add_score(name, self.word.word, chances_used, group_mode)
                    break
            else:
                print("❌ Wrong letter!")
                remaining = self.word.decrease_chance()
                print(f"❤️ Remaining chances: {remaining}")
                if self.word.game_lose():
                    break


# ============================================
# برنامه اصلی
# ============================================

def main():
    settings = SettingsManager()

    print("""
    ██╗    ██╗ ██████╗ ██████╗ ██████╗ 
    ██║    ██║██╔═══██╗██╔══██╗██╔══██╗
    ██║ █╗ ██║██║   ██║██████╔╝██║  ██║
    ██║███╗██║██║   ██║██╔══██╗██║  ██║
    ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
    """)

    while True:
        print("\n" + "=" * 50)
        print("🎮 WORD GUESS GAME")
        print("=" * 50)
        print("1. Start new game")
        print("2. Change difficulty")
        print("3. Exit")
        print("=" * 50)

        choice = input("Choose: ")

        if choice == "1":
            game = Choose()
            game.guess()
            input("\nPress Enter to continue...")

        elif choice == "2":
            print("\n🎯 Difficulty Levels:")
            print("1. Easy (15 chances)")
            print("2. Normal (10 chances)")
            print("3. Hard (6 chances)")
            print("4. Impossible (4 chances)")

            diff_choice = input("Choose difficulty: ")
            diff_map = {"1": "easy", "2": "normal", "3": "hard", "4": "impossible"}
            if diff_choice in diff_map:
                settings.set_difficulty(diff_map[diff_choice])
                print(f"✅ Difficulty changed to {diff_map[diff_choice].capitalize()}!")
            else:
                print("❌ Invalid choice!")

        elif choice == "3":
            print("👋 Thanks for playing!")
            break

        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()
