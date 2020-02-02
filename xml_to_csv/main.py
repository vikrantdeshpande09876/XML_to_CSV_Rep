import re
from lxml import etree as ET
import pandas as pd


class Main:
    def __init__(self):
        ''' DOCSTRING:  Default constructor of class. 
                        It initializes an empty 2-d array for our tags.
            INPUT:      Class_Instance
            OUTPUT:     N/A '''
        self.x=[]
       
        
    def exec_main_functions(self,path,ftype):
        ''' DOCSTRING:  Parent function to parse the selected XML File and invoke the child function for generating 2-d array of tags
            INPUT:      Absolute_File_Location, Type_of_File
            OUTPUT:     N/A '''
        self.generate_tag_nesting(ET.parse(path).getroot(),self.insert_tag_info,self.x,ftype,level=0)


    def insert_tag_info(self,node,x,ftype,level):
        ''' DOCSTRING:  Doer/Utility function which will populate the 2-d array with tag-names (replaces namespaces with NULL) and their nesting-level
            INPUT:      XML_Node_Element, 2D_Array, Type_of_File, Nesting_Level
            OUTPUT:     N/A '''
        nsdict=node.nsmap
        for ns in nsdict.values():
            node.tag=re.sub(r'\{'+ns+r'\}','',node.tag)
        if ftype=='XML':
            x.append([node.tag,level])
        else:
            x.append([node.attrib['name'],level])


    def generate_tag_nesting(self,element,callbackfunc, x, ftype, level=0):
        ''' DOCSTRING:  Sub-Parent Function which invokes the utility/doer function. 
                        If Type_of_File is XSD then pass only element-tags to utility function
                        since <element> tags contain actual tag-names.
            INPUT:      XML_Node_Element, Utility_function_name, 2D_Array, Type_of_File, Nesting_level
            OUTPUT:     N/A '''
        if ftype=='XSD':
            if 'element' in element.tag:
                callbackfunc(element,x,ftype,level)
        else:
            callbackfunc(element,x,ftype,level)
        for child in element.getchildren():
            if 'element' in element.tag or ftype=='XML':
                level+=1
            self.generate_tag_nesting(child,callbackfunc,x,ftype,level)
    
    
    def retrieve_dataframe(self,x):
        ''' DOCSTRING:  Attempts to create Pandas-DataFrame object using the resultant 2D array
            INPUT:      2D_Array
            OUTPUT:     DataFrame '''
        try:
            df_x=pd.DataFrame(x,columns=['XML_TAG_NAME','NESTING_LEVEL'])
            print(df_x,end='\n\n')
            return df_x
        except Exception as e:
            return "\nError converting the 2d array into DataFrame: "+e
    
    
    def write_dataframe_to_csv(self,directory,filename,df_x,seperator=','):
        ''' DOCSTRING:  Attempts to write DataFrame into CSV file at the input Directory location
            INPUT:      Directory_Location, Name_of_File, DataFrame, Seperator
            OUTPUT:     N/A '''
        trimmed_filename=re.sub('.xsd','',re.sub('.xml','',filename))
        try:
            df_x.to_csv(directory+'\\'+trimmed_filename+'.csv',sep=seperator,index=False)
            print("\nCSV File created successfully!")
        except Exception as e:
            print("\nError writing the DataFrame into .CSV file: "+e)