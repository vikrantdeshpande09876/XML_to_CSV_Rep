import re
from lxml import etree as ET
import pandas as pd

def insert_tag_info(node,x,ftype,level):
    '''
        DOCSTRING: 
        INPUT: 
        OUTPUT:  
    '''
    nsdict=node.nsmap
    for ns in nsdict.values():
        node.tag=re.sub(r'\{'+ns+r'\}','',node.tag)
    if ftype=='XML':
        x.append([node.tag,level])
    else:
        x.append([node.attrib['name'],level])


def generate_tag_nesting(element,callbackfunc, x, ftype, level=0):
    '''
        DOCSTRING: 
        INPUT: 
        OUTPUT:  
    '''
    if ftype=='XSD':
        if 'element' in element.tag:
            callbackfunc(element,x,ftype,level)
    else:
        callbackfunc(element,x,ftype,level)
    for child in element.getchildren():
        if 'element' in element.tag or ftype=='XML':
            level+=1
        generate_tag_nesting(child,callbackfunc,x,ftype,level)

directory='C:\\Users\\vdeshpande\\Desktop\\Python_Notes\\XML_Schema_Task\\'
fxml=directory+r'Sample.xml'
fxsd=directory+r'MySample.xsd'

x,y=[],[]
generate_tag_nesting(ET.parse(fxml).getroot(),insert_tag_info,x,ftype='XML',level=0)
generate_tag_nesting(ET.parse(fxsd).getroot(),insert_tag_info,y,ftype='XSD',level=0)


#XML TRY-CATCH BLOCKS
try:
    df_x=pd.DataFrame(x,columns=['XML_TAG_NAME','NESTING_LEVEL'])
    print(df_x,end='\n\n')
except Exception as e:
    print("\nError converting the 2d array into DataFrame: "+e)
    
try:
    df_x.to_csv(directory+'SampleXML.csv',sep=',',index=False)
except Exception as e:
    print("\nError writing the DataFrame into .CSV file: "+e)

#XSD TRY_CATCH_BLOCKS
try:    
    df_y=pd.DataFrame(y,columns=['XSD_TAG_NAME','NESTING_LEVEL'])
    print(df_y)
except Exception as e:
    print("\nError converting the 2d array into DataFrame: "+e)
try:
    df_y.to_csv(directory+'MySampleXSD.csv',sep=',',index=False)
except Exception as e:
    print("\nError writing the DataFrame into .CSV file: "+e)
