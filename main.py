import csv
import matplotlib.pyplot as plt
"""
input four floats e W h,I
output calculateSolarPower
"""
def calculateSolarPower(e, W, H, I):
    return e*W*H*I
"""
input filepath
the program will read data from the specified CSV file
output time and intensities as list of float
"""
def getIntensityData(filepath):
    time = []
    intensities = []
    with open(file=filepath) as csvFile:

        reader = csv.reader(csvFile, delimiter=',')
        reader = list(reader)
        #the  first row in the reader isn't data so we need to skip that.
        # every line the first number is time and the second number is intensities
        for i in range(1, len(reader)):
            time.append(float(reader[i][0]))
            intensities.append(float(reader[i][1]))
    return time, intensities
"""
input time and intensities 
"""
def plotSolarPowerOverTime(time, intensities):
# solar power for type A,B,C
    powersA = [calculateSolarPower(0.13, 0.8, 1.0, intensity) for intensity in intensities]
    powersB = [calculateSolarPower(0.22, 0.6, 0.5, intensity) for intensity in intensities]
    powersC = [calculateSolarPower(0.16, 0.6, 0.6, intensity) for intensity in intensities]
    plt.plot(time, powersA, label="Type A")
    plt.plot(time, powersB, label="Type B")
    plt.plot(time, powersC, label="Type C")
    plt.legend()
    plt.savefig("ex3_question1.pdf", format="pdf", bbox_inches="tight")
    plt.show()
"""
input hours,intensities,require_power
"""
def print_solar_power_percentage_of_hour(hours,intensities,require_power):
    # use a variable to count the number of hours with powers under required powers
    p=0
    #Substitute each intensity into the equation for solving
    # and then identify the values that satisfy the given range
    for intensity in intensities:
        powers = 10*calculateSolarPower(0.13, 0.8, 1.0, intensity)
        if powers <require_power:
            p+=1
    percentage=p/len(hours)
    print("percentage",percentage*100)
"""
input intensities
output everyday SolarPower
"""
def calcuateAverageSolarPowerPerDay(intensities):
    powersA=[calculateSolarPower(0.13, 0.8, 1.0, intensity) for intensity in intensities]
    return sum(powersA)
"""
plot a graph
"""
def plotAveragePowerVersusMonth():
    months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    powers=[]
    #according to the month in months and intensities,we can get the data from the file
    for month in months:
        filepath='Solar_intensity_'+month+'.csv'
        time,intensities =getIntensityData(filepath)
        powers.append(calcuateAverageSolarPowerPerDay(intensities))
    plt.plot(months,powers)
    plt.savefig("ex3_question3.pdf", format="pdf", bbox_inches="tight")
    plt.show()
    """
    print the function about the rotation_rate
    """
def calculatePowerBWind(rotation_rate):
    return (0.6*rotation_rate**2)/(1+rotation_rate**2*4.0*10**-4)
"""
print the function about calculate rotation
"""
def calculatrRotation(rotation_rate,wind_speed):
    return rotation_rate +3600/(6.2*10**5)*(25*wind_speed**2-2.1*rotation_rate)
"""
input filepath and month
open file 
"""
def getWindSpeedData(filepath,month):
    hours=[]
    windspeed=[]
    with open (file=filepath) as csvfile:
        reader =csv.reader(csvfile,delimiter=',')
        reader=list(reader)
        #a is thelocation for reader items
        for a in range(1,len(reader)):
            hours.append(float(reader[a][0]))
            windspeed.append(float(reader[a][month]))
    return hours,windspeed
"""
input month
output hour and wind power
"""
def plotRotationRateVersusTime(month):
    hours,wind_speeds= getWindSpeedData("wind_data.csv",month)
    current_rotation_rate=0
    rotation_rates=[]
    #to make the graph for a range
    for a in range (len(wind_speeds)):
        current_rotation_rate=calculatrRotation(current_rotation_rate,wind_speeds[a])
        rotation_rates.append(current_rotation_rate)
        # when a equals to 5 print draw the graph of current_rotation_rate
        if (a==5):
            wind_power = calculatePowerBWind(current_rotation_rate)
            print(f'at hour {hours [a]} the wind power is {wind_power}')
    plt.plot(hours,rotation_rates)
    plt.savefig("ex3_question4.pdf", format="pdf", bbox_inches="tight")
    plt.show()
"""
input starting_month and ending_month
"""
def plotPowerOverTime(starting_month, ending_month):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    time_intervals=[]
    solar_powers = []
    wind_powers = []
    total_powers = []
    insufficient_power_in_ending_month = False
    for i in range(starting_month-1, ending_month):
        intensity_filepath = 'Solar_intensity_' + months[i] + '.csv'
        wind_speed_filepath = 'wind_data.csv'
        time, intensities = getIntensityData(intensity_filepath)
        hours, windspeeds = getWindSpeedData(wind_speed_filepath, i+1)
        current_rotation_rate = 0
        #according to the variable j calculateSolarPower
        for j in range(len(intensities)):
            solar_power = calculateSolarPower(0.13, 0.8, 1.0,intensities[j])
            current_rotation_rate = calculatrRotation(current_rotation_rate, windspeeds[j])
            wind_power = calculatePowerBWind(current_rotation_rate)
            total_power = solar_power * 6 + wind_power
            solar_powers.append(solar_power)
            wind_powers.append(wind_power)
            total_powers.append(total_power)
            #because can't get the end of the month so we need to reduce one
    if (i == ending_month-1 and total_power < 250):
        insufficient_power_in_ending_month = True
        #make functions to calculate the total_number
    if (i == ending_month - 1):
        time_intervals = hours
        starting_index_of_ending_month = (ending_month - starting_month) * 24 + 0
        #according to the calculations to printing the result and drawing the graph
    if insufficient_power_in_ending_month:
        print(f'the total power drop below 250W in {months[ending_month-1]}')
    plt.plot(time_intervals, solar_powers[starting_index_of_ending_month:], label="Solar Power")
    plt.plot(time_intervals, wind_powers[starting_index_of_ending_month:], label="Wind Power")
    plt.plot(time_intervals, total_powers[starting_index_of_ending_month:], label="Total Power")
    plt.legend()
    plt.savefig("ex3_question5.pdf", format="pdf", bbox_inches="tight")
    plt.show()


















if __name__ == "__main__":
    #1
    time, intensities = getIntensityData('Solar_intensity_December.csv')
    plotSolarPowerOverTime(time, intensities)
    #2
    print_solar_power_percentage_of_hour(time,intensities,250)
    #3
    plotAveragePowerVersusMonth()
    #4
    plotRotationRateVersusTime(7)
    #5
    plotPowerOverTime(6, 12)

