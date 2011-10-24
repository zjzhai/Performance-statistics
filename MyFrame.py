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
        hbox2.Add(startBtn,flag = wx.EXPAND|wx.RIGHT)
        contrainBox.Add(hbox2, flag = wx.ALIGN_RIGHT|wx.TOP, border = 10)
        panel.SetSizer(contrainBox)
        self.Bind(wx.EVT_BUTTON, self.btnE, startBtn)
        
        #self.createMenuBar()
        

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        helpMenu = wx.Menu()
        #helpItem = helpMenu.Append(wx.ID_ANY, u"使用说明", '' )
        menuBar.Append(helpMenu, '&Help')
        self.SetMenuBar(menuBar)
        #selfBind(wx.EVT_MENU, self.helpMenuCallback, helpMenu)

    def helpMenuCallback(self, e):
        pass
    
    def dbbCallback(self, e):
        #wx.MessageDialog(None, e.GetString().strip()," ", wx.OK).ShowModal()
        if not os.path.isdir(e.GetString().strip()):
            wx.MessageDialog(None, u"必须是目录"," ", wx.OK).ShowModal()
            e.SetValue(self,'')
        else :
            self.dirAddress = e.GetString().strip()
        

    def btnE(self,e):
        self.mingDan = os.path.join(self.dirAddress, self.dirAddress.split(os.path.sep)[-1] + '.txt')
       
        if not os.path.exists(self.mingDan):
            wx.MessageDialog(None, u'名单不存在', u"注意", wx.YES_NO).ShowModal()
            os.system('cd ' + self.dirAddress.encode(codingUTF))
            return
        if not self.dirAddress :
            wx.MessageDialog(None, u'地址不能为空',u"注意", wx.YES_NO).ShowModal()
            return
        else :
            self.calculate(self.dirAddress)
            
                
    
    def calculate(self, address):
        
        self.listStu = self.readListOfStudent(self.mingDan)
        self.loopIt(address)
        self.writeMingDan(self.mingDan, self.convert_disc_string(self.listStu))
        wx.MessageDialog(None, 'finished!', " ", wx.OK).ShowModal()
        os.system('notepad ' + self.mingDan)
        
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
            #是否给学生加分规则
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
    def pullChinese(self,txt):
        ret_str = []
        for s in txt:
            if self.is_cn_char(s):
                ret_str.append(s)
        
        return "".join(ret_str)

    def is_cn_char(self, i): 
        return 0x4e00 <= ord(i) < 0x9fa6
    
if __name__ == '__main__':
    app = wx.App()
    iFrame(None, title=u'文件统计')
    app.MainLoop()
