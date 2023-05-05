#!/usr/bin/python3

"""
OlyExifSort GUI
"""

import wx
import OlyExifSort
import sys
import wx.lib.agw.hyperlink as hl
import wx.lib.intctrl
from threading import Thread


class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)


class MainFrame(wx.Frame):
    """
    Main Frame
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        sizeX = 600
        sizeY = 560
        super(MainFrame, self).__init__(*args, **kw, size=(sizeX, sizeY))
        MainFrame.SetMinSize(self, size=(sizeX, sizeY))
        MainFrame.SetMaxSize(self, size=(sizeX, sizeY))

        # create a panel in the frame
        panel = wx.Panel(self)

        # 1st Line
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        l1 = wx.StaticText(panel, label="Folder:")
        hbox1.Add(l1, 1, wx.CENTER | wx.ALIGN_LEFT, 5)

        self.tcPath = wx.TextCtrl(panel, size=(430, 20))
        hbox1.Add(self.tcPath, 1, wx.CENTER | wx.ALIGN_LEFT, 5)

        # dialog button
        dirDlgBtn = wx.Button(panel, label="Choose Folder")
        hbox1.Add(dirDlgBtn, wx.CENTER | wx.ALIGN_LEFT, 5)
        dirDlgBtn.Bind(wx.EVT_BUTTON, self.onDir)

        # 2nd Line
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # process button
        font = wx.Font(wx.FontInfo(14).Bold())
        self.searchBtn = wx.Button(panel, label="Search Sequences")
        self.searchBtn.Bind(wx.EVT_BUTTON, self.onSearchSeq)
        self.searchBtn.SetFont(font)
        hbox2.Add(self.searchBtn, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 5))

        self.moveBtn = wx.Button(panel, label="Move Sequences")
        self.moveBtn.Bind(wx.EVT_BUTTON, self.onMoveSeq)
        self.moveBtn.SetFont(font)
        self.moveBtn.Disable()
        hbox2.Add(self.moveBtn, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 5))

        # 3th Line
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        # process button
        self.tcOutput = wx.TextCtrl(
            panel, size=(600, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)
        hbox3.Add(self.tcOutput, 1, wx.CENTER | wx.ALIGN_LEFT | wx.ALL, 5)

        # redirect output to log
        redir = RedirectText(self.tcOutput)
        sys.stdout = redir

        # 4th line

        hsub1 = wx.BoxSizer(wx.HORIZONTAL)

        lHDR = wx.StaticText(panel, label="HDR Offset: ")
        self.iHDR = wx.lib.intctrl.IntCtrl(panel, size=(1, -1))

        hsub1.Add(lHDR, 1, wx.CENTER | wx.ALIGN_LEFT, 5)
        hsub1.Add(self.iHDR, 1, wx.CENTER | wx.ALIGN_LEFT, 5)

        lFOC = wx.StaticText(panel, label="  FOC Offset: ")
        self.iFOC = wx.lib.intctrl.IntCtrl(panel, size=(1, -1))
        hsub1.Add(lFOC, 1, wx.CENTER | wx.ALIGN_LEFT, 5)
        hsub1.Add(self.iFOC, 1, wx.CENTER | wx.ALIGN_LEFT, 5)

        lAE = wx.StaticText(panel, label="  AE Offset: ")
        self.iAE = wx.lib.intctrl.IntCtrl(panel, size=(1, -1))
        hsub1.Add(lAE, 1, wx.CENTER | wx.ALIGN_LEFT, 5)
        hsub1.Add(self.iAE, 1, wx.CENTER | wx.ALIGN_LEFT, 5)

        lWB = wx.StaticText(panel, label="  WB Offset: ")
        self.iWB = wx.lib.intctrl.IntCtrl(panel, size=(1, -1))
        hsub1.Add(lWB, 1, wx.CENTER | wx.ALIGN_LEFT, 5)
        hsub1.Add(self.iWB, 1, wx.CENTER | wx.ALIGN_LEFT, 5)

        hsub2 = wx.BoxSizer(wx.HORIZONTAL)

        lFL = wx.StaticText(panel, label="FL Offset:  ")
        self.iFL = wx.lib.intctrl.IntCtrl(panel, size=(1, -1))
        hsub2.Add(lFL, 1, wx.CENTER | wx.ALIGN_LEFT, 5)
        hsub2.Add(self.iFL, 1, wx.CENTER | wx.ALIGN_LEFT, 5)

        lMF = wx.StaticText(panel, label="  MF Offset: ")
        self.iMF = wx.lib.intctrl.IntCtrl(panel, size=(1, -1))
        hsub2.Add(lMF, 1, wx.CENTER | wx.ALIGN_LEFT, 5)
        hsub2.Add(self.iMF, 1, wx.CENTER | wx.ALIGN_LEFT, 5)

        lISO = wx.StaticText(panel, label="  ISO Offset: ")
        self.iISO = wx.lib.intctrl.IntCtrl(panel, size=(1, -1))
        hsub2.Add(lISO, 1, wx.CENTER | wx.ALIGN_LEFT, 5)
        hsub2.Add(self.iISO, 1, wx.CENTER | wx.ALIGN_LEFT, 5)

        # 5th line

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        # set font  for output
        fontOutput = wx.Font(8, wx.MODERN, wx.NORMAL,
                             wx.NORMAL, False, u'Consolas')
        self.tcOutput.SetFont(fontOutput)

        self.link500px = hl.HyperLinkCtrl(
            panel, -1, "If you like the script please support me on 500px", URL="https://500px.com/p/dbs06")
        hbox5.Add(self.link500px, 1, wx.CENTER | wx.ALIGN_LEFT | wx.ALL, 5)

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hbox1, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 5))
        sizer.Add(0, 10, 0)
        sizer.Add(hbox2, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 5))
        sizer.Add(hbox3, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 5))
        sizer.Add(hsub1, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 5))
        sizer.Add(hsub2, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 5))
        sizer.Add(hbox5, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 5))
        sizer.Add(0, 10, 0)
        panel.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to OlyExitSort!")

    def onDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
                           # | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self.tcPath.SetValue(dlg.GetPath())
        dlg.Destroy()

    def onSearchSeq(self, event):
        """
        Search for Sequences
        """
        self.searchBtn.Disable()
        self.moveBtn.Disable()
        self.tcOutput.Clear()
        self.SetStatusText("Search for Sequences...")
        self.path = self.tcPath.GetValue()
        # create a thread
        thread = Thread(target=self.searchSequenceTask)
        # run the thread
        thread.start()
        self.searchBtn.Enable()

    def onMoveSeq(self, event):
        """
        Move Sequences
        """
        if (len(self.aeaBrkt) > 0 or len(self.focBrkt) > 0 or len(self.aeBrkt) > 0 or len(self.wbBrkt) > 0 or len(self.flBrkt) > 0 or len(self.mfBrkt) > 0 or len(self.isoBrkt) > 0):
            self.searchBtn.Disable()
            self.moveBtn.Disable()
            self.SetStatusText("Moving Sequences...")

            # create a thread
            thread = Thread(target=self.moveSequenceTask)
            # run the thread
            thread.start()

            self.SetStatusText("Moving Sequences finished!")
            self.moveBtn.Disable()
            self.searchBtn.Enable()

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # When using a stock ID we don't need to specify the menu item's label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        # The "\t..." syntax defines an accelerator key that also triggers the same event
        helpMenu = wx.Menu()
        helpItem = helpMenu.Append(-1, "&Help...\tCtrl-H",
                                   "Help string shown in status bar for this menu item")
        helpMenu.AppendSeparator()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHelp, helpItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnHelp(self, event):
        """Help"""
        wx.MessageBox("This Script detects and sorts photos which where taken with AEA/HDR- and Focus-Bracketing-Mode with an Olympus/OM-System camera.\nThis script is intended to simplify the sort-out process, after you come back from a photo session.\nFor more Information please read the Readme or visit the GitHub Repo: https://github.com/DBS06/OlyExifSort")

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("Written by DBS06\nIf you want to support me, I would really happy if you would add me on 500px and/or like my photos\nhttps://500px.com/p/dbs06 ",
                      "About OlyExifSort",
                      wx.OK | wx.ICON_INFORMATION)

    def searchSequenceTask(self):
        retStatus, self.aeaBrkt, self.focBrkt, self.aeBrkt, self.wbBrkt, self.flBrkt, self.mfBrkt, self.isoBrkt = OlyExifSort.executeExifRead(
            self.path)

        print("")
        status = ""
        if (retStatus == OlyExifSort.ReturnStatus.SUCCESS):
            status = "Search for Sequences finished!"
            self.moveBtn.Enable()
        elif (retStatus == OlyExifSort.ReturnStatus.ERROR):
            status = "Search for Sequences ended with an unknown Error!"
        elif (retStatus == OlyExifSort.ReturnStatus.INVALID_PATH):
            status = "Given Path is invalid!"
        elif (retStatus == OlyExifSort.ReturnStatus.NO_IMAGES_FOUND):
            status = "No images found in given folder!"
        elif (retStatus == OlyExifSort.ReturnStatus.NO_FILES):
            status = "No files found in given folder!"
        elif (retStatus == OlyExifSort.ReturnStatus.NO_SEQUENCES_FOUND):
            status = "No Bracketing-Sequences found in given folder!"

        print(status)
        print("")
        self.SetStatusText(status)

    def moveSequenceTask(self):
        OlyExifSort.moveSequences(self.path, self.aeaBrkt, self.focBrkt,
                                  self.aeBrkt, self.wbBrkt, self.flBrkt, self.mfBrkt, self.isoBrkt,
                                  self.iHDR.GetValue(), self.iFOC.GetValue(), self.iAE.GetValue(), self.iWB.GetValue(), self.iFL.GetValue(), self.iMF.GetValue(), self.iISO.GetValue())


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MainFrame(None, title='OlyExifSort GUI')
    frm.Show()
    app.MainLoop()
