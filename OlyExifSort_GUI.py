"""
#!/usr/bin/env python
OlyExifSort GUI
"""

import wx


class MainFrame(wx.Frame):
    """
    Main Frame
    """

    path = ""

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, **kw, size=(600, 250))

        # create a panel in the frame
        panel = wx.Panel(self)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        l1 = wx.StaticText(panel, label="Folder:")
        hbox1.Add(l1, 1, wx.CENTER | wx.ALIGN_LEFT | wx.ALL, 5)

        self.tcPath = wx.TextCtrl(panel, size=(400, 20))
        hbox1.Add(self.tcPath, 1, wx.CENTER | wx.ALIGN_LEFT | wx.ALL, 5)
        self.tcPath.Bind(wx.EVT_TEXT, self.OnKeyTyped)

        '''
        # put some text with a larger bold font on it
        self.stPath = wx.StaticText(panel, label="no path selected")
        font = self.stPath.GetFont()
        # font.PointSize += 10
        font = font.Bold()
        self.stPath.SetFont(font)
        
        sizer.Add(self.stPath, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 25))
        '''

        # A dialog button
        dirDlgBtn = wx.Button(panel, label="Choose Folder")
        hbox1.Add(dirDlgBtn, wx.CENTER | wx.ALIGN_LEFT | wx.ALL, 5)
        dirDlgBtn.Bind(wx.EVT_BUTTON, self.onDir)

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hbox1, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 5))
        panel.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to OylExitSort!")

    def onDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
                           # | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print("You chose %s" % path)
            # self.stPath.SetLabel("Selected Path: " + path)
            self.tcPath.SetValue(path)
        dlg.Destroy()

    def OnKeyTyped(self, event):
        print(event.GetString())
        path = event.GetString()

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


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MainFrame(None, title='OlyExifSort GUI')
    frm.Show()
    app.MainLoop()
