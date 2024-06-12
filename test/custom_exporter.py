#import library
from prometheus_client import start_http_server, Gauge
import time
import subprocess
import re

#Metrik
Cluster_UT =Gauge('Cluster_UT', 'Metrik yang menghitung jumlah koneksi node ipfs-cluster UT')
Cluster_UNHAS=Gauge('Cluster_UNHAS', 'Metrik yang menghitung jumlah koneksi node ipfs-cluster UNHAS')
Cluster_UGM=Gauge('Cluster_UGM', 'Metrik yang menghitung jumlah koneksi node ipfs-cluster UGM')
Cluster_UMS=Gauge('Cluster_UMS', 'Metrik yang menghitung jumlah koneksi node ipfs-cluster UMS')
Cluster_ITB=Gauge('Cluster_ITB', 'Metrik yang menghitung jumlah koneksi node ipfs-cluster ITB')

#Function jalankan bash script
def run_bash_script():
    result = subprocess.run(['./test/exporter.sh'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()
    return output

#Function mengelola hasil dari bash script untuk mendapatkan metrik koneksi node ipfs-cluster
def cluster_peers():
    output = run_bash_script()
    matches = re.findall(r'cluster-(\w+) \| Sees (\d+) other peers', output)
    PT = [match[0] for match in matches]
    peers = [int(match[1]) for match in matches]
    Cluster_UT.set(float(0))
    Cluster_UNHAS.set(float(0))
    Cluster_UGM.set(float(0))
    Cluster_UMS.set(float(0))
    Cluster_ITB.set(float(0))
    for i in PT:
        if i=="UT":
            posisi = PT.index(i)
            Cluster_UT.set(float(peers[posisi]))
        elif i=="UNHAS":
            posisi = PT.index(i)
            Cluster_UNHAS.set(float(peers[posisi]))
        elif i=="UGM":
            posisi = PT.index(i)
            Cluster_UGM.set(float(peers[posisi]))
        elif i=="UMS":
            posisi = PT.index(i)
            Cluster_UMS.set(float(peers[posisi]))
        elif i=="ITB":
            posisi = PT.index(i)
            Cluster_ITB.set(float(peers[posisi]))
            
#jalankan app prometheus_client sebagai exporter
if __name__ == '__main__':
    start_http_server(2512)
    while True:
        cluster_peers()
        time.sleep(10)
