import argparse
import numpy as np
import sys
from math import *

class Coordinates_transformation:

    def __init__(self):
    
        self.a = 6378137
        self.e2 = 0.00669438002290
    
    def Np(self, f):
        N = self.a / np.sqrt(1- self.e2 * np.sin(f)**2)
        return(N)
    
    def dms2rad(d,m,s):
        kat_rad = radians(d + m/60 + s/3600)
        return (kat_rad)
    
    def A_0(self):
        A0 = 1 - (self.e2 / 4) - ((3 * self.e2 ** 2) / 64) - ((5 * self.e2 ** 3) / 256)
        return(A0)

    def A_2(self):
        A2 = (3 / 8) * (self.e2 + (self.e2 ** 2) / 4 + (15 * self.e2 ** 3) / 128)
        return(A2)

    def A_4(self):
        A4 = (15 / 256) * (self.e2 ** 2 + (3 * self.e2 ** 3) / 4)
        return(A4)

    def A_6(self):
        A6 = (35 * self.e2 ** 3) / 3072
        return(A6)
    
    def sigma(self,b):
        A0 = A_0(self.e2)
        A2 = A_2(self.e2)
        A4 = A_4(self.e2)
        A6 = A_6(self.e2)
        sig = self.a * ((A0 * b) - (A2 * np.sin(2 * b)) + (A4 * np.sin(4 * b)) - (A6 * np.sin(6 * b)))
        return(sig)
    
    def xyz2blh(self, X, Y, Z):
        p = np.sqrt(X**2 + Y**2)
        #print('p=',p)
        f = np.arctan(Z /( p * (1 - self.e2)))
        #dms(f)
        while True:
            N = self.Np(f)
            #print('N = ',N)
            h = (p / np.cos(f)) - N
           # print('h = ',h)
            fp = f
            f = np.arctan(Z / (p * (1 - self.e2 * (N / (N + h)))))
            #dms(f)
            if np.abs(fp - f) <( 0.000001/206265):
                break
        l = np.arctan2(Y,X)
        return (f,l,h)
    
    def blh2xyz(self,f,l,h):
            N = self.Np(f)
            X = (N + h) * np.cos(f) * np.cos(l)
            Y = (N + h) * np.cos(f) * np.sin(l)
            Z = (N * (1 - self.e2) + h) * np.sin(f)
            return(X,Y,Z)
    
    #chyba trzba printować na końcu wyniki funkcji żeby się wywietlały na tablicy użytkownika
    #nie wiem czy dobrze ale użytkownik musi podac XYZ0 - dla satelity
    # oraz XYZ - dla anteny
    def xyz2neu(self,X,Y,Z,X0,Y0,Z0):
        p = np.sqrt(X**2 + Y**2)
        #print('p=',p)
        f = np.arctan(Z /( p * (1 - self.e2)))
        #dms(f)
        while True:
            N = self.Np(f)
            #print('N = ',N)
            h = (p / np.cos(f)) - N
           # print('h = ',h)
            fp = f
            f = np.arctan(Z / (p * (1 - self.e2 * (N / (N + h)))))
            #dms(f)
            if np.abs(fp - f) <( 0.000001/206265):
                break
        l = np.arctan2(Y,X)
        R = np.array([[-np.sin(f)*np.cos(l), -np.sin(l), np.cos(f)*np.cos(l)],
                      [-np.sin(f)*np.sin(l), np.cos(l), np.cos(f)*np.sin(l)],
                      [np.cos(f), 0, np.sin(f)]])
        dXYZ = np.array([X0,Y0,Z0])- np.array([X,Y,Z])
        NEU = R.T @ dXYZ
        return(NEU)    
    
    def blGRS802xyz2000(self,b,l):
        lam0 = 0
        n = 0
        if l > dms2rad(13, 30, 0) and l < dms2rad(16, 30, 0):
            lam0 = lam0 + dms2rad(15, 0, 0)
            n = n + 5
        if l > dms2rad(16, 30, 0) and l < dms2rad(19, 30, 0): 
            lam0 = lam0 + dms2rad(18, 0, 0)
            n = n + 6
        if l > dms2rad(19, 30, 0) and l < dms2rad(22, 30, 0): 
            lam0 = lam0 + dms2rad(21, 0, 0)
            n = n + 7
        if l > dms2rad(22, 30, 0) and l < dms2rad(25, 30, 0): 
            lam0 = lam0 + dms2rad(24, 0, 0)
            n = n + 8
        b2 = (self.a ** 2) * (1 - self.e2)
        ep2 = (self.a ** 2 - b2) / b2
        dl = l - lam0
        t = tan(b)
        n2 = ep2 * (cos(b) ** 2)
        N = Np(self,b)
        sig = sigma(self,b)
        xgk = sig + ((dl ** 2 / 2) * N * np.sin(b) * np.cos(b) * (1 + (((dl ** 2)/12) * (np.cos(b) ** 2) * (5 - t **2 + 9 * n2 + 4 * n2 ** 2)) + (((dl ** 4) / 360) * (np.cos(b) ** 4 ) * (61 - 58 * (t ** 2) + t ** 4 + 270 * n2 - 330 * n2 * (t ** 2)))))
        ygk = dl * N * np.cos(b) * (1 + (((dl ** 2)/6) * (np.cos(b) ** 2) * (1 - t ** 2 + n2)) + (((dl ** 4 ) / 120) * (np.cos(b) ** 4) * (5 - 18 * t ** 2 + t ** 4 + 14 * n2 - 58 * n2 * t ** 2))) 
        m = 0.999923
        x = xgk * m
        y = ygk * m + n * 1000000 + 500000  
        return(x,y)                  
    
    def blGRS802xy1992(self,b,l):
        L1 = dms2rad(19, 0 ,0)
        b2 = (self.a ** 2) * (1 - self.e2)
        ep2 = (self.a ** 2 - b2) / b2
        dl = l - L1
        t = tan(b)
        n2 = ep2 * (cos(b) ** 2)
        N = Np(self,b)
        sig = sigma(self,b)
        xgk = sig + ((dl ** 2 / 2) * N * np.sin(b) * np.cos(b) * (1 + (((dl ** 2)/12) * (np.cos(b) ** 2) * (5 - t **2 + 9 * n2 + 4 * n2 ** 2)) + (((dl ** 4) / 360) * (np.cos(b) ** 4 ) * (61 - 58 * (t ** 2) + t ** 4 + 270 * n2 - 330 * n2 * (t ** 2)))))
        ygk = dl * N * np.cos(b) * (1 + (((dl ** 2)/6) * (np.cos(b) ** 2) * (1 - t ** 2 + n2)) + (((dl ** 4 ) / 120) * (np.cos(b) ** 4) * (5 - 18 * t ** 2 + t ** 4 + 14 * n2 - 58 * n2 * t ** 2))) 
        m = 0.9993 
        x = xgk * m - 5300000
        y = ygk * m + 500000
        return(x,y)
    


if __name__ == "__main__":

    trans = Coordinates_transformation()

    parser = argparse.ArgumentParser(description='Transform coordinates.')
    parser.add_argument(dest='method', metavar='M', nargs=1, type=str,
                        help="""write name of the method
                                xyz2blh - Metoda zmiany współrzędnych prostokątnych (zyz) na współrzędne geodezyjne (blh)
                                blh2xyz - Metoda zmiany współrzędnych geodezyjnych (blh) na współrzędne prostokątne (xyz)
                                xyz2neu - Metoda zmiany współrzędnych protokątnych (xyz) na współrzędne topocentryczne (neu)
                                blGRS802xyz2000 - Metoda zmiany współrzędnych z układy GRS80 na współrzędne w układzie 2000
                                blGRS802xy1992 - Metoda zmiany współrzędnych z układy GRS80 na współrzędne w układzie 1999
                                """)
                                
    # trzeba stworzyć funkcję wywołującą w jaki sposób użytkownik chce wgrać dane do pliku
    parser.add_argument(dest='data_loading', metavar='L', nargs=1, type=str,
                            help="""choose how would you like to load data:
                                by .txt file
                                by input""")   
                                
    parser.add_argument(dest='data', metavar='D', type=float, nargs='+',
                        help="""write coordinates coordinates for convertion""")

                                    
    args = parser.parse_args()
    print(args) #?
    func = getattr(trans, args.method[0])
    
    # prepearing structure of data based on selected method
    if args.method[0] in {'xyz2blh'}:
        
        # checks if the given data is correct based on its length
        if len(args.data) % 3 != 0:
            print("insufficient number of given positioning data")
            sys.exit()
        
        data = [(args.data[i], args.data[i+1], args.data[i+2]) for i in range(0, len(args.data), len(args.data)//3)]
        print(data)
    if args.method[0] in {'xyz2neu'}:
        pass
    if args.method[0] in {'blGRS802xyz2000', 'blGRS802xy1992'}:
        pass
    else:
        print("""please, pick proper function""")    
    
    # calculations based on chosen method
    result = []
    for point in data:
        result.append(func(*point))
    
    print(result)
    #if not Path.is_file("results_10.txt"):
    with open("results.txt", 'w') as file:
        for point in result:
            for i in point:
                file.write(str(i)+';')
            file.write('\n')
        
    
    
    

