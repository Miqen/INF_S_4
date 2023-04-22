import argparse
import numpy as np
import sys

class Coordinates_transformation:

    def __init__(self):
    
        self.a = 6378137
        self.e2 = 0.00669438002290
    
    def Np(self, f):
        N = self.a / np.sqrt(1- self.e2 * np.sin(f)**2)
        return(N)
    
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
    
    def blh2xyz(self):
        pass
    
    def xyz2neu(self):
        pass
    
    def bl2xyz2000(self):
        pass
    
    def bl2xyz1992(self):
        pass
    


if __name__ == "__main__":

    trans = Coordinates_transformation()

    parser = argparse.ArgumentParser(description='Transform coordinates.')
    parser.add_argument(dest='method', metavar='M', nargs=1, type=str,
                        help="""write name of the method
                                xyz2blh - opis
                                kolejne i itd""")
                                
    parser.add_argument(dest='data', metavar='D', type=float, nargs='+',
                        help="""write coordinates coordinates for convertion""")
                                    

    args = parser.parse_args()
    print(args)
    func = getattr(trans, args.method[0])
    
    # prepearing structure of data based on selected method
    if args.method[0] in {'xyz2blh', 'xyz2neu'}:
        
        # checks if the given data is correct based on its length
        if len(args.data) % 3 != 0:
            print("insufficient number of given positioning data")
            sys.exit()
        
        data = [(args.data[i], args.data[i+1], args.data[i+2]) for i in range(0, len(args.data), len(args.data)//3)]
        print(data)
    else:
        pass # wszykie inne -> ze stopni na metry
    
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
        
    
    
    

