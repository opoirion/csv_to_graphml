import sys
import networkx as nx


usage = """
usage: python csv_to_graphml.py <csv path> option
option:
    -h help
    -s separator (default ';')
    -o output name
"""

def main():
    sep = ';'
    outname = None

    if len(sys.argv) < 2:
        print usage
        return
    filename = sys.argv[1]
    if filename =='-h':
        print usage
        return
    try:
        f = open(filename, 'r')
    except IOError:
        print 'bad filename: {0}'.format(filename)
        return

    if '-s' in sys.argv:
        sep = sys.argv[sys.argv.index('-s') + 1]
    if '-o' in sys.argv:
        outname = sys.argv[sys.argv.index('-o') + 1]
    else:
        outname = filename

    do_graph_from_file(f, sep, outname)

def do_graph_from_file(f, sep, outname):
    G = nx.Graph()
    for line in f:
        lines = line.split(sep)
        if len(lines) < 2:
            continue
        G.add_edge(lines[0].encode('utf8'), lines[1].encode('utf8'))

    nx.write_graphml(G, outname.split('.')[0] +'.graphml')


if __name__ == '__main__':
    main()
