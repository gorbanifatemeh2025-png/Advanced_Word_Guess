# 🎮 Word Guess Game

An advanced word guessing game written in Python. Guess the hidden word letter by letter before you run out of chances!

============================

## ✨ Features

**Real API Integration:** Fetches random words from an online API for endless variety.

**Offline Fallback:** Uses a built-in word list when the API is unavailable.

**Category Mode:** Play with a category hint (easier) or without it (harder).

**Four Difficulty Levels:** Easy, Normal, Hard, and Impossible.

**Score Tracking:** All scores are saved automatically in a CSV file.

**Persistent Settings:** Your difficulty preference is saved between sessions.

===========================

## 🎯 Difficulty Levels
Level : Chances
Easy : 15
Normal : 10
Hard : 6
Impossible : 4

Note: Choosing category mode reduces your chances by 3.

===========================

## 🎮 How to Play

Choose your mode (with or without category).

A word is selected and displayed as underscores.

Guess one letter at a time.

Correct letters are revealed in their positions.

Wrong letters cost you a chance.

Win by guessing all letters before running out of chances.

===========================

## 📁 Files Created by the Program

game_settings.json
Stores your difficulty preference and max tries.

scores.csv
Stores all game scores with player name, word, chances used, and date.

===========================

## 🛠️ Technologies Used
Python 3

Requests library for API calls

JSON for settings storage

CSV for score tracking

Object-Oriented Programming (OOP)

===========================

## 🚀 How to Run

First, install the required library:

```bash
pip install requests