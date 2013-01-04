import urllib

def email (new):
    print "page has changed";
    return;
def saveToServer (new):
    print "page has been saved";
    return;
current = urllib.urlopen('http://www.bloomberg.com/view/bios/jonathan-alter');\
old = urllib.urlopen('http://www.bloomberg.com/view/bios/jonathan-alter');
prevC = '';
prevO = '';
for (lineC, lineO) in zip (current, old):
        if prevC == '<h3><a class="author" href="/view/bios/jonathan-alter/">Jonathan Alter</a></h3>':
            #<h2><a href="/news/2013-01-03/liberals-nip-obama-as-he-battles-republicans.html" class="q">Liberals Nip Obama as He Battles Republicans</a></h2>
            if lineC != lineO:
                print lineC;
                print lineO;
                email(lineC);
                saveToServer(current);
                break;
        prevC = lineC;
        prevO = lineO;
current.close();
old.close();
