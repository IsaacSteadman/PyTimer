import sys
import os
import math
import pygame

AlarmFile = "TornadoSiren.ogg"

class Button:
    def __init__(self, x, y, Width, Height, Txt, Bkgr, Frgr, OnClr):
        self.x = x
        self.y = y
        self.Width = Width
        self.Height = Height
        self.Txt = Txt
        self.Disp = True
        self.Bkgr = Bkgr
        self.Frgr = Frgr
        self.OnClr = OnClr
        self.IsOn = False
        self.ClkFunc = None
        self.CtlTrans = [None] * 4
        self.SelClr = (255, 255, 0)
        self.LastDraw = None
        self.Enabled = True
        self.NeedDraw = True
    def Click(self, x, y):
        if not self.Enabled:
            return None
        if self.ClkFunc != None:
            self.ClkFunc(self)
            return self
        return self
    def Text(self, Ch, IsInsert):
        if not self.Enabled:
            return None
        if Ch == ' ' or Ch == '\r': return self.Click()
        else: return self
    def Up(self):
        return self.GetCtlDir(0)
    def Down(self):
        return self.GetCtlDir(2)
    def Left(self):
        return self.GetCtlDir(3)
    def Right(self):
        return self.GetCtlDir(1)
    def Tab(self):
        return self.GetCtlDir(1)
    def ShiftTab(self):
        return self.GetCtlDir(3)
    def GetCtlDir(self, Num):
        if Num >= 0 and Num < 4:
            if self.CtlTrans[Num] == None:
                return self
            else:
                return self.CtlTrans[Num]
        else:
            return self
    def NoDisp(self, Surf, Bkgr):
        self.Clear(Surf, Bkgr)
        self.Disp = False
        self.NeedDraw = False
    def Disable(self):
        self.Enabled = False
        return None
    def Clear(self, Surf, Bkgr):
        if self.LastDraw != None: Surf.fill(Bkgr, self.LastDraw)
        self.LastDraw = None
    def Draw(self, IsSel, Fnt):
        if not self.Disp: return None
        Bkgr = self.Bkgr
        if self.IsOn:
            Bkgr = self.OnClr
        Rtn = pygame.surface.Surface((self.Width, self.Height))
        Tmp = Fnt.render(self.Txt, 1, self.Frgr, Bkgr)
        Pos = (self.Width - Tmp.get_width()) / 2, (self.Height - Tmp.get_height()) / 2
        if Pos[0] < 0 or Pos[1] < 0:
            Rtn = Tmp
        else:
            Rtn.fill(Bkgr)
            Rtn.blit(Tmp, pygame.rect.Rect(Pos, Tmp.get_size()))
        self.LastDraw = pygame.rect.Rect((self.x, self.y), Rtn.get_size())
        if IsSel: pygame.draw.rect(Rtn, self.SelClr, self.LastDraw)
        self.NeedDraw = False
        return Rtn
    def UnFocus(self):
        self.NeedDraw = True
class Label:
    def __init__(self, x, y, Txt, Fnt, Frgr, Bkgr):
        self.Fnt = Fnt
        self.Disp = True
        self.Enabled = False
        self.x = x
        self.y = y
        self.Txt = Txt
        self.Frgr = Frgr
        self.Bkgr = Bkgr
        self.NeedDraw = True
        self.Bmp = Fnt.render(Txt, 1, Frgr, Bkgr)
        self.Width = self.Bmp.get_width()
        self.Height = self.Bmp.get_height()
        self.LastDraw = pygame.rect.Rect(x, y, self.Width, self.Height)
    def Clear(self, Surf, Bkgr):
        if self.LastDraw != None: Surf.fill(Bkgr, self.LastDraw)
    def Click(self):
        return None
    def NoDisp(self, Surf, Bkgr):
        self.Clear(Surf, Bkgr)
        self.Disp = False
        self.NeedDraw = False
    def Draw(self, IsSel, Fnt):
        if self.Disp: return self.Bmp
        else: return None
def DrawCircle(Rad, x, y, Surf, Start, Finish, Thickness, Color, Bkgr):
    Outer = pygame.rect.Rect((x, y), (2 * Rad, 2 * Rad))
    Inner = pygame.rect.Rect((x, y), (2 * (Rad - Thickness), 2 * (Rad - Thickness)))
    pygame.draw.arc(Surf, Color, Outer, Start, Finish, 0)
    pygame.draw.arc(Surf, Bkgr, Inner, Start, Finish, 0)
class ProgressCircle:
    def __init__(self, x, y, Radius, Width, Frgr, Bkgr, Cpy=None):
        self.Disp = False
        self.Enabled = False
        self.x = x
        self.y = y
        self.Frgr = Frgr
        self.Bkgr = Bkgr
        self.NeedDraw = False
        self.Bmp = None
        self.Other = Cpy
        self.Width = 2 * Radius
        self.Height = 2 * Radius
        self.Thickness = Width
        self.Percent = 0.0
        self.LastDraw = pygame.rect.Rect(x, y, self.Width, self.Height)
        self.DrawRect = pygame.rect.Rect(0, 0, 2 * Radius, 2 * Radius)
    def Clear(self, Surf, Bkgr):
        if self.LastDraw != None: Surf.fill(Bkgr, self.LastDraw)
    def Click(self):
        return None
    def NoDisp(self, Surf, Bkgr):
        self.Clear(Surf, Bkgr)
        self.Disp = False
        self.NeedDraw = False
    def MkDisp(self):
        self.Disp = True
        self.NeedDraw = True
    def MkNoDisp(self):
        self.Disp = False
        self.NeedDraw = True
    def Draw(self, IsSel, Fnt):
        if self.Disp:
            if self.Other != None and self.Other.Bmp != None:
                Rtn = self.Other.Bmp
                self.Other.Bmp = None
                return Rtn
            Rtn = pygame.Surface((self.Width, self.Height))
            Rtn.fill(self.Bkgr)
            #DrawCircle(self.Width / 2, self.x, self.y, Rtn, math.pi / 2, math.pi * 2 * self.Percent + (math.pi / 2), self.Thickness, self.Frgr, self.Bkgr)
            pygame.draw.arc(Rtn, self.Frgr, self.DrawRect, math.pi / 2, math.pi * 2 * self.Percent + (math.pi / 2), self.Thickness)
            self.Bmp = Rtn
            return Rtn
        else: return None
class TxtInput:
    def __init__(self, x, y, Width, Height, MaxLen, Restrict, InitDat, InsIfMaxed):
        self.Rest = Restrict
        self.MaxLen = MaxLen
        self.CtlTrans = [None] * 4
        self.Dat = list(InitDat[0:MaxLen])
        self.Pos = 0
        self.InsIfMax = InsIfMaxed
        self.x = x
        self.y = y
        self.Width = Width
        self.Height = Height
        self.Enabled = True
        self.Disp = True
        self.Bkgr = (0,0,0)
        self.Frgr = (255, 255, 255)
        self.SelClr = (255, 255, 0)
        self.LastDraw = None
        self.NeedDraw = True
    def Up(self):
        return self.GetCtlDir(0)
    def Down(self):
        return self.GetCtlDir(2)
    def Right(self):
        if self.Pos < len(self.Dat):
            self.Pos += 1
            self.NeedDraw = True
        return self
    def Left(self):
        if self.Pos > 0:
            self.Pos -= 1
            self.NeedDraw = True
        return self
    def Tab(self):
        return self.GetCtlDir(1)
    def ShiftTab(self):
        return self.GetCtlDir(3)
    def GetCtlDir(self, Num):
        if Num >= 0 and Num < 4:
            if self.CtlTrans[Num] == None:
                return self
            else:
                self.UnFocus()
                self.CtlTrans[Num].NeedDraw = True
                return self.CtlTrans[Num]
        else:
            return self
    def Click(self, x, y):
        if self.Enabled:
            self.NeedDraw = True
            return self
    def Backspace(self):
        if not self.Enabled:
            return None
        if self.Pos == 0:
            return self
        self.Pos -= 1
        self.Dat.pop(self.Pos)
        self.NeedDraw = True
        return self
    def Delete(self):
        if not self.Enabled:
            return None
        if self.Pos == len(self.Dat):
            return self
        self.Dat.pop(self.Pos)
        self.NeedDraw = True
        return self
    def Text(self, Ch, IsIns):
        if not self.Enabled: return None
        if IsIns and self.Pos >= len(self.Dat):
            return self
        if len(self.Dat) >= self.MaxLen and self.InsIfMax:
            IsIns = True
        if self.Pos == self.MaxLen:
            if self.InsIfMax: self.Pos -= 1
            else: return self
        if not self.Rest.allows(self.Dat, self.Pos, IsIns, Ch): return self
        if IsIns:
            self.Dat[self.Pos] = Ch
            self.NeedDraw = True
        elif self.Pos < self.MaxLen:
            self.Dat.insert(self.Pos, Ch)
            self.Pos += 1
            self.NeedDraw = True
        else: return self
        return self.Right()
    def Disable(self):
        self.Enabled = False
        return None
    def NoDisp(self, Surf, Bkgr):
        self.Clear(Surf, Bkgr)
        self.Disp = False
        self.NeedDraw = False
    def Clear(self, Surf, Bkgr):
        if self.LastDraw != None: Surf.fill(Bkgr, self.LastDraw)
        self.LastDraw = None
    def Draw(self, IsSel, Fnt):
        if not self.Disp: return None
        Txt = u''.join(self.Dat)
        Rtn = Fnt.render(Txt, 1, self.Frgr, self.Bkgr)
        self.LastDraw = pygame.rect.Rect((self.x, self.y), Rtn.get_size())
        if IsSel:
            Rtn.fill(self.Frgr, pygame.rect.Rect((self.Pos * FntSz[0] - 1, FntSz[1] - CursSz[1]), CursSz))
        self.NeedDraw = False
        return Rtn
    def UnFocus(self):
        self.NeedDraw = True
class RestctNum:
    def __init__(self, Min, Max):
        self.Min = Min
        self.Max = Max
    def allows(self, Extra, Pos, Ins, Ch):
        if not Ch.isdigit(): return False
        Dat = list(Extra)
        if not Ins: Dat.insert(Pos, Ch)
        else: Dat[Pos] = Ch
        Val = int(u''.join(Dat))
        return Val >= self.Min and Val <= self.Max
def IsInCtl(x, y, Ctl):
    return x >= Ctl.x and x < Ctl.x + Ctl.Width and y >= Ctl.y and y < Ctl.y + Ctl.Height
def StartStop(Btn):
    global TmrCount
    global OrigCount
    global PauseBtn
    global MidCount
    Btn.IsOn = not Btn.IsOn
    Btn.NeedDraw = True
    if Btn.IsOn:
        Btn.Txt = "Stop"
        LstCtls[0].Disable()
        LstCtls[1].Disable()
        LstCtls[2].Disable()
        TmrCount = int('0' + ''.join(LstCtls[0].Dat)) * 3600
        TmrCount += int('0' + ''.join(LstCtls[1].Dat)) * 60
        TmrCount += int('0' + ''.join(LstCtls[2].Dat))
        OrigCount = TmrCount
        MidCount = 0
        PauseBtn.Enabled = True
        PauseBtn.Disp = True
        PauseBtn.NeedDraw = True
        LstCtls[7].MkDisp()
        LstCtls[8].MkDisp()
        pygame.time.set_timer(TMR_EVENT, 20)#50 times per second
    else:
        pygame.time.set_timer(TMR_EVENT, 0)
        TmrCount = 0
        Hr = str(int(OrigCount/3600))
        Min = str(int((OrigCount/60) % 60))
        Sec = str(int(OrigCount % 60))
        if len(Hr) == 1:
            Hr = "0" + Hr
        if len(Min) == 1:
            Min = "0" + Min
        if len(Sec) == 1:
            Sec = "0" + Sec
        LstCtls[0].Dat = list(Hr)
        LstCtls[1].Dat = list(Min)
        LstCtls[2].Dat = list(Sec)
        LstCtls[0].NeedDraw = True
        LstCtls[1].NeedDraw = True
        LstCtls[2].NeedDraw = True
        LstCtls[0].Enabled = True
        LstCtls[1].Enabled = True
        LstCtls[2].Enabled = True
        PauseBtn.Enabled = False
        PauseBtn.IsOn = False
        LstCtls[7].MkNoDisp()
        LstCtls[8].MkNoDisp()
        PauseBtn.Disp = False #This along with the line below will be recognized when rendering occurs
        PauseBtn.NeedDraw = True
        Btn.Txt = "Start"
        TmrStopFunc()
TMR_EVENT = pygame.USEREVENT
def PauseResume(Btn):
    Btn.IsOn = not Btn.IsOn
    Btn.NeedDraw = True
    if Btn.IsOn:
        Btn.Txt = "Resume"
        pygame.time.set_timer(TMR_EVENT, 0)
    else:
        Btn.Txt = "Pause"
        pygame.time.set_timer(TMR_EVENT, 20)#50 times per second
AlarmSnd = None
def TmrDoneFunc():
    global AlarmSnd
    pygame.mixer.init(44100)
    AlarmSnd = pygame.mixer.Sound(AlarmFile)
    AlarmSnd.play(-1)
def TmrStopFunc():
    global AlarmSnd
    if AlarmSnd != None:
        AlarmSnd.stop()
        AlarmSnd = None
    pygame.mixer.quit()
def Tick():
    global MidCount
    global TmrCount
    global OrigCount
    global StartBtn
    MidCount += 1
    if MidCount < 50:
        return None
    MidCount = 0
    TmrCount -= 1
    Hr = str(int(TmrCount/3600))
    Min = str(int((TmrCount/60) % 60))
    Sec = str(int(TmrCount % 60))
    if len(Hr) == 1:
        Hr = "0" + Hr
    if len(Min) == 1:
        Min = "0" + Min
    if len(Sec) == 1:
        Sec = "0" + Sec
    LstCtls[0].Dat = list(Hr)
    LstCtls[1].Dat = list(Min)
    LstCtls[2].Dat = list(Sec)
    LstCtls[0].NeedDraw = True
    LstCtls[1].NeedDraw = True
    LstCtls[2].NeedDraw = True
    LstCtls[7].NeedDraw = True
    LstCtls[8].NeedDraw = True
    if OrigCount != 0: LstCtls[7].Percent = 1.0 - float(TmrCount)/OrigCount
    else: LstCtls[7].Percent = 0
    LstCtls[8].Percent = LstCtls[7].Percent
    if TmrCount <= 0:
        pygame.time.set_timer(TMR_EVENT, 0)
        PauseBtn.Disp = False
        PauseBtn.NeedDraw = True
        TmrDoneFunc()
BLUE = (0, 0, 255)
GREED = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
ProgRad = 32
ProgX = 16
ProgY = 16
pygame.display.init()
pygame.font.init()

NotExit = True

IsCount = False
TmrFnt = pygame.font.SysFont("Courier New", 64)
FntSz = TmrFnt.size(" ")
CursSz = 2, FntSz[1]

MinSec = RestctNum(0, 59)
RestHr = RestctNum(0, 23)
Surface = pygame.display.set_mode((640, 240))
xTop = 170
xBot = 92


LstCtls=[TxtInput(xTop, 32, 2 * FntSz[0], FntSz[1], 2, RestHr, "00", True),
         TxtInput(xTop + 3 * FntSz[0], 32, 2 * FntSz[0], FntSz[1], 2, MinSec, "00", True),
         TxtInput(xTop + 6 * FntSz[0], 32, 2 * FntSz[0], FntSz[1], 2, MinSec, "00", True),
         Label(xTop + 2 * FntSz[0], 32, ":", TmrFnt, (191, 191, 191), (0, 0, 0)),
         Label(xTop + 5 * FntSz[0], 32, ":", TmrFnt, (191, 191, 191), (0, 0, 0)),
         Button(xBot + 6 * FntSz[0], 40 + FntSz[1], 6 * FntSz[0], FntSz[1], "Pause", (255, 0, 0), (255, 255, 255), (0, 255, 0)),
         Button(xBot, 40 + FntSz[1], 5 * FntSz[0], FntSz[1], "Start", (0, 255, 0), (255, 255, 255), (255, 0, 0)),
         ProgressCircle(ProgX, ProgY, ProgRad, 4, RED, BLACK), ProgressCircle(640 - (ProgRad * 2 + ProgX), ProgY, ProgRad, 4, RED, BLACK)]
LstCtls[7].Other = LstCtls[8]
LstCtls[8].Other = LstCtls[7]

PauseBtn = LstCtls[5]
StartBtn = LstCtls[6]

PauseBtn.Disp = False
PauseBtn.NeedDraw = False

StartBtn.ClkFunc = StartStop
PauseBtn.ClkFunc = PauseResume

LstCtls[0].CtlTrans[1] = LstCtls[1]
LstCtls[1].CtlTrans[1] = LstCtls[2]
LstCtls[1].CtlTrans[3] = LstCtls[0]
LstCtls[2].CtlTrans[3] = LstCtls[1]

CurCtl = None
GlblBkgr = (0, 0, 0)
IsInsert = False
OrigCount = 0
TmrCount = 0
MidCount = 0
while NotExit:
    Evt = pygame.event.wait()
    if Evt.type == pygame.QUIT:
        NotExit = False
    elif Evt.type == TMR_EVENT:
        Tick()
    elif Evt.type == pygame.MOUSEBUTTONDOWN:
        for Ctl in LstCtls:
            if IsInCtl(Evt.pos[0], Evt.pos[1], Ctl) and Ctl.Enabled:
                TmpCtl = Ctl.Click(Evt.pos[0] - Ctl.x, Evt.pos[1] - Ctl.y)
                if CurCtl != TmpCtl and CurCtl != None:
                    CurCtl.UnFocus()
                CurCtl = TmpCtl
    elif Evt.type == pygame.KEYDOWN:
        if Evt.key == pygame.K_INSERT:
            IsInsert = not IsInsert
        elif Evt.key == pygame.K_TAB:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT > 0:
                if CurCtl != None: CurCtl = CurCtl.ShiftTab()
            else:
                if CurCtl != None: CurCtl = CurCtl.Tab()
        elif Evt.key == pygame.K_BACKSPACE:
            if CurCtl != None: CurCtl = CurCtl.Backspace()
        elif Evt.key == pygame.K_DELETE:
            if CurCtl != None: CurCtl = CurCtl.Delete()
        elif Evt.key == pygame.K_UP:
            if CurCtl != None: CurCtl = CurCtl.Up()
        elif Evt.key == pygame.K_DOWN:
            if CurCtl != None: CurCtl = CurCtl.Down()
        elif Evt.key == pygame.K_LEFT:
            if CurCtl != None: CurCtl = CurCtl.Left()
        elif Evt.key == pygame.K_RIGHT:
            if CurCtl != None: CurCtl = CurCtl.Right()
        elif Evt.unicode != None and len(Evt.unicode) > 0:
            if CurCtl != None: CurCtl = CurCtl.Text(Evt.unicode, IsInsert)
    for Ctl in LstCtls:
        if Ctl.NeedDraw:
            RectUpd1 = Ctl.LastDraw
            RectUpd = None
            Ctl.Clear(Surface, GlblBkgr)
            Bmp = Ctl.Draw(Ctl == CurCtl, TmrFnt)
            if Bmp != None:
                RectUpd = pygame.rect.Rect((Ctl.x, Ctl.y), Bmp.get_size())
                Surface.blit(Bmp, RectUpd)
                if Ctl == CurCtl:
                    try:
                        pygame.draw.rect(Surface, Ctl.SelClr, Ctl.LastDraw, 1)
                    except:
                        pass
            pygame.display.update([RectUpd, RectUpd1])
pygame.quit()
