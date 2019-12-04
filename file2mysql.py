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
  con=MySQLdb.connect('127.0.0.1','root','xyz','pathology')
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
	"\xff":22, #"RecordType"],
	"p":23, #"AnalyserNumber"],
	"q":24, #"AnalysisDateTime"],
	"p":25, #"AnalyserNumber"],
	"q":26, #"DateTime"],
	"s":27, #"AnalyzerSequence"],
	"t":28, #"SamplingMode"],
	"u":29, #"SampleIDbyAnalyser"],
	"v":30, #"sample_id"],
	"\x80":31, #"AnalyserMode"],
	"!":1, #"WBC"],
	"2":2, #"RBC"],
	"3":3, #"Hemoglobin"],
	"4":4, #"Hematocrit"],
	"5":5, #"MCV"],
	"6":6, #"MCH"],
	"7":7, #"MCHC"],
	"8":8, #"RDW"],
	"@":9, #"Platelet"],
	"A":10, #"MPV"],
	"B":11, #"THT"],
	"C":12, #"PWD"],
	"#":13, #"Lymphocyte%"],
	"%":14, #"Monocyte%"],
	"'":15, #"Granulocyte%"],
	"\"":16, #"LymphocyteCount"],
	"$":17, #"MonocyteCount"],
	"&":18, #"GranulocyteCount"],
	"X":19, #"RDWGraph"],
	"W":20, #"WBCWGraph"],
	"Y":21, #"PlateletWGraph"],
	"S":32, #"PlateletIdentifier?"],
	"_":33, #"PlateletThresold"],
	"P":34, #"WBCIdentifier?"],
	"]":35, #"WBCThresold"],
	"\xfb":36, #"AnalyserName"],
	"\xfe":37, #"Version"],
	"\xfd":38, #"Checksum"],
     }

  abx_result={}
  current_file=''
#Globals for configuration################
  inbox='/root/inbox/'
  archived='/root/archived/'
  
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
      if(token[0] in self.abx):
        self.abx_result[self.abx[token[0]]] = token[1]
        
  def send_to_mysql(self):
    for key in self.abx_result.keys():
      sql='insert into result (sample_id,examination_id,result,uniq) values (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE result=%s'
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
  
