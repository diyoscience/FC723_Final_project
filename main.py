"""Sofware for Apache airlines"""

#class for creating seats and showing them
class Seats:
    def __init__(self):
        self.seats={} #initializing seats

    #define function that creates seats
    def create_seats(self):
        rows=["A","B","C","D","E","F"] #rows for identifying seats
        for row in rows:
            for col in range(1,81): # iterating for demanded seats
                seat_id=f"{col}{row}"
                if row in ("D","E","F") and col>=77:
                    self.seats[seat_id]="S"
                else:
                    self.seats[seat_id]="F"

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
#class for Booking and other operation
class Booking:
    def __init__(self, seats):

        self.seats=seats #loading seats
        self.booked_seats = []
   #define function that checks avaibility of seats
    def check_availability(self):
        print("Check seats availability")
        self.seats.show_seats() #calling the function

        seat_number = input("Enter seat number: ").strip().upper()

        if seat_number not in self.seats.seats: # if input is not correct, it will show invalidity
            print("Invalid seat number. Please try again.")
        elif self.seats.seats[seat_number]=="S":
            print(f" {seat_number} is not available!")
        elif self.seats.seats[seat_number]=="F":
            print(f" {seat_number} is available ")


        else:
            print("Enter a valid seat number!")

    #define function that will create booking for user
    def create_booking(self):
        print("WELCOME TO BOOKING PAGE:")
        print("You can select your seat by checking its availability from seats below")
        self.seats.show_seats() #calling the function
        seat_number=input("Enter your seat number: ").strip().upper()
        if seat_number not in self.seats.seats: #checking for validity of seat number
            print("Invalid seat number. Please try again.")

        elif self.seats.seats[seat_number]=="S":
            print("Please select another seat!")
        elif self.seats.seats[seat_number]=="F":
            print(f"Do you want to book {seat_number}?")
            assure=input("Do you want to book another seat? (y/n): ")
            if assure=="y":
                self.seats.seats[seat_number]="R"
                self.booked_seats.append(seat_number)
                print("Booking successful!")
            else:
                print("Booking process cancelled!")
        else:
            print("Please select another seat!")
    #define function that will free the booked seat
    def free_seat(self):
        print("FREEING SEAT!")
        seat_number_f=input("Enter your seat number: ")
        if seat_number_f not in self.seats.seats:
            print("Invalid seat number. Please try again.")
        elif self.seats.seats[seat_number_f]=="R":
            assurance=input(f"Do you want to free {seat_number_f} seat? (y/n): ")
            if assurance=="y":
                self.seats.seats[seat_number_f] = "F" #freeing the seat
                self.booked_seats.remove(seat_number_f) #freeing from the booked list
                print(f" {seat_number_f} is freed successful!")
            else:
                print("Process cancelled!")

        else:
            print("The process cancelled, try later!")
    #define function that will show the list of booked seats
    def show_booking_status(self):
        print("Booking Status")
        print("Booked seats:")
        for spot in self.booked_seats:
            print(f"{spot}")





#class for interface of the software
class Interface:
    def __init__(self):
        self.seats=Seats() #initializing instance
        self.seats.create_seats() #creating the seats
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
                break
            else:
                print("Please enter a valid choice!")




app=Interface() #intializing instance for running
app.application() #running the function




