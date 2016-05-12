def multiply_vectors(v1, v2):
    return [a * b for a, b in zip(v1, v2)]


def addition_vectors(v1, v2):
    return [a + b for a, b in zip(v1, v2)]


def devide_vectors(v1, v2):
    return [a / b for a, b in zip(v1, v2)]


def multiply_matrices(m1, m2):
    return [[sum(a * b for a, b in zip(m1_row, m2_col)) for m2_col in zip(*m2)] for m1_row in m1]


def multiply_matrix_and_vector(m, v):
    return vector_to_row(multiply_matrices(m, vector_to_column(v)))


def vector_to_column(v):
    return list(map(list, zip(v)))

def vector_to_row(v):
    return [item for sub_list in v for item in sub_list]
