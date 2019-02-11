import numpy as np
from numpy import linalg as LA
from matplotlib import pyplot as plt
from matplotlib import animation

class Oscillator:

    def __init__(self,
                 numberMasses = 5,
                 relAmp = [1.0 , 0.8 , 0.6 , 0.4 , 0.4],
                 howLong = 4.0*np.pi*5.0,
                 howMany = 4000):
        self.numberMasses = numberMasses
        self.relAmp = np.array(relAmp)
        self.howLong = howLong
        self.howMany = howMany
        if numberMasses!=len(relAmp):
            raise RuntimeError("number of masses must equal length of relative amplitudes array")

    def setTime(self):
        time = np.linspace(0 , self.howLong , self.howMany)
        return time

    def setMatrix(self,BC):
        N = self.numberMasses
        Dntemp = []
        for ii in range(N):
            Dntemp.append(np.zeros(N))
            Dn = np.matrix(Dntemp)
        for ii in range(N):
            Dn[ii,ii] = 2.0
        for ii in range(N-1):
            Dn[ii+1,ii] = -1.0
            Dn[ii,ii+1] = -1.0
        if BC=="open":
            Dn[0,0] = 1.0
            Dn[N-1,N-1] = 1.0
        return Dn





    def diagonalizeMatrix(self,Dn,BC):
        N = self.numberMasses  
        eValues,eVectors=LA.eig(Dn)
        idx = np.argsort(eValues)
        eValues = eValues[idx]
        eVectors = eVectors[:,idx]
        #scale the frequencies
        if BC=="fixed":
            eValuesMin = eValues[0]
        if BC=="open":
            eValuesMin = eValues[1]
        frequencies = []
        for ii in range(N):
            frequencies.append(eValues[ii]/eValuesMin)
        # extract the amplitudes:
        amplitudes = []
        for ii in range(N):
            Atemp = []
            for jj in range(N):
                Atemp.append(self.relAmp[ii]*eVectors[jj,ii])
            amplitudes.append(Atemp)
        return frequencies , amplitudes
    
    

    def find_x_coord(self,frequencies,amplitudes,x0):
        N = self.numberMasses
        tabLength = float(N)+1.0 
        springLength = tabLength/(float(N+1))
        time = self.setTime()   
        xall = []
        for ii in range(N):
            for jj in range(N):
                xall.append(amplitudes[ii][jj]*np.cos(frequencies[ii]*time) + x0[jj])
        return xall

#################################################################################################################
#################################################################################################################

class longFixed(Oscillator):
    def __init__(self,
                 numberMasses = 5,
                 relAmp = [1.0 , 0.8 , 0.6 , 0.4 , 0.4],
                 howLong = 4.0*np.pi*5.0,
                 howMany = 4000):  
        Oscillator.__init__(self,
                            numberMasses,
                            relAmp,
                            howLong,
                            howMany) 


    def getLengthTableLF(self):
        return float(self.numberMasses + 1)

    def getEqbPositionsLF(self):
        tabLength = self.getLengthTableLF()
        springLength = tabLength/float(self.numberMasses + 1)
        N = self.numberMasses
        x0 = []
        for ii in range(N):
            x0.append((-tabLength*0.5)+(ii+1)*springLength)
        return x0

    def setGraphLimitsLF(self):
        N = self.numberMasses
        xmin = -(float(N)+1)/2.0
        xmax = -xmin
        ymin = xmin
        ymax = xmax
        return (xmin,xmax,ymin,ymax)



    def sineCurvesLF(self):
        pi = np.pi
        N = self.numberMasses
        xmin,xmax,ymin,ymax = self.setGraphLimitsLF()
        sine_size = 50.0*float(N)
        x_sine_curve = np.arange(xmin,xmax,(xmax-xmin)/float(sine_size))
        y_sine_curve = []
        for ii in range(N):
            lmbda = 2.0*(xmax-xmin)/float(ii+1)
            kx = 2.0*pi/lmbda
            y_sine_curve.append(0.5*np.sin(kx*(x_sine_curve-xmin)))
        return x_sine_curve , y_sine_curve


    def plotAnimationLF(self):
        N = self.numberMasses
        Dn = self.setMatrix("fixed")
        (freq,amp) = self.diagonalizeMatrix(Dn,"fixed")
        xall = self.find_x_coord(freq,amp,self.getEqbPositionsLF())
        nmax = 0.5*(float(N)-1.0)
        nmin = -0.5*(float(N)-1.0)
        bias = np.arange(nmax,nmin-1,-1)
        time = self.setTime()
        timeSize = time.size

        tabLength = float(N)+1.0             
        springLength = tabLength/(float(N+1))
        x0 = []
        for ii in range(N):
            x0.append((-tabLength*0.5)+(ii+1)*springLength)

        nspr = 20
        dy = 0.06

        xmin,xmax,ymin,ymax = self.setGraphLimitsLF()
        x_sine_curve , y_sine_curve = self.sineCurvesLF()

        fig = plt.figure()
        ax = plt.axes(xlim=(xmin,xmax),ylim=(ymin,ymax))
        ax.set_aspect("equal")
        ax.text(xmin,ymax+0.1,'$\copyright$2019, Bhaskar Kamble',fontsize=10,rotation=0)
        ax.axis("off")


        lines = []

        for ii in range(N):
            lobj = ax.plot([],[],lw=1,color="black")[0] # sine curves
            lines.append(lobj)

        for ii in range(N):
            lobj = ax.plot([],[],lw=1,color="black",linestyle = "-.")[0] # vertical dotted lines
            lines.append(lobj)

        for ii in range(N):
            for jj in range(N+1):
                lobj = ax.plot([],[],lw=1,color="black")[0]
                lines.append(lobj)
        for ii in range(N):
            for jj in range(N):
                lobj = ax.plot([],[],linestyle="none",marker="s",color="red",markersize=8)[0]
                lines.append(lobj)

        def init():
            for line in lines:
                line.set_data([],[])
            return lines


        def animate(i):
            for lnum,line in enumerate(lines):
                for ii in range(N):
                    if lnum == ii:
                        line.set_data(x_sine_curve,y_sine_curve[ii]+bias[ii])
                for ii in range(N):
                    if lnum == N+ii:
                        xeqb = np.array([x0[ii],x0[ii]])
                        yeqb = np.array([ymin,ymax])
                        line.set_data(xeqb,yeqb)
                for ii in range(N):
                    for jj in range(N+1):
                        if jj==0:
                            sp1 = xmin
                            sp2 = xall[N*ii][i]
                        if jj==N:
                            sp1 = xall[N*ii+N-1][i]
                            sp2 = xmax
                        if (jj != 0) and (jj != N):
                            sp1 = xall[N*ii+jj-1][i]
                            sp2 = xall[N*ii+jj][i]
                        if lnum == 2*N + ii*(N+1) + jj:
                            xspring = np.linspace(sp1,sp2,nspr)
                            yspring_temp = np.arange(xspring.size)
                            yspring = bias[ii] + dy*((-1.0)**yspring_temp)
                            line.set_data(xspring,yspring)
                for ii in range(N):
                    for jj in range(N):
                        if lnum == 2*N + N*(N+1)+N*ii+jj:
                            xls = xall[N*ii+jj][i]
                            yls = bias[ii]
                            line.set_data(xls,yls)
            return lines

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=timeSize, interval=50, blit=True)
        plt.show()

#################################################################################################################
#################################################################################################################

class longOpen(Oscillator):
    def __init__(self,
                 numberMasses = 5,
                 relAmp = [0.0 , 0.4 , 0.4 , 0.4 , 0.4],
                 howLong = 4.0*np.pi*5.0,
                 howMany = 4000):  
                 #in the above YOU specify the arguments to create an instance of the "longFixed" class
        Oscillator.__init__(self,
                            numberMasses,
                            relAmp,
                            howLong,
                            howMany) 
                            # Now the parent class "Oscillator" is instanced with the parameters
                            # you specified in the previous line for the "longFixed" class - Hence
                            # both "Oscillator" and "longFixed" instances have the same parameters



    def getLengthTableLO(self):
        return float(self.numberMasses)

    def getEqbPositionsLO(self):
        tabLength = self.getLengthTableLO()
        springLength = tabLength/float(self.numberMasses)
        N = self.numberMasses
        x0 = []
        for ii in range(N):
            x0.append((-tabLength*0.5 + 0.5*springLength)+ii*springLength)
        return x0


    def setGraphLimitsLO(self):
        N = self.numberMasses
        xmin = -float(N)/2.0
        xmax = -xmin
        ymin = xmin
        ymax = xmax
        return (xmin,xmax,ymin,ymax)

    def sineCurvesLO(self):
        pi = np.pi
        N = self.numberMasses
        xmin,xmax,ymin,ymax = self.setGraphLimitsLO()
        sine_size = 50.0*float(N)
        x_sine_curve = np.arange(xmin,xmax,(xmax-xmin)/float(sine_size))
        y_sine_curve = []
        for ii in range(N-1):
            lmbda = 2.0*(xmax-xmin)/float(ii+1)
            kx = 2.0*pi/lmbda
            y_sine_curve.append(0.5*np.cos(kx*(x_sine_curve-xmin)))
        return x_sine_curve , y_sine_curve


    def plotAnimationLO(self):
        N = self.numberMasses
        Dn = self.setMatrix("open")
        (freq,amp) = self.diagonalizeMatrix(Dn,"open")
        xall = self.find_x_coord(freq,amp,self.getEqbPositionsLO())
        xall = xall[N:]
        nmax = 0.5*(float(N-1)-1.0) 
        nmin = -0.5*(float(N-1)-1.0)
        bias = np.arange(nmax,nmin-1,-1)
        time = self.setTime()
        timeSize = time.size

        tabLength = self.getLengthTableLO()
        springLength = tabLength/(float(N))
        x0 = self.getEqbPositionsLO()

        nspr = 20
        dy = 0.06

        xmin,xmax,ymin,ymax = self.setGraphLimitsLO()
        x_sine_curve , y_sine_curve = self.sineCurvesLO()

        fig = plt.figure()
        ax = plt.axes(xlim=(xmin,xmax),ylim=(ymin,ymax))
        ax.set_aspect("equal")
        ax.text(xmin,ymax+0.1,'$\copyright$2019, Bhaskar Kamble',fontsize=10,rotation=0)
        ax.axis("off")


        lines = []

        for ii in range(N-1):
            lobj = ax.plot([],[],lw=1,color="black")[0] # sine curves
            lines.append(lobj)

        for ii in range(N):
            lobj = ax.plot([],[],lw=1,color="black",linestyle = "-.")[0] # vertical dotted lines
            lines.append(lobj)

        for ii in range(N-1):
            for jj in range(N-1):
                lobj = ax.plot([],[],lw=1,color="black")[0] #springs
                lines.append(lobj)
        for ii in range(N-1):
            for jj in range(N):
                lobj = ax.plot([],[],linestyle="none",marker="s",color="red",markersize=8)[0] #masses
                lines.append(lobj)

        def init():
            for line in lines:
                line.set_data([],[])
            return lines


        def animate(i):
            for lnum,line in enumerate(lines):
                for ii in range(N-1): #sine curves
                    if lnum == ii:
                        line.set_data(x_sine_curve,y_sine_curve[ii]+bias[ii])
                for ii in range(N):   #vertical dotted lines
                    if lnum == N-1+ii:
                        xeqb = np.array([x0[ii],x0[ii]])
                        yeqb = np.array([ymin,ymax])
                        line.set_data(xeqb,yeqb)
                for ii in range(N-1):
                    for jj in range(N-1):
                        sp1 = xall[N*ii+jj][i]
                        sp2 = xall[N*ii+jj+1][i]
                        if lnum == (2*N-1) + ii*(N-1) + jj:
                            xspring = np.linspace(sp1,sp2,nspr)
                            yspring_temp = np.arange(xspring.size)
                            yspring = bias[ii] + dy*((-1.0)**yspring_temp)
                            line.set_data(xspring,yspring)
                for ii in range(N-1):
                    for jj in range(N):
                        if lnum == (2*N-1) + (N-1)*(N-1)+N*ii+jj:
                            xls = xall[N*ii+jj][i]
                            yls = bias[ii]
                            line.set_data(xls,yls)
            return lines

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=timeSize, interval=50, blit=True)
        plt.show()




def main():
    """ """
    numberMasses = 6
    relAmp = [1.0 , 0.8 , 0.6 , 0.4 , 0.4 , 0.3]
    howLong = 4.0*np.pi*5.0
    howMany = 4000
    oscillator_1 = longFixed(numberMasses, relAmp, howLong, howMany)
    oscillator_1.plotAnimationLF()

if __name__ == '__main__':
    main()



