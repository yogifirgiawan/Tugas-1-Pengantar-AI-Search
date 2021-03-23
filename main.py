import math

from GeneticAlgorithm import GenericAlgorithm


def fungsi(x, y):
    """
    fungsi yang digunakan dalam genetic algorithm
    """
    return math.cos(x**2) * math.sin(y**2) + (x + y)


if __name__ == "__main__":

    # config yang akan digunakan
    config = {
        "jumlahPopulasi": 50,
        "panjangKromosom": 16,
        "generasi": 50,
        "probCrossOver": 0.85,
        "probMutasi": 0.3,
        "fungsi": fungsi,
        "batas": [[-1, 2], [-1, 1]]
    }
    ga = GenericAlgorithm(config)
    # menampilkan hasil dari perhitungan ga
    ga.perpindahanGenerasi()
    ga.nilaiMaks()
