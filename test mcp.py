from MCP import Channel
import time
from DbClass import DbClass
from a4988 import a4988
from HX711 import HX711
import datetime


c= Channel(0)
mot = a4988()
db=DbClass()
hx = HX711(20, 21)
hx_res = HX711(5, 6)

list_times = db.getFeedingTimes()
while True:
    light_val= c.data()

    #without this de de get feedign time doesnt get the updated table
    db.remove_feedingtime('00:01:00')

    list_times = db.getFeedingTimes()


    for item in list_times:
        for i in item:
            if str(datetime.datetime.now().strftime('%H:%M:%S')) ==str(i):
                # get's how much food can be eaten today
                rest_portionsize = db.getResting_portionsize()
                rest_portionsize = rest_portionsize[-1]
                rest_portionsize = rest_portionsize[0]
                print(rest_portionsize)
                time.sleep(1)
                # checks if the max portionsize has een reached
                if 25 < int(rest_portionsize):

                    # starts up the scale
                    hx.set_reading_format("LSB", "MSB")
                    hx.set_reference_unit(2167)
                    hx.reset()
                    hx.tare()

                    # turns the motor
                    mot.turn_motor()
                    print("motro moe geadaair in")


                    # gets the weight and put the resluts in a list
                    list_weight = []
                    for i in range(0, 10):
                        val = max(0, int(hx.get_weight(5)))
                        print(val)
                        hx.power_down()
                        hx.power_up()
                        list_weight.append(int(val))
                        time.sleep(0.5)

                    # the list gets sorted so hightest value would be last
                    weight = sorted(list_weight)
                    portion_weight = int(weight[-1])

                    # insert how much food is eaten in to to food_eaten tabe
                    if portion_weight > 1000:
                        portion_Data = float(portion_weight / 1000)
                        db.setDataToFood_eaten(portion_Data, 2, 0)
                    else:
                        db.setDataToFood_eaten(portion_weight, 1, 0)

                    # calculates how much is resting from the max portionsize
                    rest_portionsize = rest_portionsize - portion_weight
                    print(rest_portionsize)

                    if rest_portionsize < 0:
                        rest_portionsize = 0
                    else:
                        rest_portionsize = rest_portionsize

                    db.setDataToResting_portionsize(rest_portionsize, 1)

                    ##################################################

                    # starts up the reservoir scale
                    hx_res.set_reading_format("LSB", "MSB")
                    hx_res.set_reference_unit(392.12)
                    hx_res.reset()

                    # gets the weight and put the resluts in a list
                    list_weight = []
                    for i in range(0, 10):
                        val = max(0, int(hx_res.get_weight(5)))
                        print(val)
                        hx_res.power_down()
                        hx_res.power_up()
                        list_weight.append(int(val))
                        time.sleep(0.5)

                    # calculate how much food is left
                    weight = sorted(list_weight)
                    portion_weight = int(weight[-1])
                    portion_weight = portion_weight - 22929  # can only be done when de reference unit is positive

                    # inserts how much food is leftt in de Food reservoir tale
                    if portion_weight > 1000:
                        portion_Data = float(portion_weight / 1000)
                        db.setDataToFood_reservoir(portion_Data, 2)
                    elif portion_weight < 0:
                        portion_weight = 0
                        db.setDataToFood_reservoir(portion_weight, 1)
                    else:
                        db.setDataToFood_reservoir(portion_weight, 1)

    if light_val > 100:
        # get's how much food can be eaten today
        rest_portionsize = db.getResting_portionsize()
        rest_portionsize = rest_portionsize[-1]
        rest_portionsize = rest_portionsize[0]
        print(rest_portionsize)
        time.sleep(1)
        # checks if the max portionsize has een reached
        if 25 < int(rest_portionsize):

            # starts up the scale
            hx.set_reading_format("LSB", "MSB")
            hx.set_reference_unit(2167)
            hx.reset()
            hx.tare()

            # turns the motor
            mot.turn_motor()
            print("motro moe geadaair in")

            # gets the weight and put the resluts in a list
            list_weight = []
            for i in range(0, 10):
                val = max(0, int(hx.get_weight(5)))
                print(val)
                hx.power_down()
                hx.power_up()
                list_weight.append(int(val))
                time.sleep(0.5)

            # the list gets sorted so hightest value would be last
            weight = sorted(list_weight)
            portion_weight = int(weight[-1])

            # insert how much food is eaten in to to food_eaten tabe
            if portion_weight > 1000:
                portion_Data = float(portion_weight / 1000)
                db.setDataToFood_eaten(portion_Data, 2, 0)
            else:
                db.setDataToFood_eaten(portion_weight, 1, 0)

            # calculates how much is resting from the max portionsize
            rest_portionsize = rest_portionsize - portion_weight
            print(rest_portionsize)

            if rest_portionsize < 0:
                rest_portionsize = 0
            else:
                rest_portionsize = rest_portionsize

            db.setDataToResting_portionsize(rest_portionsize, 1)

            ##################################################

            # starts up the reservoir scale
            hx_res.set_reading_format("LSB", "MSB")
            hx_res.set_reference_unit(392.12)
            hx_res.reset()

            # gets the weight and put the resluts in a list
            list_weight = []
            for i in range(0, 10):
                val = max(0, int(hx_res.get_weight(5)))
                print(val)
                hx_res.power_down()
                hx_res.power_up()
                list_weight.append(int(val))
                time.sleep(0.5)

            # calculate how much food is left
            weight = sorted(list_weight)
            portion_weight = int(weight[-1])
            portion_weight = portion_weight - 22929 # can only be done when de reference unit is positive

            # inserts how much food is leftt in de Food reservoir tale
            if portion_weight > 1000:
                portion_Data = float(portion_weight / 1000)
                db.setDataToFood_reservoir(portion_Data, 2)
            elif portion_weight < 0:
                portion_weight = 0
                db.setDataToFood_reservoir(portion_weight, 1)
            else:
                db.setDataToFood_reservoir(portion_weight, 1)







