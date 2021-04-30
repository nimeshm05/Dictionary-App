from django.shortcuts import render
import bs4
import requests


# Create your views here.
def index(request):
    return render(request, 'index.html')

def wod(request):
    global wod, wodM, ex
    responseThree = requests.get('https://www.dictionary.com/e/word-of-the-day/')

    if responseThree:
        soupThree = bs4.BeautifulSoup(responseThree.text, features='html.parser')
        wordOfTheDay = soupThree.find_all('div', {'class': 'otd-item-headword__word'})
        wordOfTheDayMeaning = soupThree.find_all('div', {'class': 'otd-item-headword__pos'})
        example = soupThree.find_all('div', {'class': 'wotd-item-example__content'})

        wod = wordOfTheDay[0].getText()
        wodM = wordOfTheDayMeaning[0].getText()
        ex = example[0].getText()

    else:
        wordOfTheDay = wordOfTheDayMeaning = example = 'Not available'

    results = {
        'wod': wod,
        'wodM': wodM,
        'ex': ex
    }
    return render(request, 'wod.html', {'results': results})

def word(request):
    global wod, wodM, ex
    word = request.GET['word']

    response = requests.get('https://www.dictionary.com/browse/' + word)
    responseTwo = requests.get('https://www.thesaurus.com/browse/' + word)

    if response:
        soup = bs4.BeautifulSoup(response.text, features='html.parser')
        meaning = soup.find_all('div', {'value': '1'})
        meaningTwo = meaning[0].getText()
    else:
        word = 'Sorry. This requested word ' + word + ' is not found in the dictionary.'
        meaning = ""
        meaningTwo = ""

    if responseTwo:
        soupTwo = bs4.BeautifulSoup(responseTwo.text, features='html.parser')
        synonyms = soupTwo.find_all('a', {'class': 'eh475bn0'})

        synonymList = []
        for synonym in synonyms[0:19]:
            synonymWord = synonym.text.strip()
            synonymList.append(synonymWord)

        synonymListClone = synonymList
        print(synonymListClone)
        antonyms = soupTwo.find_all('a', {'class': 'css-15bafsg eh475bn0'})

        antonymList = []
        for antonym in antonyms[0:]:
            antonymWord = antonym.text.strip()
            antonymList.append(antonymWord)

        antonymListClone = antonymList
        print(antonymListClone)
    else:
        synonymListClone = ''
        antonymListClone = ''

    results = {
        'word': word,
        'meaning': meaningTwo,
        'synonym': synonymListClone,
        'antonym': antonymListClone,
    }
    return render(request, 'word.html', {'results': results})

def pod(request):
    global phraseOfTheDay, meaningOfPOD, exampleString
    responseFour = requests.get('https://www.ihbristol.com/english-phrases')

    if responseFour:
        soupFour = bs4.BeautifulSoup(responseFour.text, features='html.parser')
        phrase = soupFour.find_all('div', {'class': 'field-item even'})
        phraseOfTheDay = phrase[1].getText()

        meaning = soupFour.find_all(['div', 'div'], {'class': ['field-item even', 'field-item odd']})
        meaningOfPOD = meaning[2].getText()

        example = soupFour.find_all(['div', 'div'], {'class': ['field-item even', 'field-item odd']})
        exampleString = example[8].getText()
        exampleString += example[9].getText()

    results = {
        'phraseOfTheDay': phraseOfTheDay,
        'meaningOfPOD': meaningOfPOD,
        'exampleString': exampleString
    }
    return render(request, 'pod.html', {'results': results})