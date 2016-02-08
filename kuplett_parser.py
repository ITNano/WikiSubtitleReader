# Contains overall functionality.

import codecs #to write utf-8 output
import re
from spex_spider import Spex_spider

class StyleData():
    def __init__(self, stylename):
        self.stylename = stylename
        self.fontsize = "32"
        self.color = "&H00FFFFFF"
        self.generate_down = 1
        self.font = ""

def load_data(sourcefile):
    # Data containers
    urls = []
    dictionary = {}
    styles = []
    
    file = codecs.open(sourcefile, 'r', 'utf-8')
    mode = ''
    baseurl = ''
    meta={}
    for line in file.readlines():
        if line.strip() != "" and not line.strip().startswith("#"):
            if not line.startswith("\t"):                           # No tab --> Section descriptor
                mode = line.strip().lower();
            else:
                line = line.strip()
                if mode == "web":
                    property = line.split("=")[0].strip().lower()
                    if property == "basepage":
                        baseurl = line.split("=")[1].strip()[1:-1]
                    elif property == "pages":
                        for url in get_string_list(line.split("=")[1]):
                            urls.append(baseurl+url.strip())
                    else:
                        print("Found invalid property in Web section: %s", property)
                elif mode == "meta":
                    # Parse all meta properties as strings.
                    property = line.split("=")[0].strip().lower()
                    meta[property] = line.split("=")[1].strip()[1:-1]
                elif mode == "dictionary":
                    # Do stuff
                    if len(line.split("=")) == 2:
                        for dictionary_item in get_string_list(line.split("=")[1]):
                            dictionary[dictionary_item.strip()] = line.split("=")[0].strip()
                    else:
                        print("Invalid format of a directory entry. Should be in format name={\"entry1\", \"entry2\"}")
                elif mode == "styles":
                    index = line.index("=")
                    stylename = line[:index].strip()
                    style = StyleData(stylename)
                    for property in line[index+2:-1].split(","):
                        propname = property.split("=")[0].strip().lower()
                        if propname == "color":
                            style.color = property.split("=")[1].strip()
                        elif propname == "size":
                            style.fontsize = property.split("=")[1].strip()
                        elif propname == "font":
                            style.font = property.split("=")[1].strip()
                        elif propname == "nere":
                            style.generate_down = not (property.split("=")[1].strip().lower() == "false")
                        else:
                            print("Invalid property found: %s" % propname)
                    styles.append(style)
                else:
                    print("No functionality bound to section '%s'", mode)
    
    return {"urls": urls, 'meta': meta, "dictionary": dictionary, "styles": styles}
    
def get_all_lyrics(sourcefile, username, password):
    #fetch urls of all songs
    urls = load_data(sourcefile).get("urls")

    #login to f-spexet/wiki NOTE: this depends on implementation details of
    #the mediawiki, but it works as of 2015-11-03
    #NOTE: Firefox is the only supported driver so far. Trivial to add other browsers supported by Selenium, though.
    spider=Spex_spider(username,password,"Firefox")
    
    # container for the data
    lyrics=[]
    
    #to skip first and last lines of the text body
    #This might be useful, since those should/could contain metadata.
    exclude_first=0;
    exclude_last=0;

    for url in urls:
        #get body text in one big string suitable for human reading.
        text=spider.get_text_body(url)
        #Break the text into a list of strings, one for each line.
        textlist=text.splitlines()
        first=0+exclude_first
        last=len(textlist)-exclude_last
        kuplett_text=textlist[first:last]
        lyrics.append(kuplett_text)
    
    return lyrics

def get_generic_name(filename):
    index = filename.rfind("/")
    if index > 0:                               # Use only filename, not path
        filename = filename[index+1:]
    if filename.startswith("Hemlig:"):          # Ignore prefix 'Hemlig:'
        filename = filename[7:]
        
    parts = re.split("_|-", filename)
    result = parts[0].lower()
    for part in parts[1:]:
        result += part.capitalize()
    
    return unescape(result).replace(":", "_")
    
def get_ass_header(sourcefile):
    # get data
    data = load_data(sourcefile);
    
    preamble="[Script Info]\
        \nTitle: %s\
        \nScriptType: v4.00+\
        \nWrapStyle: 1\
        \nScaledBorderAndShadow: yes\
        \nYCbCr Matrix: None\
        \nAegisub Scroll Position: 0\
        \nAegisub Active Line: 18\
        \nAegisub Video Zoom Percent: 1.000000\
        \nLast Style Storage: Default\
        \nPlayResX: 0\
        \nScroll Position: 78\
        \nActive Line: 96\
        \nVideo Zoom Percent: 1\
        \nCollisions: Normal\
        \nPlayResY: 0\n" % data.get("meta").get("title", "UndefinedTitle")
        
    styles=r"[V4+ Styles]\n"\
           +r"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    defFont = data.get("meta").get("font", "Arial")
    for style in data.get("styles"):
        currentFont = defFont
        if(len(style.font)>0):
            currentFont = style.font
            
        styles += r"Style: %s,%s,%s,%s,%s,%s,%s,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1" % (style.stylename, currentFont, style.fontsize, style.color, style.color, style.color, style.color)+"\n"
        if style.generate_down:
            styles += r"Style: %s NERE,%s,%s,%s,%s,%s,%s,0,0,0,0,100,100,0,0,1,2,2,2,50,50,45,1" % (style.stylename, currentFont, style.fontsize, style.color, style.color, style.color, style.color)+"\n"
        
    event_preamble="[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    
    return preamble+"\n"+styles+"\n"+event_preamble


def get_string_list(str):
    return re.findall(r'\"(.+?)\"', str[1:-1])

# unescapes swedish characters.
def unescape(text):
    text = text.replace("%c3%b6", "ö")
    text = text.replace("%c3%a4", "ä")
    text = text.replace("%c3%a5", "å")
    text = text.replace("%c3%96", "Ö")
    text = text.replace("%c3%84", "Ä")
    text = text.replace("%c3%85", "Å")
    return text
    
if __name__ == "__main__":
    print(unescape("m%c3%a4ssaACappella"))
