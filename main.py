
import os
import sqlite3
import subprocess
import urllib.request

def grade_calculator():
    print("\n--- Student Grade Calculator ---")

    student = input("Enter student name: ")
    grade = input("Enter grade: ")

    print(f"{student} received {grade}")


def campus_announcements():
    print("\n--- Campus Announcements ---")

    announcements = [
        "Welcome to the new semester!",
        "Library hours: 8 AM - 10 PM",
        "Join the campus coding club!"
    ]

    for announcement in announcements:
        print(announcement)


def study_calculator():
    print("\n--- Study Time Calculator ---")

    hours = float(input("Hours studied: "))
    days = int(input("Number of days: "))

    print("Total study hours:", hours * days)


def student_notes():
    print("\n--- Student Notes ---")

    filename = input("Enter notes filename: ")

    with open(filename, "r") as file:
        print(file.read())


def database_search():
    print("\n--- Student Database Search ---")

    name = input("Enter student name: ")

    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE students (name TEXT)"
    )
    connection.execute(
        "INSERT INTO students VALUES ('Alice')"
    )

    query = "SELECT * FROM students WHERE name = '" + name + "'"
    result = connection.execute(query).fetchall()

    print(result)
    connection.close()


def network_lookup():
    print("\n--- Campus Network Lookup ---")

    url = input("Enter a website URL: ")

    response = urllib.request.urlopen(url, timeout=3)
    print(response.status)


def system_information():
    print("\n--- System Information ---")

    command = input("Enter a system command: ")

    subprocess.run(command, shell=True)


def main():
    while True:
        print("\n==============================")
        print("       CAMPUS TOOLKIT")
        print("==============================")
        print("1. Grade Calculator")
        print("2. Campus Announcements")
        print("3. Study Time Calculator")
        print("4. Student Notes")
        print("5. Database Search")
        print("6. Network Lookup")
        print("7. System Information")
        print("8. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            grade_calculator()
        elif choice == "2":
            campus_announcements()
        elif choice == "3":
            study_calculator()
        elif choice == "4":
            student_notes()
        elif choice == "5":
            database_search()
        elif choice == "6":
            network_lookup()
        elif choice == "7":
            system_information()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
