from xml.dom.minidom import parse
dom = parse("/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/data/TantalKondensator/TantalKondensator_dataset.xml")

#for node in dom.getElementsByTagName('Imagename'):  # visit every node <bar />
#    print node.firstChild.nodeValue
    
    
#print(dom.getElementsByTagName('Creation_date').item(0).firstChild.nodeValue)   
    
#for node in dom.childNodes:
#    print node.childNodes[4].toxml()

#print(dom.getElementsByTagName('Imagename').item(0).childNodes.item(2))

#print(dom.childNodes.item(0).childNodes[9].childNodes[4].childNodes[0].nodeValue)


Imagename=list()
for node in dom.childNodes.item(0).childNodes[11].childNodes:
    if(node.hasChildNodes()==True):
        Imagename.append(node.childNodes[0].nodeValue)
        
for i in Imagename:
    print(i)