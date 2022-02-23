import shutil

def getHostname(cluster):
    return cluster + '.sigma2.no'


def getCluster(hostname):
    return hostname.split('.')[0]


def clearDir(dir):
    shutil.rmtree(dir)


def determineQMCode(path):
    if path is None:
        return

    isGaussian, isORCA, isMRChem = False, False, False

    with open(path) as f:
        s = f.read()

    if 'Frank Neese' in s:
        isORCA = True
    elif 'Stig Rune Jensen' in s:
        isMRChem = True
    elif 'Gaussian, Inc' in s:
        isGaussian = True

    return isGaussian, isORCA, isMRChem