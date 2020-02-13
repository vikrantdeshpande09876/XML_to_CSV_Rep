import re
from lxml import etree as ET
import pandas as pd
from flask import flash

temp_depth=0

class Main:
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
        if ftype=='XML':
            overallstring=self.depthFirstXML(tree.getroot(),0,'')
        else:
            overallstring=self.depthFirstXSD(tree.getroot(),0,'')
        overallstring='<ul>'+overallstring+"""</ul>
                        <button type="submit" id="sendDataToCSV">Send Data to CSV</button>"""
        return overallstring


    def depthFirstXSD(self, node, depth, tagname):
        ''' DOCSTRING:  Traverse the XSD Nodes using DFS and create a string containing dynamic+clickable
                        nested checkboxes.
                        The inter-linking of checkboxes by using Parent-Child hierarchy will be handled in JS.
            INPUT:      XSD_Node_Element, Depth, Temporary_Tag_Name
            OUTPUT:     N/A '''
        global temp_depth
        if 'element' in node.tag:
            if tagname!='':
                tagname+='.'+node.attrib['name']
            else:
                tagname=node.attrib['name']
            text='<li><input type="checkbox" name="'+'MyPythonCheckbox'+'" id="'+tagname+'">'+'<label for="'+tagname+'"><b>'+node.attrib['name']+'</b></label>'
            if depth>temp_depth:
                text='<ul>'+text
            print(node.attrib['name'] + ': has Depth: '+str(depth) + ', Temp_Depth: '+str(temp_depth)+' and id='+ tagname)
        else:
            text=''
        temp_depth=depth
        for child in node.getchildren():
          text += self.depthFirstXSD(child, depth+1,tagname)
        if 'element' in node.tag and depth<temp_depth: 
            while depth!=temp_depth:
                text+='</ul>'
                temp_depth-=1  
        return text+'</li>'













    def depthFirstXML(self, node, depth, tagname):
        ''' DOCSTRING:  Traverse the XML Nodes using DFS and create a string containing dynamic+clickable
                        nested checkboxes.
                        The inter-linking of checkboxes by using Parent-Child hierarchy will be handled in JS.
            INPUT:      XML_Node_Element, Depth, Temporary_Tag_Name
            OUTPUT:     N/A '''
        global temp_depth
        nsdict=node.nsmap
        for ns in nsdict.values():
            node.tag=re.sub(r'\{'+ns+r'\}','',node.tag)
        if tagname!='':
          tagname+='.'+node.tag
        else:
          tagname=node.tag
        text='<li><input type="checkbox" name="'+'MyPythonCheckbox'+'" id="'+tagname+'">'+'<label for="'+tagname+'"><b>'+node.tag+'</b></label>'
        if depth>temp_depth:
          text='<ul>'+text
        #print(node.tag + ': has Depth: '+str(depth) + ', Temp_Depth: '+str(temp_depth)+' and id='+ tagname)
        temp_depth=depth
        for child in node.getchildren():
          text += self.depthFirstXML(child, depth+1,tagname)
        if depth<temp_depth: 
          while depth!=temp_depth:
            text+='</ul>'
            temp_depth-=1  
        return text+'</li>'

    
 
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
            df_tag_nesting.to_csv(directory+'\\'+trimmed_filename+'.csv',sep=seperator,index=True, index_label='INDEX')
            print("\nCSV File created successfully!")
        except Exception as e:
            print("\nError writing the DataFrame into .CSV file: "+e)