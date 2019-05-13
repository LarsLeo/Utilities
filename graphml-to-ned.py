import click
import re

@click.command()
@click.option('--path', help='Path to GraphML file.')
@click.option('--output', help='Path to output NED file.')

def main(path, output):
    nodes = []
    edges = {}
    nodesCreated = []

    # Extract all Nodes and Edges from the Graphml file
    extractEntities(path, nodes, edges)
    
    nedFile = open("Sality.ned","w+")
    writePreamble(nedFile, nodes)
    writeConnections(nedFile, nodes, edges, nodesCreated)
    writePostamble(nedFile)

    nedFile.close()

def extractEntities(path, nodes, edges):
    graphFile = open(path, "r")
    for line in graphFile:
        line = line.strip()
        m = re.search(r"<node id=\"(\w+)\" />", line)
        if m:
            nodeID = m.group(1)
            nodes.append(nodeID)
        else:
            m = re.search(r"<edge source=\"(\w+)\" target=\"(\w+)\" />", line)
            if m:
                edgeSource = m.group(1)
                edgeTarget = m.group(2)   
                if edgeSource in edges:
                    edges[edgeSource].append(edgeTarget)  
                else:
                    edges[edgeSource] = list(edgeTarget)
    graphFile.close()

def writePreamble(nedFile, nodes):
    nedFile.write("package bachelor_thesis_sality;\nimport bachelor_thesis_sality.Superpeer;\n")
    nedFile.write("network Sality\n{\n\ttypes:\n\t\tchannel Channel extends ned.DelayChannel\n")
    nedFile.write("\t\t{\n\t\t\tdelay = 100ms;\n\t\t}\n\tsubmodules:\n\t\tnode[%d]: Superpeer;\n" %(len(nodes)))
    nedFile.write("\tconnections:\n")

def writeConnections(nedFile, nodes, edges, nodesCreated):
    for source,targets in edges.items():
        sourceIndex = checkNodeExistsOrCreate(source, nodesCreated)

        for target in targets:
            targetIndex = checkNodeExistsOrCreate(target, nodesCreated)
            nedFile.write("\t\tnode[%d].outputGate++ <--> Channel <--> node[%d].inputGate++;\n" %(sourceIndex, targetIndex))

def checkNodeExistsOrCreate(node, nodesCreated):
    if node not in nodesCreated:
        nodesCreated.append(node)
    return nodesCreated.index(node)

def writePostamble(nedFile):
    nedFile.write("}\n")
    
if __name__ == '__main__':
    main()