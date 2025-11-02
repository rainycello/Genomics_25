import matplotlib.pyplot as plt

sizes = [2, 75, 150]
mapped_reads = [1000, 9800, 15000]  # wstaw swoje wartości
times = [5, 12, 20]                  # wstaw swoje czasy w sekundach

plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.plot(sizes, mapped_reads, marker='o')
plt.xlabel('Ziarno (bp)')
plt.ylabel('Zmapowane odczyty')
plt.title('Liczba zmapowanych odczytów')

plt.subplot(1,2,2)
plt.plot(sizes, times, marker='o', color='r')
plt.xlabel('Ziarno (bp)')
plt.ylabel('Czas mapowania (s)')
plt.title('Czas mapowania')

plt.tight_layout()
plt.show()
