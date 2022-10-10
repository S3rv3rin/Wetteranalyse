import numpy as np

listeMitListen = [[10, 20, 30], [10, 20, 30], [10, 20, 30]]
npArray = np.array(listeMitListen)

print("Liste mit drei Listen, Die "
      "Trennung durch Kommata: \n",
      "listeMitListen = ", listeMitListen)

print("\nArray mit zwei Dimensionen. "
      "Jedes enthaltene Array \n"
      "enthält ein weiteres Array.\n"
      "npArray = np.array(listeMitListen)\n", npArray)

npArray[0] *= 2
npArray[1] *= 3
npArray[2] *= 4
print("\nVektorisieren:")
for i in range(len(npArray)):
    print(f"npArray[{i}] *= {i + 2} ergibt {npArray[i]}")

print("\nZugriff auf die zweite Zahl im zweiten Array:\n"
      "1. Name des Arrays          = npArray\n"
      "2. Index des ersten Arrays  = [0]\n"
      "3. Index des zweiten Arrays = [2]\n"
      f"npArray[0][2] = {npArray[0][2]}")

