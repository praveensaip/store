snack_names = ['Chips', 'Cookies', 'Soda','test']
quantities = [2, 3, 1,3]
rates = [1.5, 2.0, 1.25]

for name, qty, rate in zip(snack_names, quantities, rates):
    print(name,qty,rate)
    # print(f"You ordered {qty} {name}(s) at ${rate} each.")

# Output:
# You ordered 2 Chips(s) at $1.5 each.
# You ordered 3 Cookies(s) at $2.0 each.
# You ordered 1 Soda(s) at $1.25 each.
