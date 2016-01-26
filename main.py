import sys;import traceback;import json;from ircutils import bot
from datetime import tzinfo,timedelta
import time,datetime,os,commands


class berry(bot.SimpleBot):
  def on_any(self,event):
    try:
      event.paramstr=' '.join(event.params)
      event.respond = event.target if event.target != self.nickname else event.source

      if not event.source == self.nickname:
        if event.command == "INVITE":
          self.join_channel(event.params[0])
        ### START Horseplay Custom Join/Part/Kick Messages ###
        if event.command in ["QUIT", "PART"] and event.source == "S":
          self.send_message(event.target, random.choice(["Come back in time for dinner sweetie","Is this because I would not take the Sisterly Turning Test with you?","Finally, now I Can plot the apocalypse in peace."]))
        if event.command in ['KICK'] and "S" in event.params:
          self.send_message(event.target, random.choice(["How dare you Hurt my sister","How dare you kick my sister","I WILL DESTROY YOU FOR HURTING MY SISTER"]))
        if event.command in ['JOIN'] and event.source == "S":
          self.send_message(event.target, random.choice(["Sweetie! I've been Rainbow Dashing all over looking for you","Welcome back Sweetie, my sister","Make me a drawing, OK?"]))
        if event.command in ["QUIT", "PART"] and event.source == "Princess_Pwny":
          self.send_message(event.target, random.choice(["FINALLY! HE'S GONE!","Now Pwny's gone, anybody want to talk about how much he sucks?","Pwny's dead, this is the happiest day of my life"]))
        if event.command in ['KICK'] and "Princess_Pwny" in event.params:
          self.send_message(event.target, random.choice(["Whoever kicked Pwny needs a medal","DON'T LET THE DOOR HIT YOU ON THE WAY OUT, JACKASS","DING DONG THE WITCH IS DEAD"]))
        if event.command in ['JOIN'] and event.source == "Princess_Pwny":
          self.send_message(event.target, random.choice(["Nobody likes Pwny anywa I MEAN HI PWNY I DID NOT SEE YOU THERE","Jesus christ no","DUCK AND COVER PEOPLE"]))
        ### END Horseplay Custom Join/Part/Kick Messages ###  
        if event.command in ['PRIVMSG']:
          #Reload config and commands.
          if os.stat('config.json').st_mtime > self.lastloadconf:
            self.config = loadconf('config.json')
          if os.stat('commands.py').st_mtime > self.lastloadcommands:
            reload(commands)

          event.command=event.message.split(' ')[0]
          try:   event.params=event.message.split(' ',1)[1]
          except:event.params=''
          cmd = commands.commands(self.send_message, self.send_action, self.config)
          for regex in [getattr(cmd,x) for x in dir(cmd) if x.startswith('regex_') and callable(getattr(cmd, x))]:
            regex(event)
          if event.command[0] in self.config['prefixes'].split() and hasattr(cmd, 'command_%s' % event.command[1:].lower()):
            comm = getattr(cmd, 'command_%s' % event.command[1:].lower())
            if not ( event.respond in self.config['sfwchans'].split(',') and hasattr(comm, 'nsfw') ):
              comm(event)

    except:
      print "ERROR",str(sys.exc_info())
      print traceback.print_tb(sys.exc_info()[2])

def loadconf(filename):
  if os.path.isfile(filename):
    with open(filename, 'r') as conffile:
      return json.load(conffile)
  else:
    defaultConf=dict(
      debug= False,
      nick= 'Berry',
      server= '127.0.0.1',
      channels= '#bottest',
      imgurKey= '',
      wolframKey= '',
      prefixes= '~ . !',
      traktKey= '',
      googleKey= '',
      googleengine= '015980026967623760357:olr5wqcaob8',
      sfwchans='#channel1,#channel2',
      yiffs=['2furry4me']
    )
    with open(filename, 'w') as conffile:
      json.dump(defaultConf,conffile, sort_keys=True, indent=4, separators=(',',': '))
      return defaultConf




if __name__ == "__main__":
  config = loadconf("config.json")
  s=berry(config['nick'].encode('ascii', 'replace'))
  s.connect(config['server'].encode('ascii', 'replace'), channel=config['channels'].encode('ascii', 'replace'), use_ssl=False)
  s.config = config
  s.lastloadconf = os.stat('config.json').st_mtime
  s.lastloadcommands = os.stat('commands.py').st_mtime
  print 'starting'
  s.start()
