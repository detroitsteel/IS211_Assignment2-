#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Intakes a URL in a csv file format with columns including
    personData(ID, Name, Birthday) and creates searchable function."""

import urllib2
import datetime
import logging
import argparse

 
def downloadData(url):
    """downloadData Function - intakes string and creates
    list, which is then passed to the function processData().
    The function is meant to parse a csv file with columns including
    personData(ID, Name, Birthday).
    Args:
        url (string): A url in csv format
    Output: A list. 
    Example:
        d = downloadData('https://s3.amazonaws.com
        /cuny-is211-spring2015/birthdays100.csv')
    """
    url = url
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    a_file = response.read()
    return processData(a_file)

def processData(conts):
    """processData Function - intakes a list and creates
    parsed dict, which is then passed to the function displayData().
    The function is meant to parse a three column list with columns including
    personData(ID, Name, Birthday).
    Args:
        conts (list): A list with 3 columns
    Output: A dict 
    Example:
        d = processData(a_list)
    """
    a_dict = {}
    a_list = conts.splitlines()
    logger2 = logging.getLogger('assignment2')
    ln_ct = 0
    for line in a_list:
        ln_ct += 1
        a_line = line.split(',')
        try:
            bday = datetime.datetime.strptime(a_line[2], '%d/%m/%Y')
        except (ValueError, TypeError) as e:
            logger2.warning("Error processing line %i for ID %s"
            % (ln_ct, a_line[0]))
            pass
        else:
            a_dict[int(a_line[0])] = (a_line[1],a_line[2])
    return a_dict

def displayPerson(pid, personData):
    """displayPerson Function - intakes a dict and creates
    searchable dict function. The function will present a UI to allow single
    user searches of passed dict.
    Args:
        pid (int): The ID of the single ID to search in the first column of the
        list.
        personData (dict): A dictionary to be searched.
    Output: A formated sentence 
    Example:
        d = displayPerson(3, a_dict)
        Person 3 is Setian Huon with a birthday of 1971/08/18
    """
    if pid in personData.keys():
        print ("Person %i is %s with a birthday of %s"
        % (pid, personData[pid][0],
            datetime.datetime.strptime(personData[pid][1],'%d/%m/%Y')
           .strftime('%Y/%m/%d')))
    else:
        print "No user found with that ID %i" % pid
        
def main():
    """Main Function - intakes passed command line URL arg and creates
    searchable dict function. The URL must provide a csv file with columns including
    personData(ID, Name, Birthday).
    Args:
        url (string): A url in csv format
    Output: A searchiable dict funtional. 
    Example:
        $python Assign2_Loader.py 'https://s3.amazonaws.com/
        cuny-is211-spring2015/birthdays100.csv'
        Enter User ID to lookup. To EXIT enter 0. 3
        Person 3 is Charles Reid with a birthday of 2009/06/14
        Enter User ID to lookup. To EXIT enter 0. 
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help = "URL you'd like to parse", type = str)
    args = parser.parse_args()
    url = args.url
    Log_Filename = 'errors.log'
    logging.basicConfig(filename = Log_Filename, level = logging.ERROR)
    logger1 = logging.getLogger('assingment2')
    try:
        personData = downloadData(url)
        response = int(raw_input('Enter User ID to lookup. To EXIT enter 0. '))
        while response > 0:
            displayPerson(response, personData)
            response = int(raw_input('Enter User ID to lookup. To EXIT enter 0. '))
    except Exception as e:
        logger1.error('Main Error %s' % e)
main()
