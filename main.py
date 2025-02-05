# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd

# Create a sample DataFrame
data = {'name': ['John', 'Alice', 'Bob', 'Jane', 'Mike'],
        'age': [25, 30, 35, 40, 45],
        'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']}

df = pd.DataFrame(data)

# Delete rows where the city is Chicago
df = df.drop(df[df['city'] == 'Chicago'].index)
print(df)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
