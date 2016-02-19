# Contains overall functionality.

import codecs #to write utf-8 output
import re
from spex_spider import Spex_spider

def load_data(sourcefile):
    # Data containers
    urls = []
    dictionary = {}
    shortdictionary = {}
    styles = []
    
    file = codecs.open(sourcefile, 'r', 'utf-8')
    mode = ''
    baseurl = ''
    meta={}
    for line in file.readlines():
        if line.strip() != "" and not line.strip().startswith("#"):
            if not line.startswith("\t"):                           # No tab --> Section descriptor
                mode = line.strip().lower()
            else:
                line = line.strip()
                data_split = line.split("=", 1)
                if mode == "web":
                    property = data_split[0].strip().lower()
                    if property == "basepage":
                        baseurl = data_split[1].strip()
                    elif property == "pages":
                        for url in get_string_list(data_split[1]):
                            urls.append(baseurl+url.strip())
                    else:
                        print("Found invalid property in Web section: %s", property)
                elif mode == "meta":
                    # Parse all meta properties as strings.
                    property = data_split[0].strip().lower()
                    meta[property] = data_split[1].strip()
                elif mode == "dictionary":
                    # Do stuff
                    if len(data_split) == 2:
                        for dictionary_item in get_string_list(data_split[1]):
                            dictionary[dictionary_item.strip()] = data_split[0].strip()
                    else:
                        print("Invalid format of a directory entry. Should be in format name={\"entry1\", \"entry2\"}")
                elif mode == "shortdictionary":
                    # Parse all meta properties as strings.
                    property = data_split[0].strip().lower()
                    shortdictionary[property] = data_split[1].strip()
                elif mode == "styles":
                    style = {"name":data_split[0]}
                    for property in data_split[1][1:-1].split(","):
                        prop_data = property.split("=")
                        if len(prop_data) == 2:
                            propname = prop_data[0].strip().lower()
                            propvalue = prop_data[1].strip()
                            if propname == "nere":
                                style[propname] = not (propvalue.lower() == "false")
                            else:
                                style[propname] = propvalue
                    styles.append(style)
                else:
                    print("No functionality bound to section '%s'", mode)
    
    return {"urls": urls, 'meta': meta, "dictionary": dictionary, "shortdictionary": shortdictionary, "styles": styles}
    
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
        
    styles="[V4+ Styles]\n"\
           +"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    defaultFont = data.get("meta").get("font", "Arial")
    for style in data.get("styles"):
        name = style.get("name", "unknown_style")
        font = style.get("font", defaultFont)
        fontsize = style.get("fontsize", "32")
        color = style.get("color", "&H00FFFFFF")
        
        styles += r"Style: %s,%s,%s,%s,%s,%s,%s,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1" % (name, font, fontsize, color, color, color, color)+"\n"
        if style.get("nere", 1):
            styles += r"Style: %s NERE,%s,%s,%s,%s,%s,%s,0,0,0,0,100,100,0,0,1,2,2,2,50,50,45,1" % (name, font, fontsize, color, color, color, color)+"\n"
            styles += r"Style: %s UPPE,%s,%s,%s,%s,%s,%s,0,0,0,0,100,100,0,0,1,2,2,8,50,50,45,1" % (name, font, fontsize, color, color, color, color)+"\n"
        
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
