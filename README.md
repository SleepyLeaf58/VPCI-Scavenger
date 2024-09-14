# HTN 2024 Scavenger Hunt

## What is Scavenger Hunt?
Scavenger Hunt is a tool to create and join scavenger hunt games to help students learn and get acclimatized to the campus. 

## How does it work?
Users can create a game room by submitting a form, and join open game rooms 

## Tools used
### HTML/CSS (Bootstrap)
HTML/CSS makes up most of our front-end, with many components from Bootstrap
### Groq
Groq powers our riddle generator
### mappedin
Mappedin
### Genesys
When players find an item, they send an image to a Genesys survey, where it can be verified by an organizer/moderator
### Flask
Flask is our back-end idk

## Features
* Some sort of user needs to be created to join the scavenger
  * User needs to be able to submit a “find” of an item
  * This should ideally be timetracked
Needs both an organizer account and a player account
Probably need to have a list of open scavenger hunts
Need a way to generate an object item and place it on the map at some location
Need a way to verify that they have found the object?
Does not need to be checked with image recognition, we could totally just get them to send an image on a Genesys survey form or something
A teacher/coordinator can verify
Perhaps the user could have 2 riddle/hunts open at a time, and they must find an object to get the next revealed
Groq AI to generate hints for items
Organizer can specify location and item to generate interestingly themed hints
Needs description of how the item is hidden such that we can generate more interesting and revealing hints

* Winners
  * The first player to find each object wins 2 points
  * The first player to find all the objects wins 5 points
* There is a MappedIn map implementation to help players locate rooms

## Steps

### Organizers
Start a hunt
List of objects
Specify object
Specify room
Maybe riddle depending on time
Share the game to the players
Verify

### Players
1. Find and join a game on the join game tab
2. Enter your username for leaderboard purposes
3. Get your first hint, and find potential rooms on MappedIn
4. Submit a photo of your item to a survey on Genesys
(Item has a code on it attached)
5. If your item is accepted, recieve a hint for the next item
6. Repeat until someone finds all the items!

### Code of Conduct
1. Safety first! We know that scavenger hunts are exciting, espcially when the race is close, but make sure safety comes first! You have the opportinuity to play as many scavenger hunts as you want, but only one life!
2. HAVE FUN! Transitioning to university is stressful (but fun), and we want to make sure you have fun!



