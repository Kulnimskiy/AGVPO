from coodinates import work_selenium
from geopy.distance import geodesic as GD



def main():
    addresses = []
    counter = 1
    where_from = input("From: ")
    if where_from:
        addresses.append(where_from)
    while True:
        address = input(f"Location {counter}: ")
        if address:
            addresses.append(address)
            counter += 1
        else:
            break

    locations = work_selenium(addresses, url_adress='https://yandex.ru/maps/')
    trips = []
    for i in range(len(locations)-1):
        frm = locations[i]
        to = locations[i + 1]
        print(f"Trip {i+1}")
        print(frm["address"])
        print(to["address"])
        print("Distance: ", distance_calculation(frm["coordinates"], to["coordinates"]))
        print()

    frm = locations[-1]
    to = locations[0]
    print("Going back!")
    print("From: ", frm["address"])
    print("To: ", to["address"])
    print("Distance: ", distance_calculation(frm["coordinates"], to["coordinates"]))


def distance_calculation(start_coord, end_coord):
    # Для расчета расстояния используем функцию GD([1 координаты точки],[2 координаты точки].[единица измерения расстояния])
    dist = GD(start_coord, end_coord).km
    # Возвращаем минимальную дистанцию из списке
    return dist

main()
input()
# print(f"The distance is: {distance_calculation(coords[0][0], coords[0][1]):.2f} km.")
