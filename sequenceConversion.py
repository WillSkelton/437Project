

def convertSequenceToData(sequence, chunkSize):
    data = []
    labels = []

    if len(sequence) < chunkSize:
        return data, labels

    for index in range(len(sequence) - chunkSize + 1):
        chunk = sequence[index:index + chunkSize]

        data.append(chunk[:-1])
        labels.append(chunk[-1])

    return data, labels


def main():
    chunkSize = 6
    sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    s2 = [1, 2, 3, 4, 5, 6]

    data, labels = convertSequenceToData(s2, chunkSize)

    for item, label in zip(data, labels):
        print(item, label)


main()
