#Author: Y.K.Hirun Emalsha
#Date: 23/12/2024
#Student ID: 2120013
from graphics import * 

class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data  
        self.date = date  
        self.window = GraphWin("Traffic Histogram", 1000, 600)  # Creating graphics window
        self.window.setBackground("lightgrey")

    def draw_axes(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        # X axis line
        x_axis = Line(Point(75, 550), Point(926, 550))  # X-axis
        x_axis.draw(self.window)

        # Labels for hours
        for i in range(0, 24):
            x_pos = 75 + i * 37  # giving Space between bars evenly
            label = Text(Point(x_pos, 570), f"{i:02d}")  # Format hours as two digits
            label.setSize(8)
            label.draw(self.window)

    def draw_bars(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        elm_data, hanley_data = self.traffic_data  # Unpack hourly data
        max_traffic = max(max(elm_data), max(hanley_data))  # To scale bars dynamically
        bar_width = 15

        for i in range(24):
            # Scale the bar height
            elm_height = (elm_data[i] / max_traffic) * 500 if max_traffic else 0
            hanley_height = (hanley_data[i] / max_traffic) * 500 if max_traffic else 0

            # Elm Avenue/Rabbit Road Bar
            elm_bar = Rectangle(Point(75 + i * 37 - bar_width, 550),
                                Point(75 + i * 37, 550 - elm_height))
            elm_bar.setFill("green")
            elm_bar.draw(self.window)

            # Hanley Highway/Westway Bar
            hanley_bar = Rectangle(Point(75 + i * 37 + 2, 550),
                                   Point(75 + i * 37 + bar_width, 550 - hanley_height))
            hanley_bar.setFill("red")
            hanley_bar.draw(self.window)

            # Add vehicle count labels on top of bars
            elm_label = Text(Point(75 + i * 37 - bar_width / 2, 550 - elm_height - 10), f"{elm_data[i]}")
            hanley_label = Text(Point(75 + i * 37 + bar_width / 2 + 2, 550 - hanley_height - 10), f"{hanley_data[i]}")
            elm_label.setSize(8)
            hanley_label.setSize(8)
            elm_label.draw(self.window)
            hanley_label.draw(self.window)

    def draw_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        # Elm Avenue/Rabbit Road
        elm_box = Rectangle(Point(75, 30), Point(95, 50))
        elm_box.setFill("green")
        elm_box.draw(self.window)
        elm_label = Text(Point(175, 40),"Elm Avenue/Rabbit Road")
        elm_label.setSize(10)
        elm_label.draw(self.window)

        # Hanley Highway/Westway
        hanley_box = Rectangle(Point(75, 50), Point(95, 70))
        hanley_box.setFill("red")
        hanley_box.draw(self.window)
        hanley_label = Text(Point(175, 60), "Hanley Highway/Westway")
        hanley_label.setSize(10)
        hanley_label.draw(self.window)

        """Draws the histogram title."""
        # Convert the date format from DDMMYYYY to DD/MM/YYYY
        formatted_date = f"{self.date[:2]}/{self.date[2:4]}/{self.date[4:]}"
        title = Text(Point(350, 20), f"Histogram of Vehicle Frequency per Hour ({formatted_date})")
        title.setSize(14)
        title.setStyle("bold")
        title.draw(self.window)

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        try:
            self.draw_axes()
            self.draw_bars()
            self.draw_legend()
            self.window.getMouse()  # Wait for user click to close
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            self.window.close()

# drawing histogram
def Draw_histogram(elm_traffic, hanley_traffic, date):
    app = HistogramApp((elm_traffic, hanley_traffic), date)
    app.run()
    
class MultiCSVProcessor:
    def validate_date_input(self):
        while True:
            try:
                while True:
                    day = int(input("Please enter the day of the survey in the format DD: "))
                    if 1 <= day <= 31:
                        break
                    print("Out of range - values must be in the range 1 and 31.")

                while True:
                    month = int(input("Please enter the month of the survey in the format MM: "))
                    if 1 <= month <= 12:
                        break
                    print("Out of range - values must be in the range 1 to 12.")

                while True:
                    year = int(input("Please enter the year of the survey in the format YYYY: "))
                    if 2000 <= year <= 2024:
                        break
                    print("Out of range - values must range from 2000 and 2024.")

                return f"traffic_data{day:02d}{month:02d}{year:04d}.csv"
            except ValueError:
                print("Integer required")

    def validate_continue_input(self):
        """
        Prompts the user to decide whether to load another dataset:
        - Validates "Y" or "N" input
        """
        while True:
            user_input = input("Do you want to select another data file for a different date? (Y/N): ").strip().upper()
            if user_input in ["Y", "N"]:
                if user_input == "N":
                    exit()
                return user_input
            else:
                print("Enter 'Y' or 'N'.")

    def process_csv_data(self, file_path):
        try:# Opening file and read lines
            with open(file_path, 'r') as file:
                lines = file.readlines()
                # Initializing variables
                total_vehicles = 0
                total_trucks = 0
                total_electric_vehicles = 0
                two_wheeled_vehicles = 0
                busses_north = 0
                straight_through = 0
                trucks_percentage = 0
                bike_average_per_hour = 0
                over_speed_limit = 0
                elm_vehicles = 0
                scooters_in_elm = 0
                hanley_vehicles = 0
                elm_scooter_percentage = 0
                bicycle_count = 0
                rain_hours_set = set() #Hours with rain
            # Hourly traffic for Elm Avenue and Hanley Highway
                elm_hourly_traffic = [0] * 24
                hanley_hourly_traffic = [0] * 24
            # Process each line in the CSV file and skipping the header
                for line in lines[1:]:
                    row = line.strip().split(",")
                    total_vehicles += 1
                    # Extracting data from file
                    junction = row[0]
                    time_of_day = row[2]
                    direction_in = row[3]
                    direction_out = row[4]
                    weather = row[5].strip().lower()
                    speed_limit = int(row[6])
                    vehicle_speed = int(row[7])
                    vehicle_type = row[8].lower()
                    is_electric = row[9].strip().lower()
                    # Extracting hour from the time of day
                    hour = int(time_of_day.split(":")[0])

                    if vehicle_type == "truck":
                        total_trucks += 1
                    if is_electric == "true":
                        total_electric_vehicles += 1
                    if vehicle_type in ["bicycle", "motorcycle", "scooter"]:
                        two_wheeled_vehicles += 1
                    if vehicle_type == "bicycle":
                        bicycle_count += 1
                    if direction_in == direction_out:
                        straight_through += 1
                    if total_vehicles > 0:
                        trucks_percentage = int(total_trucks / total_vehicles * 100)
                    if hour > 0:
                        bike_average_per_hour = int(bicycle_count / hour)
                    if vehicle_speed > speed_limit:
                        over_speed_limit += 1
                    if junction == "Elm Avenue/Rabbit Road":
                        elm_vehicles += 1
                        elm_hourly_traffic[hour] += 1 # Increment hourly count
                        if vehicle_type == "scooter":
                            scooters_in_elm += 1
                        if elm_vehicles > 0:
                            elm_scooter_percentage = int(scooters_in_elm / elm_vehicles * 100)
                    if junction == "Hanley Highway/Westway":
                        hanley_vehicles += 1
                    if junction == "Elm Avenue/Rabbit Road" and direction_out.upper() == "N" and vehicle_type == "buss":
                        busses_north += 1
                    if weather in ["heavy rain", "light rain"]:
                        rain_hours_set.add(hour)
                    if junction == "Hanley Highway/Westway":
                        hanley_hourly_traffic[hour] += 1 # Increment hourly count
                 # Determining peak hour   
                highest_vehicle_count = max(hanley_hourly_traffic)
                peak_hour = hanley_hourly_traffic.index(highest_vehicle_count)
                rain_hours = len(rain_hours_set) # Determining rain hours 
                # Returning calculated values
                return (
                    total_vehicles, total_trucks, total_electric_vehicles, two_wheeled_vehicles,
                    busses_north, straight_through, trucks_percentage, bike_average_per_hour, over_speed_limit, elm_vehicles,
                    elm_scooter_percentage, hanley_vehicles, highest_vehicle_count, peak_hour, rain_hours, elm_hourly_traffic, hanley_hourly_traffic
                )
        except FileNotFoundError:
            print("File not found.")# Handling file not found errors
        except Exception as e:
            print(f"An error occurred: {e}") # Handling other errors

    def display_outcomes(self, file_name):
        if not outcomes:
            print("No outcomes to display.")
            return
    # Extracting outcomes
        (
            total_vehicles, total_trucks, total_electric_vehicles, two_wheeled_vehicles,
            busses_north, straight_through, trucks_percentage, bike_average_per_hour, over_speed_limit, elm_vehicles,
            elm_scooter_percentage, hanley_vehicles, highest_vehicle_count, peak_hour, rain_hours, elm_hourly_traffic, hanley_hourly_traffic
        ) = outcomes
    # Display outcomes
        print("\n***************************************")
        print(f"Data file selected is {file_name}")
        print("***************************************")
        print(f"The total number of vehicles recorded for this date is {total_vehicles}")
        print(f"The total number of trucks recorded for this date is {total_trucks}")
        print(f"The total number of electric vehicles for this date is {total_electric_vehicles}")
        print(f"The total number of two-wheeled vehicles for this date is {two_wheeled_vehicles}")
        print(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {busses_north}")
        print(f"The total number of vehicles through both junctions not turning left or right is {straight_through}")
        print(f"The percentage of total vehicles recorded that are trucks for this date is {trucks_percentage}%")
        print(f"The average number of bikes per hour for this date is {bike_average_per_hour}")
        print(f"The total number of vehicles recorded as over the speed limit for this date is {over_speed_limit}")
        print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {elm_vehicles}")
        print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {hanley_vehicles}")
        print(f"{elm_scooter_percentage}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
        print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {highest_vehicle_count}")
        print(f"The most vehicles through Hanley Highway/Westway were recorded between {peak_hour}:00 and {peak_hour + 1}:00")
        print(f"The number of hours of rain for this date is {rain_hours}")
    # Write results to the specified output file
    def save_results_to_file(self, results, file_name, output_file_name="results.txt"):
        try:
            with open(output_file_name,"a") as file:   
                (
                    total_vehicles, total_trucks, total_electric_vehicles, two_wheeled_vehicles, 
                    busses_north, straight_through, trucks_percentage,bike_average_per_hour, over_speed_limit, elm_vehicles, 
                    elm_scooter_percentage,hanley_vehicles,highest_vehicle_count, peak_hour,rain_hours,elm_hourly_traffic,hanley_hourly_traffic
                ) = results

                file.write(f"Data file selected is {file_name}\n")
                file.write(f"The total number of vehicles recorded for this date is {total_vehicles}\n")
                file.write(f"The total number of trucks recorded for this date is {total_trucks}\n")
                file.write(f"The total number of electric vehicles for this date is {total_electric_vehicles}\n")
                file.write(f"The total number of two-wheeled vehicles for this date is {two_wheeled_vehicles}\n")
                file.write(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {busses_north}\n")
                file.write(f"The total number of vehicles through both junctions not turning left or right is {straight_through}\n")
                file.write(f"The percentage of total vehicles recorded that are trucks for this date is {trucks_percentage}%\n")
                file.write(f"The average number of bikes per hour for this date is {bike_average_per_hour}\n")
                file.write(f"The total number of vehicles recorded as over the speed limit for this date is {over_speed_limit}\n")
                file.write(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {elm_vehicles}\n")
                file.write(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {hanley_vehicles}\n")
                file.write(f"{elm_scooter_percentage}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n")
                file.write(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {highest_vehicle_count}\n")
                file.write(f"The most vehicles through Hanley Highway/Westway were recorded between {peak_hour}:00 and {peak_hour +1}:00\n")
                file.write(f"The number of hours of rain for this date is {rain_hours}.\n")
                file.write("\n*******************************************\n")
            
        except Exception as e:
            print(f"An error occurred:{e}")
#calling functions
while True:
    file = MultiCSVProcessor()
    file_name = file.validate_date_input()
    outcomes = file.process_csv_data(file_name)
    file.display_outcomes(file_name)
    file.save_results_to_file(outcomes, file_name)
    # Extracting traffic data for histogram
    elm_traffic = [hour for hour in outcomes[15]]  # Assuming hourly data in outcomes
    hanley_traffic = [hour for hour in outcomes[16]]
    # Drawing histogram
    Draw_histogram(elm_traffic, hanley_traffic, file_name[12:20])
    file.validate_continue_input()

    
