"""Sofware for Apache airlines"""
import sqlite3 #importing sqlite3 for connecting python with sqlite code
import string #importing string for checking the string variables
import random #importing random for taking random alphanumerics for reference number

#class for delivering process with database
class Database:
    #initializing connection with database and python program.
    def __init__(self):
        self.conn = sqlite3.connect("airline.db")
        self.cursor = self.conn.cursor()
        self.create_table()
   #define function for creating table
    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_ref TEXT PRIMARY KEY,
            passport TEXT,
            first_name TEXT,
            surname TEXT,
            seat_row INTEGER,
            seat_col TEXT
        );
        """)
        self.conn.commit()
    #define function for adding new data into database
    def insert_booking(self, booking_ref, passport, first_name, surname, seat_row, seat_col):
        self.cursor.execute("""
        INSERT INTO bookings (booking_ref,passport, first_name, surname, seat_row, seat_col)
                            VALUES (?, ?, ?, ?, ?, ?)""", (booking_ref, passport, first_name, surname, seat_row, seat_col)
        )
        self.conn.commit()
    #define function for deleting the booked data from dataset
    def delete_booking(self, booking_ref):
        self.cursor.execute("""
        DELETE FROM bookings WHERE booking_ref=?""",(booking_ref,))
        self.conn.commit()

    # define function that returns exisitng reference numbers
    def references(self):
        self.cursor.execute("""
        SELECT booking_ref FROM bookings;
        """)
        exisitng_refs={row[0] for row in self.cursor.fetchall()}
        return exisitng_refs
    #define function that returns the booked seats data
    def booking_status(self):
        self.cursor.execute("SELECT seat_row, seat_col FROM bookings")
        rows=self.cursor.fetchall()
        booked_seats=[]
        for seat_row,seat_col in rows:
            seat_id=str(seat_row)+seat_col
            booked_seats.append(seat_id)
        return booked_seats
    #define function that return reference number of booked seats based on seatnumber
    def reference_booked(self, seatnum):
        row=int(seatnum[:-1])
        col=seatnum[-1]
        self.cursor.execute("""
        SELECT booking_ref FROM bookings WHERE seat_row=? AND seat_col=?""" ,(row,col))
        ref=self.cursor.fetchone()
        return ref
    #define function that returns users details from dataset according to booking reference
    def user_details(self,booking_ref):
        self.cursor.execute("""
        SELECT passport, first_name,surname FROM bookings WHERE booking_ref=?""",(booking_ref,))
        name=self.cursor.fetchone()
        if name is None:
            return None
        return name[0],name[1], name[2]
    #define function that returns passport detail of seat owner who booked
    def user_passport(self,booking_ref):
        self.cursor.execute("""
        SELECT passport FROM bookings WHERE booking_ref=?""",(booking_ref,))
        passport=self.cursor.fetchone()
        if passport is None:
            return None
        return passport[0]

    #define function that closes the connection with dataset
    def close(self):
        self.conn.close()

#define class for generating reference number
class Reference:
    #define functionf or creating unique reference numbers
    def generate_unique_id(self,existing_refs):
        self.existing_refs=existing_refs
        #string.ascii_letters gives Capital letters
        #string.digits  gives all digital number (0,1,2,3...9)
        characters = string.ascii_letters + string.digits

        while True:
            reference="".join(random.choices(characters, k=8))

            if reference not in self.existing_refs:
                return reference

#class for creating seats and showing them
class Seats:
    def __init__(self):
        self.seats={} #initializing seats
        self.database=Database()

    #define function that creates seats
    def create_seats(self):
        cols=["A","B","C","D","E","F"] #rows for identifying seats
        for col in cols:
            for row in range(1,81): # iterating for demanded seats
                seat_id=f"{row}{col}"
                if col in ("D","E","F") and row>=77:
                    self.seats[seat_id]="S"
                else:
                    self.seats[seat_id]="F"
        # return self.seats

     # checking the already booked seats in the database
    def check_bookedSeats(self):
        bookedSeats = self.database.booking_status()
        for seat in self.seats:
            if seat in bookedSeats:
                self.seats[seat] = "R"
        return self.seats

    #function to show seats for user
    def show_seats(self):

        seats=self.seats
        print("   A     B     C     X     D     E     F   ")
        print(" ----------------------------------------")
        for seat in range(1, 81):
            print(
                f"{seat:2}"
                f" {seats[f'{seat}A']}     {seats[f'{seat}B']}     {seats[f'{seat}C']}     X     {seats[f'{seat}D']}     {seats[f'{seat}E']}     {seats[f'{seat}F']} "
            )

#class for choosing the seats according to preference
class SeatSelection:
    def __init__(self,seats):
        self.seats=seats #loading the seat
    #define function that will show the seats located near the window
    def window_seats(self):
        print(" WINDOWS SEATS seats")
        print(" A     F")
        print(" -------")
        for seat in range(1, 81):
            print(
                f"{seat:2}"
                f" {self.seats[f'{seat}A']}     {self.seats[f'{seat}F']}"
            )
    #define function that will show seats located in the middle
    def aisle_adjacent_seats(self):
        print("AISLE ADJACENT SEATS")
        print(" C     D")
        print(" -------")
        for seat in range(1, 81):
            print(
                f"{seat:2}"
                f" {self.seats[f'{seat}C']}     {self.seats[f'{seat}D']}"
            )
    #define function for showing the seats in the chosen row
    def row_seats(self,row):
        print(f"Seats in {row} row")
        print(
            f"A:{self.seats[f'{row}A']} "
            f"B:{self.seats[f'{row}B']} "
            f"C:{self.seats[f'{row}C']} "
            f"D:{self.seats[f'{row}D']} "
            f"E:{self.seats[f'{row}E']} "
            f"F:{self.seats[f'{row}F']}"
        )

   #define function that will show the interface of searching among seats
    def priority_searching(self):
        print(
            "1. Search Windows seats \n",
            "2. Search Aisle adjacent seats \n",
            "3. Search row seats \n",
        )
        search = input("Enter your choice: ")
        if search == "1":
            self.window_seats()
        elif search == "2":
            self.aisle_adjacent_seats()
        elif search == "3":
            while True:
                row = input("Enter row number (1-80): ").strip()
                #checking if input is digit
                if not row.isdigit():
                    print("Please enter a number.")
                    continue

                row = int(row)

                if 1 <= row <= 80:
                    self.row_seats(row)
                    break
                else:
                    print("Row must be between 1 and 80.")

        else:
            print("Enter a valid choice!")

    #define function that will hold the interface of searching among seats
    def interface_seats(self):
        while True:
            ask = input("Do you want to choose seats according to your priority? (y/n): ").lower().strip()
            if ask == "y":
                self.priority_searching()
            else:
                break


#class for Booking and other operation
class Booking:
    def __init__(self, seats):
        self.seats=seats #loading seats
        self.database=Database()
        self.reference=Reference()
        self.search = SeatSelection(self.seats.seats) #calling a class
   #define function that checks avaibility of seats
    def check_availability(self):
        print("Check seats availability")
        self.search.interface_seats() #calling function
        self.seats.show_seats()  # calling the function
        seat_number = input("Enter seat number: ").strip().upper()

        if seat_number not in self.seats.seats: # if input is not correct, it will show invalidity
            print("Invalid seat number. Please try again.")
        elif self.seats.seats[seat_number]=="S":
            print(f" {seat_number} is not available!")
        elif self.seats.seats[seat_number]=="F":
            print(f" {seat_number} is available ")
        elif self.seats.seats[seat_number]=="R":
            print(f" {seat_number} is not available ")
        else:
            print("Enter a valid seat number!")

    #define function that will create booking for user
    def create_booking(self):
        print("WELCOME TO BOOKING PAGE:")
        print("You can select your seat by checking its availability from seats below")
        existing_ref=self.database.references()
        while True:
            self.seats.show_seats()# calling the function
            seat_number = input("Enter your seat number: ").strip().upper()
            if seat_number not in self.seats.seats:  # checking for validity of seat number
                print("Invalid seat number. Please try again.")

            elif self.seats.seats[seat_number] == "S":
                print("Please select another seat!")
            elif self.seats.seats[seat_number] == "F":
                first_name = input("Enter your first name: ")
                last_name = input("Enter your last name: ")
                passport = input("Enter your passport number: ")
                assure = input(f"Do you want to book {seat_number} seat? (y/n): ").lower().strip()

                if assure == "y":
                    seat_row=int(seat_number[:-1])
                    seat_col=seat_number[-1]
                    booking_ref=self.reference.generate_unique_id(existing_ref)
                    self.database.insert_booking(booking_ref, passport, first_name, last_name,seat_row,seat_col)
                    self.seats.seats[seat_number] = "R"
                    print("Booking successful!")

                else:
                    print("Booking process cancelled!")

            else:
                print("Please select another seat!")
            con=input("Do you want to book another seat? (y/n): ").lower().strip()
            if con=="y":
                pass
            else:
                print("Thank you!")
                break

    #define function that will free the booked seat
    def free_seat(self):
        print("FREEING SEAT!")

        seat_number_f=input("Enter your seat number: ").strip().upper()


        if seat_number_f not in self.seats.seats:
            print("Invalid seat number. Please try again.")
        elif self.seats.seats[seat_number_f]=="R":
            ref = self.database.reference_booked(seat_number_f)[0]  # it returns tuple (ref,) so [0] can give only ref part.
            user_passport = input("Enter your passport number: ")
            if user_passport==self.database.user_passport(ref):
                 assurance = input(f"Do you want to free {seat_number_f} seat? (y/n): ").lower().strip()
                 if assurance == "y":
                     ref = self.database.reference_booked(seat_number_f)[
                        0]  # it provides with ref part only instead of tuple like  (ref,)
                     self.database.delete_booking(ref)
                     self.seats.seats[seat_number_f] = "F"  # freeing the seat
                     print(f" {seat_number_f} is freed successful!")
                 else:
                     print("Process cancelled!")

            else:
                print("Passport is not valid!")


        else:
            print("The process cancelled, try later!")
    #define function that will show the list of booked seats
    def show_booking_status(self):
        print("Booking Status")
        print("Booked seats:")

        for spot in self.database.booking_status():
            ref = self.database.reference_booked(spot)[0]  # it returns tuple (ref,) so [0] can give only ref part.
            passport, first, last = self.database.user_details(ref)
            print(f"seat: {spot} \n",
                  f"  First Name: {first} \n",
                  f"  Last Name: {last} \n",
                  f"  Reference number: {ref} \n",
                  f"  Password: {passport} \n")






#class for interface of the software
class Interface:
    def __init__(self):
        self.seats=Seats() #initializing instance
        self.seats.create_seats()#creating the seats
        self.seats.check_bookedSeats()
        self.database=Database()
        self.booking=Booking(self.seats) #initializing instance
    #define function that will keep running the application
    def application(self):
        print("WELCOME TO APACHE AIRLINES")

        while True: #while loop for continues use
            print(
                "1. Check availability of seats \n",
                "2. Book seats \n",
                "3. Free seats \n",
                "4. Show booking status \n",
                "5. Exist program \n",
            )
            user = input("Enter your choice: ")
            if user == "1":
                self.booking.check_availability()
            elif user == "2":
                self.booking.create_booking()
            elif user == "3":
                self.booking.free_seat()
            elif user == "4":
                self.booking.show_booking_status()
            elif user == "5":
                print("Thank you for choosing Airlines")
                self.database.close()
                break
            else:
                print("Please enter a valid choice!")




app=Interface() #initializing instance for running
app.application() #running the function




