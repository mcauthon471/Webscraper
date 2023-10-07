from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem
known_skills = ['python','javascript','html','css','sql','java','c++','c#','php','c','typescript','shell','swift','objective-c','ruby','r','vba','assembly','matlab','go','perl','scala','groovy','powershell','lua','delphi','rust','elixir','coffeescript','haskell','erlang','clojure','ocaml','julia','dart','kotlin','hack','verilog','vhdl','fortran','abap','ada','apex','autoit','awk','ballerina','blitzbasic','blitzmax','borland','caml','ceylon','chapel','chuck','clarion','clean','clipper','cobol','cobra','coldfusion','commonlisp','crystal','d','dylan','eiffel','elm','erlang','f#','factor','forth','fortran','foxpro','gambas','gnu','golang','groovy','haskell','haxe','icon','idl','inform','j','jcl','julia','kotlin','labview','ladder','lisp','logo','logtalk','lotus','lpc','lsl','lua','m4','maple','mathematica','matlab','max','maxscript','mel','mercury','metapost','mirah','mql4','mql5','ms','mumps','nemerle','nim','oberon','objc','ocaml','octave','openedge','oxygene','oz','paradox','parrot','pascal','pawn','perl','php','pic','pike','pl/i','pl/sql','postgresql','postscript','powershell','prolog','puppet','purebasic','python','q','r','racket','rebol','rexx','ring','rpg','ruby','rust','sas','scala','scheme','scilab','scratch','sed','seed7','smalltalk','solidity','spss','sql','swift','tcl','tex','thinbasic','transact-sql','typescript','vala','vb','verilog','vhdl','vim','visual','visualbasic','visualfoxpro','whitespace','xbase','xml','xorg','xquery','xslt','yacc','zsh', 'github']
known_status = ['in progress', 'future', 'complete', 'unknown', 'completed']
class StackSpider(Spider):
    name = 'stack'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/mcauthon471?tab=repositories&q=&type=public&language=&sort=']

    def parse(self, response):
        questions = Selector(response).xpath('//div[@id="user-repositories-list"]/ul/li/div[1]')

        for question in questions:
            item = StackItem()
            item['title'] = question.xpath('div[1]/h3/a/text()').extract()[0]
            item['title'] = item['title'].replace('\n', '').replace(' ', '')
            item['url'] = "https://" + self.allowed_domains[0] + question.xpath('div[1]/h3/a/@href').extract()[0]
            item['description'] = question.xpath('div[2]/p/text()').extract_first()
            item['skills'] = []
            item['status'] = None
            if item['description'] != None:
                soup = item['description'].split()
                soup = [word.replace('\n', '').replace(' ', '') for word in soup]
                soup = [word.replace(',', '').replace('.', '') for word in soup]
                soup = [word.replace('(', '').replace(')', '') for word in soup]
                for skill in soup:
                    if (skill.lower() in known_skills): 
                        item['skills'].append(skill.capitalize())
                        item['skills'] = list(set(item['skills']))
                for word in soup:
                    if word.lower() == "in":
                        if soup[soup.index(word) + 1].lower() == "progress":
                            item['status'] = "In progress"
                            break
                    if word.lower() in known_status:
                        item['status'] = word.capitalize()
            if item['status'] == None:
                item['status'] = "Unknown"
            if item['skills'] == []:
                item['skills'] = "Unknown"
            else:
                item['skills'] = ', '.join(item['skills'])
            yield item
