import urllib

current = urllib.urlopen('http://www.bloomberg.com/view/bios/jonathan-alter');
prevC = '';
for lineC in current:
        if prevC == '<h3><a class="author" href="/view/bios/jonathan-alter/">Jonathan Alter</a></h3>':
            link = lineC[(lineC.find('/news/')) : (lineC.find('" class=') - 1)];
            title = lineC[(lineC.find('"q">') + 4) : (lineC.find('</a>'))];
            print title;
            print link;
            break;
        prevC = lineC;
        prevO = lineO;
current.close();
