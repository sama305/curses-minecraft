def arrToData(c):
    current_type = c.data[0]
    count = 0
    result = []

    for i in range(len(c.data)):
        if (current_type == c.data[i] and i < len(c.data) - 1):
            count += 1
        else:
            result.append(str(current_type) + '-' + str(count))
            count = 1
            current_type = c.data[i]

    return result

def dataToArr(d):
    result = []
    for i in range(len(d)):
        split = d[i].split('-')
        type = split[0]
        count = split[1]

        for t in range(int(count)):
            result.append(int(type))

    return result
