#!/usr/bin/python3.7
import os
import MySQLdb
import time

#functions################################

##########MYSQL##
def show_results():
  cur=con.cursor()
  cur.execute('select * from result;')
  while True:
    row = cur.fetchone()
    if row == None:
      print(row)
      break
    else:
      print(row)

def run_query(prepared_sql,data_tpl):
  con=MySQLdb.connect('127.0.0.1','root','nishiiilu','cl_general')
  #print(con)
  if(con==None):
    print("Can't connect to database")
  else:
    pass
    #print('connected')
  cur=con.cursor()
  cur.execute(prepared_sql,data_tpl)
  con.commit()
  return cur

def get_single_row(cur):
    return cur.fetchone()

#classes#################################
class micros(object):
  abx={
	"\xff":(22,0,0), #"RecordType"],0,0),
	"p":(23,0,0), #"AnalyserNumber"],0,0),
	"q":(24,0,0), #"AnalysisDateTime"],0,0),
	"p":(25,0,0), #"AnalyserNumber"],0,0),
	"q":(26,0,0), #"DateTime"],0,0),
	"s":(27,0,0), #"AnalyzerSequence"],0,0),
	"t":(28,0,0), #"SamplingMode"],0,0),
	"u":(29,0,0), #"SampleIDbyAnalyser"],0,0),
	"v":(30,0,0), #"sample_id"],0,0),
	"\x80":(31,0,0), #"AnalyserMode"],0,0),
	"!":(1,5,1000), #"WBC"],0,1000),
	"2":(2,5,0), #"RBC"],0,0),
	"3":(3,5,0), #"Hemoglobin"],0,0),
	"4":(4,5,0), #"Hematocrit"],0,0),
	"5":(5,5,0), #"MCV"],0,0),
	"6":(6,5,0), #"MCH"],0,0),
	"7":(7,5,0), #"MCHC"],0,0),
	"8":(8,5,0), #"RDW"],0,0),
	"@":(9,5,1000), #"Platelet"],0,1000),
	"A":(10,5,0), #"MPV"],0,0),
	"B":(11,5,0), #"THT"],0,0),
	"C":(12,5,0), #"PWD"],0,0),
	"#":(13,5,0), #"Lymphocyte%"],0,0),
	"%":(14,5,0), #"Monocyte%"],0,0),
	"'":(15,5,0), #"Granulocyte%"],0,0),
	"\"":(16,5,0), #"LymphocyteCount"],0,0),
	"$":(17,5,0), #"MonocyteCount"],0,0),
	"&":(18,5,0), #"GranulocyteCount"],0,0),
	"X":(19,0,0), #"RDWGraph"],0,0),
	"W":(20,0,0), #"WBCWGraph"],0,0),
	"Y":(21,0,0), #"PlateletWGraph"],0,0),
	"S":(32,0,0), #"PlateletIdentifier?"],0,0),
	"_":(33,0,0), #"PlateletThresold"],0,0),
	"P":(34,0,0), #"WBCIdentifier?"],0,0),
	"]":(35,0,0), #"WBCThresold"],0,0),
	"\xfb":(36,0,0), #"AnalyserName"],0,0),
	"\xfe":(37,0,0), #"Version"],0,0),
	"\xfd":(38,0,0), #"Checksum"],0,0),
     }

  
  abx_result={}
  current_file=''
#Globals for configuration################
  inbox='/root/inbox1/'
  archived='/root/archived1/'
  
  def get_first_file(self):
    inbox_files=os.listdir(self.inbox)
    for each_file in inbox_files:
      if(os.path.isfile(self.inbox+each_file)):
        self.current_file=each_file
        return True
    return False  #no file to read
    
  def get_abx_result(self):
    fh=open(self.inbox+self.current_file,'r')
    while True:
      data=fh.readline().rstrip('\n')
      if data=='':
        break
      token=data.split(' ',1)
      analyser_code=token[0]
      if(analyser_code in self.abx):
        analyser_result=token[1]
        db_code=self.abx[analyser_code][0]
        field_size=self.abx[analyser_code][1]
        multiplication_factor=self.abx[analyser_code][2]
        if(field_size>0):
          db_result=(analyser_result[:field_size])
        else:
          db_result=analyser_result

        if(multiplication_factor>0):
          db_result=round(float(db_result)*multiplication_factor)
        else:
          db_result= db_result

        self.abx_result[db_code]=db_result
        
  def send_to_mysql(self):
    print('sample_id='+self.abx_result[30].rstrip(' '));
    if(self.abx_result[30].rstrip(' ').isnumeric() == False):
      print('sample_id is not number')
      return False;
    for key in self.abx_result.keys():
      sql='insert into primary_result (sample_id,examination_id,result,uniq) values (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE result=%s'
      data_tpl=(self.abx_result[30].rstrip(' '),key,self.abx_result[key],self.abx_result[26],self.abx_result[key])
      run_query(sql,data_tpl)
      
  def archive_file(self):
    os.rename(self.inbox+self.current_file,self.archived+self.current_file)
    current_file='';
      
#Main Code###############################
if __name__=='__main__':
  #print('__name__ is ',__name__,',so running code')
  m=micros()
  while True:
    if(m.get_first_file()):
      m.get_abx_result()
      m.send_to_mysql()
      m.archive_file()
    time.sleep(1)
  
