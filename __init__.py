plugin=None
import Tkinter as tkint

class Results(object):

    def __init__(self, parent):
        self.parentclass = parent
        self.parent=parent.parent        

        self.h=(9*height)/10
        self.w=width

        self.frame = tkint.Frame(self.parent, bg="#0f0f0f")
        self.frame.place(x=0,y=height/10,width=self.w, height=self.h)

        #self.populate([{'title':'Met het Mes op Tafel', 'duration':'19:00','broadcasted_on':'23-09-2015'}, {'title':'Met het Vork op de Stoel', 'duration':'20:59','broadcasted_on':'29-01-2016'}])
        self.populate(plugin.recent())


    def populate(self, items):
        self.items=[]

        h=self.h/10

        import time

        def add_item(item, position):
            
            if item['episode']['name']:
                if item['episode']['series']['name']:
                    item_title="%s: %s" % (item['episode']['series']['name'], item['episode']['name'])
                else:
                    item_title=item['episode']['name']
            else:
                if item['episode']['series']['name']:
                    item_title=item['episode']['series']['name']
                else:
                    item_title="*Unknown*"
            z=time.ctime(item['episode']['broadcasted_at']).split()
            z[-1], z[-2] = z[-2], z[-1]
            item_date=" ".join(z)
            #item_available=item['available']
            s=item['episode']['duration']
            item_duration="%s:%s" % (s/60, s%60)
            
            c=tkint.Canvas(self.frame, bg="#3f3f3f" if i%2==0 else "#5f5f5f", highlightthickness=0)
            c.place(x=0,y=position*h, width=self.w, height=h)
            ctitle=c.create_text(self.w/100, h/3, anchor=tkint.W, text=item_title, fill="white", font=("Verdana", 18), tags="title")
            cdur=c.create_text(self.w/100, (3*h)/4, anchor=tkint.W, text=item_duration, fill="white", font=("Verdana", 14), tags="duration")
            cbroad=c.create_text(99*self.w/100, (3*h)/4, anchor=tkint.E, text=item_date, fill="white", font=("Verdana", 14), tags="broadcasted")

            self.items.append(c)

            

        for i in range(len(items)):
            add_item(items[i], i)
        

class Tabs(object):

    def __init__(self, parent):
        self.parentclass = parent
        self.parent=parent.parent

        self.h=height/10
        self.w=width

        self.frame = tkint.Frame(self.parent, bg="#1f1f1f")
        self.frame.place(x=0,y=0,width=self.w, height=self.h)

        self.tabslist=['Recent','Series','Search','Tips']

        self.tabs=[]

        for i in range(len(self.tabslist)):
            ww=self.w/4
            c=tkint.Canvas(self.frame,bg="#1f1f1f", highlightthickness=0)
            c.place(x=i*ww,y=0,width=ww,height=self.h)
            ctext=c.create_text(ww/2, 2*self.h/3, text=self.tabslist[i], fill="white", font=("Verdana", 18), tags="text")
            self.tabs.append(c)

class Main(object):

    def __init__(self, parent):
        self.parent=parent
        self.results=Results(self)
        self.tabs=Tabs(self)
        

def init():
    global plugin
    import plugin
    plugin.load_recent()

def display(parent, geom=(1280,720)):
    global width
    width=parent.winfo_width() if parent.winfo_width() > 1 else geom[0]
    global height
    height=parent.winfo_height() if parent.winfo_height() > 1 else geom[1]
    
    frame = tkint.Frame(parent, bg="black")
    frame.place(x=0,y=0,relwidth=1,relheight=1)

    global main_frame
    main_frame=Main(frame)

def ui_loop():
    import namb.userinput
    namb.userinput.process_next()
    root.after(10, ui_loop)

if __name__=="__main__":
    import sys, os
    sys.path.insert(0, os.path.join("..","..",".."))

    import extensions
    extensions.load_extension("vlc")

    global root
    
    #import Tkinter as tkint
    root=tkint.Tk()
    #root.geometry("1280x720+0+0")
    root.attributes('-fullscreen', True)
    root.bind("<Escape>", lambda e: root.destroy())
    root.focus_set()

    import namb.userinput.keyboard
    namb.userinput.keyboard.setup()
    namb.userinput.keyboard.bind(root)

    import namb.userinput.ui_server
    namb.userinput.ui_server.run()

    init()
    display(root, (root.winfo_screenwidth(), root.winfo_screenheight()))
    import namb.userinput
    #namb.userinput.set_receiver(menu_frame.list)
    #ui_loop()
    root.mainloop()
