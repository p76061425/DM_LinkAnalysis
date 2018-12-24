if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser()

    parser.add_argument('FILE')
    parser.add_argument('-o',
                        default='',
                        dest='OUTPUT',
                        help='Place the output into <file>')
    parser.add_argument('-d',
                        default='directed',
                        dest='DIRECT',
                        help='Set directed or bi-directed edge. {directed|bidirected} (default: direct)')
    args = parser.parse_args()

    infile  = args.FILE
    outfile = infile.split('.')[0] + '_g.txt' if args.OUTPUT == '' else args.OUTPUT
    direct  = 0 if args.DIRECT.upper() != 'BIDIRECTED' else 1
    if args.DIRECT.upper() == 'DIRECTED':
        direct = 0
    elif args.DIRECT.upper() == 'BIDIRECTED':
        direct = 1
    else:
        print('Unknow direct:', args.DIRECT)
        sys.exit()

    trans = {}
    with open(infile, 'r') as f:
        lines = f.read().split('\n')
        for line in lines: 
            if line == '': continue
            spli = line.split()
            trans_id = spli[0]
            item_id  = spli[2]
            try:
                trans[trans_id]
                trans[trans_id].append(item_id)
            except:
                trans[trans_id] = [item_id]

    record = set()
    nodes  = set()
    with open(outfile, 'w') as f:
        for t in trans:
            node_list = trans[t]
            if len(node_list) < 2: continue
            pre_node = node_list[0]
            nodes.add(pre_node)
            for nxt_node in node_list[1:]:
                if not (pre_node, nxt_node) in record:
                    f.write(pre_node + ',' + nxt_node + '\n')
                    record.add((pre_node, nxt_node))
                if direct and not (nxt_node, pre_node) in record:
                    f.write(nxt_node + ',' + pre_node + '\n')
                    record.add((nxt_node, pre_node))
                pre_node = nxt_node
                nodes.add(pre_node)
    
    print('Total number of nodes:', len(nodes))
    print('Total number of edges:', len(record))
