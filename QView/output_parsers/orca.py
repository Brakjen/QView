import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['axes.formatter.useoffset'] = False


class OrcaOutput:
    def __init__(self, filename):
        self.filename = filename
        self.content = open(self.filename).readlines()
        self.printLevel = self.getPrintLevel()

    def __str__(self):
        return open(self.filename).read()

    def __repr__(self):
        return f'OrcaOutput object <from file: {self.filename}>'

    def findUnique(self, query, col, type):
        for line in self.content:
            if line.strip().startswith(query):
                return type(line.split()[col])

    def getPrintLevel(self):
        for line in self.getInputSection():
            if 'largeprint' in line.lower():
                return 'large'
            elif 'smallprint' in line.lower():
                return 'small'
            elif 'minimalprint' in line.lower():
                return 'minimal'
            else:
                return 'normal'

    def isSinglePointRun(self):
        if '* Single Point Calculation *' in self.__str__():
            return True
        else:
            return False

    def isGeometryOptimizationRun(self):
        if '* Geometry Optimization Run *' in self.__str__():
            return True
        else:
            return False

    def isFrequencyRun(self):
        if '* Energy+Gradient Calculation *' in self.__str__():
            return True
        else:
            return False

    def getNumberOfSCFRuns(self):
        return self.__str__().count('SCF ITERATIONS')

    def getNumberOfSCFIterationsPerGeomCycle(self):
        """Return a list of floats containing the number of SCF iterations needed for converging each geom step"""
        c = filter(lambda x: ' '.join(x.split()).startswith("* SCF CONVERGED AFTER"), self.content)
        return list(map(int, map(lambda x: x.split()[4], c)))

    def getMaxForcesInGeomOpt(self):
        """Return a list of floats containing all Max Forces for each geometry iteration"""
        l = filter(lambda x: x.strip().startswith("MAX gradient"), self.content)
        l = filter(lambda x: len(x.split()) > 4, l)
        return list(map(float, map(lambda x: x.strip().split()[2], l)))

    def getRMSForcesInGeomOpt(self):
        """Return a list of floats containing all RMS Forces for each geometry iteration"""
        l = filter(lambda x: x.strip().startswith("RMS gradient"), self.content)
        l = filter(lambda x: len(x.split()) > 4, l)
        return list(map(float, map(lambda x: x.strip().split()[2], l)))

    def getToleranceMaxForceGeomOpt(self):
        """Return the Max Force convergence tolerance as float"""
        for line in self.content:
            if line.strip().startswith("MAX gradient") and len(line.split()) > 4:
                return float(line.strip().split()[3])

    def getToleranceRMSForceGeomOpt(self):
        """Return the RMSD Force convergence tolerance as float"""
        for line in self.content:
            if line.strip().startswith("RMS gradient") and len(line.split()) > 4:
                return float(line.strip().split()[3])

    def getToleranceMaxStepGeomOpt(self):
        """Return the Max Step convergence tolerance as float
        :return: float
        """
        for line in self.content:
            if line.strip().startswith("MAX step"):
                return float(line.strip().split()[3])

    def getToleranceRMSStepGeomOpt(self):
        """Return the RMSD Step convergence tolerance as float
        :return: float
        """
        for line in self.content:
            if line.strip().startswith("RMS step"):
                return float(line.strip().split()[3])

    def getMaxStepsInGeomOpt(self):
        """Return a list of floats containing all Max Steps for each geometry iteration"""
        l = filter(lambda x: x.strip().startswith("MAX step"), self.content)
        return list(map(float, map(lambda x: x.strip().split()[2], l)))

    def getRMSStepsInGeomOpt(self):
        """Return a list of floats containing all RMS Steps for each geometry iteration"""
        l = filter(lambda x: x.strip().startswith("RMS step"), self.content)
        return list(map(float, map(lambda x: x.strip().split()[2], l)))

    def getToleranceEnergyChangeInGeomOpt(self):
        return self.findUnique('Energy Change', 4, float)

    def getSCFRuns(self):
        """Return a dict of SCF iterations and energies"""

        # FIXME: Account for different print levels. SCF section very different in !largeprint
        if self.printLevel != 'normal':
            return {}

        result = {i: {'Energy': []} for i in range(self.getNumberOfSCFRuns())}
        iter_counter = 0
        for i, line in enumerate(self.content):
            if line.strip().startswith('SCF ITERATIONS'):
                # Set the start index three down from the matched line
                start = i + 3

                # Counter for going through scf iteration lines
                line_counter = 0

                subline = 1
                while subline:
                    # Break if we reach the end of the file
                    try:
                        subline = self.content[start + line_counter].strip()
                    except IndexError:
                        break
                    line_counter += 1
                    if '*' not in subline and subline != '':
                        try:
                            e = float(subline.split()[1])
                            result[iter_counter]['Energy'].append(e)
                        except ValueError:
                            continue
                iter_counter += 1
        return result

    def getInputSection(self):
        """Retrieve input section from output file"""
        inputfile = []
        for i, line in enumerate(self.content):
            if line.strip().startswith('INPUT FILE'):
                start = i + 3
                subline = ''

                counter = 0
                while 'END OF INPUT' not in subline:
                    subline = self.content[start + counter]
                    inline = subline.split('>')[-1].strip()
                    inputfile.append(inline)
                    counter += 1
        return inputfile[:-1]

    def plotGeometryConvergence(self, pid=None):
        tolMaxForce = self.getToleranceMaxForceGeomOpt()
        tolRMSForce = self.getToleranceRMSForceGeomOpt()
        tolMaxStep = self.getToleranceMaxStepGeomOpt()
        tolRMSStep = self.getToleranceRMSStepGeomOpt()

        maxForces = self.getMaxForcesInGeomOpt()
        RMSForces = self.getRMSForcesInGeomOpt()
        maxSteps = self.getMaxStepsInGeomOpt()
        RMSSteps = self.getRMSStepsInGeomOpt()

        NoSCFIterations = self.getNumberOfSCFIterationsPerGeomCycle()

        totalEnergies = [val['Energy'][0] for key, val in self.getSCFRuns().items()]

        energyChanges = [abs(totalEnergies[i] - totalEnergies[i-1]) for i in range(1, len(totalEnergies))]

        fig, ((tl, tr), (ll, lr)) = plt.subplots(ncols=2, nrows=2, dpi=100, figsize=(6, 6))
        fig.suptitle(f'Geometry Convergence Plots')

        # Top left axis: Number of SCF iterations
        tl.bar([i for i in range(len(NoSCFIterations))], NoSCFIterations, color='skyblue', ec='black')
        tl.set_xlabel('Geometry iteration')
        tl.set_ylabel('Number of SCF iterations')

        # Top right axis: Energetics
        tr2 = tr.twinx()
        tr.plot([i for i in range(len(energyChanges))], energyChanges, color='Blue', ls='-', lw=2, marker='.')
        tr2.plot([i for i in range(len(totalEnergies))], totalEnergies, color='black', ls='-', lw=2, marker='.')
        tr.axhline(self.getToleranceEnergyChangeInGeomOpt(), color='blue', ls=':', lw=1)
        tr.set_yscale('log')
        tr.set_ylabel('Energy change (au)')
        tr2.set_ylabel('Final SCF Energy (au)')
        tr.set_xlabel('Geometry iteration')

        # Lower left axis: Forces
        ll.plot(maxForces, color='blue', ls='-', lw=2, marker='.')
        ll.plot(RMSForces, color='crimson', ls='-', lw=2, marker='.')
        ll.axhline(tolMaxForce, color='blue', ls=':', lw=2)
        ll.axhline(tolRMSForce, color='crimson', ls=':', lw=2)
        ll.set_yscale('log')
        ll.set_ylabel('Forces (au)')
        ll.set_xlabel('Geometry iteration')

        # Lower left axis: Displacements
        lr.plot(maxSteps, color='blue', ls='-', lw=2, marker='.')
        lr.plot(RMSSteps, color='crimson', ls='-', lw=2, marker='.')
        lr.axhline(tolMaxStep, color='blue', ls=':', lw=2)
        lr.axhline(tolRMSStep, color='crimson', ls=':', lw=2)
        lr.set_yscale('log')
        lr.set_ylabel('Displacements (au)')
        lr.set_xlabel('Geometry iteration')

        plt.tight_layout()
        plt.show()
        return