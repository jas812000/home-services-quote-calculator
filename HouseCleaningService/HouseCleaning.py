# Puropse ----------------------------------------
# This program will offer house cleaning and yard services, displaying the cost for the services selected

# Welcome--------------------------------------------
def MyWelcome():
    # This function will display the programmer's name, class and date
    print("James Stevens\t\t", "CMIS 102/6383\t\t", "07 July 2022")
    print(
        "\nThis program will offer house cleaning and yard services, displaying the cost for the services selected.\n")
    # End ----------------------------------------


# Display Services----------------------------------------
def DisplayServices():
    # Display the house services and associated prices.
    # Display the yard services and associated prices.
    # Create a space to make the program easier to read
    print()
    print("These are the house services available:\n", "\nCarpet Cleaning (per room)\n", "\tSmall House: $100\n",
          "\tMedium House: $200\n", "\tLarge House: $100 plus 5%\n")
    print("Bathroom Cleaning (per room)\n", "\tSmall House: $80\n", "\tMedium House: $100\n", "\tLarge House: $120\n")
    print("Dusting (per room)\n", "\tSmall House: $60\n", "\tMedium House: $80\n", "\tLarge House: $100\n")
    print("There is a $2.50 surcharge per square foot for any house over 3,000 square feet.")
    print()
    print("These are the yard services available:\n", "\nMowing\n", "\t$6.00 per square foot.\n")
    print("Edging\n", "\t$4.00 per square foot.\n")
    print("Shrub Pruning (per shrub)\n", "\t$25.00\n")
    print(
        "Labor is $80.00 per hour for a crew of 2. There is a scaled surcharge is $35.00 per hour for any additional increments of 2000 square feet over 5000 square feet.\n")
    # End ----------------------------------------


# Select Services --------------------------
def SelectServices():
    # This function will prompt the user to select what services they want: house cleaning, yard service or both

    global service
    global serviceType

    print("Please select which service you want:\n", "\tHouse Cleaning = 1\n", "\tYard Service = 2\n",
          "\tBoth House and Yard Service = 3\n")
    i = 0
    while i < 2:
        selection = int(input("Please enter 1, 2 or 3:\t"))
        if selection == 1:
            service = selection
            i = 3
        elif selection == 2:
            service = selection
            i = 3
        elif selection == 3:
            service = selection
            i = 3
        else:
            print("Please enter the correct number.")
    i = i + 1
    serviceType = int(service)
    # End ----------------------------------------


# Define Service_Type --------------------------------------------------
def GetServiceType():
    # Determine whether service will be a light(maintenance)cleaning or complete (thorough) cleaning

    typeS = int(input(
        "\nFor a light(maintenance)cleaning, select 1\nFor a complete (thorough) cleaning, select 2\nSelection: "))

    if typeS == 2:
        typeFee = 0.1  # Fee for Complete (Thorough) Cleaning
        print("\nYou selected a complete (thorough) cleaning.\n")

    elif typeS == 1:
        typeFee = 0
        print("\nYou selected a light (maintenance) cleaning.\n")
    else:
        print("You entered a wrong digit. Please start over.")
        exit()

    global g01sT
    g01sT = typeFee

    return (GetServiceType)
    # End ----------------------------------------


# Define House Size---------------------------------
def GetBigHouse():
    # Determine the size of the house
    # Input: houseSize (numerical value)
    # Output: Small, Med, or Large

    BigHouse = (input("Please enter the square footage of the house: "))
    houseSize = int(BigHouse)

    if (houseSize <= 1200):
        print("\nYou have a small house.")

    elif houseSize <= 2000 and houseSize > 1200:
        print("\nYou have a medium house.")

    elif houseSize > 2000:
        print("\nYou have a large house.")

    global g02bH
    g02bH = houseSize

    return (GetBigHouse)
    # End ----------------------------------------


# Carpet Service Costs ---------------------------------------------------
def GetCarpetCosts():
    # Determine the cost to clean the carpet

    carpetQuant = int(input("\nPlease enter how many rooms have carpets: "))

    houseSize = g02bH

    if houseSize <= 1200:
        priceCarpet = carpetQuant * 100

    elif houseSize <= 2000 and houseSize > 1200:
        priceCarpet = carpetQuant * 200

    elif houseSize > 2000:
        priceCarpet = carpetQuant * 300

    else:
        print(GetCarpetCosts)

    global typeTwo
    typeTwo = carpetQuant

    global g03cC
    g03cC = priceCarpet

    return (GetCarpetCosts)
    # End ----------------------------------------


# Bathroom Service Costs --------------------------------------------------
def GetBathroomCosts():
    # Determine the cost to clean the bathroom

    bathQuant = int(input("\nPlease enter how many bathrooms need cleaning: "))
    houseSize = g02bH

    if houseSize <= 1200:
        priceBath = bathQuant * 80

    elif houseSize <= 2000 and houseSize > 1200:
        priceBath = bathQuant * 100

    elif houseSize > 2000:
        priceBath = bathQuant * 120

    else:
        print(GetBathroomCosts)

    global typeThree
    typeThree = bathQuant

    global g04bC
    g04bC = priceBath

    return (GetBathroomCosts)
    # End ----------------------------------------


# Dust Price -------------------------------------------------------
def GetDustCosts():
    # Determine the cost to dust

    dustQuant = int(input("\nPlease enter how many rooms need dusting: "))
    houseSize = g02bH

    if houseSize <= 1200:
        priceDust = dustQuant * 60

    elif houseSize <= 2000 and houseSize > 1200:
        priceDust = dustQuant * 80

    elif houseSize > 2000:
        priceDust = dustQuant * 100

    else:
        print()

    global g05dC
    g05dC = priceDust

    return (GetDustCosts)
    # End ----------------------------------------


# House Size Surcharge Fees--------------------------------------------------------
def GetSurchargeFee():
    # Determine if a surcharge will be added (surcharge for houses > 3000 sq ft)

    houseSize = g02bH

    if houseSize > 3000:
        surchargeFee = (houseSize - 3000) * (2.5)

    else:
        surchargeFee = 0

    global g06sC
    g06sC = surchargeFee

    return (GetSurchargeFee)
    # End ----------------------------------------


# Define Yard Size and Cost of Services----------------------------------
def GetYardSize():
    # Determine the size of the yard

    yardSize = int(input("\nEnter the square footage of the yard: "))
    shrubQuan = int(input("\nEnter the amount of shrubs on the property: "))

    # Calculate the cost of mowing based on square footage
    mowing = yardSize * 6

    # Calculate the cost of edging based on linear footage
    # Obtain the square root of the inputted square footage of the yard and multiply by 4
    import math
    edging = ((math.sqrt(yardSize) * 4) * 4)
    # Calculate the cost of shrub pruning based on the quantity of shrubs
    shrubPrune = shrubQuan * 25

    # Determine surcharge based on yard size over 5000 square feet
    if yardSize > 5000:
        a = (yardSize - 5000) / 2000
        if a // 1 == a / 1:
            b = a
        else:
            b = int(a) + 1
    else:
        exit()
    yardSurcharge = b * 35

    global g11mO
    g11mO = mowing
    global g12eD
    g12eD = edging
    global g13sH
    g13sH = shrubPrune
    global g14yS
    g14yS = yardSurcharge
    global shrubQuant
    shrubQuant = shrubQuan

    # End ---------------------------------------


# Define Labor Hours------------------------
def GetLaborHours():
    # Get the user to input the start and end times of the yard service
    # Calculate the total hours
    starthour = int(input("\nEnter the start hour:\t"))
    startmin = int(input("Enter the start min:\t"))
    endhour = int(input("\nEnter the end hour:\t"))
    endmin = int(input("Enter the end min:\t"))

    f = endhour - starthour
    g = (endmin - startmin) / 60
    totalHours = f + g

    global g15tH
    g15tH = totalHours

    # End ----------------------------------------


# Define Senior Discount------------------------
def GetSeniorDiscount():
    # Determine senior discount based on age input
    # Senior discount is 15% of the subtotal
    print("\nSenior citizens qualify for a discount on services.\n")
    age = int(input("Enter your age: "))
    if age >= 65:
        seniorDisc = 0.15
    else:
        seniorDisc = 0
        print()

    global g16sD
    g16sD = seniorDisc

    # End ----------------------------------------


# Calculate Total House Costs ------------------------
def CalHouseCosts() -> float:
    # This function will calculate the total costs to include surcharge and taxes
    # It will also display the total.
    # Input: g02bH, g03cC, g04bC, g05dC, g06sC
    # Output: totalPrice
    # Calculate the subtotal (g03cC, g04bC, g05dC, g06sC)

    # Calculate Subtotal
    subPrice = (g03cC + g04bC + g05dC + g06sC)

    # Calculate fee for type of cleaning
    cleantypeFee = (g01sT * subPrice)

    # Calculate Senior Discount
    seniorD = ((subPrice + cleantypeFee) * g16sD)

    # Calculate sales tax
    taxTotal = ((subPrice + cleantypeFee) * 0.08)

    # Calculate total
    totalPrice = (((subPrice + cleantypeFee) - seniorD) + taxTotal)

    print("The house is ", g02bH, "square feet.")

    print("\nThe cost to clean the carpets is ${:.2f}".format(g03cC), ".")

    print("\nThe cost to clean the", typeTwo, "bathrooms is ${:.2f}".format(g04bC), ".")

    print("\nThe cost to dust all", typeThree, "rooms is ${:.2f}".format(g05dC), ".")

    print("\nThe service fee is ${:.2f}".format(cleantypeFee), ".")

    print("\nThe surcharge for square footage over 3000 square feet is ${:.2f}".format(g06sC), ".")

    print("\nTotal price with tax included is ${:.2f}".format(totalPrice), ".")
    # End ----------------------------------------


# Calculate Total Yard Costs ------------------------
def CalYardCosts() -> float:
    # This function will calculate the total yard costs to include surcharge and taxes

    # Calculate Total Labor Cost and Yard Surcharge
    totalLaborCost = (g15tH * 80) + (g14yS * g15tH)

    # Calculate Subtotal
    subPriceYard = float(g11mO) + float(g12eD) + float(g13sH) + float(totalLaborCost)

    # Calculate Senior Discount
    seniorDiscount = (subPriceYard + totalLaborCost) * (g16sD)

    suBPriceYard = (subPriceYard) - (seniorDiscount)

    # Calculate sales tax
    taxTotalYard = (float(suBPriceYard) * 0.08)

    # Calculate total

    totalPriceYard = (suBPriceYard + taxTotalYard)

    print("Mowing will cost ${:.2f}".format(g11mO), ".")

    print("\nEdging will cost ${:.2f}".format(g12eD), ".")

    print("\nTrimming", shrubQuant, "shrubs will cost ${:.2f}".format(g13sH), ".")

    print("\nThe surcharge for a larger yard is ${:.2f}".format(g14yS), "per hour.")

    print("\nThe total cost for yard services with tax and senior discount included is ${:.2f}".format(totalPriceYard),
          ".")
    # End ----------------------------------------


# Calculate Total House and Yard Costs ------------------------
def CalCosts() -> float:
    # This function will calculate the total house and yard costs to include surcharge and taxes
    # It will also display the total.
    # Input: g02bH, g03cC, g04bC, g05dC, g06sC
    # Output: totalPrice
    # Calculate the subtotal (g03cC, g04bC, g05dC, g06sC)

    # Calculate Subtotal
    subPrice = (g03cC + g04bC + g05dC + g06sC)

    # Calculate fee for type of cleaning
    cleantypeFee = (g01sT * subPrice)

    # Calculate House Total
    totalHousePrice = (subPrice + cleantypeFee)

    # Calculate Total Labor Cost and Yard Surcharge
    totalLaborCost = (g15tH * 80) + (g14yS * g15tH)

    # Calculate Yard Total
    subPriceYard = (g11mO + g12eD + g13sH + (totalLaborCost))

    # Calculate Subtotal
    subTotal = (totalHousePrice + subPriceYard)

    # Calculate senior discount
    seniorDiscount = (g16sD) * (subTotal)

    # Calculate
    subPrice = (subTotal) - (seniorDiscount)

    # Calculate sales tax
    taxTotal = (subPrice * 0.08)

    # Calculate total price
    totalPrice = (subPrice + taxTotal)

    print("\nThe house is ", g02bH, "square feet.")

    print("\nThe cost to clean the carpets is ${:.2f}".format(g03cC), ".")

    print("\nThe cost to clean the", typeTwo, "bathrooms is ${:.2f}".format(g04bC), ".")

    print("\nThe cost to dust all", typeThree, "rooms is ${:.2f}".format(g05dC), ".")

    print("\nThe surcharge for square footage over 3000 square feet is ${:.2f}".format(g06sC), ".")

    print("\nThe service fee is ${:.2f}".format(cleantypeFee), ".")

    print("\nMowing will cost ${:.2f}".format(g11mO), ".")

    print("\nEdging will cost ${:.2f}".format(g12eD), ".")

    print("\nTrimming", shrubQuant, "shrubs will cost ${:.2f}".format(g13sH), ".")

    print("\nThe surcharge for a larger yard is ${:.2f}".format(g14yS), "per hour.")

    print("\nThe total cost for both house and yard services is ${:.2f}".format(totalPrice), ".")

    # End ----------------------------------------


# Main Program ----------------------------------------
MyWelcome()
DisplayServices()
SelectServices()
if serviceType == 1:
    GetServiceType()
    GetBigHouse()
    GetCarpetCosts()
    GetBathroomCosts()
    GetDustCosts()
    GetSurchargeFee()
    GetSeniorDiscount()
    CalHouseCosts()
elif serviceType == 2:
    GetYardSize()
    GetLaborHours()
    GetSeniorDiscount()
    CalYardCosts()
elif serviceType == 3:
    GetServiceType()
    GetBigHouse()
    GetCarpetCosts()
    GetBathroomCosts()
    GetDustCosts()
    GetSurchargeFee()
    GetYardSize()
    GetLaborHours()
    GetSeniorDiscount()
    CalCosts()
# Execute----------------------------------------------
