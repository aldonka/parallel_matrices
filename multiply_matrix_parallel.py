global num_of_matrices

def read_matrices(filename):
    global num_of_matrices
    all_matrixes = []
    matrix = []
    with open(filename, 'r') as myfile:
        for line in myfile.readlines():
            if line == '\n':
                all_matrixes.append(matrix)
                matrix = []
            else:
                m = []
                for l in line.split(';'):
                    l.replace('\n', '')
                    m.append(float(l))
                matrix.append(m)
    myfile.close()
    num_of_matrices = len(all_matrixes)
    print all_matrixes
    return all_matrixes


def save_result_matrix_to_file(matrix, filename):
    with open(filename, 'wb+') as result_file:
        for row in matrix:
            a = ""
            for el in row:
                a += "%8.4f" % el

            result_file.write("[" + a + "]\n")
        result_file.write("Result of multiplication of %d  matrices in basic file." % num_of_matrices)
    result_file.close()

def multiply_all_matrices(arr_of_matrixes):
    while len(arr_of_matrixes) != 1:
        X = arr_of_matrixes.pop()
        Y = arr_of_matrixes.pop()
        arr_of_matrixes.insert(0, multiply_matrices(X, Y))
    return arr_of_matrixes[0]


def multiply_matrices(X, Y):
    zip_y = zip(*Y)
    return [[sum(ele_x*ele_y for ele_x, ele_y in zip(row_x, col_y))
             for col_y in zip_y] for row_x in X]



filename = 'test_min.txt'
m = read_matrices(filename)

result = multiply_all_matrices(m)
for row in result:
    a = ""
    for el in row:
        a += "%47.2f" %el

    print "[" + a + "]"

print "In file: %s, num of matrixes in file %d" %(filename, num_of_matrices)
save_result_matrix_to_file(result, 'result_m.txt')