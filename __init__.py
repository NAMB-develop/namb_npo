plugin=None
import Tkinter as tkint

def seconds_to_hms(seconds):
    h=seconds/3600
    if h<10:
        hstring="0%s"%h
    else:
        hstring="%s"%h
    m=(seconds%3600)/60
    if m<10:
        mstring="0%s"%m
    else:
        mstring="%s"%m
    s=seconds%60
    if s<10:
        sstring="0%s"%s
    else:
        sstring="%s"%s
    return "%s:%s:%s"%(hstring, mstring, sstring)

class Results(object):

    def __init__(self, parent):
        self.parentclass = parent
        self.parent=parent.parent        

        self.y=height/10
        self.h=(9*height)/10
        self.w=width

        self.itemh=self.h/10
        self.itemw=self.w
        self.itemoffset=self.itemh/2

        self.containerframe=tkint.Frame(self.parent, bg="#0f0f0f")
        self.containerframe.place(x=0,y=self.y,width=self.w, height=self.h)

        self.frame = tkint.Frame(self.containerframe, bg="#0f0f0f")
        self.frame.place(x=0,y=self.itemoffset,width=self.w, height=self.h)

        self.items=[]
        self.at=0

        #self.populate(plugin.recent())

        ##DEBUG:
        #self.frame.after(5000, lambda: self.shift(10))


    def focus_receive(self):
        self.activate(self.at)

    def receive(self, event):
        import namb.userinput.keys
        import namb.userinput
        if event==namb.userinput.keys.UP:
            self.shift(-1)
        elif event==namb.userinput.keys.DOWN:
            self.shift(1)
        elif event==namb.userinput.keys.ENTER:
            self.select()
        elif event==namb.userinput.keys.BACK:
            self.deactivate(self.at)
            self.clear()
            namb.userinput.set_receiver(self.parentclass.tabs)
            self.parentclass.tabs.focus_receive()

    def clear(self):
        for i in self.items:
            #i.delete("all")
            i.destroy()
        self.items=[]
        self.at=0

    def process_serie(self, serie):
        item_title=serie['name']
        item_desc=serie['description']
        if item_desc:
            item_desc=item_desc.replace("\n","")
            if len(item_desc)>140:
                words=item_desc.split(" ")
                z=0
                r=""
                while len(r+words[z]) < 140:
                    r=r+words[z]+" "
                    z=z+1
                r=r+"..."
                item_desc=r
        q=serie['broadcasters']
        qq=""
        for i in range(len(q)):
            if not i==0:
                qq=qq+", " + q[i]
            else:
                qq=""+q[i]
        item_broadcaster="(%s)"%qq
        return item_title, item_desc, item_broadcaster

    def process_episode(self, episode):
        import time
        if episode['episode']:
            if 'name' in episode:
                item_title=episode['name']
            else:
                if 'name' in episode['episode']:
                    if episode['episode']['name']:
                        if episode['episode']['series']['name']:
                            item_title="%s: %s" % (episode['episode']['series']['name'], episode['episode']['name'])
                        else:
                            item_title=episode['episode']['name']
                    else:
                        if episode['episode']['series']['name']:
                            item_title=episode['episode']['series']['name']
                        else:
                            item_title="*Unknown*"
        else:
            print("are these really episodes?! ERROR")
        z=time.ctime(episode['episode']['broadcasted_at']).split()
        z[-1], z[-2] = z[-2], z[-1]
        item_date=" ".join(z)
        #item_available=episode['available']
        s=episode['episode']['duration']
        item_duration=seconds_to_hms(s)

        return item_title, item_date, item_duration

    def populate_tips(self, items):
        self.populate_episodes(items)

    def populate_series(self, items):
        self.items=[]

        self.frame.place(height=int(self.itemh*(len(items)+1)))


        def add_item(item, position):
            item_title, item_desc, item_broadcaster=self.process_serie(item)

            c=tkint.Canvas(self.frame, bg="#5f5f5f" if i%2==0 else "#4f4f4f", highlightthickness=0)
            c.place(x=0,y=position*self.itemh, width=self.itemw, height=self.itemh)

            ctitle=c.create_text(self.w/100, self.itemh/3, anchor=tkint.W, text=item_title, fill="white", font=("Verdana", 14), tags="title")
            cdesc=c.create_text(self.w/100, 3*self.itemh/4, anchor=tkint.W, text=item_desc, fill="#cfcfcf", font=("Verdana", 10), tags="desc")
            cbroad=c.create_text(99*self.w/100, self.itemh/3, anchor=tkint.E, text=item_broadcaster, fill="#cfcfcf", font=("Verdana", 14), tags="broad")


            
            self.items.append(c)

        for i in range(len(items)):
            add_item(items[i], i)        

    def populate_episodes(self, items):
        self.items=[]

        self.frame.place(height=int(self.itemh*(len(items)+1)))

        import time

        def add_item(item, position):
            item_title, item_date, item_duration = self.process_episode(item)
            
            c=tkint.Canvas(self.frame, bg="#3f3f3f" if i%2==0 else "#5f5f5f", highlightthickness=0)
            c.place(x=0,y=position*self.itemh, width=self.itemw, height=self.itemh)
            
            ctitle=c.create_text(self.w/100, self.itemh/3, anchor=tkint.W, text=item_title, fill="white", font=("Verdana", 14), tags="title")
            #cdur=c.create_text(self.w/100, (3*h)/4, anchor=tkint.W, text=item_duration, fill="white", font=("Verdana", 14), tags="duration")
            cbroad=c.create_text(99*self.w/100, (3*self.itemh)/4, anchor=tkint.E, text=item_date, fill="#cfcfcf", font=("Verdana", 10), tags="broadcasted")

            self.items.append(c)

            

        for i in range(len(items)):
            add_item(items[i], i)

    def activate(self, item):
        self.items[item].config(bg="#9f9f9f")
        self.items[item].itemconfig("desc",fill="white")
        self.items[item].itemconfig("broadcasted",fill="white")

    def deactivate(self, item):
        self.items[item].config(bg="#5f5f5f" if item%2==0 else "#4f4f4f")
        self.items[item].itemconfig("desc",fill="#cfcfcf")
        self.items[item].itemconfig("broadcasted",fill="#cfcfcf")

    def update(self, posneg):
        prev=self.at
        cur=self.at+posneg
        self.deactivate(prev)
        self.activate(cur)
        self.at=self.at+posneg

    def shift(self, posneg):
        p=posneg
        if p+self.at<0 or p+self.at==len(self.items):
            return

        if self.items[p+self.at].winfo_y()+self.frame.winfo_y()>self.h-self.itemh or self.items[p+self.at].winfo_y()+self.frame.winfo_y()<self.itemoffset:
            offset=posneg*self.itemh*-1
            self.frame.place(y=self.frame.winfo_y()+offset)

        self.update(p)

    def select(self):
        pass

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
        self.at=0

        for i in range(len(self.tabslist)):
            ww=self.w/4
            c=tkint.Canvas(self.frame,bg="#1f1f1f", highlightthickness=0)
            c.place(x=i*ww,y=0,width=ww,height=self.h)
            ctext=c.create_text(ww/2, 2*self.h/3, text=self.tabslist[i], fill="#cccccc", font=("Verdana", 18), tags="text")
            self.tabs.append(c)

    def focus_receive(self):
        self.activate(self.at)

    def receive(self, event):
        import namb.userinput.keys
        import namb.userinput
        if event==namb.userinput.keys.UP or event==namb.userinput.keys.LEFT:
            self.shift(-1)
        elif event==namb.userinput.keys.DOWN or event==namb.userinput.keys.RIGHT:
            self.shift(1)
        elif event==namb.userinput.keys.ENTER:
            self.select()
        elif event==namb.userinput.keys.BACK:
            self.deactivate(self.at)
            namb.userinput.set_receiver(self.parentclass.tabs)
            self.parentclass.tabs.focus_receive()

    def shift(self, posneg):
        prospect=self.at+posneg
        if prospect < 0 or prospect > len(self.tabs)-1:
            return
        cur=self.at
        self.deactivate(cur)
        self.activate(prospect)
        self.at=prospect

    def activate(self, pos):
        self.tabs[pos].config(bg="#2f2f2f")
        self.tabs[pos].itemconfig("text", fill="white")

    def deactivate(self, pos):
        self.tabs[pos].config(bg="#1f1f1f")
        self.tabs[pos].itemconfig("text", fill="#cccccc")

    def select(self):

        def resultsfocus():
            namb.userinput.set_receiver(self.parentclass.results)
            self.parentclass.results.focus_receive()
        
        if self.tabslist[self.at]=="Recent":
            self.parentclass.results.clear()
            self.parentclass.results.populate_episodes(plugin.recent())
            resultsfocus()
        elif self.tabslist[self.at]=="Series":
            self.parentclass.results.clear()
            self.parentclass.results.populate_series(plugin.series())
            resultsfocus()
        elif self.tabslist[self.at]=="Search":
            self.parentclass.results.clear()
        elif self.tabslist[self.at]=="Tips":
            self.parentclass.results.clear()
            self.parentclass.results.populate_episodes(plugin.tips())
            resultsfocus()            

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
    namb.userinput.set_receiver(main_frame.tabs)
    main_frame.tabs.focus_receive()
    ui_loop()
    root.mainloop()
