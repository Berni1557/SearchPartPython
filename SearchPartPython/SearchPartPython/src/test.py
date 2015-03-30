from xml.dom.minidom import *
import sys

path="/home/bernifoellmer/Studium/SearchPartPython/SearchPartPython/SearchPartPython/SearchPartPython/src/TantalKondensator_dataset_V02.xml"
def create_dom(component):
    dom = Document();
    base = dom.createElement('datasetstruct')
    dom.appendChild(base)
    
    node1 = dom.createElement('Creation_date')
    text1 = dom.createTextNode("01.01.2005")
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)
    
    node1 = dom.createElement('Componentname')
    text1 = dom.createTextNode("01.01.2005")
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)    
    
    node1 = dom.createElement('Componenthight')
    text1 = dom.createTextNode("01.01.2005")
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)
    
    node1 = dom.createElement('Componentwidth')
    text1 = dom.createTextNode("01.01.2005")
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)  
    
    node1 = dom.createElement('Componentborder')
    text1 = dom.createTextNode("01.01.2005")
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)       
    
    node1 = dom.createElement('path')
    text1 = dom.createTextNode("01.01.2005")
    node1.appendChild(text1)
    dom.childNodes[0].appendChild(node1)  
    
    node1 = dom.createElement('Imagename')
    
    node2 = dom.createElement("item")
    text2 = dom.createTextNode("SAM_0839.JPG")
    node2.appendChild(text2)
    node1.appendChild(node2)
    
    node2 = dom.createElement("item")
    text2 = dom.createTextNode("SAM_0840.JPG")
    node2.appendChild(text2)
    node1.appendChild(node2)
    
    dom.childNodes[0].appendChild(node1)
   
    
    return dom


"""
doc = Document();
node1 = doc.createElement('datasetstruct')
doc.appendChild(node1)

node2 = doc.createElement('Creation_date')

doc.childNodes[0].appendChild(node2)

description = doc.createTextNode("A quiet, scenic park with lots of wildlife.")

doc.childNodes[0].childNodes[0].appendChild(description)
"""
dom=create_dom("datasetstruct")




st=dom.toprettyxml()
print st


f = open(path, 'w')
f.write(st)
f.close()

