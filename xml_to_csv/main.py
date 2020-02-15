import re
from lxml import etree as ET
import pandas as pd
from flask import flash

temp_depth=0

class Main:
    def __init__(self):
        ''' DOCSTRING:  Default constructor of class: Initializes an empty 2-d array for our tags.
            INPUT:      Class_Instance
            OUTPUT:     N/A '''
        self.arr_tag_nesting=[]
       
        
    def exec_main_functions(self,path,ftype):
        ''' DOCSTRING:  Parent function to parse the selected XML/XSD File and invoke Depth-First-Search
                        to generate string of nested list-element HTML tags.
            INPUT:      Absolute_File_Location, Type_of_File
            OUTPUT:     HTML_String '''
        tree=ET.parse(path)
        if ftype=='XML':
            overallstring=self.depthFirstXML(tree.getroot(),0,'')
        else:
            overallstring=self.depthFirstXSD(tree.getroot(),0,'')
        overallstring='<ul style="line-height:20%;">'+overallstring+"""</ul>
                        <button type="submit" id="sendDataToCSV">Send Data to CSV</button>"""
        return overallstring


    def depthFirstXSD(self, node, depth, tagname):
        ''' DOCSTRING:  Traverse the XSD Nodes using DFS and create a string containing dynamic+clickable
                        nested checkboxes.
                        The inter-linking of checkboxes by using Parent-Child hierarchy will be handled in JS.
            INPUT:      XSD_Node_Element, Depth, Temporary_Tag_Name
            OUTPUT:     HTML_String '''
        global temp_depth
        if tagname!='':
          tagname=tagname+'.'+node.attrib['name'] if 'element' in node.tag else tagname
        else:
          tagname=node.attrib['name'] if 'element' in node.tag else ''
        text='<li><input type="checkbox" name="'+'MyPythonCheckbox'+'" id="'+tagname+'">'+'<label for="'+tagname+'"><b>'+node.attrib['name']+'</b></label>' if 'element' in node.tag else ''
        if depth>temp_depth:
          text='<ul>'+text
        print(node.tag + ': has Depth: '+str(depth) + ', Temp_Depth: '+str(temp_depth)+' and id='+ tagname)
        temp_depth=depth
        for child in node.getchildren():
          text += self.depthFirstXSD(child, depth+1,tagname)
        if depth<temp_depth: 
          while depth!=temp_depth:
            text+='</ul>'
            temp_depth-=1  
        return text+'</li>'




    def depthFirstXML(self, node, depth, tagname):
        ''' DOCSTRING:  Traverse the XML Nodes using DFS and create a string containing dynamic+clickable
                        nested checkboxes.
                        The inter-linking of checkboxes by using Parent-Child hierarchy will be handled in JS.
            INPUT:      XML_Node_Element, Depth, Temporary_Tag_Name
            OUTPUT:     HTML_String '''
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

    def retrieve_template_dataframe(self,path):
        ''' DOCSTRING:  Attempts to create Pandas-DataFrame object using the absolute path of file.
            INPUT:      2D_Array
            OUTPUT:     DataFrame '''
        try:
            df=pd.read_csv(path,encoding='utf-8')
            return df
        except Exception as e:
            return "\nError reading the template dataframe from "+path+": "+e
 
    def retrieve_final_dataframe(self,template_df,arr_tag_nesting):
        ''' DOCSTRING:  Attempts to create Pandas-DataFrame object using the config file template, 
                        2D array of XML selected tags.
                        A key-value pair for Parent tag is statically created for Pyspark integration.
            INPUT:      Template_DataFrame, Selected_XML_Tags_DataFrame
            OUTPUT:     Resultant_DataFrame '''
        try:
            df_tag_nesting=pd.DataFrame(arr_tag_nesting,columns=['Variable','Value','TEMP']).drop(columns=['TEMP'])
            parent_tag=df_tag_nesting['Value'].iloc[0].split('.')[0]
            parent_tag_df=pd.DataFrame([['Parent_Tag',parent_tag]],columns=['Variable','Value'])
            res_df=template_df.append(parent_tag_df.append(df_tag_nesting,ignore_index=True),ignore_index=True)
            print("RES_DF=")
            print(res_df,end='\n\n')
            return res_df
        except Exception as e:
            return "\nError converting the 2d array into DataFrame: "+e
    
    
    def write_dataframe_to_csv(self,directory,filename,df_tag_nesting,seperator=','):
        ''' DOCSTRING:  Attempts to write DataFrame into CSV file at the input Directory location
            INPUT:      Directory_Location, Name_of_File, DataFrame, Seperator
            OUTPUT:     N/A '''
        trimmed_filename=re.sub('.xsd','',re.sub('.xml','',filename))
        try:
            df_tag_nesting.to_csv(directory+'\\'+trimmed_filename+'_Config.csv',sep=seperator,index=True,index_label='ID')
            print("\nCSV File created successfully!")
        except Exception as e:
            print("\nError writing the DataFrame into .CSV file: "+e)