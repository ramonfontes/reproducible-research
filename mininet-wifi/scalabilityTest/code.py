#!/usr/bin/python

"""
This code makes part of an article towards Reproducible Research.

authors: Ramon dos Reis Fontes
         Christian Rodolfo Esteve Rothenberg
         
This code can be used to evaluate the performance of Mininet-WiFi in two different topologies: single and linear
Access Points running at user and kernel space are also evaluated.

At the end for the test the data will be presented in graphics.
"""

import os
import math
import glob
import matplotlib
import subprocess
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab

nr_nodes_single = 256 #Single Topo
nr_nodes_linear = 256 #Linear Topo
repetitions = 1  #Repetitions
RANGE = 16
pmem_ovs_linear = []
pmem_user_linear = []
pmem_ovs_single = []
pmem_user_single = []

file1 = 'OVSLinearTopobenchmark.txt'
file2 = 'UserLinearTopobenchmark.txt'
file3 = 'OVSSingleTopobenchmark.txt'
file4 = 'UserSingleTopobenchmark.txt'
file5 = 'icmpOVSLinearbenchmark.txt'
file6 = 'icmpUserLinearbenchmark.txt'
file7 = 'icmpOVSSinglebenchmark.txt'
file8 = 'icmpUserSinglebenchmark.txt'
mem_ovs_linear = 'mem_ovs_linear.txt'
mem_ovs_single = 'mem_ovs_single.txt'
mem_user_linear = 'mem_user_linear.txt'
mem_user_single = 'mem_user_single.txt'

def numberOfNodes(i):
    """Returns the number of nodes"""
    
    if (i == 1 or i == 2):
        i = RANGE
    else:
        i = i + RANGE
    return i


def runExperiment():
    """Run Experiment"""
    
    print 'Testing OVS linear topo...'
    for n in range(0, repetitions):
        i = 1
        while i <= nr_nodes_linear:
            mem = 'free -m | grep ^Mem | awk \'{print $1 $3}\' | tr -d Mem: | awk NR==1'
            v = (int(subprocess.check_output(mem, shell=True)))
            os.system('echo %s >> %s' % (v, mem_ovs_linear))
            print 'Test %d: Number of access points: %d' % (n, i)
            step1 = '\"sta1 free -m | grep ^Mem | awk \'{print \$1 \$3}\'\nexit\"'
            step2 = 'mn --wifi --topo=linear,%d 2>&1' % i
            step3 = 'grep -E \"(Mem:|completed in)\" | tr -d em: | tr \'M\' \',\' | tr -d "copltd in" | tr -d ss | awk \'!(NR%2){print$0p}{p=$0}\''
            os.system('echo ' + step1 + ' | ' + step2 + ' | ' + step3 + ' >> %s' % file1)
            i = numberOfNodes(i)
    
    print '\nTesting User linear topo...'
    for n in range(0, repetitions):
        i = 1
        while i <= nr_nodes_linear:
            mem = 'free -m | grep ^Mem | awk \'{print $1 $3}\' | tr -d Mem: | awk NR==1'
            v = (int(subprocess.check_output(mem, shell=True)))
            os.system('echo %s >> %s' % (v, mem_user_linear))
            print 'Test %d: Number of access points: %d' % (n, i)
            step1 = '\"sta1 free -m | grep ^Mem | awk \'{print \$1 \$3}\'\nexit\"'
            step2 = 'mn --wifi --ap user --topo=linear,%d 2>&1' % i
            step3 = 'grep -E \"(Mem:|completed in)\" | tr -d em: | tr \'M\' \',\' | tr -d "copltd in" | tr -d ss | awk \'!(NR%2){print$0p}{p=$0}\''
            os.system('echo ' + step1 + ' | ' + step2 + ' | ' + step3 + ' >> %s' % file2)
            i = numberOfNodes(i)
    
    print '\nTesting OVS single topo...'
    for n in range(0, repetitions):
        i = 1
        while i <= nr_nodes_single:
            mem = 'free -m | grep ^Mem | awk \'{print $1 $3}\' | tr -d Mem: | awk NR==1'
            v = (int(subprocess.check_output(mem, shell=True)))
            os.system('echo %s >> %s' % (v, mem_ovs_single))
            print 'Test %d: Number of Stations: %d' % (n, i)
            step1 = '\"sta1 free -m | grep ^Mem | awk \'{print \$1 \$3}\'\nexit\"'
            step2 = 'mn --wifi --topo=single,%d 2>&1' % i
            step3 = 'grep -E \"(Mem:|completed in)\" | tr -d em: | tr \'M\' \',\' | tr -d "copltd in" | tr -d ss | awk \'!(NR%2){print$0p}{p=$0}\''
            os.system('echo ' + step1 + ' | ' + step2 + ' | ' + step3 + ' >> %s' % file3)
            i = numberOfNodes(i)
    
    print '\nTesting User single topo...'
    for n in range(0, repetitions):
        i = 1
        while i <= nr_nodes_single:
            mem = 'free -m | grep ^Mem | awk \'{print $1 $3}\' | tr -d Mem: | awk NR==1'
            v = (int(subprocess.check_output(mem, shell=True)))
            os.system('echo %s >> %s' % (v, mem_user_single))
            print 'Test %d: Number of Stations: %d' % (n, i)
            step1 = '\"sta1 free -m | grep ^Mem | awk \'{print \$1 \$3}\'\nexit\"'
            step2 = 'mn --wifi --ap user --topo=single,%d 2>&1' % i
            step3 = 'grep -E \"(Mem:|completed in)\" | tr -d em: | tr \'M\' \',\' | tr -d "copltd in" | tr -d ss | awk \'!(NR%2){print$0p}{p=$0}\''
            os.system('echo ' + step1 + ' | ' + step2 + ' | ' + step3 + ' >> %s' % file4)
            i = numberOfNodes(i)
    
    print '\nTesting ICMP OVS linear topo...'
    for n in range(0, repetitions):
        i = 2
        while i <= nr_nodes_linear:
            print 'Test %d: Number of access points: %d' % (n, i)
            step1 = '\"sta1 ping -c21 sta2\"'
            step2 = 'mn --wifi --topo=linear,%d 2>&1' % i
            step3 = 'grep -E \"(icmp_seq=20)\" | awk \'{print $7}\' | tr -d "time="'
            os.system('echo ' + step1 + ' | ' + step2 + ' | ' + step3 + ' >> %s' % file5)
            i = numberOfNodes(i)
    
    print '\nTesting ICMP User linear topo...'
    for n in range(0, repetitions):
        i = 2
        while i <= nr_nodes_linear:
            print 'Test %d: Number of access points: %d' % (n, i)
            step1 = '\"sta1 ping -c21 sta2\"'
            step2 = 'mn --wifi --ap user --topo=linear,%d 2>&1' % i
            step3 = 'grep -E \"(icmp_seq=20)\" | awk \'{print $7}\' | tr -d "time="'
            os.system('echo ' + step1 + ' | ' + step2 + ' | ' + step3 + ' >> %s' % file6)
            i = numberOfNodes(i)
    
    print '\nTesting ICMP OVS single topo...'
    for n in range(0, repetitions):
        i = 2
        while i <= nr_nodes_single:
            print 'Test %d: Number of Stations: %d' % (n, i)
            step1 = '\"sta1 ping -c11 sta2\"'
            step2 = 'mn --wifi --topo=single,%d 2>&1' % i
            step3 = 'grep -E \"(icmp_seq=10)\" | awk \'{print $7}\' | tr -d "time="'
            os.system('echo ' + step1 + ' | ' + step2 + ' | ' + step3 + ' >> %s' % file7)
            i = numberOfNodes(i)
    
    print '\nTesting ICMP User single topo...'
    for n in range(0, repetitions):
        i = 2
        while i <= nr_nodes_single:
            print 'Test %d: Number of Stations: %d' % (n, i)
            step1 = '\"sta1 ping -c11 sta2\"'
            step2 = 'mn --wifi --ap user --topo=single,%d 2>&1' % i
            step3 = 'grep -E \"(icmp_seq=10)\" | awk \'{print $7}\' | tr -d "time="'
            os.system('echo ' + step1 + ' | ' + step2 + ' | ' + step3 + ' >> %s' % file8)
            i = numberOfNodes(i)

def buildGraph():
    """Builds the Graph"""
    
    # LINEAR_OVS
    file1_ = open(file1, 'r')
    f1 = file1_.readlines()
    file1_.close()
    
    # LINEAR_USER
    file2_ = open(file2, 'r')
    f2 = file2_.readlines()
    file2_.close()
    
    # SINGLE_OVS
    file3_ = open(file3, 'r')
    f3 = file3_.readlines()
    file3_.close()
    
    # SINGLE_USER
    file4_ = open(file4, 'r')
    f4 = file4_.readlines()
    file4_.close()
    
    # LINEAR-ICMP-OVS
    file5_ = open(file5, 'r')
    f5 = file5_.readlines()
    file5_.close()
    
    # LINEAR-ICMP-USER
    file6_ = open(file6, 'r')
    f6 = file6_.readlines()
    file6_.close()
    
    # SINGLE-ICMP-OVS
    file7_ = open(file7, 'r')
    f7 = file7_.readlines()
    file7_.close()
    
    # SINGLE-ICMP-USER
    file8_ = open(file8, 'r')
    f8 = file8_.readlines()
    file8_.close()
    
    mem = open(mem_ovs_linear, 'r')
    f_mem_ovs_linear = mem.readlines()
    mem.close()
    
    mem = open(mem_user_linear, 'r')
    f_mem_user_linear = mem.readlines()
    mem.close()

    mem = open(mem_ovs_single, 'r')
    f_mem_ovs_single = mem.readlines()
    mem.close()

    mem = open(mem_user_single, 'r')
    f_mem_user_single = mem.readlines()
    mem.close()

    tovs = []
    tuser = []
    movs = []
    muser = []
    tSINGLEovs = []
    tSINGLEuser = []
    mSINGLEovs = []
    mSINGLEuser = []
    icmpOVS = []
    icmpUser = []
    icmpOVSSINGLE = []
    icmpUserSINGLE = []
    
    # scan the rows of the file stored in lines, and put the values into some variables:
    for data in f_mem_ovs_linear:
        p = data.split()
        pmem_ovs_linear.append(float(p[0]))
    
    for data in f_mem_user_linear:
        p = data.split()
        pmem_user_linear.append(float(p[0]))
        
    for data in f_mem_ovs_single:
        p = data.split()
        pmem_ovs_single.append(float(p[0]))
        
    for data in f_mem_user_single:
        p = data.split()
        pmem_user_single.append(float(p[0]))
    
    for data in f1:
        p = data.split(',')
        tovs.append(float(p[0]))
        movs.append(float(p[1]))
    
    for data in f2:
        p = data.split(',')
        tuser.append(float(p[0]))
        muser.append(float(p[1]))
    
    for data in f3:
        p = data.split(',')
        tSINGLEuser.append(float(p[0]))
        mSINGLEuser.append(float(p[1]))
    
    for data in f4:
        p = data.split(',')
        tSINGLEovs.append(float(p[0]))
        mSINGLEovs.append(float(p[1]))
        
    for m in range(0, len(movs)):
        movs[m] = (movs[m] - pmem_ovs_linear[m])
        muser[m] = (muser[m] - pmem_user_linear[m])
    for m in range(0, len(mSINGLEovs)):
        mSINGLEovs[m] = (mSINGLEovs[m] - pmem_ovs_single[m])
        mSINGLEuser[m] = (mSINGLEuser[m] - pmem_user_single[m])     
    
    for data in f5:
        p = data.split()
        icmpOVS.append(float(p[0]))
    
    for data in f6:
        p = data.split()
        icmpUser.append(float(p[0]))
    
    for data in f7:
        p = data.split()
        icmpOVSSINGLE.append(float(p[0]))
    
    for data in f8:
        p = data.split()
        icmpUserSINGLE.append(float(p[0]))
    
    ntovs = []
    ntuser = []
    nmovs = []
    nmuser = []
    nSINGLEtovs = []
    nSINGLEtuser = []
    nSINGLEmovs = []
    nSINGLEmuser = []
    nicmpOVS = []
    nicmpUser = []
    nSINGLEicmpOVS = []
    nSINGLEicmpUser = []
    
    nrn = (((nr_nodes_linear / RANGE) + 1))
    nrnSINGLE = (((nr_nodes_single / RANGE) + 1))
    for x in range(0, (nrn)):
        ntovs.append(0)
        ntuser.append(0)
        nmovs.append(0)
        nmuser.append(0)
        nicmpOVS.append(0)
        nicmpUser.append(0)
    
    for x in range(0, (nrnSINGLE)):
        nSINGLEtovs.append(0)
        nSINGLEtuser.append(0)
        nSINGLEmovs.append(0)
        nSINGLEmuser.append(0)
        nSINGLEicmpOVS.append(0)
        nSINGLEicmpUser.append(0)
    
    i = 1
    nodes = []
    icmpNodes = []
    for x in range(0, nrn):
        b = x
        for k in range(0, repetitions):
            ntovs[x] = ntovs[x] + tovs[b] / 60
            ntuser[x] = ntuser[x] + tuser[b] / 60
            nmovs[x] = nmovs[x] + movs[b]
            nmuser[x] = nmuser[x] + muser[b]
            nicmpOVS[x] = nicmpOVS[x] + icmpOVS[b]
            nicmpUser[x] = nicmpUser[x] + icmpUser[b]
            b = x + (RANGE + 1)
        ntovs[x] = ntovs[x] / repetitions
        ntuser[x] = ntuser[x] / repetitions
        nmovs[x] = nmovs[x] / repetitions
        nmuser[x] = nmuser[x] / repetitions
        nicmpUser[x] = nicmpUser[x] / repetitions
        nicmpOVS[x] = nicmpOVS[x] / repetitions
        nodes.append(i)
        if i == 1:
            icmpNodes.append(i + 1)
        else:
            icmpNodes.append(i)
        i = numberOfNodes(i)
    
    i = 1
    nodesSINGLE = []
    icmpNodesSINGLE = []
    for x in range(0, nrnSINGLE):
        b = x
        for k in range(0, repetitions):
            nSINGLEtovs[x] = nSINGLEtovs[x] + tSINGLEovs[b] / 60 #convert to minutes
            nSINGLEtuser[x] = nSINGLEtuser[x] + tSINGLEuser[b] / 60 #convert to minutes
            nSINGLEmovs[x] = nSINGLEmovs[x] + mSINGLEovs[b]
            nSINGLEmuser[x] = nSINGLEmuser[x] + mSINGLEuser[b]
            nSINGLEicmpOVS[x] = nSINGLEicmpOVS[x] + icmpOVSSINGLE[b]
            nSINGLEicmpUser[x] = nSINGLEicmpUser[x] + icmpUserSINGLE[b]
            b = x + (RANGE + 1)
        nSINGLEtovs[x] = nSINGLEtovs[x] / repetitions
        nSINGLEtuser[x] = nSINGLEtuser[x] / repetitions
        nSINGLEmovs[x] = nSINGLEmovs[x] / repetitions
        nSINGLEmuser[x] = nSINGLEmuser[x] / repetitions
        nSINGLEicmpUser[x] = nSINGLEicmpUser[x] / repetitions
        nSINGLEicmpOVS[x] = nSINGLEicmpOVS[x] / repetitions
        nodesSINGLE.append(i)
        if i == 1:
            icmpNodesSINGLE.append(i + 1)
        else:
            icmpNodesSINGLE.append(i)
        i = numberOfNodes(i)
    
    fig, ax1 = plt.subplots()
    ax1.grid(True)
    ax1.plot(nodes, ntovs, color='red', marker='*', mec='red', markersize=5, label='OVS AP', linestyle=':', linewidth=1)
    ax1.plot(nodes, ntuser, color='green', marker='x', markersize=5, label='User AP', linestyle='-', linewidth=1)
    ax1.legend(loc='best', borderaxespad=0., fontsize=14, frameon=False)
    ax1.set_ylabel("start+shutdown time (minutes)", fontsize=20)
    ax1.set_xlabel("# of Access Points", fontsize=20)
    ax1.set_title('Linear Topo')
    plt.xlim([0, nr_nodes_linear + 2])
    plt.ylim([0, plt.ylim()[1]])
    plt.savefig("report_Time_Linear.eps")
    
    fig, ax1 = plt.subplots()
    ax1.grid(True)
    ax1.plot(nodes, nmovs, color='red', marker='*', mec='red', markersize=5, label='OVS AP', linestyle=':', linewidth=1)
    ax1.plot(nodes, nmuser, color='green', marker='x', markersize=5, label='User AP', linestyle='-', linewidth=1)
    ax1.legend(loc='best', borderaxespad=0., fontsize=14, frameon=False)
    ax1.set_ylabel("memory usage (megabytes)", fontsize=20)
    ax1.set_xlabel("# of Access Points", fontsize=20)
    ax1.set_title('Linear Topo')
    plt.xlim([0, nr_nodes_linear + 2])
    plt.ylim([0, plt.ylim()[1]])
    plt.savefig("report_Memory_Linear.eps")
    
    fig, ax1 = plt.subplots()
    ax1.grid(True)
    ax1.plot(nodesSINGLE, nSINGLEtovs, color='red', marker='*', mec='red', markersize=5, label='OVS AP', linestyle=':', linewidth=1)
    ax1.plot(nodesSINGLE, nSINGLEtuser, color='green', marker='x', markersize=5, label='User AP', linestyle='-', linewidth=1)
    ax1.legend(loc='best', borderaxespad=0., fontsize=14, frameon=False)
    ax1.set_ylabel("start+shutdown time (minutes)", fontsize=20)
    ax1.set_xlabel("# of Stations", fontsize=20)
    ax1.set_title('Single Topo')
    plt.xlim([0, nr_nodes_single + 2])
    plt.ylim([0, plt.ylim()[1]])
    plt.savefig("report_Time_Single.eps")
    
    fig, ax1 = plt.subplots()
    ax1.grid(True)
    ax1.plot(nodesSINGLE, nSINGLEmovs, color='red', marker='*', mec='red', markersize=5, label='OVS AP', linestyle=':', linewidth=1)
    ax1.plot(nodesSINGLE, nSINGLEmuser, color='green', marker='x', markersize=5, label='User AP', linestyle='-', linewidth=1)
    ax1.legend(loc='best', borderaxespad=0., fontsize=14, frameon=False)
    ax1.set_ylabel("memory usage (megabytes)", fontsize=20)
    ax1.set_xlabel("# of Stations", fontsize=20)
    ax1.set_title('Single Topo')
    plt.xlim([0, nr_nodes_single + 2])
    plt.ylim([0, plt.ylim()[1]])
    plt.savefig("report_Memory_Single.eps")
    
    fig, ax1 = plt.subplots()
    ax1.grid(True)
    ax1.plot(icmpNodes, nicmpOVS, color='red', marker='*', mec='red', markersize=5, label='OVS AP', linestyle=':', linewidth=1)
    ax1.plot(icmpNodes, nicmpUser, color='green', marker='x', markersize=5, label='User AP', linestyle='-', linewidth=1)
    ax1.legend(loc='best', borderaxespad=0., fontsize=14, frameon=False)
    ax1.set_ylabel("time response (ms)", fontsize=20)
    ax1.set_xlabel("# of Access Points", fontsize=20)
    ax1.set_title('Linear Topo')
    plt.xlim([0, nr_nodes_linear + 2])
    plt.ylim([0, plt.ylim()[1]])
    plt.savefig("report_ICMP_Linear.eps")
    
    fig, ax1 = plt.subplots()
    ax1.grid(True)
    ax1.plot(icmpNodesSINGLE, nSINGLEicmpOVS, color='red', marker='*', mec='red', markersize=5, label='OVS AP', linestyle=':', linewidth=1)
    ax1.plot(icmpNodesSINGLE, nSINGLEicmpUser, color='green', marker='x', markersize=5, label='User AP', linestyle='-', linewidth=1)
    ax1.legend(loc='best', borderaxespad=0., fontsize=14, frameon=False)
    ax1.set_ylabel("time response (ms)", fontsize=20)
    ax1.set_xlabel("# of Stations", fontsize=20)
    ax1.set_title('Single Topo')
    plt.xlim([0, nr_nodes_single + 2])
    plt.ylim([0, plt.ylim()[1]])
    plt.savefig("report_ICMP_Single.eps")

def removeFiles():
    """Remove Files"""
    
    if glob.glob(file1):
        os.system('rm %s' % file1)
    if glob.glob(file2):
        os.system('rm %s' % file2)
    if glob.glob(file3):
        os.system('rm %s' % file3)
    if glob.glob(file4):
        os.system('rm %s' % file4)
    if glob.glob(file5):
        os.system('rm %s' % file5)
    if glob.glob(file6):
        os.system('rm %s' % file6)
    if glob.glob(file7):
        os.system('rm %s' % file7)
    if glob.glob(file8):
        os.system('rm %s' % file8)
    if glob.glob(mem_ovs_linear):
        os.system('rm %s' % mem_ovs_linear)
    if glob.glob(mem_ovs_single):
        os.system('rm %s' % mem_ovs_single)
    if glob.glob(mem_user_linear):
        os.system('rm %s' % mem_user_linear)
    if glob.glob(mem_user_single):
        os.system('rm %s' % mem_user_single)

if __name__ == '__main__':
    print "------------------------------------------------------------------"
    os.system('echo "CPU Model:" && cat /proc/cpuinfo | grep "model name" | awk NR==1 | awk \'{print $4 $5 $6 $7 $8 $9}\'')
    os.system('echo "Total Memory:" && cat /proc/meminfo | grep MemTotal | awk \'{print $2 $3}\'')
    print "------------------------------------------------------------------"
    print "Stopping network manager"
    os.system('service network-manager stop')
    
    removeFiles() # Remove Files
    runExperiment() # Running experiment and processing code
    buildGraph() # Presenting code
