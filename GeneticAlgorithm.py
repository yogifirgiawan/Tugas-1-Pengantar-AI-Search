import random


class GenericAlgorithm:
    def __init__(self, config):
        # jumlah populasi yang digunakan
        self.jumlahPopulasi = config['jumlahPopulasi']
        # panjang kromosom yang akan digenerate
        self.panjangKromosom = config['panjangKromosom']
        # probabilitas crossOver
        self.probCrossOver = config['probCrossOver']
        # probabilitas mutasi
        self.probMutasi = config['probMutasi']
        # banyak generasi yang akan digunakan
        self.generasi = config['generasi']
        # fungsi yang akan digunakan
        self.fungsi = config['fungsi']
        # [xMin,xMaks] , [yMin,yMaks]
        self.batas = config['batas']
        # initial
        self.populasi = []
        for _ in range(self.jumlahPopulasi):
            self.populasi.append(self.generateKromosom())

    def generateKromosom(self):
        """
        fungsi untuk membuat kromosom biner
        """
        result = []
        # looping sebanyak panjangKromosom
        for _ in range(self.panjangKromosom):
            # generate angka random 0 atau 1
            result.append(random.randint(0, 1))
        return result

    def dekodeKromosom(self, kromosom):
        """
        fungsi untuk mendekode kromosom dari biner ke real
        """
        xMin, xMaks = self.batas[0]
        yMin, yMaks = self.batas[1]
        t, x, y = 0, 0, 0
        n = (self.panjangKromosom)//2
        for i in range(0, n):
            t += 2**(-(i+1))
        for i in range(0, n):
            x += kromosom[i] * 2**-(i+1)
            y += kromosom[n + i] * 2**-(i+1)
        x *= (xMaks - xMin / t)
        y *= (yMaks - yMin / t)
        x += xMin
        y += yMin
        return [x, y]

    def totalFitness(self):
        """
        fungsi untuk menghitung nilai fitness dari setiap populasi sekarang
        """
        result = []
        for i in self.populasi:
            result.append(self.fungsi(*self.dekodeKromosom(i)))
        return result

    def RouletteWheel(self, fitness):
        """
        fungsi untuk memilih orang tua dengan metode roulette wheel
        """
        idx = 0
        totalFitness = sum(fitness)
        for i in range(self.jumlahPopulasi):
            if (fitness[i]/totalFitness) > random.uniform(0, 1):
                idx = i
                break
            i = i + 1
        return self.populasi[idx]

    def crossOver(self, x, y):
        """
        fungsi untuk melakukan crossover dengan batasan random
        """
        if random.uniform(0, 1) < self.probCrossOver:
            # generate berapa banyak perpindahan
            pindah = random.randint(0, self.panjangKromosom-1)
            for i in range(pindah):
                # melakukan swap nilai x dan y
                x[i], y[i] = y[i], x[i]
        return [x, y]

    def mutasi(self, keturunan):
        """
        fungsi untuk melakukan mutasi dari keturunan yang diberikan
        """
        for i in range(len(keturunan[0])):
            if random.uniform(0, 1) < self.probMutasi:
                # membalik nilai bit nya
                keturunan[0][i] = 1 - keturunan[0][i]
                keturunan[1][i] = 1 - keturunan[1][i]
        return keturunan

    def SeleksiSurvivor(self, fitness):
        """
        fungsi untuk mencari index dari 2 fitness dengan nilai tertinggi
        """
        elite1, elite2 = 0, 0
        for i in range(1, len(fitness)):
            if fitness[i] > fitness[elite1]:
                elite2 = elite1
                elite1 = i
        return elite1, elite2

    def perpindahanGenerasi(self):
        for _ in range(self.generasi):
            # list fitness
            fitness = self.totalFitness()
            # list populasi baru
            populasiBaru = []
            # dua index terbaik dengan mengambil nilai fitness tertinggi
            elite1, elite2 = self.SeleksiSurvivor(fitness)
            # menambahkan populasi dengan nilai index terbaik ke generasi berikutnya
            populasiBaru.append(self.populasi[elite1])
            populasiBaru.append(self.populasi[elite2])

            for _ in range((self.jumlahPopulasi-2)//2):
                # mencari orang tua dengan memanggil fungsi RouletteWheel
                ortuA = self.RouletteWheel(fitness)
                ortuB = self.RouletteWheel(fitness)
                # mencari orang tua lagi jika a dan b sama
                while(ortuA == ortuB):
                    ortuB = self.RouletteWheel(fitness)
                # melakukan crossOver pada kedua orang tua
                keturunan = self.crossOver(ortuA[:], ortuB[:])
                # melakukan mutasi pada hasil crossOver
                keturunan = self.mutasi(keturunan)
                # menambahkan keturunan ke list populasi baru
                populasiBaru.append(keturunan[0])
                populasiBaru.append(keturunan[1])
            self.populasi = populasiBaru

    def nilaiMaks(self):
        # menghitung ulang nilai fitness
        fitness = self.totalFitness()
        # mencari index finess dengan nilai tertinggi
        idx = fitness.index(max(fitness))
        print("Hasil : ")
        # hasil kromosom terbaik
        print('Kromosom terbaik\t:', self.populasi[idx])
        # nilai fitnessnya
        print('Nilai fitness\t\t:', fitness[idx])
        # nilai hasil dekode kromosom
        print('Dekode kromosom\t\t:', self.dekodeKromosom(self.populasi[idx]))
