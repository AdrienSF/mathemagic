# mathemagic
Using number theory and brute force computation, this project is used to aid a performer in giving a participant the illusion of choice.

## Installation
From the "executables" folder of this repository, download the file cooresponding to your operating system.<br>
The executable requires [Latex](https://www.latex-project.org/get/) to be installed on your system.

## Performer Guide
TODO

## Usage
To start the program, simply run the previously downloaded executable.

### First Round
You will then be asked to input the participant’s revealed digits (no spaces). The program assumes that the performer chooses 63 as their number and that the participant never chooses a zero as the digit of the product to keep secret.

After pressing enter, the program will either find the participants number and jump to the matrix section, or display a few possibilities for the secret number and proceed to the second round.

### Second Round
The program will display a list of choices to give to the participant, and ask for which one the participant chose. After pressing enter, the program will ask for the digits the participant revealed (again, enter the digits without spaces). Once this is entered, the secret number will be displayed and the program will proceed to the matrix section.

### Matrix Section
The program generates a file named "matrices.pdf" containing a number of different forcing matrices, and asks you which one the participant chose. Once this is entered, "select_entries.csv" will be generated. Edit this spreadsheet by adding a '*' to any entries that should remain invariant. Some entries are invariant by default, and are marked with brackets: '[]'. When you are done marking invariant entries, save the spreadsheet and press enter in the terminal prompt. You will then be asked for comfirmation, and then asked if the participant's forcing matrix should be scrambled. Press enter at the command line prompt to scramble the forcing matrix, and the program exits shortly.

## Analysis
In the first round, assuming the performer chooses 63, the program will narrow down the secret number to at most 4 possibilities. If another 2 digit multiple of 9 is chosen instead of 63, we will not be able to narrow down the secret number as much. This is why 63 is the preferred number for the performer to choose.

42% of the time, the first round will narrow down the secret number to just one possibility, below is the exact data. The left side shows the secret number chosen by the participant, and the right side shows what possibilities the program would find in that situation.

secret: 1 => possibilities: {1}<br>
secret: 2 => possibilities: {2}<br>
secret: 3 => possibilities: {3, 13}<br>
secret: 4 => possibilities: {4}<br>
secret: 5 => possibilities: {5}<br>
secret: 6 => possibilities: {6}<br>
secret: 7 => possibilities: {7}<br>
secret: 8 => possibilities: {8}<br>
secret: 9 => possibilities: {9, 12}<br>
secret: 10 => possibilities: {10}<br>
secret: 11 => possibilities: {11}<br>
secret: 12 => possibilities: {9, 12}<br>
secret: 13 => possibilities: {3, 13}<br>
secret: 14 => possibilities: {14}<br>
secret: 15 => possibilities: {15}<br>
secret: 16 => possibilities: {16}<br>
secret: 17 => possibilities: {17, 27}<br>
secret: 18 => possibilities: {18}<br>
secret: 19 => possibilities: {19}<br>
secret: 20 => possibilities: {32, 20}<br>
secret: 21 => possibilities: {37, 51, 21}<br>
secret: 22 => possibilities: {26, 22}<br>
secret: 23 => possibilities: {78, 23}<br>
secret: 24 => possibilities: {24}<br>
secret: 25 => possibilities: {25}<br>
secret: 26 => possibilities: {26, 22}<br>
secret: 27 => possibilities: {17, 27}<br>
secret: 28 => possibilities: {98, 28}<br>
secret: 29 => possibilities: {29}<br>
secret: 30 => possibilities: {30}<br>
secret: 31 => possibilities: {57, 31}<br>
secret: 32 => possibilities: {32, 20}<br>
secret: 33 => possibilities: {33, 43}<br>
secret: 34 => possibilities: {34, 67}<br>
secret: 35 => possibilities: {40, 35}<br>
secret: 36 => possibilities: {36}<br>
secret: 37 => possibilities: {37, 51, 21}<br>
secret: 38 => possibilities: {38}<br>
secret: 39 => possibilities: {75, 39}<br>
secret: 40 => possibilities: {40, 35}<br>
secret: 41 => possibilities: {56, 41, 45}<br>
secret: 42 => possibilities: {42, 74}<br>
secret: 43 => possibilities: {33, 43}<br>
secret: 44 => possibilities: {44}<br>
secret: 45 => possibilities: {56, 41, 45}<br>
secret: 46 => possibilities: {46}<br>
secret: 47 => possibilities: {47}<br>
secret: 48 => possibilities: {64, 48, 54}<br>
secret: 49 => possibilities: {49, 60}<br>
secret: 50 => possibilities: {81, 50}<br>
secret: 51 => possibilities: {37, 51, 21}<br>
secret: 52 => possibilities: {99, 52}<br>
secret: 53 => possibilities: {53}<br>
secret: 54 => possibilities: {64, 48, 54}<br>
secret: 55 => possibilities: {72, 58, 55}<br>
secret: 56 => possibilities: {56, 41, 45}<br>
secret: 57 => possibilities: {57, 31}<br>
secret: 58 => possibilities: {72, 58, 55}<br>
secret: 59 => possibilities: {59}<br>
secret: 60 => possibilities: {49, 60}<br>
secret: 61 => possibilities: {61}<br>
secret: 62 => possibilities: {62}<br>
secret: 63 => possibilities: {63}<br>
secret: 64 => possibilities: {64, 48, 54}<br>
secret: 65 => possibilities: {65}<br>
secret: 66 => possibilities: {66, 77, 86, 87}<br>
secret: 67 => possibilities: {34, 67}<br>
secret: 68 => possibilities: {68}<br>
secret: 69 => possibilities: {69, 71}<br>
secret: 70 => possibilities: {70}<br>
secret: 71 => possibilities: {69, 71}<br>
secret: 72 => possibilities: {72, 58, 55}<br>
secret: 73 => possibilities: {73}<br>
secret: 74 => possibilities: {74, 42}<br>
secret: 75 => possibilities: {75, 39}<br>
secret: 76 => possibilities: {76}<br>
secret: 77 => possibilities: {66, 77, 86, 87}<br>
secret: 78 => possibilities: {78, 23}<br>
secret: 79 => possibilities: {79}<br>
secret: 80 => possibilities: {80}<br>
secret: 81 => possibilities: {81, 50}<br>
secret: 82 => possibilities: {82}<br>
secret: 83 => possibilities: {83, 84, 94}<br>
secret: 84 => possibilities: {83, 84, 94}<br>
secret: 85 => possibilities: {85}<br>
secret: 86 => possibilities: {66, 77, 86, 87}<br>
secret: 87 => possibilities: {66, 77, 86, 87}<br>
secret: 88 => possibilities: {88}<br>
secret: 89 => possibilities: {89, 90}<br>
secret: 90 => possibilities: {89, 90}<br>
secret: 91 => possibilities: {91}<br>
secret: 92 => possibilities: {92}<br>
secret: 93 => possibilities: {93, 95}<br>
secret: 94 => possibilities: {83, 84, 94}<br>
secret: 95 => possibilities: {93, 95}<br>
secret: 96 => possibilities: {96}<br>
secret: 97 => possibilities: {97}<br>
secret: 98 => possibilities: {98, 28}<br>
secret: 99 => possibilities: {99, 52}<br>
