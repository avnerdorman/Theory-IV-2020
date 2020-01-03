#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:11:23 2019

@author: adorman
"""

from music21 import *


Tresillo = '10010010'


def pattern(index, duration):
    pat = bin(index)[2:]
    notes = { '1': str(duration), '0': str(duration * -1)}
    result = []
    for i in range(len(pat)):
        if pat[i] == '0':
            result.append(duration * -1)
        elif pat[i] == '1':
            result.append(duration)
    return result


def RhythmFromNumber (index):
    s = converter.parse(pattern(index))
    s.show()
    return s

def BinRhythm (tiny):
    notes = { '1': 'b8 ', '0': 'r8 ' }
    result = ''
    for i in range(len(tiny)):
        result += notes[tiny[i]]

    s = converter.parse("tinyNotation: " + result)
    s.show()
    return s



def interleave (a, b):
    if len(a) != len(b):
        pass
    string = ''
    for i in range(len(a)):
        string += a[i]
        string += b[i]
        string += ' '
    return string
        
def positive(lengths):
    counter = 0
    for i in lengths:
        if i >0 :
            counter +=1
    return (counter)

'''

to_do      recursive function SPAN PITCHES   
 fix make_omn to just go by durations
'''

def make_omn(lengths, pitch_string):
    
    pitches = pitch_string.split()

            
    if len(pitches) > positive(lengths):
        lengths = repeat_to_length (lengths, len(pitches) + how_many_negatives (lengths))
        pitches = repeat_to_length (pitches, len(lengths))

    else:
        lengths = repeat_to_length (lengths, len(pitches) + how_many_negatives (lengths))

    '''
    add rests to pitches list
    '''
    print(lengths)
    pitches = add_rests_to_pitches (pitches, lengths)
    lengths = repeat_to_length (lengths, len(pitches) + how_many_rs(pitches) )
    pitches = repeat_to_length (pitches, len(lengths))
    print(pitches)

    stream1 = stream.Stream()
    
    for i in range(len(lengths)):
        if lengths[i] >= 0:
            n1 = chord.Chord(add_space(pitches[i]))
            n1.duration.quarterLength = (4 * lengths[i])
            stream1.append(n1)
        else:
            r1 = note.Rest()
            r1.duration.quarterLength = (-4 * lengths[i]) 
            stream1.append(r1)
        
    stream1.show()
    return stream1



 
    

'''
repeat_to_length expand a list to a given length
'''


def repeat_to_length(string_to_expand, length):
    return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]


 

'''
add_rests_to_pitches prepares the pitches variable to include 'r' whereever there will be a rest 
'''

def add_rests_to_pitches (pitches, lengths):
    new_pitches = []
    counter = 0 
    for i in lengths:
        if i < 0 :
            new_pitches.append('r')
        else:
            new_pitches.append(pitches[counter])
            counter += 1
    return new_pitches
    

'''
make_list_pitches expects a list of pitches with octaves and a list of lengths. 
It prepares to pitches list
then makes both lists the same length (through repetition)
then creates a stream that uses both lists through isorhtyhm
'''

def make_list_pitches (pitch_string, lengths):

    pitches = pitch_string.split()
    
    pitches = add_rests_to_pitches (pitches, lengths)
    
    
    if len(lengths) > len (pitches):
        pitches = repeat_to_length (pitches, len(lengths))
    else:
        lengths = repeat_to_length (lengths, len(pitches))

    stream1 = stream.Stream()
    
    for i in range(len(lengths)):
        n1 = note.Note()
        if lengths[i] >= 0:
            n1.duration.quarterLength = (4 * lengths[i])
            n1.pitch.name = pitches[i]
            stream1.append(n1)
        else:
            n1 = note.Rest()
            n1.duration.quarterLength = (-4 * lengths[i]) 
            stream1.append(n1)
    stream1.show()
    return stream1

'''
binary_rhythm_map
'''

def binary_rhythm_map(binary_num, duration):
    result = []
    for i in range(len(binary_num)):
        if binary_num[i] == '0':
            result.append(duration * -1)
        elif binary_num[i] == '1':
            result.append(duration)
    return result

def how_many_negatives(a_list):
    counter = 0
    for i in a_list:
        if i <0 :
            counter +=1
    return counter

def how_many_rs(a_list):
    counter = 0
    for i in a_list:
        if i == 'r' :
            counter +=1
    return counter


''' 
'''

def make_list_binary (pitch_string, binary_num, duration, display = ''):

    pitches = pitch_string.split()

    
    '''
    create lengths from binary number entered as a string
    '''
    
    lengths = binary_rhythm_map(binary_num, duration)
    '''
    make pitches and duration lists the same length
    '''

    if (len(lengths) + how_many_negatives (lengths)) > len (pitches):
        pitches = repeat_to_length (pitches, len(lengths))
    else:
        lengths = repeat_to_length (lengths, len(pitches))

    '''
    add rests to pitches list
    '''
    
    pitches = add_rests_to_pitches (pitches, lengths)
    lengths = repeat_to_length (lengths, (len(pitches)))



    stream1 = stream.Stream()
    
    for i in range(len(lengths)):
        n1 = note.Note()
        if lengths[i] >= 0:
            n1.duration.quarterLength = (4 * lengths[i])
            n1.pitch.name = pitches[i]
            stream1.append(n1)
        else:
            n1 = note.Rest()
            n1.duration.quarterLength = (-4 * lengths[i]) 
            stream1.append(n1)
    if display == '':
        stream1.show()
    else:
        stream1.show(display)
    return stream1

'''
prompt user for input
'''

#input_string = input("Enter a list pitches separated by space ")
#pitches  = input_string.split()
#binary_num = str(input("Enter a binary number for durations "))
#duration = float(input("Enter a duration "))
#
#print (pitches)
#print (binary_num)
#
#x = make_list_binary (pitches, binary_num, duration)
#
#x.show()


'''
example 

x = make_list_binary(['c4', 'd4', 'eb4', 'f4'] * 8, '10110110101011', 1/8)

x.show()

'''

def add_space (str):
    new_string = ''
    for i in range (len(str)):
        new_string += str[i]
        if str[i].isdigit():
            new_string += ' '
    return new_string



def biRhythm(numerator, denominator, pulse_duration, repetitions = 1, time_sig = '4/4', upper_pitches = 'c5', lower_pitches = 'c4'):
    
    ts = meter.TimeSignature(time_sig)
    
    s = stream.Score(id='mainScore')
    p0 = stream.Part(id='part0')
    p0.append(ts)
    p1 = stream.Part(id='part1')
    p1.append(ts)    
    
    dur0 = pulse_duration*denominator*4
    dur1 = pulse_duration*numerator*4
    
    
    
    for i in range (denominator * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur1
        n1.pitch.name = 'c5'
        p0.append(n1)
        
    for i in range (numerator * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur0
        n1.pitch.name = 'c4'
        p1.append(n1)
        
    s.insert(0, p0)
    s.insert(0, p1)        
    s.show()
    return s


def intervalCycle(start, delta, number_of_steps):
    l = []
    if type(delta) == int:
        for i in range(number_of_steps):
            l.append(start)
            start += delta
        return l
    elif type(delta) == list:
        for i in range(number_of_steps):
            for j in delta:
                l.append(start)
                start += j
        return l
    

def midiToStream(midi_notes):
    stream1 = stream.Stream()

    for i in midi_notes:
        n1 = note.Note()
        n1.pitch.midi = i
        stream1.append(n1)
        
    return stream1
        
    
def replaceDurations(stream2, durations):
    stream1 = stream.Stream()
    counter = 0
    for i in stream2.pitches:
        n1 = note.Note()
        n1.pitch = i
        n1.duration.quarterLength = (4 * durations[counter])
        counter = (counter + 1) % len(durations)
        print(i)
        stream1.append(n1)
    stream1.show()
    
def cycletoNotes (start_note, delta, number_of_steps, output = ''):
    n1 = note.Note()
    n1.pitch.name = start_note
    start = n1.pitch.midi
    x = midiToStream(intervalCycle(start, delta, number_of_steps))
    x.show(output)
    return x

''' rotates a pitch string by given number of pitches (takes into account the existence of octaves and possibility of alternation of pitch'''


def rotatePitchString (pitch_list, how_much_to_rotate):
    x = -1 * how_much_to_rotate
    return (pitch_list[x:] + pitch_list [:x])


''' alternate_list_binary expects two pitch strings and a binary number and duration.
    it attaches pitch string 1 with the 1's in the binary number
    and pitch string 2 with the 0's in the binary number
'''

def alternate_list_binary (pitch_string1, pitch_string2, binary_num, duration, display = ''):
    output = []
    s1 = pitch_string1.split()
    s2 = pitch_string2.split()    
    for i in binary_num: 
        if i == '1':
            output += s1[:1]
            s1 = s1[-1:] + s1[:-1] 
        elif i == '0':
            output += s2[:1]
            s2 = s2[-1:] + s2[:-1]            
    
    stream1 = stream.Stream()
    
    for i in output:
        n1 = note.Note()
        n1.duration.quarterLength = 4*duration
        n1.pitch.name = i
        stream1.append(n1)
    if display == '':
        stream1.show()
    else: 
        stream1.show(display)

    return (stream1)
    
def numRhythm (numerical_list, pitches, duration, display = ''):
    pitchlist = pitches.split()
    x = len (pitchlist)

    stream1 = stream.Stream()
    ts1 = meter.TimeSignature('4/4') # assumes two partitions
    stream1.timeSignature=ts1
            
    for i in range(len(numerical_list)):
        n1 = note.Note()
        n1.duration.quarterLength = 2 * numerical_list[i] * duration 
        n1.pitch.name = pitchlist [i % x]
        stream1.append(n1)

    stream2 = stream.Stream()
    

    if display == '':
        stream1.show()
    else: 
        stream1.show(display)

    
    
    return (stream1)

