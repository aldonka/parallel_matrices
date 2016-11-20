from multiprocessing import Pool
import time

global num_of_matrices, time_simple, time_multi


def read_matrices(filename, num=0):
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
    if(num != 0):
        all_matrixes = all_matrixes[0:num]
    num_of_matrices = len(all_matrixes)
    return all_matrixes


def save_result_matrix_to_file(matrix, filename):
    with open(filename, 'wb+') as result_file:
        for row in matrix:
            a = ""
            for el in row:
                a += "%150.2f" % el

            result_file.write("[" + a + "]\n")
        result_file.write("Result of multiplication of %d  matrices in basic file." % num_of_matrices)
        result_file.write("\nBez watkow\n --- Execution time: %s seconds ---" % time_simple)
        result_file.write("\nWatki\n --- Execution time: %s seconds ---" % time_multi)
    result_file.close()


def multiply_all_matrices(arr_of_matrixes):
    arr_of_matrixes.reverse()
    while len(arr_of_matrixes) != 1:
        X = arr_of_matrixes.pop()
        Y = arr_of_matrixes.pop()
        arr_of_matrixes.insert(0, multiply_matrices(X, Y))
    return arr_of_matrixes[0]


def multiply_matrices(X, Y):
    zip_y = zip(*Y)
    return [[sum(ele_x*ele_y for ele_x, ele_y in zip(row_x, col_y))
             for col_y in zip_y] for row_x in X]


def simple_run(filename):
    global time_simple
    m = read_matrices(filename, 100)
    start_time = time.time()
    result = multiply_all_matrices(m)
    stop_time = time.time()
    time_simple = (stop_time - start_time)
    print "--- Execution time: %s seconds ---" % (stop_time - start_time)
    return result


def multi_run(filename):
    global time_multi
    m = read_matrices(filename, 100)
    start_time = time.time()
    p = Pool(6)
    result = p.map(multiply_all_matrices, devide_array(m))
    r = multiply_all_matrices(result)
    stop_time = time.time()
    time_multi = (stop_time - start_time)
    print "--- Execution time: %s seconds ---" % (stop_time - start_time)
    return r


def devide_array(matrices_arr):
    length = len(matrices_arr) / 3
    # length = len(matrices_arr) / 4
    result = [[],[],[]]
    # result = [[],[],[],[]]
    result[0] = matrices_arr[0:length]
    result[1] = matrices_arr[length: 2*length]
    result[2] = matrices_arr[2*length:]
    # result[2] = matrices_arr[2*length: 3*length]
    # result[3] = matrices_arr[3*length:]
    return result


if __name__== '__main__':
    filename = 'sample-matrices.txt'

    print "Bez watkow: "
    simple_run(filename)
    print("Watki : ")
    r = multi_run(filename)
    save_result_matrix_to_file(r, 'r_d_100.txt')