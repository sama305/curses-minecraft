def convertChunk(c):
    current_type = c.data[0]
    count = 0
    result = []

    for i in range(len(c.data)):
        if (current_type == c.data[i] and i < len(c.data) - 1):
            count += 1
        else:
            result.append(str(current_type) + '-' + str(count))
            count = 0
            current_type = c.data[i]
    
    return result