class CustomList(list):
    def __str__(self):
        return super.__str__(self) + " " + str(sum(self))

    @staticmethod
    def same_size(list1, list2):
        while len(list1) > len(list2):
            list2.append(0)
        while len(list1) < len(list2):
            list1.append(0)
        return list1, list2

    def __add__(self, other: list):
        copy, other = CustomList.same_size(self.copy(), other.copy())
        for i, num in enumerate(other):
            copy[i] += num
        return CustomList(copy)

    def __sub__(self, other: list):
        copy, other = CustomList.same_size(self.copy(), other.copy())
        for i, num in enumerate(other):
            copy[i] -= num
        return CustomList(copy)

    def __radd__(self, other: list):
        copy, other = CustomList.same_size(self.copy(), other.copy())
        for i, num in enumerate(other):
            copy[i] += num
        return CustomList(copy)

    def __iadd__(self, other: list):
        return self.__add__(other)

    def __rsub__(self, other: list):
        copy, other = CustomList.same_size(self.copy(), other.copy())
        for i, num in enumerate(copy):
            other[i] -= num
        return CustomList(other)

    def __isub__(self, other: list):
        return self.__sub__(other)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)
