

import codecs
import sys
import string
import os

def textget(filename="in.xml"):#
	"""This function grabs the text from the file, obviously just a copy of the example."""
	words=''
	text=open(filename)
	for line in text:
		words=words+line+' '
	return words
def datawrite(data,fname="converted.ass"):
    """ write out converted ass file """
    fout=codecs.open (fname,"w","utf-8");
    fout.write(u'\ufeff')
    intro=u"[Script Info]\n\
Title:NicoScript\n\
Original Script: NicoNico or else\n\
ScriptType: v4.00\n\
Collisions: Normal\n\
PlayResX: 640\n\
PlayResY: 360\n\
PlayDepth: 32\n\
Timer: 100.0000\n\
WrapStyle: 2\n\n\n"
    fout.write(intro);
    intro=u"[V4+ Styles]\n\
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColor, BackColour, Bold, \
Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, \
Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n\
Style: Default, Meiryo Bold,80,11861244,11861244,0,-2147483640,-1,0,0,0,100,100,1,0.00,1,1,0,10,30,30,30,1\n\
Style: Static,Meiryo Bold,80,11861244,11861244,0,-2147483640,-1,0,0,0,100,100,2,0.00,1,1,0,2,0,0,0,1\n\
Style: Scroll,Meiryo Bold,80,11861244,11861244,0,-2147483640,-1,0,0,0,100,100,2,0.00,1,1,0,2,0,0,0,1\n\n\n\
"
    fout.write(intro);
    intro=u"[Events]\n\
Format: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    fout.write(intro);
    intro=u"\nDialogue: Marked=0,"
    middle=u"Scroll,NicoChu,0000,0000,0000,,{\\a6\\move(1150, ";
    end=u")\c&HFFFFFF\\fs25}";#event string backbone
    pos=1;
    told=data[0][0]-200;
    for i in range (0, len (data)):
        tnow=data[i][0];
        #grab current data in 10ms format
        tnext=tnow+400;#let it roll for 4 seconds
        t1=realtime(tnow);
        t2=realtime(tnext);
        text=data[i][-1];#grab text
        if (pos>320 or tnow>told+400):
            told+=400;
            pos=1;
        fout.write(intro+unicode(t1)+u","+unicode(t2)+u","+middle+unicode(str(pos))+u", 0 , "+unicode(str(pos))+end);
        pos+=20;
        fout.write(text);
        fout.writelines(u'\n')
    fout.flush();
    fout.close();

def dictsort(data, idx):
    """ sort out the dictionary by order of value index """
    dict2={};
    tosort=[];
    for i in range(0, len (data)):
        tosort.append([int(data[i][idx]),i]);
    tosort=sorted(tosort);
    for i in range(0, len (data)):
        dict2[i]=data[tosort[i][1]];
        dict2[i][idx]=tosort[i][0];
    return dict2

def sortxml(words):
    """use the stirng literal to generate a dict of """
    text=[];
    data={};
    entry={};
    date=[];
    vpos=[];
    no=[];
    uid=[];
    enum=0;
    ordering=['enum:', 'vpos','date','no','uid','text'];
    for i in range(0,6):
        entry[i]=ordering[i];
    idx=words.find('<') #find brackets in xml
    while idx!=-1:
        #now to fill all the lists
        templ=[];
        temps='';
        idx2=words.find('vpos',idx );
        if idx2==-1:
                break;
        idx3=words.find('\"',idx2 );
        idx4=words.find('\"',idx3+1);
        temps=words[idx3+1:idx4];
        templ.append(temps);
        idx2=words.find('date',idx );
        idx3=words.find('\"',idx2 );
        idx4=words.find('\"',idx3+1);
        temps=words[idx3+1:idx4];
        templ.append(temps);
        idx2=words.find('no',idx );
        idx3=words.find('\"',idx2 );
        idx4=words.find('\"',idx3+1);
        temps=words[idx3+1:idx4];
        templ.append(temps);
        idx2=words.find('user_id',idx );
        idx3=words.find('\"',idx2 );
        idx4=words.find('\"',idx3+1);
        temps=words[idx3+1:idx4];
        templ.append(temps);
        idx2=words.find('>',idx4+1 ); 
        idx3=words.find('<',idx2+1 );
        temps=words[idx2+1:idx3];
        try:
                temps=unicode(words[idx2+1:idx3],'utf-8');
        except UnicodeDecodeError:
                temps=unicode (words[idx2+1:idx3],'shift-jis');
        templ.append(temps);
        data[enum]=templ;
        enum+=1;
        idx=words.find('<',idx3+1);
        #idx now at end bracket
    print entry;
    return data;

def realtime(oldtime):
    """docstring for realtimereturn real time in hour,minute,second format"""
    oldtime=float(oldtime)/100;
    hour=int(oldtime/3600);
    if hour<10:
        hourt='0'+str(hour);
    else:
        hourt=str(hour);
    minutes=int((oldtime-hour*3600)/60);
    if minutes<10:
        minutest='0'+str(minutes);
    else:
        minutest=str(minutes);
    seconds=round(float(oldtime-hour*3600-minutes*60),2);
    if seconds<10:
        secondst='0'+str(seconds);
    else:
        secondst=str(seconds);
    realt=str(hourt)+":"+str(minutest)+":"+str(secondst);
    return realt;
def main():
    for filename in os.listdir ('./'):
        ext='';
        try:
            name,ext=filename.split('.');
        except:
            continue;
        if ext!='xml':
            continue;
        else:
            name=name;
            text=textget(name+".xml");
            data=sortxml(text);
            data=dictsort(data,0);
            datawrite(data,name+".ass");

main();

