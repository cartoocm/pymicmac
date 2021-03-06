#!/usr/bin/python
import sys, numpy, os, math, argparse
from tabulate import tabulate
from pymicmac import utils_execution

def run(xmlFile, foldersNames):
    (gcpsXYZ, cpsXYZ) = utils_execution.readGCPXMLFile(xmlFile)
    numGCPs = len(gcpsXYZ)
    numCPs = len(cpsXYZ)
    numPs = numGCPs + numCPs

    tableGCPs = []
    tableCPs = []
    tableKOs = []

    for folderName in foldersNames.split(','):
        if folderName.endswith('/'):
            folderName = folderName[:-1]

        logFileName = folderName + '/GCPBascule.log'

        if os.path.isfile(logFileName):
            lines = open(logFileName,'r').read().split('\n')
            (dsGCPs,usGCPs,vsGCPs,wsGCPs) = ([],[],[],[])
            (dsCPs,usCPs,vsCPs,wsCPs) = ([],[],[],[])

            pKOs = []

            for line in lines:
                if line.count('Dist'):
                    gcp = line.split()[1]
                    fields = line.split('[')[-1].split(']')[0].split(',')
                    # u = math.fabs(float(fields[0]))
                    # v = math.fabs(float(fields[1]))
                    # w = math.fabs(float(fields[2]))
                    d = float(line.split('Dist')[-1].split()[0].split('=')[-1])

                    if gcp in gcpsXYZ:
                        dsGCPs.append(d)
                        # usGCPs.append(u)
                        # vsGCPs.append(v)
                        # wsGCPs.append(w)
                    elif gcp in cpsXYZ:
                        dsCPs.append(d)
                        # usCPs.append(u)
                        # vsCPs.append(v)
                        # wsCPs.append(w)
                    else:
                        raise Exception('GCP/CP: ' + gcp + ' not found')

                elif line.count('NOT OK'):
                    pKOs.append(line.split(' ')[4])

            numGCPsFile = len(dsGCPs)
            numCPsFile = len(dsCPs)
            numPKOsFile = len(pKOs)
            numPsFile = numGCPsFile + numCPsFile + numPKOsFile

            if numPsFile != numPs:
                print("WARNING: number of GCPs/CPs (" + str(numPsFile) + ") processed in " + folderName + ' does not match the number in ' + xmlFile + "(" + str(numPs) + ")")

            if len(pKOs):
                tableKOs.append([folderName ,','.join(pKOs)])
            else:
                tableKOs.append([folderName ,'-'])

            pattern = "%0.4f"
            if len(dsGCPs):
                tableGCPs.append([folderName, pattern % numpy.min(dsGCPs), pattern % numpy.max(dsGCPs), pattern % numpy.mean(dsGCPs), pattern % numpy.std(dsGCPs), pattern % numpy.median(dsGCPs)])
                #tableGCPs.append([folderName, pattern % numpy.mean(dsGCPs), pattern % numpy.std(dsGCPs), pattern % numpy.mean(usGCPs), pattern % numpy.std(usGCPs), pattern % numpy.mean(vsGCPs), pattern % numpy.std(vsGCPs), pattern % numpy.mean(wsGCPs), pattern % numpy.std(wsGCPs)])
            else:
                tableGCPs.append([folderName, '-', '-', '-', '-', '-'])
                #tableGCPs.append([folderName, '-', '-', '-', '-', '-', '-', '-', '-'])
            if len(dsCPs):
                tableCPs.append([folderName, pattern % numpy.min(dsCPs), pattern % numpy.max(dsCPs), pattern % numpy.mean(dsCPs), pattern % numpy.std(dsCPs), pattern % numpy.median(dsCPs)])
                #tableCPs.append([folderName, pattern % numpy.mean(dsCPs), pattern % numpy.std(dsCPs), pattern % numpy.mean(usCPs), pattern % numpy.std(usCPs), pattern % numpy.mean(vsCPs), pattern % numpy.std(vsCPs), pattern % numpy.mean(wsCPs), pattern % numpy.std(wsCPs)])
            else:
                tableCPs.append([folderName, '-', '-', '-', '-', '-'])
                #tableCPs.append([folderName, '-', '-', '-', '-', '-', '-', '-', '-'])
        else:
            tableKOs.append([folderName ,'-'])

            tableGCPs.append([folderName, '-', '-', '-', '-', '-'])
            #tableGCPs.append([folderName, '-', '-', '-', '-', '-', '-', '-', '-'])
            tableCPs.append([folderName, '-', '-', '-', '-', '-'])
            #tableCPs.append([folderName, '-', '-', '-', '-', '-', '-', '-', '-'])

    print("###########################")
    print("GCPBascule Dists statistics")
    print("###########################")
    print('KOs')
    print(tabulate(tableKOs, headers=['#Name', '',]))
    print()

    header = ['#Name', 'Min', 'Max', 'Mean', 'Std', 'Median']
    #header = ['#Name', 'MeanDist', 'StdDist', 'MeanXDist', 'StdXDist', 'MeanYDist', 'StdYDist', 'MeanZDist', 'StdZDist']

    print('GCPs')
    print(tabulate(tableGCPs, headers=header))
    print()

    print('CPs')
    print(tabulate(tableCPs, headers=header))
    print()


def argument_parser():
   # define argument menu
    description = "Gets statistics of GCPBascule runs in one or more execution folders"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-x', '--xml',default='', help='XML file with the 3D position of the GCPs (and possible CPs)', type=str, required=True)
    parser.add_argument('-f', '--folders',default='', help='Comma-separated list of execution folders where to look for the GCPBascule.log files', type=str, required=True)
    return parser

def main():
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.xml, a.folders)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
