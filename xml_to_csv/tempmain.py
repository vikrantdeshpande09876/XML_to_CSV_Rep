import re
from lxml import etree as ET
import pandas as pd
from flask import flash

temp_depth=0


class MyNode:
    def __init__(self, tag, parent):
        self.tag = tag
        self.parent = parent
    
    def add_children(self, children):
        self.children = children
  


def dfs(node, parent):
    children = []
    thisNode = MyNode(node.tag, parent)
    for child in node:
        children.append(dfs(child, thisNode))
    thisNode.add_children(children)
    return thisNode


class TempMain:
    def __init__(self):
        ''' DOCSTRING:  Default constructor of class. 
                        It initializes an empty 2-d array for our tags.
            INPUT:      Class_Instance
            OUTPUT:     N/A '''
        self.arr_tag_nesting=[]
       
        
    def exec_main_functions(self,path,ftype):
        ''' DOCSTRING:  Parent function to parse the selected XML File and invoke Depth-First-Search
                        to generate string of nested list-element HTML tags.
            INPUT:      Absolute_File_Location, Type_of_File
            OUTPUT:     N/A '''
        tree=ET.parse(path)
        #self.generate_tag_nesting(tree.getroot(),self.insert_tag_info,self.arr_tag_nesting,ftype,level=0)
        overallstring='<ul>'+self.depthFirst(tree.getroot(),0,'')+"""</ul>
                        <button type="submit"  id="sendDataToCSV">Proceed</button>"""
        return overallstring


    def insert_tag_info(self,node,arr_tag_nesting,ftype,level):
        ''' DOCSTRING:  Doer/Utility function which will populate the 2-d array with tag-names (replaces namespaces with NULL) and their nesting-level
            INPUT:      XML_Node_Element, 2D_Array, Type_of_File, Nesting_Level
            OUTPUT:     N/A '''
        nsdict=node.nsmap
        for ns in nsdict.values():
            node.tag=re.sub(r'\{'+ns+r'\}','',node.tag)
        if ftype=='XML':
            arr_tag_nesting.append([node.tag,level])
        else:
            arr_tag_nesting.append([node.attrib['name'],level])



    def depthFirst(self, node, depth, tagname):
        global temp_depth
        if tagname!='':
          tagname+='.'+node.tag
        else:
          tagname=node.tag
        text='<br><li><input type="checkbox" name="'+'MyPythonCheckbox'+'" id="'+tagname+'">'+'<label for="'+tagname+'"><b>'+node.tag+' has depth='+str(depth)+'</b> and tempdepth='+str(temp_depth)+'</label>'
        if depth>temp_depth:
          text='<ul>'+text
        #print(node.tag + ': has Depth: '+str(depth) + ', Temp_Depth: '+str(temp_depth)+' and id='+ tagname)
        temp_depth=depth
        for child in node.getchildren():
          text += self.depthFirst(child, depth+1,tagname)
        if depth<temp_depth: 
          while depth!=temp_depth:
            text+='</ul>'
            temp_depth-=1  
        return text+'</li>'

    def generate_tag_nesting(self,element,callbackfunc, arr_tag_nesting, ftype, level=0):
        ''' DOCSTRING:  Sub-Parent Function which invokes the utility/doer function. 
                        If Type_of_File is XSD then pass only element-tags to utility function
                        since <element> tags contain actual tag-names.
            INPUT:      XML_Node_Element, Utility_function_name, 2D_Array, Type_of_File, Nesting_level
            OUTPUT:     N/A '''
        if ftype=='XSD':
            if 'element' in element.tag:
                callbackfunc(element,arr_tag_nesting,ftype,level)
        else:
            callbackfunc(element,arr_tag_nesting,ftype,level)
        for child in element.getchildren():
                self.generate_tag_nesting(child,callbackfunc,arr_tag_nesting,ftype,level+1)
    
    def retrieve_arr_dict(self,arr_tag_nesting):
        arr_dict=[]
        for arr in arr_tag_nesting:
            arr_dict.append(dict(arr))
        print(arr_dict)
        return arr_dict
    
    def retrieve_dataframe(self,arr_tag_nesting):
        ''' DOCSTRING:  Attempts to create Pandas-DataFrame object using the resultant 2D array
            INPUT:      2D_Array
            OUTPUT:     DataFrame '''
        try:
            df_tag_nesting=pd.DataFrame(arr_tag_nesting,columns=['XML_TAG_NAME','NESTING_LEVEL'])
            print(df_tag_nesting,end='\n\n')
            return df_tag_nesting
        except Exception as e:
            return "\nError converting the 2d array into DataFrame: "+e
    
    
    def write_dataframe_to_csv(self,directory,filename,df_tag_nesting,seperator=','):
        ''' DOCSTRING:  Attempts to write DataFrame into CSV file at the input Directory location
            INPUT:      Directory_Location, Name_of_File, DataFrame, Seperator
            OUTPUT:     N/A '''
        trimmed_filename=re.sub('.xsd','',re.sub('.xml','',filename))
        try:
            df_tag_nesting.to_csv(directory+'\\'+trimmed_filename+'.csv',sep=seperator,index=False)
            flash("\nCSV File created successfully!")
        except Exception as e:
            flash("\nError writing the DataFrame into .CSV file: "+e)