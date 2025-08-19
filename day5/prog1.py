## accept a number from the user and find the next possible smallest number which is bigger than the given having all the digits of the given number.


def next_bigger_number(n):
    # Convert the number to a list of digits
    digits = list(str(n))
    length = len(digits)

    # Step 1: Find the first digit (from the right) that is smaller than the digit next to it
    for i in range(length - 2, -1, -1):
        if digits[i] < digits[i + 1]:
            break
    else:
        # If no such digit is found, the number is the highest permutation
        return "No higher number possible"

    # Step 2: Find the smallest digit on right side of (i) which is larger than digits[i]
    for j in range(length - 1, i, -1):
        if digits[j] > digits[i]:
            break

    # Step 3: Swap the two digits
    digits[i], digits[j] = digits[j], digits[i]

    # Step 4: Reverse the digits after position i
    digits[i + 1:] = reversed(digits[i + 1:])

    # Join digits back to form the final number
    return int("".join(digits))


# ---- Main program ----
if __name__ == "__main__":
    try:
        num = int(input("Enter a number: "))
        result = next_bigger_number(num)
        print("Next bigger number with same digits:", result)
    except ValueError:
        print("Please enter a valid integer.")
