import time
# import pandas as pd
from operator import itemgetter
import names
import random


class Building:
    def __init__(self, address, min_floor, max_floor, height, people):
        self.address = address
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.height = height
        self.people = people


class Elevator:
    def __init__(self, building, id, floor, max_weight, speed):
        self.building = building
        self.id = id
        self.floor = floor
        self.max_weight = max_weight
        self.speed = speed
        self.distance_between_floors = self.building.height/(self.building.max_floor - self.building.min_floor)

    def elevator_travel(self, new_floor, humans):
        """Функция описывает путь лифта с одного этажа на другой"""
        distance = abs(self.floor - new_floor) * self.distance_between_floors
        time_in_travel = distance / self.speed
        # time.sleep(time_in_travel)
        self.change_floor(new_floor)
        for human in humans:
            human.change_floor(new_floor)
        return time_in_travel

    def change_floor(self, new_floor):
        self.floor = new_floor
        print(f'Лифт №{self.id} приехал на {self.floor} этаж.')
        return

    def base_algorithm(self, humans_waiting_for_elevator):
        """Ездит по номеру заявки и везёт из точки а в точку б каждого, в порядке вызова,
        вызывает обновление этажа у лифта, вызывает обновление этажа у человека,
        выбрасывает человека из списка на поездку"""

        print(f'Лифт №{self.id} находится на {self.floor} этаже.')
        total_time = 0
        for human in humans_waiting_for_elevator:
            print(f'{human.name} вызвал лифт на {human.current_floor} этаж.')
            total_time += self.elevator_travel(human.current_floor, humans=[human])
            total_time += self.elevator_travel(human.desired_floor, humans=[human])

        print(f'Лифт №{self.id} закончил работу за {total_time} секунд.')
        return total_time

    def min_dist_algorithm(self, humans_waiting_for_elevator):
        print(f'Лифт №{self.id} находится на {self.floor} этаже.')
        total_time = 0
        humans_sorted = sorted_humans_by_distance(self.floor, humans_waiting_for_elevator, waiting=True)
        while len(humans_sorted) > 0:
            print(f'{humans_sorted[0].name} вызвал лифт на {humans_sorted[0].current_floor} этаж.')
            total_time += self.elevator_travel(humans_sorted[0].current_floor, humans=[humans_sorted[0]])
            total_time += self.elevator_travel(humans_sorted[0].desired_floor, humans=[humans_sorted[0]])
            humans_sorted.pop(0)
            humans_sorted = sorted_humans_by_distance(self.floor, humans_sorted,  waiting=True)

        print(f'Лифт №{self.id} закончил работу за {total_time} секунд.')
        return total_time

    def many_people_min_dist_algorithm(self, humans_waiting_for_elevator):
        total_time = 0

        while len(humans_waiting_for_elevator) > 0:
            print(f'Лифт №{self.id} находится на {self.floor} этаже.')
            humans_sorted = sorted_humans_by_distance(self.floor, humans_waiting_for_elevator, waiting=True)
            humans_in_elevator = []
            print(f'{humans_sorted[0].name} вызвал лифт на {humans_sorted[0].current_floor} этаж.')
            total_time += self.elevator_travel(humans_sorted[0].current_floor, [humans_sorted[0]])
            for human in humans_sorted:
                if human.current_floor == self.floor:
                    humans_in_elevator.append(human)
            humans_in_elevator_sorted = sorted_humans_by_distance(self.floor, humans_in_elevator, waiting=False)
            for human_in_elevator in humans_in_elevator_sorted:
                if human_in_elevator.desired_floor is not None:
                    total_time += self.elevator_travel(human_in_elevator.desired_floor, humans_in_elevator_sorted)
                if human_in_elevator.desired_floor is None:
                    humans_in_elevator.remove(human_in_elevator)
                    humans_waiting_for_elevator.remove(human_in_elevator)

        print(f'Лифт №{self.id} закончил работу за {total_time} секунд.')
        return total_time


class Human:
    def __init__(self, name, current_floor, desired_floor, weight):
        self.name = name
        self.current_floor = current_floor
        self.desired_floor = desired_floor
        self.weight = weight

    def change_floor(self, new_floor):
        """Человека довезли на новый этаж и если он попал туда куда нужно, то ему дальше не надо"""
        self.current_floor = new_floor
        if self.desired_floor == self.current_floor:
            self.desired_floor = None
            print(f'{self.name} довезён до нужного этажа.')
        return


def sorted_humans_by_distance(elevator_floor, humans_waiting_for_elevator, waiting):
    humans_distances_list = []
    for human in humans_waiting_for_elevator:
        if waiting:
            human_floor = human.current_floor
        else:
            human_floor = human.desired_floor
        humans_distances_list.append([human, abs(elevator_floor - human_floor)])
    humans_sorted_with_distances = sorted(humans_distances_list, key=itemgetter(1))

    humans_sorted = []
    for human in humans_sorted_with_distances:
        humans_sorted.append(human[0])
    return humans_sorted


def generate_humans(amount, building):
    humans_list = []
    for rnk in range(0, amount):
        name = names.get_full_name()
        successful = False
        while successful is False:
            current_floor = random.randint(building.min_floor, building.max_floor)
            desired_floor = random.randint(building.min_floor, building.max_floor)
            if current_floor != desired_floor:
                successful = True
        weight = random.randint(0, 150)
        humans_list.append(Human(name, current_floor, desired_floor, weight))
    return humans_list


def test_humans():
    human_1 = Human('First', 1, 5, 50)
    human_2 = Human('Second', 1, 5, 50)
    human_3 = Human('Third', 1, 3, 50)
    human_4 = Human('Fourth', 4, 1, 50)
    human_5 = Human('Fifth', 3, 5, 50)
    return [human_1, human_2, human_3, human_4, human_5]

def test_all():
    for i in range(0, 3):
        humans = test_humans()
        if i == 0:
            first_elevator.base_algorithm(humans)
            continue
        elif i == 1:
            second_elevator.min_dist_algorithm(humans)
            continue
        elif i == 2:
            third_elevator.many_people_min_dist_algorithm(humans)
            continue
    return


first_building = Building(1, 1, 9, 27, 10)
first_elevator = Elevator(first_building, 1, 1, 500, 2)
second_elevator = Elevator(first_building, 2, 1, 500, 2)
third_elevator = Elevator(first_building, 3, 1, 500, 2)

times = []
for i in range(0, 3):
    humans = generate_humans(1000, first_building)
    for human in humans:
        print(human.name, human.current_floor, human.desired_floor)
    if i == 0:
        times.append(first_elevator.base_algorithm(humans))
        continue
    elif i == 1:
        times.append(second_elevator.min_dist_algorithm(humans))
        continue
    elif i == 2:
        times.append(third_elevator.many_people_min_dist_algorithm(humans))

print(times)

