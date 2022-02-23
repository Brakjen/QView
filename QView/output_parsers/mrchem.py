import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


class MRChemOutput:
    def __init__(self, filename):
        self.filename = filename
        self.content = open(self.filename).readlines()

    def __str__(self):
        return open(self.filename).read()

    def __repr__(self):
        return f'MRChemOutput object <from file: {self.filename}>'

    def findUnique(self, query, col, type):
        for line in self.content:
            if line.strip().startswith(query):
                try:
                    return type(line.split()[col])
                except ValueError:
                    return None

    def getOrbitalThreshold(self):
        return self.findUnique('Energy threshold', 3, float)

    def getEnergyThreshold(self):
        return self.findUnique('Orbital threshold', 3, float)

    def plotSCFConvergence(self):
        runs = self.getSCFRuns()
        n = self.getNumberOfSCFRuns()
        orbital_thrs = self.getOrbitalThreshold()
        energy_thrs = self.getEnergyThreshold()

        if n == 0:
            return

        df = pd.DataFrame(runs[n-1])

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.set_context('paper')
        sns.set_style('whitegrid')

        sns.lineplot(ax=ax, x=df.index, y=abs(df.Update), marker='.', lw=2, color='blue', label='E update')
        sns.lineplot(ax=ax, x=df.index, y=abs(df.Residual), marker='.', lw=2, color='crimson', label='MO residual')

        if orbital_thrs is not None:
            ax.axhline(orbital_thrs, lw=1, ls='--', color='blue')
        if energy_thrs is not None:
            ax.axhline(energy_thrs, lw=1, ls='--', color='crimson')

        ax2 = ax.twinx()
        ax2.set_ylabel('Energy [Ha]')
        sns.lineplot(ax=ax2, x=df.index, y=df.Energy, marker='.', lw=2, ls='-', color='black')

        ax.set_yscale('log')
        ax.set_ylabel(None)
        ax.set_xlabel('SCF iterations')

        ax.legend(bbox_to_anchor=(0.5, 1.0), loc='lower center', ncol=2, fontsize=9, title=self.filename, title_fontsize='x-small')
        plt.tight_layout()
        plt.show()

    def getNumberOfSCFRuns(self):
        return self.__str__().count('Iter')

    def getSCFRuns(self):
        """Return a dict of SCF iterations and energies"""

        result = {i: {'Energy': [],
                      'Update': [],
                      'Residual': []} for i in range(self.getNumberOfSCFRuns())}
        iter_counter = 0
        for i, line in enumerate(self.content):
            if line.strip().startswith('Iter'):
                # Set the start index two down from the matched line
                start = i + 2

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
                    if not any([w in subline for w in ['error', 'Error', 'Uninitialized', 'C']]):
                        try:
                            r = float(subline.split()[1])
                            e = float(subline.split()[2])
                            u = float(subline.split()[3])
                            result[iter_counter]['Residual'].append(r)
                            result[iter_counter]['Energy'].append(e)
                            result[iter_counter]['Update'].append(u)
                        except ValueError:
                            continue
                iter_counter += 1
        return result
