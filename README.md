# Group20_HIT137_Assignment_2
CDU HIT137 Group 20 Assignment 2 

This repository contains the group submission for HIT137 Assignment 2.

All work has been developed collaboratively and tracked using GitHub version control, as required by the assignment brief.


## Repository Structure

```text
HIT137-Assignment-2/
├── question_1/
│   ├── text_encryption.py
│   ├── raw_text.txt
│   ├── encrypted_text.txt
│   └── decrypted_text.txt
│
├── question_2/
│   ├── temperature_analysis.py
│   ├── temperatures/
│   ├── average_temp.txt
│   ├── largest_temp_range_station.txt
│   └── temperature_stability_stations.txt
│
├── question_3/
│   └── turtle_pattern.py
│
├── github_link.txt
└── README.md
```

## Question 1 – Text Encryption and Decryption

This program reads text from raw_text.txt, encrypts it using a rule-based character shifting algorithm, writes the encrypted result to encrypted_text.txt, then decrypts the content back into decrypted_text.txt.

A verification step confirms whether the decrypted text matches the original input file.

How to run:
python question_1/text_encryption.py


## Question 2 – Australian Temperature Data Analysis

This program processes multiple CSV files containing temperature data from Australian weather stations.

It calculates:
- Seasonal average temperatures across all stations and years
- The station(s) with the largest temperature range
- The most stable and most variable stations based on standard deviation

Results are written to text files in the question_2 directory.

How to run:
python question_2/temperature_analysis.py


## Question 3 – Recursive Turtle Graphics Pattern

This program uses Python's turtle graphics module and recursion to generate a geometric pattern based on user-defined parameters.

The user is prompted for:
- Number of polygon sides
- Side length
- Recursion depth

How to run:
python question_3/turtle_pattern.py


## Notes
- All programs are written in Python 3
- The repository is public as required by the assignment
- Contributions from all group members are tracked via GitHub commit history

