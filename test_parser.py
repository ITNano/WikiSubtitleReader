# -*- coding: utf-8 -*-
#above is needed for åäö
from raw_to_ass import Raw_to_ass_parser
from raw_to_ass import seconds_to_time,time_to_seconds


#time conversion tests
test=Raw_to_ass_parser(2,3)
print "start "+test.time_start
print "end "+test.time_end
test.increment_time()
print "time step:"+str(test.time_step)
print "start "+test.time_start
print "end "+test.time_end
test.increment_time()
print "time step:"+str(test.time_step)
print "start "+test.time_start
print "end "+test.time_end

print seconds_to_time(3600+60+1.11)

print time_to_seconds(seconds_to_time(6))
print time_to_seconds(seconds_to_time(66))
print time_to_seconds(seconds_to_time(666))
print time_to_seconds(seconds_to_time(6666))

#print line and map things to style
#whitespaces are stripped from the text part.
line='A: Jag är Anna'
test.style_dictionary["a"]="ANNA"
print test.parse_line_to_ass(line,':')

#if no semicolon is found we will use the test.empty_style style
#Whenever a line is parsed, this variable is updated to use that line, so that
#a single singer does not have to be written out on every line.
#Can of course also be set manually, but beware of the above behavior!
line='Fortfarande är jag Anna!'
print test.parse_line_to_ass(line,':')
test.empty_style="Alla"
test.style_dictionary["alla"]="ALLA"
line='Alla sjunger men vi har inte orkat skriva ut det i denna råa linjen'
print test.parse_line_to_ass(line,':')
line='' #empty line
print test.parse_line_to_ass(line,':')
line='a:' #empty line
print test.parse_line_to_ass(line,':')
