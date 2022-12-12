"""New file where I build the logic progress on the final program"""

"""Since from the latest progress on Priority Queue, there are stil flaws: when hearsay it violates sort stability when there are elements with equal priorities---where 
they were compared by value (in this case a String) according to lexicographic order. They should be compared by insertion"""

"""Thru this program, the capability of enqueueing an element with no comparison opearator like a custom class and if the issue of already having an element with the 
same priority the user wants to use"""
#lexicographic order - the alphabetical order of the dictionaries to sequences of ordered symbols or, more generally, of elements of a totally ordered set
from dataclasses import dataclass 

@dataclass #used to represent messages in the queue; more convenient than strings but aren't comparable
class Message:
    event: str

wipers = Message("Windshield wipers turned on")
hazard_lights = Message("Hazard lights turned on")

if wipers < hazard_lights:
    print(True)
else:
    print(False)
