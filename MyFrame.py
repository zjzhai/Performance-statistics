# -*- coding: utf-8 -*-
import wx
import wx.lib.filebrowsebutton as filebrowse
import os
import os.path
import string
import codecs
codingUTF = 'utf8'
codingGBK = 'gbk'
address = ''

class iFrame(wx.Frame):
    def __init__(self, parent, title):
        super(iFrame, self).__init__(parent, title = title,
            size = (455, 130), style = wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        self.dirAddress = ''
        self.unknow = ' \r\n unknow \r\n ------------ \r\n'
        self.mingDan = ''
        self.listStu = {}
        self.InitUI()
        self.Centre()
        self.Show()   

    
    def InitUI(self):                
        panel = wx.Panel(self, -1)
        
        contrainBox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        dbb = filebrowse.DirBrowseButton(panel, -1, size = (450, -1), changeCallback = self.dbbCallback)
        hbox1.Add(dbb)
        contrainBox.Add(hbox1)
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        startBtn = wx.Button(panel, -1, label = "Start")
        self.Bind(wx.EVT_BUTTON, self.startBtnE, startBtn)
        
        openBtn = wx.Button(panel, -1, label = "Open")
        self.Bind(wx.EVT_BUTTON, self.openBtnE, openBtn)
        
        hbox2.Add(startBtn,flag = wx.EXPAND|wx.RIGHT)
        hbox2.Add(openBtn,flag = wx.EXPAND|wx.RIGHT)
        contrainBox.Add(hbox2, flag = wx.ALIGN_RIGHT|wx.TOP, border = 10)
        panel.SetSizer(contrainBox)
        
   
    def calculate(self, address):
        self.listStu = self.readListOfStudent(self.mingDan)
        self.loopIt(address)
        self.writeMingDan(self.mingDan, self.convert_disc_string(self.listStu)+ self.unknow)
        wx.MessageDialog(None, 'finished!', " ", wx.OK).ShowModal()
        self.openWithNotepad(self.mingDan)
        
    def createMenuBar(self):
        menuBar = wx.MenuBar()
        helpMenu = wx.Menu()
        menuBar.Append(helpMenu, '&Help')
        self.SetMenuBar(menuBar)

    def helpMenuCallback(self, e):
        pass
    
    def dbbCallback(self, e):
        if not os.path.isdir(e.GetString().strip()):
            wx.MessageDialog(None, u"必须是目录", " ", wx.OK).ShowModal()
            e.SetValue(self,'')
        else :
            self.dirAddress = e.GetString().strip()
            self.mingDan = self.returnMingDan(self.dirAddress)
        

    def startBtnE(self,e):
        if not self.checkFileAndAlert(self.mingDan) :
            return
        else :
            self.calculate(self.dirAddress)

    #打开名单   
    def openBtnE(self, e):
        if self.checkFileAndAlert(self.mingDan):
            pass
        else:
            self.openWithNotepad(self.mingDan)

    #使用notepad打开
    def openWithNotepad(self, address):
        os.system('notepad ' + address.encode(codingGBK))

    #名单不存在，则警告
    def checkFileAndAlert(self, fileAddress):
        if not os.path.exists(fileAddress):
            wx.MessageDialog(None, u'名单不存在', u"注意", wx.OK).ShowModal()
            return False
        else:
            return True
            

    #读取名单进入字典中
    def readListOfStudent(self, md):
        listStu = {}
        with open(md, "r") as f:
            for line in f.readlines() :
                txt = line.strip().decode(codingUTF)
                listStu[txt] = 0

        return listStu

    #遍历文件并统计分数,写入字典
    def loopIt(self, address):
        for dirpath, dirnames, filenames in os.walk(address):
           
            baseName = self.pullChinese(os.path.basename(dirpath).strip())
            #是否给学生加分的规则
            if len(baseName) == 0:
                self.unknow += dirpath.strip()+'\r\n'
            if self.listStu.has_key(baseName) and filenames:
                self.listStu[baseName] += 1
    
    #写入文件
    def writeMingDan(self, where, what):
        with open(where, "w") as f:
            f.write(what.encode(codingUTF))
            f.flush()

    #将字典转成字符串
    def convert_disc_string(self, disc):
        txt = ''
        for (k,v) in disc.items():
            txt += '%s\t%s \r\n' % (k,v)
        return txt
    
    #抽取中文
    def pullChinese(self, txt):
        ret_str = []
        for s in txt:
            if self.is_cn_char(s):
                ret_str.append(s)
        
        return "".join(ret_str)

    def is_cn_char(self, i): 
        return 0x4e00 <= ord(i) < 0x9fa6

    #检测名单路径是否合法
    def checkMingDanAndDialog():
        pass

    #返回名单
    def returnMingDan(self, address):
         return os.path.join(address, address.split(os.path.sep)[-1] + '.txt')
    
if __name__ == '__main__':
    app = wx.App()
    iFrame(None, title=u'文件统计')
    app.MainLoop()
