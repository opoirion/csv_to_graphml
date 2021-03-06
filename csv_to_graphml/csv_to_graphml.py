import sys, os
from random import randint
import networkx as nx
import re


usage = """
usage: python csv_to_graphml.py <csv path> option
option:
    -h help
    -s separator (default ';')
    -o output name
    -l max number of lines
    -p parsing position options for the two nodes: ex 1,2 or 3,4
    -r activate random mode: draw l lines from the file
    -d draw graph with pylab
"""

def main():
    sep = ','
    outname = None
    maxnbline = None
    pos1, pos2 = 0, 1

    if len(sys.argv) < 2:
        print usage
        return
    filename = sys.argv[1]

    if '-h' in sys.argv:
        print usage
        return
    try:
        f = open(filename, 'r')
    except IOError:
        print 'bad filename: {0}'.format(filename)
        return

    if '-s' in sys.argv:
        sep = sys.argv[sys.argv.index('-s') + 1].strip("'\"")
    if '-l' in sys.argv:
        maxnbline = int(sys.argv[sys.argv.index('-l') + 1])

    if '-o' in sys.argv:
        outname = sys.argv[sys.argv.index('-o') + 1]
    else:
        outname = filename

    if '-p' in sys.argv:
        pos1, pos2 = map(int, sys.argv[sys.argv.index('-p') + 1].split(','))
        print 'position:', pos1, pos2
    if '-r' in sys.argv:
        G = do_graph_from_file_random(f, sep, outname, maxnbline, pos1, pos2)
    else:
        G = do_graph_from_file(f, sep, outname, maxnbline, pos1, pos2)

    if '-d' in sys.argv:
        import pylab as plt
        nx.draw(G)
        plt.show()
        raw_input('')

def do_graph_from_file(f, sep, outname, maxnbline, pos1, pos2):
    G = nx.DiGraph()
    i = 0
    for line in f:
        i += 1
        if maxnbline and i > maxnbline:
            break
        lines = line.split(sep)
        if len(lines) < 2:
            continue
        try:
            node1 = lines[pos1].encode('utf8').strip('\\/\r\n ')
            node2 = lines[pos2].encode('utf8').strip('\\/\r\n ')
            node1 = re.sub('www\.', '', re.sub('http://', '', node1))
            node2 = re.sub('www\.', '', re.sub('http://', '', node2))

            G.add_edge(node1, node2)
        except Exception:
            print 'error at line:\n\t{0}'.format(line)
            continue

    nx.write_gml(G, outname.rsplit('.', 1)[0] +'.gml')
    return G


def do_graph_from_file_random(f, sep, outname, maxnbline, pos1, pos2):
    nb_bites = os.path.getsize(f.name)
    G = nx.DiGraph()
    i = 0
    while i < maxnbline:
        i += 1
        f.seek(0)
        f.seek(randint(0, nb_bites))
        f.readline()
        line = f.readline()
        if not line:
            continue
        lines = line.split(sep)
        if len(lines) < 2:
            continue
            try:
                node1 = lines[pos1].encode('utf8').strip('\\/\r\n ')
                node2 = lines[pos2].encode('utf8').strip('\\/\r\n ')
                node1 = re.sub('www\.', '', re.sub('http://', '', node1))
                node2 = re.sub('www\.', '', re.sub('http://', '', node2))

                G.add_edge(node1, node2)
            except Exception as e:
                print 'error e:{0} at line:\n\t{0}'.format(e, line)
                continue

    nx.write_gml(G, outname.rsplit('.', 1)[0] +'.gml')
    return G

if __name__ == '__main__':
    main()
